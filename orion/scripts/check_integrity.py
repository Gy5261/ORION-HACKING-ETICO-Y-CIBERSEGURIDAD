#!/usr/bin/env python3
"""
check_integrity.py - Valida la integridad de referencias en documentación.

Verifica que todas las referencias en backticks dentro de archivos Markdown
apunten a archivos existentes. Genera reporte JSON con estadísticas detalladas.

Uso:
    python3 check_integrity.py
    
Salida JSON:
    {
        "summary": {"total_files": int, "checked_refs": int, "missing_refs": int, "broken_by_type": dict},
        "details": {
            "files_with_broken_refs": [{"file": str, "broken_count": int, "refs": [str]}],
            "orphaned_files": [str],
            "categories": {"core": int, "reference": int, "playbook": int, ...}
        }
    }
"""

import json
import pathlib
import re
import sys
from typing import Dict, List, Tuple
from collections import defaultdict


ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
EXTS = (".md", ".py", ".ps1", ".sh", ".json")
PATTERN = re.compile(r"`([^`]+)`")
SKIP_DIRS = {"__pycache__", ".git", ".venv", "node_modules"}


def categorize_file(path: pathlib.Path) -> str:
    """Clasifica un archivo por su directorio."""
    rel = path.relative_to(REPO_ROOT).as_posix()
    if rel.startswith("orion/references/"):
        return "reference"
    if rel.startswith("orion/playbooks/"):
        return "playbook"
    if rel.startswith("orion/scripts/"):
        return "script"
    if rel.startswith("orion/"):
        return "core"
    if rel.startswith("evals/"):
        return "eval"
    if rel.startswith("eval-results/"):
        return "result"
    if rel.startswith("samples/"):
        return "sample"
    return "other"


def resolve_reference(doc_path: pathlib.Path, ref: str) -> pathlib.Path | None:
    """
    Resuelve una referencia a archivo desde la posición del documento.
    
    Soporta:
    - ../path/to/file.md (relativa hacia arriba)
    - ./path/to/file.md (relativa al directorio actual)
    - path/to/file.md (relativa desde ROOT)
    """
    if not any(ref.endswith(ext) for ext in EXTS):
        return None
    
    if ref.startswith("../") or ref.startswith("./"):
        return (doc_path.parent / ref).resolve()
    
    if "/" in ref or "." in ref:
        # Intenta primero desde el ROOT del proyecto
        candidate = (REPO_ROOT / ref).resolve()
        if candidate.exists():
            return candidate
        # Luego desde el directorio local
        candidate = (doc_path.parent / ref).resolve()
        if candidate.exists():
            return candidate
    
    return None


def get_all_valid_files() -> set[pathlib.Path]:
    """Retorna conjunto de todos los archivos válidos en el proyecto."""
    valid = set()
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix in EXTS or path.name in ("Makefile", "Dockerfile"):
            valid.add(path.resolve())
    return valid


def main() -> int:
    """Ejecuta validación de integridad y genera reporte."""
    all_valid_files = get_all_valid_files()
    missing: List[Dict] = []
    checked = 0
    files_with_broken = []
    category_counts: Dict[str, int] = defaultdict(int)
    broken_by_ext: Dict[str, int] = defaultdict(int)
    found_files = set()
    
    # Procesa todos los archivos markdown
    for path in sorted(REPO_ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        
        found_files.add(path.resolve())
        category = categorize_file(path)
        category_counts[category] += 1
        
        text = path.read_text(encoding="utf-8", errors="ignore")
        broken_refs = []
        
        for ref in PATTERN.findall(text):
            target = resolve_reference(path, ref)
            if target is None:
                continue
            
            checked += 1
            if not target.exists():
                broken_refs.append(ref)
                missing.append({
                    "file": path.relative_to(REPO_ROOT).as_posix(),
                    "ref": ref,
                    "suggestion": f"Check if {ref} exists at {target}"
                })
                ext = pathlib.Path(ref).suffix or "unknown"
                broken_by_ext[ext] += 1
        
        if broken_refs:
            files_with_broken.append({
                "file": path.relative_to(REPO_ROOT).as_posix(),
                "broken_count": len(broken_refs),
                "refs": sorted(broken_refs)
            })
    
    # Detecta archivos huérfanos (no referenciados)
    orphaned = []
    for valid_file in all_valid_files:
        if valid_file not in found_files and valid_file.suffix in (".md",):
            rel_path = valid_file.relative_to(REPO_ROOT).as_posix()
            if not any(x in rel_path for x in [".git", "__pycache__"]):
                orphaned.append(rel_path)
    
    result = {
        "summary": {
            "total_files": len(all_valid_files),
            "docs_checked": len(found_files),
            "checked_refs": checked,
            "missing_refs": len(missing),
            "files_with_broken_refs": len(files_with_broken),
            "orphaned_docs": len(orphaned),
            "broken_by_type": dict(broken_by_ext)
        },
        "details": {
            "files_with_broken_refs": sorted(files_with_broken, key=lambda x: x["broken_count"], reverse=True),
            "orphaned_files": sorted(orphaned),
            "categories": dict(category_counts)
        },
        "missing_refs": missing[:50]  # Limita output a primeros 50
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
