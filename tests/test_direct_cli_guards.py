"""Controls for stand-alone CLI entrypoints; no network or tickets created."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from orion.scripts import findings_ticket_sync, tls_posture_audit


def test_tls_target_preflight_before_socket() -> None:
    with pytest.raises(Exception):
        tls_posture_audit.split_host_port("8.8.8.8:443")
    assert tls_posture_audit.split_host_port("127.0.0.1:8443") == ("127.0.0.1", 8443)


def test_tls_certificate_without_validation_is_not_fabricated() -> None:
    result = tls_posture_audit.cert_to_json({})
    assert result["available"] is False
    assert result["subject"] is None
    assert result["days_until_expiry"] is None
    assert result["verification"] == "not_performed"


def test_tls_cli_requires_operator_provisioned_approval(capsys: pytest.CaptureFixture[str]) -> None:
    result = tls_posture_audit.main([
        "--host", "127.0.0.1:8443", "--timeout", "0.3", "--workers", "1",
        "--authorization", "TEST-LAB-AUTHORIZATION-2026", "--allow-network",
    ])
    assert result == 1
    report = json.loads(capsys.readouterr().out)
    assert report["ok"] is False
    assert report["targets_succeeded"] == 0


def test_ticket_plans_are_available_without_writes() -> None:
    rows = [{"title": "User supplied observation", "severity": "info", "asset": "fixture"}]
    plan = findings_ticket_sync.build_plan(rows, "jira")
    assert plan[0]["summary"] == "User supplied observation"
    assert plan[0]["priority"] == "P5"


def test_ticket_writes_always_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN", "SNOW_INSTANCE"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(PermissionError, match="disabled"):
        findings_ticket_sync.apply_jira([])
    with pytest.raises(PermissionError, match="disabled"):
        findings_ticket_sync.apply_servicenow([])


def test_ticket_cli_rejects_apply_before_any_effect(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    input_path = tmp_path / "findings.json"
    input_path.write_text('[{"title":"synthetic","severity":"medium"}]', encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["findings_ticket_sync.py", str(input_path), "--mode", "jira", "--apply"])
    assert findings_ticket_sync.main() == 1
    assert "disabled" in capsys.readouterr().err


def test_ticket_plan_rejects_missing_title_and_ambiguous_severity() -> None:
    with pytest.raises(ValueError, match="title"):
        findings_ticket_sync.build_plan([{"severity": "high"}], "plan")
    with pytest.raises(ValueError, match="severity"):
        findings_ticket_sync.build_plan([{"title": "synthetic", "severity": "what"}], "plan")
