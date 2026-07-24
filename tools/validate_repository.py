"""Deterministic repository validation used by CI."""

from __future__ import annotations

import ast
import json
from pathlib import Path

from orion.plugins.core import PluginRegistry
from orion.resources import ResourceCatalog

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PLUGINS = {
    "findings_ticket_sync",
    "ioc_enricher",
    "tls_posture_audit",
    "spiderfoot",
    "theharvester",
    "sherlock",
    "osint_spy",
    "phoneinfoga",
    "photon",
}
FORBIDDEN_CALLS = {"os.system", "os.popen", "subprocess.call", "subprocess.check_output"}


def dotted_name(node: ast.AST) -> str:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
    return ".".join(reversed(parts))


def validate_source() -> None:
    for path in sorted((ROOT / "orion").rglob("*.py")):
        if "scripts" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = dotted_name(node.func)
            if name in FORBIDDEN_CALLS:
                raise AssertionError(f"forbidden process API {name} in {path}")
            if name == "subprocess.run":
                keywords = {keyword.arg: keyword.value for keyword in node.keywords if keyword.arg}
                shell = keywords.get("shell")
                if not isinstance(shell, ast.Constant) or shell.value is not False:
                    raise AssertionError(f"subprocess.run must set shell=False in {path}")


def validate_plugins() -> None:
    registry = PluginRegistry(load_external=False)
    identifiers = {plugin.metadata.plugin_id for plugin in registry.list()}
    if identifiers != EXPECTED_PLUGINS:
        raise AssertionError(f"plugin set mismatch: {sorted(identifiers)}")
    if registry.discovery_errors:
        raise AssertionError(f"plugin discovery errors: {registry.discovery_errors}")
    for plugin in registry.list():
        metadata = plugin.metadata
        if metadata.requires_authorization is not True:
            raise AssertionError(f"authorization must be enabled: {metadata.plugin_id}")
        if metadata.integration == "subprocess" and not metadata.homepage:
            raise AssertionError(f"external adapter missing homepage: {metadata.plugin_id}")


def validate_manifest() -> None:
    manifest_path = ROOT / "skills" / "skills.json"
    static = json.loads(manifest_path.read_text(encoding="utf-8"))
    runtime = PluginRegistry(load_external=False).manifest()
    static_ids = {plugin["plugin_id"] for plugin in static["plugins"]}
    runtime_ids = {plugin["plugin_id"] for plugin in runtime["plugins"]}
    if static_ids != runtime_ids:
        raise AssertionError("skills/skills.json is out of sync with the runtime")


def validate_resources() -> None:
    catalog = ResourceCatalog(ROOT)
    index = catalog.index()
    if len(index["resources"]) < 10:
        raise AssertionError("MCP resource catalog is unexpectedly small")
    try:
        catalog.read("../outside.txt")
    except ValueError:
        return
    raise AssertionError("resource catalog allowed path traversal")


def main() -> int:
    validate_source()
    validate_plugins()
    validate_manifest()
    validate_resources()
    print("ORION repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
