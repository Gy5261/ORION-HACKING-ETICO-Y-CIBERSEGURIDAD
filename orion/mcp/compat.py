"""MCP interoperability helpers independent from the optional MCP SDK."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from importlib import metadata
from typing import Any, Literal

from orion import __version__

Transport = Literal["stdio", "streamable-http", "sse"]
ResponseMode = Literal["json", "stream"]


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    normalized = value.strip().casefold()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean value")


def _path(value: str, default: str) -> str:
    normalized = (value or default).strip()
    if not normalized.startswith("/"):
        normalized = f"/{normalized}"
    return normalized


@dataclass(frozen=True, slots=True)
class McpServerConfig:
    """Validated runtime settings shared by stdio and HTTP transports."""

    transport: Transport = "stdio"
    host: str = "127.0.0.1"
    port: int = 8000
    streamable_http_path: str = "/mcp"
    sse_path: str = "/sse"
    message_path: str = "/messages/"
    stateless_http: bool = True
    response_mode: ResponseMode = "json"
    cors_origins: tuple[str, ...] = ()
    log_level: str = "INFO"

    @classmethod
    def from_environment(cls) -> "McpServerConfig":
        transport = os.getenv("ORION_MCP_TRANSPORT", "stdio").strip().casefold()
        if transport not in {"stdio", "streamable-http", "sse"}:
            raise ValueError("ORION_MCP_TRANSPORT must be stdio, streamable-http, or sse")
        response_mode = os.getenv("ORION_MCP_RESPONSE_MODE", "json").strip().casefold()
        if response_mode not in {"json", "stream"}:
            raise ValueError("ORION_MCP_RESPONSE_MODE must be json or stream")
        origins = tuple(
            item.strip() for item in os.getenv("ORION_MCP_CORS_ORIGINS", "").split(",") if item.strip()
        )
        return cls(
            transport=transport,  # type: ignore[arg-type]
            host=os.getenv("ORION_MCP_HOST", "127.0.0.1").strip() or "127.0.0.1",
            port=int(os.getenv("ORION_MCP_PORT", "8000")),
            streamable_http_path=_path(os.getenv("ORION_MCP_PATH", "/mcp"), "/mcp"),
            sse_path=_path(os.getenv("ORION_MCP_SSE_PATH", "/sse"), "/sse"),
            message_path=_path(os.getenv("ORION_MCP_MESSAGE_PATH", "/messages/"), "/messages/"),
            stateless_http=_env_bool("ORION_MCP_STATELESS", True),
            response_mode=response_mode,  # type: ignore[arg-type]
            cors_origins=origins,
            log_level=os.getenv("ORION_MCP_LOG_LEVEL", "INFO").strip().upper() or "INFO",
        ).validated()

    def validated(self) -> "McpServerConfig":
        if self.transport not in {"stdio", "streamable-http", "sse"}:
            raise ValueError(f"unsupported MCP transport: {self.transport}")
        if not 1 <= self.port <= 65535:
            raise ValueError("MCP port must be between 1 and 65535")
        if self.response_mode not in {"json", "stream"}:
            raise ValueError("response mode must be json or stream")
        for name, value in {
            "streamable_http_path": self.streamable_http_path,
            "sse_path": self.sse_path,
            "message_path": self.message_path,
        }.items():
            if not value.startswith("/"):
                raise ValueError(f"{name} must start with /")
        if self.transport == "stdio" and self.cors_origins:
            raise ValueError("CORS origins only apply to HTTP transports")
        if "*" in self.cors_origins and len(self.cors_origins) > 1:
            raise ValueError("wildcard CORS origin cannot be combined with explicit origins")
        return self

    @property
    def json_response(self) -> bool:
        return self.response_mode == "json"

    @property
    def endpoint(self) -> str:
        return f"http://{self.host}:{self.port}{self.streamable_http_path}"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["json_response"] = self.json_response
        payload["endpoint"] = self.endpoint
        return payload


def mcp_sdk_version() -> str | None:
    try:
        return metadata.version("mcp")
    except metadata.PackageNotFoundError:
        return None


def capability_document(config: McpServerConfig) -> dict[str, Any]:
    """Return a client-neutral description of the MCP surface."""

    return {
        "server": {
            "name": "ORION Security Runtime",
            "version": __version__,
            "sdk": {"name": "mcp-python", "version": mcp_sdk_version()},
        },
        "protocol": {
            "encoding": "UTF-8",
            "rpc": "JSON-RPC 2.0",
            "transports": {
                "stdio": {"supported": True, "recommended_for": "local process clients"},
                "streamable-http": {
                    "supported": True,
                    "recommended_for": "remote and browser-capable clients",
                    "endpoint": config.endpoint,
                    "response_modes": ["application/json", "text/event-stream"],
                },
                "sse": {"supported": True, "legacy": True, "path": config.sse_path},
            },
            "primitives": ["tools", "resources", "resource_templates", "prompts", "logging"],
            "tool_results": ["structuredContent", "text fallback", "resource links"],
            "resource_content": ["text", "base64 blob"],
            "schema_dialect": "https://json-schema.org/draft/2020-12/schema",
        },
        "runtime": config.to_dict(),
    }


def client_configuration(
    client: str,
    transport: Transport,
    *,
    command: str = "orion-mcp",
    endpoint: str = "http://127.0.0.1:8000/mcp",
) -> dict[str, Any]:
    """Generate common MCP client configuration shapes without coupling to one vendor."""

    normalized = client.strip().casefold().replace("_", "-") or "generic"
    if transport == "stdio":
        server: dict[str, Any] = {"command": command, "args": ["--transport", "stdio"]}
    elif transport == "streamable-http":
        server = {"url": endpoint, "transport": "streamable-http"}
    elif transport == "sse":
        server = {"url": endpoint.replace("/mcp", "/sse"), "transport": "sse"}
    else:  # pragma: no cover - guarded by callers and type checking
        raise ValueError(f"unsupported transport: {transport}")

    if normalized in {"vscode", "visual-studio-code", "github-copilot"}:
        vscode_server = dict(server)
        vscode_server["type"] = "stdio" if transport == "stdio" else "http"
        return {"client": normalized, "format": "vscode-mcp.json", "payload": {"servers": {"orion": vscode_server}}}
    if normalized in {"claude-code"}:
        if transport == "stdio":
            command_line = f"claude mcp add orion -- {command} --transport stdio"
        else:
            command_line = f"claude mcp add --transport http orion {server['url']}"
        return {"client": normalized, "format": "shell", "payload": command_line, "server": server}
    if normalized in {"generic", "claude-desktop", "cursor", "windsurf", "cline", "roo-code"}:
        return {
            "client": normalized,
            "format": "mcpServers.json",
            "payload": {"mcpServers": {"orion": server}},
        }
    return {
        "client": normalized,
        "format": "generic-json",
        "payload": {"name": "orion", **server},
        "note": "Unknown client name; use this standards-based MCP connection descriptor.",
    }


def render_configuration(payload: dict[str, Any]) -> str:
    value = payload.get("payload")
    if isinstance(value, str):
        return value
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True)
