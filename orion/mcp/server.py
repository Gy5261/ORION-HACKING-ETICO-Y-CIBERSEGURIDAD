"""Model Context Protocol server exposing ORION plugins and resources."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from typing import Any, Sequence, cast

from orion.mcp.compat import (
    McpServerConfig,
    Transport,
    capability_document,
    client_configuration,
    render_configuration,
)
from orion.plugins.core import OrionRuntime, PluginContext, PluginRegistry, dumps_json
from orion.resources import ResourceCatalog

_SERVER_INSTRUCTIONS = (
    "ORION exposes authorized defensive-security and public-source-intelligence plugins through MCP. "
    "Every plugin execution requires an authorization reference. Keep network access and side effects disabled "
    "unless they are explicitly required by the approved scope. Resources are read-only and bounded."
)


def _resource_reader(catalog: ResourceCatalog, path: str) -> Callable[[], str | bytes]:
    """Create a zero-argument reader for one exact repository resource."""

    def read_resource() -> str | bytes:
        return catalog.read_mcp(path)

    return read_resource


def _configure_fastmcp(server: Any, config: McpServerConfig) -> None:
    """Apply settings through the stable FastMCP settings surface."""

    settings = server.settings
    values = {
        "host": config.host,
        "port": config.port,
        "streamable_http_path": config.streamable_http_path,
        "sse_path": config.sse_path,
        "message_path": config.message_path,
        "stateless_http": config.stateless_http,
        "json_response": config.json_response,
        "log_level": config.log_level,
    }
    for name, value in values.items():
        if hasattr(settings, name):
            setattr(settings, name, value)


def build_server(config: McpServerConfig | None = None) -> Any:
    """Build the standards-based FastMCP server without making MCP a base dependency."""

    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError('MCP support is not installed; run: pip install "orion-hacking-etico[mcp]"') from exc

    active_config = (config or McpServerConfig.from_environment()).validated()
    registry = PluginRegistry()
    runtime = OrionRuntime(registry=registry)
    catalog = ResourceCatalog()
    server = FastMCP(
        "ORION Security Runtime",
        instructions=_SERVER_INSTRUCTIONS,
        stateless_http=active_config.stateless_http,
        json_response=active_config.json_response,
    )
    _configure_fastmcp(server, active_config)

    @server.tool()
    def orion_mcp_capabilities() -> dict[str, Any]:
        """Describe transports, MCP primitives, encodings, and response formats supported by ORION."""

        payload = capability_document(active_config)
        payload["surface"] = {
            "plugins": len(registry.list()),
            "resources": len(catalog.list()),
            "tools": [
                "orion_mcp_capabilities",
                "orion_client_config",
                "orion_list_plugins",
                "orion_get_plugin",
                "orion_doctor",
                "orion_run_plugin",
                "orion_search_resources",
                "orion_resource_links",
                "orion_read_resource",
                "orion_read_resource_content",
            ],
        }
        return payload

    @server.tool()
    def orion_client_config(
        client: str = "generic",
        transport: str = "stdio",
        endpoint: str | None = None,
        command: str = "orion-mcp",
    ) -> dict[str, Any]:
        """Generate a standards-based MCP connection configuration for common AI clients."""

        if transport not in {"stdio", "streamable-http", "sse"}:
            raise ValueError("transport must be stdio, streamable-http, or sse")
        return client_configuration(
            client,
            cast(Transport, transport),
            command=command,
            endpoint=endpoint or active_config.endpoint,
        )

    @server.tool()
    def orion_list_plugins(include_health: bool = True) -> dict[str, Any]:
        """List all ORION plugins and their machine-readable contracts."""

        payload = registry.manifest()
        if include_health:
            payload["health"] = registry.health()
        return payload

    @server.tool()
    def orion_get_plugin(plugin_id: str, include_health: bool = True) -> dict[str, Any]:
        """Return one exact plugin contract, permissions, schemas, and optional dependency health."""

        plugin = registry.get(plugin_id)
        payload = plugin.metadata.to_dict()
        if include_health:
            payload["health"] = plugin.health().to_dict()
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
            "resource_count": len(catalog.list()),
            "optional_unavailable": unavailable,
            "health": health,
            "discovery_errors": list(registry.discovery_errors),
            "mcp": capability_document(active_config),
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
        """Execute an ORION plugin with explicit authorization and least-privilege permissions."""

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
        """Search ORION documentation, playbooks, references, schemas, samples, and source."""

        return catalog.search(query, limit)

    @server.tool()
    def orion_resource_links(query: str = "", limit: int = 100) -> dict[str, Any]:
        """Return MCP resource-link descriptors for repository resources."""

        bounded_limit = max(1, min(limit, 500))
        descriptors = catalog.list()
        if query.strip():
            normalized = query.strip().casefold()
            descriptors = tuple(item for item in descriptors if normalized in item.path.casefold())
        links = [
            {
                "type": "resource_link",
                "uri": item.uri,
                "name": item.name,
                "title": item.path,
                "description": f"Read-only ORION repository resource: {item.path}",
                "mimeType": item.media_type,
                "size": item.size_bytes,
            }
            for item in descriptors[:bounded_limit]
        ]
        return {"count": len(links), "resources": links}

    @server.tool()
    def orion_read_resource(path: str) -> str:
        """Read one UTF-8 repository resource by its traversal-safe relative path."""

        return catalog.read(path)

    @server.tool()
    def orion_read_resource_content(path: str) -> dict[str, Any]:
        """Read text or binary resource content with MIME type and explicit encoding metadata."""

        return catalog.payload(path)

    @server.resource("orion://manifest", mime_type="application/json")
    def manifest_resource() -> str:
        """Current plugin manifest generated from executable code."""

        return catalog.manifest_json()

    @server.resource("orion://mcp/capabilities", mime_type="application/json")
    def mcp_capabilities_resource() -> str:
        """Transport-neutral MCP interoperability document."""

        return dumps_json(capability_document(active_config))

    @server.resource("orion://repository/index", mime_type="application/json")
    def repository_index_resource() -> str:
        """Index of all MCP-readable ORION repository resources."""

        return dumps_json(catalog.index())

    @server.resource("orion://plugins/{plugin_id}", mime_type="application/json")
    def plugin_resource(plugin_id: str) -> str:
        """Machine-readable metadata and health for one plugin."""

        return catalog.plugin_json(plugin_id)

    @server.resource("orion://mcp/client-config/{client}/{transport}", mime_type="application/json")
    def client_config_resource(client: str, transport: str) -> str:
        """Generate a client-specific MCP configuration resource."""

        if transport not in {"stdio", "streamable-http", "sse"}:
            raise ValueError("transport must be stdio, streamable-http, or sse")
        return dumps_json(client_configuration(client, cast(Transport, transport), endpoint=active_config.endpoint))

    for index, descriptor in enumerate(catalog.list()):
        reader = _resource_reader(catalog, descriptor.path)
        reader.__name__ = f"repository_resource_{index}"
        reader.__doc__ = f"Read the ORION repository resource {descriptor.path}."
        server.resource(descriptor.uri, mime_type=descriptor.media_type)(reader)

    @server.prompt()
    def authorized_security_workflow(task: str, authorization: str) -> str:
        """Create a safe operating context for an authorized ORION task."""

        return (
            f"Task: {task}\nAuthorization reference: {authorization}\n"
            "Select the least-privileged ORION plugin. Keep network and side effects disabled unless required. "
            "Preserve evidence, return normalized JSON, and stop if scope is ambiguous."
        )

    @server.prompt()
    def mcp_integration_guide(client: str = "generic", transport: str = "stdio") -> str:
        """Return an integration prompt and exact client configuration for ORION MCP."""

        if transport not in {"stdio", "streamable-http", "sse"}:
            raise ValueError("transport must be stdio, streamable-http, or sse")
        configuration = client_configuration(client, cast(Transport, transport), endpoint=active_config.endpoint)
        return (
            "Integrate ORION as a Model Context Protocol server. Initialize the session, negotiate capabilities, "
            "list tools/resources/prompts, and prefer structuredContent while retaining text fallback support.\n\n"
            f"Configuration:\n{render_configuration(configuration)}"
        )

    return server


def build_http_app(server: Any, config: McpServerConfig, *, legacy_sse: bool = False) -> Any:
    """Build an ASGI app with browser-compatible CORS for HTTP MCP clients."""

    try:
        from starlette.middleware.cors import CORSMiddleware
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError('HTTP MCP support requires the "mcp" optional dependency') from exc

    app = server.sse_app() if legacy_sse else server.streamable_http_app()
    if not config.cors_origins:
        return app
    return CORSMiddleware(
        app,
        allow_origins=list(config.cors_origins),
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "Last-Event-ID",
            "MCP-Protocol-Version",
            "Mcp-Session-Id",
        ],
        expose_headers=["MCP-Protocol-Version", "Mcp-Session-Id"],
        allow_credentials="*" not in config.cors_origins,
    )


def build_parser(defaults: McpServerConfig | None = None) -> argparse.ArgumentParser:
    config = defaults or McpServerConfig.from_environment()
    parser = argparse.ArgumentParser(
        prog="orion-mcp",
        description="ORION MCP server for stdio, Streamable HTTP, and legacy SSE clients.",
    )
    parser.add_argument("--transport", choices=("stdio", "streamable-http", "sse"), default=config.transport)
    parser.add_argument("--host", default=config.host)
    parser.add_argument("--port", type=int, default=config.port)
    parser.add_argument("--path", default=config.streamable_http_path, help="Streamable HTTP endpoint path.")
    parser.add_argument("--sse-path", default=config.sse_path)
    parser.add_argument("--message-path", default=config.message_path)
    parser.add_argument("--log-level", choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"), default=config.log_level)
    parser.add_argument("--cors-origin", action="append", default=list(config.cors_origins))
    parser.add_argument("--allow-any-origin", action="store_true", help="Allow wildcard browser CORS. Not recommended.")
    parser.add_argument("--allow-remote", action="store_true", help="Permit binding to a non-loopback interface.")
    parser.add_argument("--print-config", action="store_true", help="Print resolved configuration as JSON and exit.")
    state = parser.add_mutually_exclusive_group()
    state.add_argument("--stateless", dest="stateless_http", action="store_true")
    state.add_argument("--stateful", dest="stateless_http", action="store_false")
    parser.set_defaults(stateless_http=config.stateless_http)
    response = parser.add_mutually_exclusive_group()
    response.add_argument("--json-response", dest="response_mode", action="store_const", const="json")
    response.add_argument("--stream-response", dest="response_mode", action="store_const", const="stream")
    parser.set_defaults(response_mode=config.response_mode)
    return parser


def _config_from_args(args: argparse.Namespace) -> McpServerConfig:
    origins = ("*",) if args.allow_any_origin else tuple(dict.fromkeys(args.cors_origin))
    config = McpServerConfig(
        transport=cast(Transport, args.transport),
        host=args.host,
        port=args.port,
        streamable_http_path=args.path,
        sse_path=args.sse_path,
        message_path=args.message_path,
        stateless_http=args.stateless_http,
        response_mode=args.response_mode,
        cors_origins=origins,
        log_level=args.log_level,
    ).validated()
    if config.transport != "stdio" and config.host not in {"127.0.0.1", "localhost", "::1"} and not args.allow_remote:
        raise ValueError("remote HTTP binding requires --allow-remote")
    return config


def _run_http(server: Any, config: McpServerConfig, *, legacy_sse: bool = False) -> None:
    if not config.cors_origins:
        server.run(transport="sse" if legacy_sse else "streamable-http")
        return
    try:
        import uvicorn
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError('HTTP MCP support requires the "mcp" optional dependency') from exc
    uvicorn.run(
        build_http_app(server, config, legacy_sse=legacy_sse),
        host=config.host,
        port=config.port,
        log_level=config.log_level.casefold(),
    )


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        config = _config_from_args(args)
        if args.print_config:
            sys.stdout.write(dumps_json(config.to_dict()) + "\n")
            return 0
        server = build_server(config)
        if config.transport == "stdio":
            server.run(transport="stdio")
        elif config.transport == "streamable-http":
            _run_http(server, config)
        else:
            _run_http(server, config, legacy_sse=True)
        return 0
    except (RuntimeError, ValueError) as exc:
        sys.stderr.write(f"orion-mcp: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
