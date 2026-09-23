"""Regression tests for authorization, quotas and bounded local resources. No external targets."""
from __future__ import annotations

import json
import math
import os
import sqlite3
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pytest

from orion.controls import (
    ControlDenied, canonical_json, controls_status, enforce_request, lab_preflight,
    load_private_json, request_fingerprint, review_approval,
)
from orion.plugins.core import (
    AuthorizationError, ExecutionPolicy, InputValidationError, OrionRuntime, PluginContext, PluginRegistry,
    validate_json_schema,
)
from orion.resources import ResourceCatalog

PAYLOAD = {"targets": ["127.0.0.1:8443"], "workers": 1, "timeout": 0.5}


@pytest.fixture(autouse=True)
def clean_controls(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("ORION_EMERGENCY_STOP", "ORION_LAB_APPROVAL_FILE", "ORION_AUDIT_DATABASE", "ORION_RESOURCE_ROOT"):
        monkeypatch.delenv(key, raising=False)


def approval() -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    return {"schema_version": 1, "authorization": "LAB-REVIEW-TEST-2026", "actor": "pytest",
            "asset_owner": "test-owner", "approved_by": "independent-reviewer", "purpose": "synthetic TLS test",
            "legal_basis_reference": "TEST-ONLY-OWNER-CONSENT", "environment": "isolated-lab",
            "not_before": (now - timedelta(minutes=1)).isoformat(),
            "expires_at": (now + timedelta(minutes=10)).isoformat(), "revoked": False,
            "request_sha256": request_fingerprint("tls_posture_audit", PAYLOAD), "max_uses": 2}


def provision(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, document: dict[str, Any] | None = None) -> Path:
    path = tmp_path / "operator-permit.json"
    path.write_text(json.dumps(document or approval()), encoding="utf-8")
    path.chmod(0o600)
    monkeypatch.setenv("ORION_LAB_APPROVAL_FILE", str(path))
    monkeypatch.setenv("ORION_AUDIT_DATABASE", str(tmp_path / "audit.sqlite3"))
    return path


def admit(request_id: str | None = None, payload: dict[str, Any] | None = None) -> None:
    enforce_request("tls_posture_audit", payload or PAYLOAD, authorization="LAB-REVIEW-TEST-2026",
                    actor="pytest", request_id=request_id or str(uuid.uuid4()), network=True, side_effects=False)


def test_fingerprint_is_stable_and_exact() -> None:
    assert request_fingerprint("demo", {"b": 2, "a": 1}) == request_fingerprint("demo", {"a": 1, "b": 2})
    assert request_fingerprint("demo", {"a": 1}) != request_fingerprint("other", {"a": 1})
    assert request_fingerprint("demo", {"a": 1}) != request_fingerprint("demo", {"a": 2})


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf, {"nested": math.nan}, {1: "invalid-key"}, object()])
def test_non_json_values_are_rejected(value: Any) -> None:
    with pytest.raises(ValueError):
        canonical_json(value)


def test_nested_and_oversized_json_are_rejected() -> None:
    nested: Any = 0
    for _ in range(40):
        nested = [nested]
    with pytest.raises(ValueError):
        canonical_json(nested)
    with pytest.raises(ValueError):
        canonical_json("x" * (1024 * 1024 + 1))


def test_oneof_sibling_constraints_are_not_skipped() -> None:
    with pytest.raises(InputValidationError):
        validate_json_schema("xx", {"oneOf": [{"type": "string"}], "minLength": 3})


@pytest.mark.parametrize("target", ["8.8.8.8:443", "169.254.169.254", "0.0.0.0", "example.org",
                                       "https://127.0.0.1", "127.0.0.1:0", "127.0.0.1:65536",
                                       "::ffff:127.0.0.1", "127.0.0.1 ", "192.168.1.255"])
def test_lab_rejects_ambiguous_or_external_targets(target: str) -> None:
    with pytest.raises(ControlDenied):
        lab_preflight({"targets": [target]})


@pytest.mark.parametrize("field,value", [("workers", True), ("workers", 5), ("timeout", math.nan), ("timeout", 11)])
def test_lab_limits_are_enforced(field: str, value: Any) -> None:
    with pytest.raises(ControlDenied):
        lab_preflight({**PAYLOAD, field: value})


