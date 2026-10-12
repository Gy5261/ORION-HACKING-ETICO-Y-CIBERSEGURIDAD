"""Findings normalization must never turn an invalid score into a plausible fact."""
from __future__ import annotations

import json
import subprocess
import sys

import pytest

from orion.scripts.normalize_findings import normalize_finding


def test_info_not_mislabeled_low() -> None:
    result = normalize_finding({"title": "Informational only", "severity": "info"})
    assert result is not None
    assert result["severity"] == "info"
    assert result["evidence"] is None
    assert result["risk_score_method"] == "severity_heuristic"


def test_accepted_risk_is_not_remediated() -> None:
    result = normalize_finding({"title": "Risk accepted", "status": "accepted"})
    assert result is not None
    assert result["status"] == "accepted"


@pytest.mark.parametrize("score", [float("nan"), float("inf"), -1, 10.1, "9.8", True])
def test_invalid_cvss_fails_instead_of_clamping(score: object) -> None:
    with pytest.raises(ValueError, match="CVSS"):
        normalize_finding({"title": "Invalid score", "cvss": score})


def test_cvss_is_labeled_unverified() -> None:
    result = normalize_finding({"title": "Claim", "cvss": 7.5, "cwe": "CWE-79"})
    assert result is not None
    assert result["cvss"] == 7.5
    assert result["cwe"] == "CWE-79"
    assert result["risk_score_method"] == "supplied_cvss_unverified"


def test_cli_reports_skipped_rows_and_heursitic_warning() -> None:
    example = [
        {"title": "Data provided", "severity": "high"},
        {"title": "", "severity": "medium"},
    ]
    result = subprocess.run(
        [sys.executable, "-m", "orion.scripts.normalize_findings"],
        input=json.dumps(example), capture_output=True, text=True, check=False, timeout=10,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["summary"]["total_findings"] == 1
    assert data["summary"]["skipped_entries"] == 1
    assert data["summary"]["risk_scores_estimated"] == 1
    assert "not a verified risk metric" in data["summary"]["risk_score_warning"]
