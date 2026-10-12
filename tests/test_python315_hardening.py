"""Python 3.15 support and adapter resource-bound regression tests (offline)."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pytest

from orion.cli import main
from orion.plugins.adapters import ToolRunner, ToolSpec
from orion.runtime_info import interpreter_report


def _runner(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, source: str) -> ToolRunner:
    script = tmp_path / 'controlled_tool.py'
    script.write_text(source, encoding='utf-8')
    monkeypatch.setenv('ORION_TEST_TOOL_BINARY', str(script))
    return ToolRunner(ToolSpec(
        tool_id='orion-test-tool', candidates=('missing-tool',),
        environment_variable='ORION_TEST_TOOL_BINARY',
        homepage='https://example.invalid', license='MIT',
    ))


def test_python_capabilities_are_observed_not_assumed() -> None:
    report = interpreter_report()
    assert report['python_315_or_newer'] == (sys.version_info >= (3, 15))
    assert report['jit']['available'] in {True, False, None}
    assert report['jit']['enabled'] in {True, False, None}
    assert report['gil_enabled'] in {True, False, None}
    assert report['no_network_contacted'] is True
    assert report['benchmark_performed'] is False


def test_runtime_info_cli_is_valid_json(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(['runtime-info', '--json']) == 0
    data = json.loads(capsys.readouterr().out)
    assert data['python_version']
    assert 'free_threaded_build' in data


def test_cli_rejects_duplicate_json_keys(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    payload = tmp_path / 'duplicate.json'
    payload.write_text('{"iocs":["127.0.0.1"],"iocs":[]}', encoding='utf-8')
    result = main(['plugins', 'run', 'ioc_enricher', '--input', str(payload),
                   '--authorization', 'LOCAL-CLASSIFICATION-001'])
    assert result == 2
    assert 'duplicate JSON key' in capsys.readouterr().out


def test_cli_rejects_oversized_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    payload = tmp_path / 'oversized.json'
    payload.write_bytes(b'{' + b'a' * (1024 * 1024) + b'}')
    result = main(['plugins', 'run', 'ioc_enricher', '--input', str(payload),
                   '--authorization', 'LOCAL-CLASSIFICATION-001'])
    assert result == 2
    assert 'exceeds' in capsys.readouterr().out


def test_cli_rejects_nonfinite_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    payload = tmp_path / 'nonfinite.json'
    payload.write_text('{"iocs":[], "timeout": NaN}', encoding='utf-8')
    result = main(['plugins', 'run', 'ioc_enricher', '--input', str(payload),
                   '--authorization', 'LOCAL-CLASSIFICATION-001'])
    assert result == 2
    assert 'non-finite' in capsys.readouterr().out


def test_external_command_output_is_bounded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    runner = _runner(tmp_path, monkeypatch,
        'import sys\nsys.stdout.buffer.write(b"x" * (3 * 1024 * 1024))\n')
    result = runner.run([], timeout_seconds=10)
    assert result['stdout_truncated'] is True
    assert len(result['stdout']) < (2 * 1024 * 1024 + 100)
    assert result['stderr_truncated'] is False
    assert 'TRUNCATED' in result['stdout']


def test_external_command_deadline_is_enforced(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    runner = _runner(tmp_path, monkeypatch, 'import time\ntime.sleep(8)\n')
    started = time.monotonic()
    with pytest.raises(TimeoutError, match='exceeded'):
        runner.run([], timeout_seconds=0.2)
    assert time.monotonic() - started < 4


def test_tool_rejects_infinite_deadline(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    runner = _runner(tmp_path, monkeypatch, 'print("ok")\n')
    with pytest.raises(ValueError, match='finite'):
        runner.run([], timeout_seconds=float('inf'))