def test_lab_preflight_is_not_an_authorization_or_isolation_test() -> None:
    result = lab_preflight(PAYLOAD)
    assert result["network_contacted"] is False
    assert result["isolation_verified"] is False
    assert result["peers"] == [{"address": "127.0.0.1", "port": 8443}]


def test_review_never_certifies_consent_or_identity() -> None:
    result = review_approval(approval())
    assert result["ok"] is True
    assert result["legal_validity_verified"] is False
    assert result["identity_verified"] is False


@pytest.mark.parametrize("field,value", [("revoked", True), ("environment", "production"),
    ("approved_by", "PYTEST"), ("max_uses", True), ("max_uses", 101), ("schema_version", True),
    ("request_sha256", "wrong"), ("expires_at", "2000-01-01T00:00:00Z"),
    ("not_before", "2999-01-01T00:00:00Z"), ("expires_at", "2999-01-01T00:00:00Z"),
    ("not_before", "2026-01-01T00:00:00")])
def test_invalid_approvals_fail_closed(field: str, value: Any) -> None:
    with pytest.raises(ControlDenied):
        review_approval({**approval(), field: value})


def test_no_approval_no_probe() -> None:
    with pytest.raises(ControlDenied, match="ORION_LAB_APPROVAL_FILE"):
        admit()


