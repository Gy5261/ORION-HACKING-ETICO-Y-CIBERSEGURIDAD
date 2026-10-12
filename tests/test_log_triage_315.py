"""Regression tests for deterministic, timezone-aware event triage."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import timezone
from pathlib import Path

from orion.scripts.log_triage import parse_timestamp


def _triage(tmp_path: Path, events: object) -> subprocess.CompletedProcess[str]:
    path = tmp_path / "events.json"
    path.write_text(json.dumps(events), encoding="utf-8")
    return subprocess.run(
        [sys.executable, "-m", "orion.scripts.log_triage", str(path)],
        capture_output=True, text=True, check=False, timeout=10,
    )


def test_timeline_sorted_by_utc_not_file_order(tmp_path: Path) -> None:
    events = [
        {"timestamp": "2026-10-12T15:00:00Z", "user": "a", "type": "auth_success"},
        {"timestamp": "2026-10-12T08:00:00-05:00", "user": "b", "type": "auth_failed"},
        {"timestamp": "2026-10-12T19:00:00+02:00", "user": "c", "type": "auth_success"},
    ]
    result = _triage(tmp_path, events)
    assert result.returncode == 0, result.stderr
    timeline = json.loads(result.stdout)["timeline"]
    assert timeline["first_event"] == "2026-10-12T08:00:00-05:00"
    assert timeline["last_event"] == "2026-10-12T19:00:00+02:00"
    assert timeline["invalid_timestamps"] == 0


def test_bad_event_is_reported_as_error(tmp_path: Path) -> None:
    result = _triage(tmp_path, ["this is not an event"])
    assert result.returncode != 0
    assert "must be a JSON object" in result.stdout


def test_invalid_timestamp_is_not_mislabeled(tmp_path: Path) -> None:
    result = _triage(tmp_path, [{"timestamp": "not-a-time", "type": "access"}])
    assert result.returncode == 0
    timeline = json.loads(result.stdout)["timeline"]
    assert timeline["first_event"] is None
    assert timeline["invalid_timestamps"] == 1


def test_legacy_timestamps_explicit_utc_assumption() -> None:
    parsed = parse_timestamp("2026-10-12 14:00:00")
    assert parsed is not None
    assert parsed.tzinfo == timezone.utc
