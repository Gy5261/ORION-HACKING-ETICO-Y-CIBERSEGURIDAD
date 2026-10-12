"""Cross-directory defensive regressions. All cases run without network."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from orion.plugins.core import OrionRuntime, PluginContext
from orion.scripts import build_singlefile_site, check_integrity, evidence_manifest


def test_offline_ioc_domain_and_url_have_no_dns(monkeypatch: pytest.MonkeyPatch) -> None:
    from orion.scripts import ioc_enricher

    def forbidden(*args: object, **kwargs: object) -> None:
        pytest.fail("offline IOC classification attempted DNS resolution")

    monkeypatch.setattr(ioc_enricher, "dns_lookup", forbidden)
    payload = {"iocs": ["example.org", "https://example.org/news"], "external_sources": False}
    result = OrionRuntime().execute("ioc_enricher", payload,
                                    PluginContext(authorization="OFFLINE-TEST-REFERENCE-001"))
    assert result.ok, result.error
    assert result.data is not None
    assert result.data["count"] == 2
    assert all(item["local"].get("dns_performed") is False for item in result.data["items"])


def test_evidence_hashes_exact_contents_without_absolute_path(tmp_path: Path) -> None:
    path = tmp_path / "evidence.txt"
    path.write_bytes(b"fixture bytes\n")
    entry = evidence_manifest.file_record(path, root=tmp_path)
    assert entry["path"] == "evidence.txt"
    assert entry["sha256"] == evidence_manifest.sha256_file(path)
    assert entry["content_stable_while_read"] is True


def test_evidence_rejects_top_level_symlink(tmp_path: Path) -> None:
    original = tmp_path / "data.txt"
    original.write_text("data", encoding="utf-8")
    linked = tmp_path / "link.txt"
    try:
        linked.symlink_to(original)
    except (OSError, NotImplementedError):
        pytest.skip("symlink not available")
    with pytest.raises(ValueError, match="symbolic"):
        evidence_manifest.iter_files([str(linked)])


def test_evidence_never_overwrites_existing_manifest(tmp_path: Path) -> None:
    target = tmp_path / "manifest.json"
    target.write_text("KEEP", encoding="utf-8")
    with pytest.raises(FileExistsError):
        evidence_manifest.write_output({"safe": True}, str(target))
    assert target.read_text(encoding="utf-8") == "KEEP"


def test_integrity_reports_real_missing_link(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                             capsys: pytest.CaptureFixture[str]) -> None:
    page = tmp_path / "README.md"
    page.write_text("[broken](missing.md)\n[external](https://example.invalid)\n", encoding="utf-8")
    monkeypatch.setattr(check_integrity, "REPO_ROOT", tmp_path)
    assert check_integrity.main() == 1
    result = json.loads(capsys.readouterr().out)
    assert result["summary"]["missing_refs"] == 1
    assert result["missing_refs"][0]["ref"] == "missing.md"
    page.write_text("[exists](document.md)\n", encoding="utf-8")
    (tmp_path / "document.md").write_text("# Document", encoding="utf-8")
    assert check_integrity.main() == 0


def test_singlefile_does_not_embed_raw_closing_script_or_private_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "README.md").write_text("# Demo\n</ScRiPt><img src=x onerror=alert(1)>", encoding="utf-8")
    (tmp_path / "private").mkdir()
    (tmp_path / "private" / "secrets.json").write_text('{"secret": "DO_NOT_PUBLISH"}', encoding="utf-8")
    monkeypatch.setattr(build_singlefile_site, "REPO_ROOT", tmp_path)
    assert [path.name for path in build_singlefile_site.files_to_include()] == ["README.md"]
    output = build_singlefile_site.build_html()
    assert "DO_NOT_PUBLISH" not in output
    block = output.split('id="orion-dataset"', 1)[1].split("</script>", 1)[0]
    assert "</ScRiPt>" not in block
    assert "\\u003c" in block
    assert "&lt;img" in output
