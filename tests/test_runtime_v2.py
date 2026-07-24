from __future__ import annotations

import json
from pathlib import Path

import pytest

from orion.plugins.adapters import ToolRunner, ToolSpec
from orion.plugins.core import AuthorizationError, OrionRuntime, PluginContext, PluginRegistry
from orion.resources import ResourceCatalog


def context(**values: object) -> PluginContext:
    data: dict[str, object] = {
        "authorization": "TOR-2026-ORION-TEST-001",
        "actor": "pytest",
        "allow_network": True,
    }
    data.update(values)
    return PluginContext(**data)  # type: ignore[arg-type]


def test_optional_tools_do_not_break_default_doctor() -> None:
    registry = PluginRegistry(load_external=False)
    assert len(registry.health()) == 9


def test_network_permission_is_explicit() -> None:
    runtime = OrionRuntime(registry=PluginRegistry(load_external=False))
    with pytest.raises(AuthorizationError):
        runtime.execute(
            "spiderfoot",
            {"operation": "list"},
            context(allow_network=False),
            raise_errors=True,
        )


def test_spiderfoot_start_requires_side_effect_permission() -> None:
    runtime = OrionRuntime(registry=PluginRegistry(load_external=False))
    with pytest.raises(AuthorizationError):
        runtime.execute(
            "spiderfoot",
            {"operation": "start", "target": "example.org"},
            context(allow_side_effects=False),
            raise_errors=True,
        )


def test_tool_runner_uses_environment_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    executable = tmp_path / "fake_tool.py"
    executable.write_text(
        "import json, sys\nprint(json.dumps({'args': sys.argv[1:]}))\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("ORION_FAKE_TOOL", str(executable))
    runner = ToolRunner(
        ToolSpec(
            tool_id="fake",
            candidates=("missing-fake-tool",),
            environment_variable="ORION_FAKE_TOOL",
            homepage="https://example.invalid",
            license="MIT",
        )
    )
    assert runner.health().available is True
    result = runner.run(["--target", "example.org"], timeout_seconds=5)
    assert json.loads(result["stdout"])["args"] == ["--target", "example.org"]


def test_resource_catalog_blocks_path_traversal(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("ORION resource", encoding="utf-8")
    catalog = ResourceCatalog(tmp_path)
    assert catalog.read("README.md") == "ORION resource"
    with pytest.raises(ValueError):
        catalog.read("../secret.txt")


def test_resource_search_returns_bounded_results(tmp_path: Path) -> None:
    (tmp_path / "guide.md").write_text("authorized defensive security", encoding="utf-8")
    catalog = ResourceCatalog(tmp_path)
    results = catalog.search("defensive", limit=1)
    assert len(results) == 1
    assert results[0]["path"] == "guide.md"
