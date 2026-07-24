"""Model Context Protocol server exposing ORION plugins and resources."""

from __future__ import annotations

import argparse
from typing import Any, Sequence

from orion.plugins.core import OrionRuntime, PluginContext, PluginRegistry
from orion.resources import ResourceCatalog


def build_server() -> Any:
    """Build FastMCP without making MCP a mandatory base dependency."""

    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError('MCP support is not installed; run: pip install "orion-hacking-etico[mcp]"') from exc

    registry = PluginRegistry()
    runtime = OrionRuntime(registry=registry)
    catalog = ResourceCatalog()
    server = FastMCP(
        "ORION Security Runtime",
        instructions=(
            "Use ORION only for authorized defensive security and public-source intelligence. "
            "Every plugin execution requires a valid authorization reference."
        ),
    )

    @server.tool()
    def orion_list_plugins(include_health: bool = True) -> dict[str, Any]:
        """List all ORION plugins and their machine-readable contracts."""

        payload = registry.manifest()
        if include_health:
            payload["health"] = registry.health()
        return payload

    @server.tool()
    def orion_doctor(strict: bool = False) -> dict[str, Any]:
        """Check contracts, discovery, and optional third-party tool availability."""

        health = registry.health()
        unavailable = sum(1 for item in health.values() if not item["available"])
        ok = not registry.discovery_errors and (not strict or unavailable == 0)
        return {
            "ok": ok,
            "strict": strict,
            "plugin_count": len(registry.list()),
            "optional_unavailable": unavailable,
            "health": health,
            "discovery_errors": list(registry.discovery_errors),
        }

    @server.tool()
    def orion_run_plugin(
        plugin_id: str,
        payload: dict[str, Any],
        authorization: str,
        actor: str = "mcp-client",
        allow_network: bool = False,
        allow_side_effects: bool = False,
        timeout_seconds: float | None = None,
    ) -> dict[str, Any]:
        """Execute an ORION plugin with explicit authorization and permissions."""

        context = PluginContext(
            authorization=authorization,
            actor=actor,
            allow_network=allow_network,
            allow_side_effects=allow_side_effects,
        )
        return runtime.execute(
            plugin_id,
            payload,
            context,
            timeout_seconds=timeout_seconds,
        ).to_dict()

    @server.tool()
    def orion_search_resources(query: str, limit: int = 20) -> list[dict[str, Any]]:
        """Search ORION documentation, playbooks, references, schemas, and source."""

        return catalog.search(query, limit)

    @server.resource("orion://manifest")
    def manifest_resource() -> str:
        """Current plugin manifest generated from executable code."""

        return catalog.manifest_json()

    @server.resource("orion://repository/index")
    def repository_index_resource() -> str:
        """Index of all MCP-readable ORION repository resources."""

        from orion.plugins.core import dumps_json

        return dumps_json(catalog.index())

    @server.resource("orion://plugins/{plugin_id}")
    def plugin_resource(plugin_id: str) -> str:
        """Machine-readable metadata and health for one plugin."""

        return catalog.plugin_json(plugin_id)

    @server.resource("orion://repository/{path}")
    def repository_resource(path: str) -> str:
        """Read one bounded text resource from the repository."""

        return catalog.read(path)

    @server.prompt()
    def authorized_security_workflow(task: str, authorization: str) -> str:
        """Create a safe operating context for an authorized ORION task."""

        return (
            f"Task: {task}\nAuthorization reference: {authorization}\n"
            "Select the least-privileged ORION plugin. Keep network and side effects disabled unless required. "
            "Preserve evidence, return normalized JSON, and stop if scope is ambiguous."
        )

    return server


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="orion-mcp")
    parser.add_argument(
        "--transport",
        choices=("stdio", "streamable-http", "sse"),
        default="stdio",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    server = build_server()
    server.run(transport=args.transport)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