def test_changed_payload_is_not_approved(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    provision(tmp_path, monkeypatch)
    with pytest.raises(ControlDenied, match="differs"):
        admit(payload={**PAYLOAD, "timeout": 1.0})


def test_usage_limit_and_duplicate_request_ids(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    provision(tmp_path, monkeypatch)
    request_id = str(uuid.uuid4())
    admit(request_id)
    with pytest.raises(ControlDenied, match="already consumed"):
        admit(request_id)
    admit()
    with pytest.raises(ControlDenied, match="usage limit"):
        admit()


def test_quota_is_atomic_under_concurrency(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    provision(tmp_path, monkeypatch)

    def attempt(_: int) -> bool:
        try:
            admit()
            return True
        except ControlDenied:
            return False

    with ThreadPoolExecutor(max_workers=8) as pool:
        assert sum(pool.map(attempt, range(8))) == 2


def test_approval_requires_private_permissions(tmp_path: Path) -> None:
    path = tmp_path / "permit.json"
    path.write_text(json.dumps(approval()), encoding="utf-8")
    path.chmod(0o644)
    if os.name == "posix":
        with pytest.raises(ControlDenied, match="permissions"):
            load_private_json(str(path))


def test_duplicate_json_keys_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "permit.json"
    path.write_text('{"revoked":true,"revoked":false}', encoding="utf-8")
    path.chmod(0o600)
    with pytest.raises(ControlDenied):
        load_private_json(str(path))


def test_emergency_stop_blocks_even_offline_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ORION_EMERGENCY_STOP", "true")
    with pytest.raises(AuthorizationError, match="emergency"):
        OrionRuntime().execute("ioc_enricher", {"iocs": ["127.0.0.1"]},
                               PluginContext(authorization="TEST-AUTHORIZATION-001"))


def test_offline_ioc_does_not_need_network_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    from orion.scripts import ioc_enricher

    def forbidden_dns(_: str) -> Any:
        pytest.fail("offline classification must not resolve DNS")

    monkeypatch.setattr(ioc_enricher, "dns_lookup", forbidden_dns)
    result = OrionRuntime().execute("ioc_enricher", {"iocs": ["127.0.0.1", "a" * 64]},
                                    PluginContext(authorization="TEST-AUTHORIZATION-001"))
    assert result.ok is True


def test_online_osint_cannot_be_self_authorized() -> None:
    plugin = PluginRegistry().get("sherlock")
    with pytest.raises(AuthorizationError, match="not admitted"):
        ExecutionPolicy().validate(plugin, {}, PluginContext(authorization="I-APPROVE-MYSELF-001", allow_network=True))


def test_writes_stay_disabled_despite_flags() -> None:
    plugin = PluginRegistry().get("findings_ticket_sync")
    with pytest.raises(AuthorizationError, match="writes are disabled"):
        ExecutionPolicy().validate(plugin, {"mode": "jira", "apply": True}, PluginContext(
            authorization="TEST-AUTHORIZATION-001", allow_network=True, allow_side_effects=True))


def test_permission_flags_are_not_truthy_strings() -> None:
    with pytest.raises(ValueError, match="booleans"):
        PluginContext(allow_network="false")  # type: ignore[arg-type]


@pytest.mark.parametrize("timeout", [math.nan, math.inf, True, 0])
def test_runtime_rejects_invalid_timeouts(timeout: Any) -> None:
    with pytest.raises(InputValidationError):
        OrionRuntime().execute("ioc_enricher", {"iocs": ["127.0.0.1"]}, PluginContext(), timeout_seconds=timeout)


def test_external_entrypoints_are_not_imported_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden() -> Any:
        pytest.fail("external entry point discovery requires an explicit trusted opt-in")
    monkeypatch.setattr("importlib.metadata.entry_points", forbidden)
    assert len(PluginRegistry().list()) == 9


def test_status_does_not_export_control_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ORION_LAB_APPROVAL_FILE", "/secret/operator/permit.json")
    assert "/secret" not in json.dumps(controls_status())


def test_audit_contains_metadata_not_payload(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    database = tmp_path / "audit.sqlite3"
    monkeypatch.setenv("ORION_AUDIT_DATABASE", str(database))
    result = OrionRuntime().execute("ioc_enricher", {"iocs": ["127.0.0.1"]},
                                    PluginContext(authorization="PRIVATE-REFERENCE-123"))
    assert result.ok is True
    with sqlite3.connect(database) as connection:
        rows = connection.execute("SELECT event FROM events ORDER BY sequence").fetchall()
    assert [json.loads(row[0])["event"] for row in rows] == ["started", "succeeded"]
    assert "127.0.0.1" not in str(rows)
    assert "PRIVATE-REFERENCE" not in str(rows)


def test_configured_private_resources_are_excluded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "published.md").write_text("public knowledge", encoding="utf-8")
    hidden = tmp_path / "looks-public.json"
    hidden.write_text('{"private":true}', encoding="utf-8")
    monkeypatch.setenv("ORION_LAB_APPROVAL_FILE", str(hidden))
    catalog = ResourceCatalog(tmp_path)
    assert [item.path for item in catalog.list()] == ["published.md"]
    with pytest.raises(FileNotFoundError):
        catalog.read(hidden.name)


@pytest.mark.parametrize("directory", [".git", ".hidden", "evidence", "engagements", "private", "audit"])
def test_private_directories_are_not_published(tmp_path: Path, directory: str) -> None:
    folder = tmp_path / directory
    folder.mkdir()
    (folder / "record.json").write_text("{}", encoding="utf-8")
    catalog = ResourceCatalog(tmp_path)
    assert catalog.list() == ()
    with pytest.raises(FileNotFoundError):
        catalog.read(f"{directory}/record.json")


def test_resource_symlinks_are_rejected(tmp_path: Path) -> None:
    (tmp_path / "safe.md").write_text("data", encoding="utf-8")
    try:
        (tmp_path / "alias.md").symlink_to(tmp_path / "safe.md")
    except OSError:
        pytest.skip("symbolic links are unavailable")
    with pytest.raises(ValueError, match="symbolic"):
        ResourceCatalog(tmp_path).read("alias.md")


def test_resource_growth_is_bounded_at_read(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "growing.md"
    path.write_text("small", encoding="utf-8")
    catalog = ResourceCatalog(tmp_path, max_resource_bytes=8)
    descriptor = catalog.descriptor("growing.md")
    monkeypatch.setattr(catalog, "descriptor", lambda _: descriptor)
    path.write_text("larger than the budget", encoding="utf-8")
    with pytest.raises(ValueError, match="read-byte"):
        catalog.read_bytes("growing.md")


def test_binary_resource_roundtrip(tmp_path: Path) -> None:
    import base64
    content = b"\x89PNG\r\n\x1a\n"
    (tmp_path / "sample.png").write_bytes(content)
    payload = ResourceCatalog(tmp_path).payload("sample.png")
    assert payload["encoding"] == "base64"
    assert base64.b64decode(payload["blob"]) == content
    assert payload["size"] == len(content)
