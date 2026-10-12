"""Retired synthetic-content expander; read-only audit of generated material.

Older versions appended repetitive scenarios to reach arbitrary line counts.
Those sections are illustrative, not evidence of integrations or verified work.
Keeping the script name preserves existing references while preventing further
fabrication, documentation inflation or accidental data modifications.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

MARKER = "<!-- ORION-EXPANSION-2026-04-05 -->"
MAX_DOCS = 1000
MAX_DOC_BYTES = 2 * 1024 * 1024
EXCLUDED_DIRS = {".git", ".github", ".venv", "__pycache__", "node_modules", "build", "dist"}


def inventory(root: Path) -> dict[str, Any]:
    """Locate historical auto-generated blocks without modifying a byte."""
    root = root.resolve()
    candidates = sorted(path for path in root.rglob("*.md") if path.is_file() and not path.is_symlink()
                        and not any(part in EXCLUDED_DIRS for part in path.relative_to(root).parts))
    if len(candidates) > MAX_DOCS:
        raise ValueError(f"documentation count exceeds {MAX_DOCS}")
    generated: list[dict[str, Any]] = []
    by_folder: Counter[str] = Counter()
    for path in candidates:
        if path.stat().st_size > MAX_DOC_BYTES:
            raise ValueError(f"Markdown file exceeds 2 MiB: {path.relative_to(root).as_posix()}")
        content = path.read_text(encoding="utf-8")
        if MARKER not in content:
            continue
        relative = path.relative_to(root).as_posix()
        generated.append({"path": relative, "markers": content.count(MARKER),
                          "generated_block_needs_review": True})
        by_folder[relative.split("/", 1)[0]] += 1
    return {
        "ok": True, "read_only": True, "expansion_disabled": True,
        "scope": "Historical marker detection; not a factual accuracy certification",
        "files_scanned": len(candidates), "documents_with_generated_sections": len(generated),
        "by_folder": dict(by_folder), "generated": generated,
    }


def expand(path: Path, root: Path) -> None:
    """Historical API entrypoint: explicitly reject synthetic expansion."""
    raise PermissionError(
        "Synthetic documentation expansion has been retired. "
        "Edit sources manually with verified references and tests."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only audit of historical generated documentation.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--fail-if-generated", action="store_true",
                        help="Fail when historical generated sections still require review.")
    args = parser.parse_args(argv)
    try:
        result = inventory(args.root)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if args.fail_if_generated and result["documents_with_generated_sections"] else 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
