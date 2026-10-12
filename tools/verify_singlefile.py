"""Offline structural verifier for the generated ORION single-file knowledge site.

Tests actual HTML produced from the repository instead of just unit fixtures.
This is static verification and NOT an interactive browser end-to-end test.
"""
from __future__ import annotations

import argparse
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

MAX_HTML_BYTES = 32 * 1024 * 1024


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.current_script: str | None = None
        self.scripts: dict[str, list[str]] = {"dataset": [], "application": []}
        self.document_ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.articles = 0
        self.toc_links = 0
        self.has_search_field = False
        self.external_scripts = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        identifier = attributes.get("id")
        if identifier:
            if identifier in self.document_ids:
                self.duplicate_ids.add(identifier)
            self.document_ids.add(identifier)
        if tag == "script":
            if attributes.get("src"):
                self.external_scripts += 1
            self.current_script = ("dataset" if identifier == "orion-dataset" else "application")
        elif tag == "article" and attributes.get("class") == "doc-card":
            self.articles += 1
        elif tag == "a" and "toc-link" in (attributes.get("class") or "").split():
            self.toc_links += 1
        elif tag == "input" and identifier == "search":
            self.has_search_field = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self.current_script = None

    def handle_data(self, data: str) -> None:
        if self.current_script:
            self.scripts[self.current_script].append(data)


def verify_html(source: str) -> tuple[dict[str, Any], str]:
    parser = SiteParser()
    parser.feed(source)
    parser.close()
    if parser.duplicate_ids:
        raise ValueError(f"duplicate document IDs: {sorted(parser.duplicate_ids)[:5]}")
    if parser.external_scripts:
        raise ValueError("standalone HTML must not load JavaScript from the network")
    if not parser.has_search_field:
        raise ValueError("search input is missing")
    dataset_text = "".join(parser.scripts["dataset"]).strip()
    if not dataset_text:
        raise ValueError("embedded JSON dataset is missing")
    dataset = json.loads(dataset_text)
    entries = dataset.get("entries")
    if not isinstance(entries, list) or len(entries) < 10:
        raise ValueError("generated site has unexpectedly few document entries")
    if parser.articles != len(entries) or parser.toc_links != len(entries):
        raise ValueError("article, navigation and JSON document counts disagree")
    if dataset.get("stats", {}).get("total_documents") != len(entries):
        raise ValueError("embedded document count does not match its metadata")
    known_paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("site document entry must be a JSON object")
        path = entry.get("path")
        anchor = entry.get("anchor")
        if not isinstance(path, str) or not isinstance(anchor, str):
            raise ValueError("site document is missing a path or an anchor")
        if path in known_paths:
            raise ValueError(f"duplicate source document: {path}")
        known_paths.add(path)
        if anchor not in parser.document_ids:
            raise ValueError(f"document anchor is missing in HTML: {path}")
    executable = "\n".join(parser.scripts["application"]).strip()
    if not executable or "applyFilters" not in executable:
        raise ValueError("interactive search script is missing")
    if "</script" in dataset_text.casefold():
        raise ValueError("unsafe closing script tag appeared in embedded JSON")
    return {
        "ok": True,
        "document_count": len(entries),
        "navigation_count": parser.toc_links,
        "article_count": parser.articles,
        "external_script_count": parser.external_scripts,
        "verification_scope": "generated HTML structure and JavaScript syntax (with node --check), not browser interaction",
    }, executable


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check generated standalone HTML without network")
    parser.add_argument("site", type=Path)
    parser.add_argument("--js-output", type=Path, help="Save JavaScript for external syntax verification")
    args = parser.parse_args(argv)
    try:
        if args.site.stat().st_size > MAX_HTML_BYTES:
            raise ValueError("standalone site exceeds the 32 MiB validation limit")
        content = args.site.read_text(encoding="utf-8")
        report, javascript = verify_html(content)
        if args.js_output:
            with args.js_output.open("x", encoding="utf-8") as handle:
                handle.write(javascript + "\n")
        print(json.dumps(report, ensure_ascii=False))
        return 0
    except (OSError, UnicodeError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
