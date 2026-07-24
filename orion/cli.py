"""CLI oficial del runtime de plugins ORION."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from orion import __version__
from orion.plugins.core import (
    OrionPluginError,
    OrionRuntime,
    PluginContext,
    PluginRegistry,
    dumps_json,
    validate_json_schema,
)


def _read_json(path: str) -> dict[str, Any]:
    raw = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("La entrada del plugin debe ser un objeto JSON.")
    return payload


def _write_json(payload: Any, output: str | None = None) -> None:
    rendered = dumps_json(payload) + "\n"
    if output:
        Path(output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="orion",
        description="Runtime auditable de plugins para ciberseguridad ética y autorizada.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plugins = subparsers.add_parser("plugins", help="Administrar y ejecutar plugins.")
    plugin_commands = plugins.add_subparsers(dest="plugin_command", required=True)

    list_parser = plugin_commands.add_parser("list", help="Listar plugins disponibles.")
    list_parser.add_argument("--json", action="store_true", help="Salida JSON completa.")

    describe = plugin_commands.add_parser("describe", help="Mostrar el contrato de un plugin.")
    describe.add_argument("plugin_id")

    run = plugin_commands.add_parser("run", help="Ejecutar un plugin con entrada JSON.")
    run.add_argument("plugin_id")
    run.add_argument("--input", required=True, help="Archivo JSON o '-' para stdin.")
    run.add_argument("--output", help="Archivo de salida; por defecto stdout.")
    run.add_argument("--authorization", required=True, help="Ticket, ToR o referencia de autorización.")
    run.add_argument("--actor", default="local-user")
    run.add_argument("--request-id", help="UUID externo para correlación; se genera si se omite.")
    run.add_argument("--allow-network", action="store_true")
    run.add_argument("--allow-side-effects", action="store_true")
    run.add_argument("--timeout", type=float)

    export = plugin_commands.add_parser("export-manifest", help="Generar manifiesto desde el runtime real.")
    export.add_argument("--output", required=True)

    plugin_commands.add_parser("doctor", help="Validar runtime, contratos y descubrimiento.")
    return parser


def _plugins_list(registry: PluginRegistry, as_json: bool) -> int:
    if as_json:
        _write_json(registry.manifest())
        return 0
    for plugin in registry.list():
        metadata = plugin.metadata
        permissions: list[str] = []
        if metadata.network_access:
            permissions.append("network")
        if metadata.side_effects:
            permissions.append("side-effects")
        suffix = f" [{', '.join(permissions)}]" if permissions else ""
        print(f"{metadata.plugin_id:<24} {metadata.version:<10} {metadata.risk_level:<6}{suffix}")
    return 0


def _doctor(registry: PluginRegistry) -> int:
    checks: list[dict[str, Any]] = []
    for plugin in registry.list():
        metadata = plugin.metadata
        validate_json_schema(
            metadata.to_dict(),
            {
                "type": "object",
                "required": ["plugin_id", "name", "version", "input_schema", "output_schema"],
            },
        )
        checks.append({"plugin_id": metadata.plugin_id, "version": metadata.version, "status": "ok"})

    ok = not registry.discovery_errors
    _write_json(
        {
            "ok": ok,
            "runtime_version": __version__,
            "plugin_count": len(checks),
            "checks": checks,
            "discovery_errors": list(registry.discovery_errors),
        }
    )
    return 0 if ok else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        registry = PluginRegistry()
        if args.command == "plugins" and args.plugin_command == "list":
            return _plugins_list(registry, args.json)
        if args.command == "plugins" and args.plugin_command == "describe":
            _write_json(registry.get(args.plugin_id).metadata.to_dict())
            return 0
        if args.command == "plugins" and args.plugin_command == "export-manifest":
            _write_json(registry.manifest(), args.output)
            return 0
        if args.command == "plugins" and args.plugin_command == "doctor":
            return _doctor(registry)
        if args.command == "plugins" and args.plugin_command == "run":
            runtime = OrionRuntime(registry=registry)
            context_kwargs: dict[str, Any] = {
                "authorization": args.authorization,
                "actor": args.actor,
                "allow_network": args.allow_network,
                "allow_side_effects": args.allow_side_effects,
            }
            if args.request_id:
                context_kwargs["request_id"] = args.request_id
            result = runtime.execute(
                args.plugin_id,
                _read_json(args.input),
                PluginContext(**context_kwargs),
                timeout_seconds=args.timeout,
            )
            _write_json(result.to_dict(), args.output)
            return 0 if result.ok else 1
        parser.error("Comando no implementado")
    except (OrionPluginError, ValueError, OSError, json.JSONDecodeError) as exc:
        _write_json({"ok": False, "error": {"type": type(exc).__name__, "message": str(exc)}})
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
