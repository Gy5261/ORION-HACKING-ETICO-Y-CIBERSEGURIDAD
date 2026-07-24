"""Núcleo del runtime de plugins de ORION.

Este módulo ofrece contratos tipados, validación JSON Schema acotada,
guardrails de autorización, descubrimiento mediante entry points, ejecución
uniforme y resultados auditables sin dependencias obligatorias externas.
"""

from __future__ import annotations

import importlib.metadata
import json
import platform
import re
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Any, Iterable, Mapping, MutableMapping

JsonObject = dict[str, Any]


class OrionPluginError(RuntimeError):
    """Error base del runtime."""


class InputValidationError(OrionPluginError):
    """La entrada o salida no cumple el contrato del plugin."""


class AuthorizationError(OrionPluginError):
    """La política bloqueó una ejecución no autorizada."""


class PluginNotFoundError(OrionPluginError):
    """No existe un plugin con el identificador solicitado."""


class PluginExecutionError(OrionPluginError):
    """El plugin falló durante la ejecución."""


@dataclass(frozen=True, slots=True)
class PluginMetadata:
    """Contrato inmutable y serializable de un plugin ORION."""

    plugin_id: str
    name: str
    version: str
    category: str
    description: str
    risk_level: str
    capabilities: tuple[str, ...]
    input_schema: JsonObject
    output_schema: JsonObject
    requires_authorization: bool = True
    network_access: bool = False
    side_effects: bool = False
    default_timeout_seconds: float = 30.0
    max_timeout_seconds: float = 300.0
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[a-z][a-z0-9_.-]{2,63}", self.plugin_id):
            raise ValueError(f"plugin_id inválido: {self.plugin_id!r}")
        if not self.name.strip():
            raise ValueError("name no puede estar vacío")
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?", self.version):
            raise ValueError(f"version semántica inválida: {self.version!r}")
        if self.risk_level not in {"low", "medium", "high"}:
            raise ValueError("risk_level debe ser low, medium o high")
        if not self.capabilities:
            raise ValueError("capabilities debe declarar al menos una capacidad")
        if self.default_timeout_seconds <= 0:
            raise ValueError("default_timeout_seconds debe ser positivo")
        if self.max_timeout_seconds < self.default_timeout_seconds:
            raise ValueError("max_timeout_seconds no puede ser menor al timeout por defecto")
        if self.input_schema.get("type") != "object":
            raise ValueError("input_schema debe declarar type=object")

    def to_dict(self) -> JsonObject:
        payload = asdict(self)
        payload["capabilities"] = list(self.capabilities)
        payload["tags"] = list(self.tags)
        return payload


@dataclass(frozen=True, slots=True)
class PluginContext:
    """Contexto explícito de seguridad para una ejecución."""

    authorization: str | None = None
    allow_network: bool = False
    allow_side_effects: bool = False
    actor: str = "local-user"
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    environment: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.actor.strip():
            raise ValueError("actor no puede estar vacío")
        try:
            uuid.UUID(self.request_id)
        except ValueError as exc:
            raise ValueError("request_id debe ser un UUID válido") from exc


@dataclass(frozen=True, slots=True)
class PluginResult:
    """Resultado normalizado para CLI, agentes, MCP y pipelines."""

    plugin_id: str
    plugin_version: str
    request_id: str
    actor: str
    ok: bool
    duration_ms: int
    data: JsonObject | list[Any] | None = None
    warnings: tuple[str, ...] = ()
    error: JsonObject | None = None

    def to_dict(self) -> JsonObject:
        payload = asdict(self)
        payload["warnings"] = list(self.warnings)
        return payload


class BasePlugin(ABC):
    """Interfaz mínima que todo plugin interno o externo debe implementar."""

    metadata: PluginMetadata

    @abstractmethod
    def run(self, payload: JsonObject, context: PluginContext) -> JsonObject | list[Any]:
        """Ejecutar el plugin y devolver una estructura JSON serializable."""


_JSON_TYPES: dict[str, type[Any] | tuple[type[Any], ...]] = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


def _is_type(value: Any, expected: str) -> bool:
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, _JSON_TYPES[expected])


