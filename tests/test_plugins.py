from __future__ import annotations

import uuid

import pytest

from orion.plugins.core import (
    AuthorizationError,
    ExecutionPolicy,
    InputValidationError,
    OrionRuntime,
    PluginContext,
    PluginMetadata,
    PluginRegistry,
    validate_json_schema,
)


def auth(**kwargs: object) -> PluginContext:
    values: dict[str, object] = {
        "authorization": "TOR-2026-ORION-001",
        "allow_network": True,
        "actor": "pytest",
    }
    values.update(kwargs)
    return PluginContext(**values)  # type: ignore[arg-type]


def test_schema_rejects_unknown_and_missing_fields() -> None:
    schema = {
        "type": "object",
        "required": ["name"],
        "additionalProperties": False,
        "properties": {"name": {"type": "string", "minLength": 2}},
    }
    with pytest.raises(InputValidationError):
        validate_json_schema({}, schema)
    with pytest.raises(InputValidationError):
        validate_json_schema({"name": "ok", "extra": True}, schema)


def test_schema_supports_const_and_exclusive_minimum() -> None:
    validate_json_schema("orion", {"const": "orion"})
    validate_json_schema(1, {"type": "integer", "exclusiveMinimum": 0})
    with pytest.raises(InputValidationError):
        validate_json_schema(0, {"type": "integer", "exclusiveMinimum": 0})


def test_policy_requires_authorization_and_network() -> None:
    metadata = PluginMetadata(
        plugin_id="demo_plugin",
        name="Demo",
        version="1.0.0",
        category="test",
        description="Plugin de prueba defensiva.",
        risk_level="low",
        capabilities=("test",),
        input_schema={"type": "object"},
        output_schema={"type": "object"},
        network_access=True,
    )
    with pytest.raises(AuthorizationError):
        ExecutionPolicy().validate(metadata, {}, PluginContext())
    with pytest.raises(AuthorizationError):
        ExecutionPolicy().validate(metadata, {}, PluginContext(authorization="TOR-123456789"))


def test_context_requires_uuid() -> None:
    with pytest.raises(ValueError):
        PluginContext(request_id="not-a-uuid")
    assert PluginContext(request_id=str(uuid.uuid4())).request_id


def test_registry_contains_three_official_plugins() -> None:
    registry = PluginRegistry(load_external=False)
    assert [plugin.metadata.plugin_id for plugin in registry.list()] == [
        "findings_ticket_sync",
        "ioc_enricher",
        "tls_posture_audit",
    ]


def test_manifest_is_generated_from_runtime() -> None:
    manifest = PluginRegistry(load_external=False).manifest()
    assert manifest["runtime"]["entry_point_group"] == "orion.plugins"
    assert manifest["runtime"]["minimum_python"] == "3.10"
    assert len(manifest["plugins"]) == 3


def test_ioc_plugin_executes_without_external_sources() -> None:
    runtime = OrionRuntime(registry=PluginRegistry(load_external=False))
    result = runtime.execute(
        "ioc_enricher",
        {"iocs": ["8.8.8.8", "d41d8cd98f00b204e9800998ecf8427e"], "external_sources": False},
        auth(),
    )
    assert result.ok is True
    assert result.actor == "pytest"
    assert result.data is not None
    assert result.data["count"] == 2
    assert [item["type"] for item in result.data["items"]] == ["ip", "hash"]


def test_ticket_plugin_is_dry_run_by_default() -> None:
    runtime = OrionRuntime(registry=PluginRegistry(load_external=False))
    result = runtime.execute(
        "findings_ticket_sync",
        {"findings": [{"title": "TLS débil", "severity": "medium"}], "mode": "plan"},
        auth(allow_network=False),
    )
    assert result.ok is True
    assert result.data is not None
    assert result.data["count"] == 1
    assert "created" not in result.data


def test_ticket_apply_requires_side_effect_permission() -> None:
    runtime = OrionRuntime(registry=PluginRegistry(load_external=False))
    with pytest.raises(AuthorizationError):
        runtime.execute(
            "findings_ticket_sync",
            {"findings": [{"title": "X"}], "mode": "jira", "apply": True},
            auth(allow_side_effects=False),
            raise_errors=True,
        )
