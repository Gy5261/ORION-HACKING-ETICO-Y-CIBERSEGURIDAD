"""Regressions for offline sanity and evidence-first reporting."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from orion.scripts import run_skill_sanity as sanity


def test_health_percentage_counts_only_passes() -> None:
    data = {'a': {'status': 'pass'}, 'b': {'status': 'fail'}, 'c': {'status': 'skip'}}
    assert sanity.calculate_health_score(data) == 100 / 3
    assert sanity.calculate_health_score({}) == 0.0


def test_http_sanity_requires_expected_usage(monkeypatch) -> None:
    def simulated_failure(command, *, input_text=None, timeout=30):
        return subprocess.CompletedProcess(command, 9, '', 'unrelated failure')
    monkeypatch.setattr(sanity, 'run', simulated_failure)
    assert sanity.test_http_audit_syntax()['status'] == 'fail'


def test_report_template_has_no_claimed_findings(tmp_path: Path) -> None:
    output = tmp_path / 'report.md'
    command = [sys.executable, '-m', 'orion.scripts.report_skeleton', str(output)]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    document = output.read_text(encoding='utf-8')
    assert 'Pendiente de evaluación' in document
    assert 'No se han registrado hallazgos' in document
    assert 'No ejecutado' in document


def test_report_cannot_overwrite_without_flag(tmp_path: Path) -> None:
    output = tmp_path / 'report.md'
    output.write_text('ORIGINAL', encoding='utf-8')
    result = subprocess.run([sys.executable, '-m', 'orion.scripts.report_skeleton', str(output)],
                            capture_output=True, text=True, check=False)
    assert result.returncode != 0
    assert output.read_text(encoding='utf-8') == 'ORIGINAL'


def test_sanity_end_to_end_without_network() -> None:
    assert sanity.test_python_compilation()['status'] == 'pass'
    assert sanity.test_http_audit_syntax()['status'] == 'pass'
    assert sanity.test_report_skeleton()['status'] == 'pass'
