"""Legacy-script and adapter restrictions with synthetic, network-free fixtures."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from orion.plugins.osint import SpiderFootPlugin
from orion.scripts import http_surface_audit, ioc_enricher


@pytest.mark.parametrize("endpoint", [
    "https://example.com", "http://169.254.169.254/latest/meta-data/",
    "http://10.0.0.10", "http://127.0.0.1.evil.example",
    "http://user:pass@127.0.0.1", "http://127.0.0.1#fragment",
])
def test_http_loopback_only_validator(endpoint: str) -> None:
    with pytest.raises(ValueError):
        http_surface_audit._loopback_url(endpoint)


def test_http_header_observations_are_not_claimed_exploits() -> None:
    findings, score = http_surface_audit.analyze_headers(
        {"X-Content-Type-Options": "nosniff", "Content-Security-Policy": "default-src 'self'"},
    )
    assert isinstance(score, float)
    assert all(item["confirmed_vulnerability"] is False for item in findings)
    assert all(item["severity"] in {"review", "informational"} for item in findings)


def test_http_offline_fixture_never_contacts_network(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    input_path = tmp_path / "headers.json"
    input_path.write_text(json.dumps({"url": "https://example.net", "status": 200,
                                      "headers": {"Content-Security-Policy": "default-src 'self'"}}),
                          encoding="utf-8")

    def forbidden(*args: object, **kwargs: object) -> None:
        pytest.fail("offline mode attempted a network request")

    monkeypatch.setattr(http_surface_audit, "fetch_with_retry", forbidden)
    assert http_surface_audit.main(["--input", str(input_path)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["summary"]["network_contacted"] is False
    assert result["summary"]["confirmed_vulnerabilities"] == 0
    assert result["results"][0]["risk_score_method"] == "configuration-heuristic-not-cvss"


def test_http_cli_refuses_remote_url(capsys: pytest.CaptureFixture[str]) -> None:
    assert http_surface_audit.main(["--allow-loopback", "https://example.com"]) == 2
    assert "loopback" in capsys.readouterr().err


@pytest.mark.parametrize("endpoint", [
    "http://169.254.169.254", "https://spiderfoot.example.com",
    "http://evil.example", "http://user:pass@localhost",
    "http://127.0.0.1@host.evil", "http://localhost/path",
    "http://localhost:invalid",
])
def test_spiderfoot_cannot_reach_arbitrary_network(endpoint: str) -> None:
    with pytest.raises(ValueError):
        SpiderFootPlugin._validate_local_service(endpoint)


def test_spiderfoot_loopback_url_passes_preflight() -> None:
    SpiderFootPlugin._validate_local_service("http://127.0.0.1:5001")
    SpiderFootPlugin._validate_local_service("http://localhost:5001")


def test_ioc_direct_cli_is_truly_offline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        pytest.fail("direct IOC CLI contacted DNS or external OSINT")

    monkeypatch.setattr(ioc_enricher, "dns_lookup", forbidden)
    monkeypatch.setattr(ioc_enricher, "enrich_external", forbidden)
    monkeypatch.setattr(sys, "argv", ["ioc_enricher.py", "--ioc", "example.org"])
    assert ioc_enricher.main() == 0
    output = json.loads(capsys.readouterr().out)
    assert output["count"] == 1
    assert output["items"][0]["classification_only"] is True
    assert output["items"][0]["local"]["dns_performed"] is False


def test_offline_http_script_has_valid_usage_output() -> None:
    process = subprocess.run([sys.executable, "-m", "orion.scripts.http_surface_audit"],
                             capture_output=True, text=True, check=False)
    assert process.returncode == 1
    assert process.stdout.startswith("Uso: http_surface_audit.py")
