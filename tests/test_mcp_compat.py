from __future__ import annotations

import json

import pytest

from orion.mcp.compat import McpServerConfig, capability_document, client_configuration, render_configuration


def test_default_config_is_local_and_stdio() -> None:
    config = McpServerConfig().validated()
    assert config.transport == "stdio"
    assert config.host == "127.0.0.1"
    assert config.endpoint == "http://127.0.0.1:8000/mcp"
    assert config.json_response is True


def test_remote_binding_and_origins_are_explicit() -> None:
    config = McpServerConfig(
        transport="streamable-http",
        cors_origins=("https://client.example",),
    ).validated()
    assert config.cors_origins == ("https://client.example",)

    with pytest.raises(ValueError, match="wildcard"):
        McpServerConfig(
            transport="streamable-http",
            cors_origins=("*", "https://client.example"),
        ).validated()


def test_client_configuration_shapes() -> None:
    generic = client_configuration("cursor", "stdio")
    assert generic["payload"]["mcpServers"]["orion"]["command"] == "orion-mcp"

    vscode = client_configuration("vscode", "streamable-http", endpoint="https://orion.example/mcp")
    assert vscode["payload"]["servers"]["orion"]["type"] == "http"
    assert vscode["payload"]["servers"]["orion"]["url"] == "https://orion.example/mcp"

    claude_code = client_configuration("claude-code", "stdio")
    assert "claude mcp add" in render_configuration(claude_code)


def test_capability_document_is_machine_readable() -> None:
    document = capability_document(McpServerConfig(transport="streamable-http"))
    assert document["protocol"]["rpc"] == "JSON-RPC 2.0"
    assert document["protocol"]["transports"]["streamable-http"]["supported"] is True
    json.dumps(document)
