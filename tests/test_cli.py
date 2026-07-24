from __future__ import annotations

import json

from orion.cli import main


def test_cli_lists_plugins_as_json(capsys) -> None:
    assert main(["plugins", "list", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["manifest_version"] == "1.0"
    assert [plugin["plugin_id"] for plugin in payload["plugins"]] == [
        "findings_ticket_sync",
        "ioc_enricher",
        "tls_posture_audit",
    ]


def test_cli_doctor_reports_healthy_runtime(capsys) -> None:
    assert main(["plugins", "doctor"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["plugin_count"] == 3
    assert payload["discovery_errors"] == []


def test_cli_runs_local_ioc_request(tmp_path, capsys) -> None:
    request = tmp_path / "request.json"
    request.write_text(
        json.dumps(
            {
                "iocs": ["d41d8cd98f00b204e9800998ecf8427e"],
                "external_sources": False,
            }
        ),
        encoding="utf-8",
    )
    exit_code = main(
        [
            "plugins",
            "run",
            "ioc_enricher",
            "--input",
            str(request),
            "--authorization",
            "TOR-2026-ORION-CLI-001",
            "--actor",
            "pytest-cli",
            "--allow-network",
        ]
    )
    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["actor"] == "pytest-cli"
    assert payload["data"]["count"] == 1
