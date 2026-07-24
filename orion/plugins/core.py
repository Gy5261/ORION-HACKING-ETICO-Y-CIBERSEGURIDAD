"""Core contracts and execution runtime for ORION plugins."""

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
    """Base error for the ORION plugin runtime."""


class InputValidationError(OrionPluginError):
    """Raised when plugin input or output violates its contract."""


class AuthorizationError(OrionPluginError):
    """Raised when execution policy rejects a request."""


class PluginNotFoundError(OrionPluginError):
    """Raised when a plugin identifier is not registered."""


class PluginExecutionError(OrionPluginError):
    """Raised when plugin execution fails."""


class ToolUnavailableError(PluginExecutionError):
    """Raised when an optional third-party tool is not installed."""


@dataclass(frozen=True, slots=True)
class PluginHealth:
    """Availability report for a plugin and its optional dependencies."""

    available: bool
    status: str = "ready"
    message: str = ""
    details: JsonObject = field(default_factory=dict)

    def to_dict(self) -> JsonObject:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PluginMetadata:
    """Immutable, machine-readable contract for an ORION plugin."""

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
    homepage: str | None = None
    license: str | None = None
    integration: str = "native"

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[a-z][a-z0-9_.-]{2,63}", self.plugin_id):
            raise ValueError(f"invalid plugin_id: {self.plugin_id!r}")
        if not self.name.strip():
            raise ValueError("name cannot be empty")
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?", self.version):
            raise ValueError(f"invalid semantic version: {self.version!r}")
        if self.risk_level not in {"low", "medium", "high"}:
            raise ValueError("risk_level must be low, medium, or high")
        if not self.capabilities:
            raise ValueError("capabilities must contain at least one item")
        if self.default_timeout_seconds <= 0:
            raise ValueError("default_timeout_seconds must be positive")
        if self.max_timeout_seconds < self.default_timeout_seconds:
            raise ValueError("max_timeout_seconds cannot be lower than the default")
        if self.input_schema.get("type") != "object":
            raise ValueError("input_schema must declare type=object")
        if self.output_schema.get("type") not in {"object", "array"}:
            raise ValueError("output_schema must declare type=object or type=array")

    def to_dict(self) -> JsonObject:
        payload = asdict(self)
        payload["capabilities"] = list(self.capabilities)
        payload["tags"] = list(self.tags)
        return payload


@dataclass(frozen=True, slots=True)
class PluginContext:
    """Explicit authorization and execution context."""

    authorization: str | None = None
    allow_network: bool = False
    allow_side_effects: bool = False
    actor: str = "local-user"
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    environment: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.actor.strip():
            raise ValueError("actor cannot be empty")
        try:
            uuid.UUID(self.request_id)
        except ValueError as exc:
            raise ValueError("request_id must be a valid UUID") from exc