def validate_json_schema(value: Any, schema: Mapping[str, Any], path: str = "$") -> None:
    """Validar el subconjunto de JSON Schema usado por ORION.

    Soporta type, required, properties, additionalProperties, items, enum,
    const, min/maxItems, min/maxLength, minimum, maximum, pattern, anyOf y oneOf.
    """

    if "oneOf" in schema:
        successes = 0
        errors: list[str] = []
        for candidate in schema["oneOf"]:
            try:
                validate_json_schema(value, candidate, path)
                successes += 1
            except InputValidationError as exc:
                errors.append(str(exc))
        if successes != 1:
            raise InputValidationError(
                f"{path}: debe coincidir exactamente con una variante de oneOf; "
                f"coincidencias={successes}; detalles={errors[:3]}"
            )
        return

    if "anyOf" in schema:
        errors: list[str] = []
        for candidate in schema["anyOf"]:
            try:
                validate_json_schema(value, candidate, path)
                break
            except InputValidationError as exc:
                errors.append(str(exc))
        else:
            raise InputValidationError(f"{path}: no coincide con ninguna variante de anyOf; detalles={errors[:3]}")

    expected = schema.get("type")
    if expected:
        expected_types = [expected] if isinstance(expected, str) else list(expected)
        unknown = [item for item in expected_types if item not in _JSON_TYPES]
        if unknown:
            raise InputValidationError(f"{path}: tipos de schema no soportados: {unknown}")
        if not any(_is_type(value, item) for item in expected_types):
            raise InputValidationError(f"{path}: se esperaba {expected_types}, se recibió {type(value).__name__}")

    if "const" in schema and value != schema["const"]:
        raise InputValidationError(f"{path}: debe ser exactamente {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise InputValidationError(f"{path}: valor {value!r} fuera de enum {schema['enum']!r}")

    if isinstance(value, dict):
        required = schema.get("required", [])
        missing = [key for key in required if key not in value]
        if missing:
            raise InputValidationError(f"{path}: faltan campos obligatorios {missing}")
        properties: Mapping[str, Any] = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            unexpected = sorted(set(value) - set(properties))
            if unexpected:
                raise InputValidationError(f"{path}: campos no permitidos {unexpected}")
        for key, child_schema in properties.items():
            if key in value:
                validate_json_schema(value[key], child_schema, f"{path}.{key}")

    if isinstance(value, list):
        min_items = schema.get("minItems")
        max_items = schema.get("maxItems")
        if min_items is not None and len(value) < min_items:
            raise InputValidationError(f"{path}: requiere al menos {min_items} elementos")
        if max_items is not None and len(value) > max_items:
            raise InputValidationError(f"{path}: admite máximo {max_items} elementos")
        if schema.get("uniqueItems"):
            rendered = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(set(rendered)) != len(rendered):
                raise InputValidationError(f"{path}: no permite elementos duplicados")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                validate_json_schema(item, item_schema, f"{path}[{index}]")

    if isinstance(value, str):
        min_length = schema.get("minLength")
        max_length = schema.get("maxLength")
        if min_length is not None and len(value) < min_length:
            raise InputValidationError(f"{path}: longitud mínima {min_length}")
        if max_length is not None and len(value) > max_length:
            raise InputValidationError(f"{path}: longitud máxima {max_length}")
        pattern = schema.get("pattern")
        if pattern and re.search(pattern, value) is None:
            raise InputValidationError(f"{path}: no cumple el patrón requerido")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if schema.get("minimum") is not None and value < schema["minimum"]:
            raise InputValidationError(f"{path}: debe ser >= {schema['minimum']}")
        if schema.get("exclusiveMinimum") is not None and value <= schema["exclusiveMinimum"]:
            raise InputValidationError(f"{path}: debe ser > {schema['exclusiveMinimum']}")
        if schema.get("maximum") is not None and value > schema["maximum"]:
            raise InputValidationError(f"{path}: debe ser <= {schema['maximum']}")
        if schema.get("exclusiveMaximum") is not None and value >= schema["exclusiveMaximum"]:
            raise InputValidationError(f"{path}: debe ser < {schema['exclusiveMaximum']}")


class ExecutionPolicy:
    """Guardrails centralizados de autorización y capacidad."""

    def validate(self, metadata: PluginMetadata, payload: JsonObject, context: PluginContext) -> None:
        if metadata.requires_authorization:
            authorization = (context.authorization or "").strip()
            if len(authorization) < 12:
                raise AuthorizationError(
                    "Se requiere una referencia de autorización explícita y suficientemente descriptiva."
                )
        if metadata.network_access and not context.allow_network:
            raise AuthorizationError(
                f"El plugin {metadata.plugin_id} requiere red; habilítala de forma explícita."
            )
        requests_side_effects = metadata.side_effects and bool(payload.get("apply"))
        if requests_side_effects and not context.allow_side_effects:
            raise AuthorizationError(
                f"El plugin {metadata.plugin_id} solicita cambios externos; "
                "habilita side effects explícitamente."
            )


class PluginRegistry:
    """Registro determinista con soporte para plugins externos por entry points."""

    ENTRY_POINT_GROUP = "orion.plugins"

    def __init__(self, *, load_external: bool = True) -> None:
        self._plugins: MutableMapping[str, BasePlugin] = {}
        self._discovery_errors: list[JsonObject] = []
        self._load_builtins()
        if load_external:
            self._load_entry_points()

    @property
    def discovery_errors(self) -> tuple[JsonObject, ...]:
        return tuple(self._discovery_errors)

    def _load_builtins(self) -> None:
        from .builtin import BUILTIN_PLUGINS

        for plugin_type in BUILTIN_PLUGINS:
            self.register(plugin_type())

    def _load_entry_points(self) -> None:
        entry_points = importlib.metadata.entry_points()
        selected: Iterable[Any]
        if hasattr(entry_points, "select"):
            selected = entry_points.select(group=self.ENTRY_POINT_GROUP)
        else:  # pragma: no cover - compatibilidad con importlib antiguo
            selected = entry_points.get(self.ENTRY_POINT_GROUP, [])

        for entry_point in selected:
            try:
                loaded = entry_point.load()
                plugin = loaded() if isinstance(loaded, type) else loaded
                if not isinstance(plugin, BasePlugin):
                    raise TypeError(f"Entry point {entry_point.name!r} no implementa BasePlugin")
                if plugin.metadata.plugin_id in self._plugins:
                    continue
                self.register(plugin)
            except Exception as exc:  # noqa: BLE001
                self._discovery_errors.append(
                    {
                        "entry_point": entry_point.name,
                        "type": type(exc).__name__,
                        "message": str(exc),
                    }
                )

    def register(self, plugin: BasePlugin) -> None:
        if not isinstance(plugin, BasePlugin):
            raise TypeError("plugin debe implementar BasePlugin")
        plugin_id = plugin.metadata.plugin_id
        if plugin_id in self._plugins:
            raise ValueError(f"Plugin duplicado: {plugin_id}")
        self._plugins[plugin_id] = plugin

    def get(self, plugin_id: str) -> BasePlugin:
        try:
            return self._plugins[plugin_id]
        except KeyError as exc:
            available = ", ".join(sorted(self._plugins))
            raise PluginNotFoundError(f"Plugin no encontrado: {plugin_id}. Disponibles: {available}") from exc

    def list(self) -> tuple[BasePlugin, ...]:
        return tuple(self._plugins[key] for key in sorted(self._plugins))

    def manifest(self) -> JsonObject:
        return {
            "manifest_version": "1.0",
            "runtime": {
                "name": "orion-hacking-etico",
                "version": "1.0.0",
                "python_runtime": platform.python_version(),
                "minimum_python": "3.10",
                "entry_point_group": self.ENTRY_POINT_GROUP,
            },
            "plugins": [plugin.metadata.to_dict() for plugin in self.list()],
        }


class OrionRuntime:
    """Fachada de ejecución uniforme y auditable."""

    def __init__(
        self,
        registry: PluginRegistry | None = None,
        policy: ExecutionPolicy | None = None,
    ) -> None:
        self.registry = registry or PluginRegistry()
        self.policy = policy or ExecutionPolicy()

    def execute(
        self,
        plugin_id: str,
        payload: JsonObject,
        context: PluginContext,
        *,
        timeout_seconds: float | None = None,
        raise_errors: bool = False,
    ) -> PluginResult:
        plugin = self.registry.get(plugin_id)
        metadata = plugin.metadata
        timeout = timeout_seconds if timeout_seconds is not None else metadata.default_timeout_seconds
        if timeout <= 0 or timeout > metadata.max_timeout_seconds:
            raise InputValidationError(f"timeout_seconds debe estar entre 0 y {metadata.max_timeout_seconds}")

        validate_json_schema(payload, metadata.input_schema)
        self.policy.validate(metadata, payload, context)

        started = time.perf_counter()
        try:
            data = plugin.run(payload, context)
            validate_json_schema(data, metadata.output_schema)
            duration_ms = round((time.perf_counter() - started) * 1000)
            warnings: list[str] = []
            if duration_ms > timeout * 1000:
                warnings.append(
                    "La ejecución superó el límite lógico solicitado; "
                    "los motores deben aplicar timeouts internos por operación."
                )
            return PluginResult(
                plugin_id=metadata.plugin_id,
                plugin_version=metadata.version,
                request_id=context.request_id,
                actor=context.actor,
                ok=True,
                duration_ms=duration_ms,
                data=data,
                warnings=tuple(warnings),
            )
        except Exception as exc:  # noqa: BLE001
            duration_ms = round((time.perf_counter() - started) * 1000)
            if raise_errors:
                raise
            return PluginResult(
                plugin_id=metadata.plugin_id,
                plugin_version=metadata.version,
                request_id=context.request_id,
                actor=context.actor,
                ok=False,
                duration_ms=duration_ms,
                error={"type": type(exc).__name__, "message": str(exc)},
            )


def dumps_json(payload: Any) -> str:
    """Serialización canónica usada por CLI y pipelines."""

    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)
