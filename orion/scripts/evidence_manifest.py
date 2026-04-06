#!/usr/bin/env python3
"""
evidence_manifest.py - Genera manifiestos de evidencia con hashes SHA-256.

Entradas:
- archivos o directorios

Salida:
- JSON con archivos, tamaño, hash, timestamps y tags de cadena de custodia
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone
from typing import Dict, Iterable, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crea manifiestos de evidencia reproducibles.")
    parser.add_argument("paths", nargs="+", help="Archivos o directorios a inventariar.")
    parser.add_argument("--output", help="Archivo JSON de salida.")
    parser.add_argument("--tag", action="append", default=[], help="Tag de cadena de custodia.")
    return parser.parse_args()


def iter_files(paths: Iterable[str]) -> List[pathlib.Path]:
    collected: List[pathlib.Path] = []
    for raw in paths:
        path = pathlib.Path(raw)
        if path.is_file():
            collected.append(path)
        elif path.is_dir():
            collected.extend(sorted(item for item in path.rglob("*") if item.is_file()))
    if not collected:
        raise ValueError("No se encontraron archivos para evidenciar.")
    return collected


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: pathlib.Path) -> Dict[str, object]:
    stat = path.stat()
    return {
        "path": str(path.resolve()),
        "size_bytes": stat.st_size,
        "sha256": sha256_file(path),
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
    }


def write_output(payload: Dict[str, object], output: str | None) -> None:
    rendered = json.dumps(payload, indent=2, ensure_ascii=False)
    if output:
        pathlib.Path(output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


def main() -> int:
    try:
        args = parse_args()
        files = iter_files(args.paths)
        payload = {
            "tool": "evidence_manifest",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "tags": args.tag,
            "count": len(files),
            "items": [file_record(path) for path in files],
        }
        write_output(payload, args.output)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"[evidence_manifest] error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
