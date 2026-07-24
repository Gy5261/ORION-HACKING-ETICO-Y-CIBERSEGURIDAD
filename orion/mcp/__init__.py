"""MCP integration for ORION."""

from orion.mcp.compat import McpServerConfig, capability_document, client_configuration
from orion.mcp.server import build_http_app, build_server

__all__ = [
    "McpServerConfig",
    "build_http_app",
    "build_server",
    "capability_document",
    "client_configuration",
]
