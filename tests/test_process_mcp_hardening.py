"""Defense-in-depth for process environment and MCP request framing."""
from __future__ import annotations

import asyncio
from typing import Any

import pytest

from orion.mcp.compat import McpServerConfig
from orion.mcp.security import LocalHttpGuard
from orion.plugins.adapters import ToolRunner


@pytest.mark.parametrize("key", [
    "PATH", "Path", "PYTHONPATH", "PYTHONHOME", "LD_PRELOAD",
    "DYLD_INSERT_LIBRARIES", "ORION_EMERGENCY_STOP", "ORION_LAB_APPROVAL_FILE",
])
def test_external_tools_cannot_override_protected_environment(key: str) -> None:
    with pytest.raises(ValueError, match="protected"):
        ToolRunner._environment({key: "malicious"})


def test_external_tool_allows_bounded_non_privileged_env() -> None:
    environment = ToolRunner._environment({"ORION_TOOL_TEST_TOKEN": "synthetic"})
    assert environment["ORION_TOOL_TEST_TOKEN"] == "synthetic"


@pytest.mark.parametrize("extra", [
    {"ORION_TOOL_A": "x" * 4097}, {"ORION_TOOL_A": "x\x00y"},
    {"PYTHONPATH": "malicious"},
])
def test_invalid_tool_environment_fails_closed(extra: dict[str, str]) -> None:
    with pytest.raises(ValueError):
        ToolRunner._environment(extra)


async def _app(scope: Any, receive: Any, send: Any) -> None:
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": b"ok"})


def _request(method: str, headers: list[tuple[bytes, bytes]]) -> int:
    async def scenario() -> int:
        messages: list[dict[str, Any]] = []
        guard = LocalHttpGuard(_app, McpServerConfig(transport="streamable-http"))
        async def receive() -> dict[str, Any]:
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(message: dict[str, Any]) -> None:
            messages.append(message)

        await guard({"type": "http", "method": method, "headers": headers}, receive, send)
        return messages[0]["status"]

    return asyncio.run(scenario())


def test_mcp_http_rejects_conflicting_request_length_headers() -> None:
    assert _request("POST", [
        (b"host", b"127.0.0.1:8000"),
        (b"content-length", b"5"), (b"transfer-encoding", b"chunked"),
    ]) == 400


def test_mcp_http_rejects_duplicate_transfer_encoding() -> None:
    assert _request("POST", [
        (b"host", b"127.0.0.1:8000"),
        (b"transfer-encoding", b"chunked"), (b"transfer-encoding", b"chunked"),
    ]) == 400


def test_mcp_http_rejects_get_request_body() -> None:
    assert _request("GET", [(b"host", b"127.0.0.1:8000"), (b"content-length", b"2")]) == 400
    assert _request("GET", [(b"host", b"127.0.0.1:8000")]) == 200
