from __future__ import annotations

import pytest


def test_mcp_server_builds_when_dependency_is_installed() -> None:
    pytest.importorskip("mcp")
    from orion.mcp.server import build_server

    assert build_server() is not None