@dataclass(frozen=True, slots=True)
class PluginResult:
    """Normalized result for CLI, MCP, agents, and pipelines."""

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
    """Stable interface implemented by internal and third-party plugins."""

    metadata: PluginMetadata

    @abstractmethod
    def run(self, payload: JsonObject, context: PluginContext) -> JsonObject | list[Any]:
        """Execute the plugin and return a JSON-serializable value."""

    def health(self) -> PluginHealth:
        """Report whether the plugin can execute in the current environment."""

        return PluginHealth(available=True)

    def requests_side_effects(self, payload: JsonObject) -> bool:
        """Return whether this particular request performs external changes."""

        return self.metadata.side_effects and bool(payload.get("apply"))


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
    """Validate the deterministic JSON Schema subset used by ORION."""

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
                f"{path}: expected exactly one oneOf match; matches={successes}; details={errors[:3]}"
            )
        return

    if "anyOf" in schema:
        errors = []
        for candidate in schema["anyOf"]:
            try:
                validate_json_schema(value, candidate, path)
                break
            except InputValidationError as exc:
                errors.append(str(exc))
        else:
            raise InputValidationError(f"{path}: no anyOf variant matched; details={errors[:3]}")

    expected = schema.get("type")
    if expected:
        expected_types = [expected] if isinstance(expected, str) else list(expected)
        unknown = [item for item in expected_types if item not in _JSON_TYPES]
        if unknown:
            raise InputValidationError(f"{path}: unsupported schema types: {unknown}")
        if not any(_is_type(value, item) for item in expected_types):
            raise InputValidationError(f"{path}: expected {expected_types}, received {type(value).__name__}")

    if "const" in schema and value != schema["const"]:
        raise InputValidationError(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise InputValidationError(f"{path}: value {value!r} is outside enum {schema['enum']!r}")

    if isinstance(value, dict):
        required = schema.get("required", [])
        missing = [key for key in required if key not in value]
        if missing:
            raise InputValidationError(f"{path}: missing required fields {missing}")
        properties: Mapping[str, Any] = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            unexpected = sorted(set(value) - set(properties))
            if unexpected:
                raise InputValidationError(f"{path}: unknown fields {unexpected}")
        for key, child_schema in properties.items():
            if key in value:
                validate_json_schema(value[key], child_schema, f"{path}.{key}")

    if isinstance(value, list):
        min_items = schema.get("minItems")
        max_items = schema.get("maxItems")
        if min_items is not None and len(value) < min_items:
            raise InputValidationError(f"{path}: requires at least {min_items} items")
        if max_items is not None and len(value) > max_items:
            raise InputValidationError(f"{path}: allows at most {max_items} items")
        if schema.get("uniqueItems"):
            rendered = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(set(rendered)) != len(rendered):
                raise InputValidationError(f"{path}: duplicate items are not allowed")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                validate_json_schema(item, item_schema, f"{path}[{index}]")

    if isinstance(value, str):
        min_length = schema.get("minLength")
        max_length = schema.get("maxLength")
        if min_length is not None and len(value) < min_length:
            raise InputValidationError(f"{path}: minimum length is {min_length}")
        if max_length is not None and len(value) > max_length:
            raise InputValidationError(f"{path}: maximum length is {max_length}")
        pattern = schema.get("pattern")
        if pattern and re.search(pattern, value) is None:
            raise InputValidationError(f"{path}: value does not match the required pattern")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if schema.get("minimum") is not None and value < schema["minimum"]:
            raise InputValidationError(f"{path}: must be >= {schema['minimum']}")
        if schema.get("exclusiveMinimum") is not None and value <= schema["exclusiveMinimum"]:
            raise InputValidationError(f"{path}: must be > {schema['exclusiveMinimum']}")
        if schema.get("maximum") is not None and value > schema["maximum"]:
            raise InputValidationError(f"{path}: must be <= {schema['maximum']}")
        if schema.get("exclusiveMaximum") is not None and value >= schema["exclusiveMaximum"]:
            raise InputValidationError(f"{path}: must be < {schema['exclusiveMaximum']}")


class ExecutionPolicy:
    """Centralized authorization and capability guardrails."""

    def validate(self, plugin: BasePlugin, payload: JsonObject, context: PluginContext) -> None:
        metadata = plugin.metadata
        if metadata.requires_authorization:
            authorization = (context.authorization or "").strip()
            if len(authorization) < 12:
                raise AuthorizationError("an explicit authorization reference is required")
        if metadata.network_access and not context.allow_network:
            raise AuthorizationError(f"plugin {metadata.plugin_id} requires explicit network permission")
        if plugin.requests_side_effects(payload) and not context.allow_side_effects:
            raise AuthorizationError(f"plugin {metadata.plugin_id} requires explicit side-effect permission")


class PluginRegistry:
    """Deterministic plugin registry with Python entry-point discovery."""

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
        from .osint import OSINT_PLUGINS

        for plugin_type in (*BUILTIN_PLUGINS, *OSINT_PLUGINS):
            self.register(plugin_type())

    def _load_entry_points(self) -> None:
        entry_points = importlib.metadata.entry_points()
        selected: Iterable[Any]
        if hasattr(entry_points, "select"):
            selected = entry_points.select(group=self.ENTRY_POINT_GROUP)
        else:  # pragma: no cover
            selected = entry_points.get(self.ENTRY_POINT_GROUP, [])

        for entry_point in selected:
            try:
                loaded = entry_point.load()
                plugin = loaded() if isinstance(loaded, type) else loaded
                if not isinstance(plugin, BasePlugin):
                    raise TypeError(f"entry point {entry_point.name!r} does not implement BasePlugin")
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
            raise TypeError("plugin must implement BasePlugin")
        plugin_id = plugin.metadata.plugin_id
        if plugin_id in self._plugins:
            raise ValueError(f"duplicate plugin: {plugin_id}")
        self._plugins[plugin_id] = plugin

    def get(self, plugin_id: str) -> BasePlugin:
        try:
            return self._plugins[plugin_id]
        except KeyError as exc:
            available = ", ".join(sorted(self._plugins))
            raise PluginNotFoundError(f"plugin not found: {plugin_id}; available: {available}") from exc

    def list(self) -> tuple[BasePlugin, ...]:
        return tuple(self._plugins[key] for key in sorted(self._plugins))

    def health(self) -> JsonObject:
        return {plugin.metadata.plugin_id: plugin.health().to_dict() for plugin in self.list()}

    def manifest(self) -> JsonObject:
        from orion import __version__

        return {
            "manifest_version": "2.0",
            "runtime": {
                "name": "orion-hacking-etico",
                "version": __version__,
                "python_runtime": platform.python_version(),
                "minimum_python": "3.10",
                "entry_point_group": self.ENTRY_POINT_GROUP,
            },
            "plugins": [plugin.metadata.to_dict() for plugin in self.list()],
        }


class OrionRuntime:
    """Uniform, auditable plugin execution facade."""

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
            raise InputValidationError(f"timeout_seconds must be between 0 and {metadata.max_timeout_seconds}")

        validate_json_schema(payload, metadata.input_schema)
        self.policy.validate(plugin, payload, context)

        started = time.perf_counter()
        try:
            health = plugin.health()
            if not health.available:
                raise ToolUnavailableError(health.message or f"plugin {plugin_id} is unavailable")
            data = plugin.run(payload, context)
            validate_json_schema(data, metadata.output_schema)
            duration_ms = round((time.perf_counter() - started) * 1000)
            warnings: list[str] = []
            if duration_ms > timeout * 1000:
                warnings.append("execution exceeded the requested logical timeout")
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
    """Serialize data using ORION's canonical JSON representation."""

    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)
