"""Comprobaciones locales y reproducibles de ORION.

No consulta objetivos, no realiza solicitudes HTTP y no modifica el repositorio.
Cada prueba valida una salida concreta; un error arbitrario nunca cuenta como éxito.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
SCRIPTS = ROOT / "scripts"
SAMPLES = REPO_ROOT / "samples"


def run(command: list[str], *, input_text: str | None = None, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    """Ejecutar un proceso local sin shell, con salida y duración acotadas."""
    try:
        return subprocess.run(
            command,
            input=input_text,
            text=True,
            capture_output=True,
            check=False,
            shell=False,
            cwd=REPO_ROOT,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(command, 124, "", f"Timeout después de {timeout} segundos")
    except OSError as exc:
        return subprocess.CompletedProcess(command, 127, "", f"{type(exc).__name__}: {exc}")


def _result(ok: bool, message: str, **details: Any) -> dict[str, Any]:
    return {"status": "pass" if ok else "fail", "message": message, **details}


def _json_output(process: subprocess.CompletedProcess[str]) -> Any:
    if process.returncode != 0:
        raise ValueError(f"proceso terminado con código {process.returncode}: {process.stderr[:240]}")
    return json.loads(process.stdout)


def test_python_compilation() -> dict[str, Any]:
    """Compilar el código fuente en memoria; no crear __pycache__."""
    paths = sorted((REPO_ROOT / "orion").rglob("*.py"))
    paths += sorted((REPO_ROOT / "tools").rglob("*.py"))
    paths += sorted((REPO_ROOT / "tests").rglob("*.py"))
    errors: list[dict[str, str]] = []
    for path in paths:
        try:
            source = path.read_text(encoding="utf-8-sig")
            compile(source, str(path), "exec")
        except (OSError, SyntaxError, UnicodeError) as exc:
            errors.append({"path": path.relative_to(REPO_ROOT).as_posix(), "error": str(exc)})
    return _result(bool(paths) and not errors, "Compilación sintáctica de Python", files_checked=len(paths), errors=errors)


def test_integrity() -> dict[str, Any]:
    """Comprobar referencias locales usando el verificador existente."""
    process = run([sys.executable, str(SCRIPTS / "check_integrity.py")])
    try:
        data = json.loads(process.stdout)
        summary = data["summary"]
        if process.returncode not in {0, 1}:
            raise ValueError(f"link verifier failed unexpectedly: {process.stderr[:200]}")
        ok = process.returncode == 0 and summary["docs_checked"] > 0 and summary["missing_refs"] == 0
        return _result(ok, "Integridad de referencias Markdown", exit_code=process.returncode,
                       docs_checked=summary["docs_checked"], missing_refs=summary["missing_refs"],
                       examples=data.get("missing_refs", [])[:15])
    except (ValueError, KeyError, TypeError) as exc:
        return _result(False, "Salida inválida de verificación de referencias",
                       exit_code=process.returncode, error=str(exc))


def test_normalize_findings() -> dict[str, Any]:
    """Comparar número y distribución de hallazgos con datos sintéticos."""
    sample = SAMPLES / "findings.sample.json"
    try:
        source = json.loads(sample.read_text(encoding="utf-8"))
        process = run([sys.executable, str(SCRIPTS / "normalize_findings.py")],
                      input_text=json.dumps(source))
        data = _json_output(process)
        findings = data["findings"]
        total = data["summary"]["total_findings"]
        distribution = data["summary"]["by_severity"]
        ok = isinstance(findings, list) and total > 0 and total == len(findings)
        ok = ok and total == sum(distribution.values())
        return _result(ok, "Normalización de hallazgos sintéticos",
                       exit_code=process.returncode, total_findings=total)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return _result(False, "No se pudo validar la normalización", error=str(exc))


def test_log_triage() -> dict[str, Any]:
    """Comprobar recuentos contra el archivo de eventos de ejemplo."""
    sample = SAMPLES / "events.sample.json"
    try:
        source = json.loads(sample.read_text(encoding="utf-8"))
        process = run([sys.executable, str(SCRIPTS / "log_triage.py"), str(sample)])
        data = _json_output(process)
        total = data["total_events"]
        ok = isinstance(source, list) and len(source) > 0 and total == len(source)
        ok = ok and sum(data["severity_distribution"].values()) == total
        return _result(ok, "Triaje de eventos sintéticos", exit_code=process.returncode,
                       total_events=total)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        return _result(False, "No se pudo validar el triaje", error=str(exc))


def test_http_audit_syntax() -> dict[str, Any]:
    """Probar SOLO el mensaje de uso, sin contactar servidores HTTP."""
    script = SCRIPTS / "http_surface_audit.py"
    process = run([sys.executable, str(script)])
    ok = process.returncode == 1 and process.stdout.startswith("Uso: http_surface_audit.py")
    return _result(ok, "CLI HTTP rechaza ausencia de URL; no verifica sondeos HTTP",
                   exit_code=process.returncode, stdout=process.stdout[:180],
                   stderr=process.stderr[:180])


def test_report_skeleton() -> dict[str, Any]:
    """Generar y comprobar un informe vacío fuera del repositorio."""
    with tempfile.TemporaryDirectory(prefix="orion-sanity-") as directory:
        output = Path(directory) / "report.md"
        process = run([sys.executable, str(SCRIPTS / "report_skeleton.py"), str(output)])
        if process.returncode != 0 or not output.is_file():
            return _result(False, "No se generó la plantilla de informe",
                           exit_code=process.returncode, stderr=process.stderr[:180])
        content = output.read_text(encoding="utf-8")
        required = ("## Resumen ejecutivo", "## Alcance y autorización", "## Hallazgos",
                    "## Evidencia", "## Plan de remediación")
        ok = all(section in content for section in required)
        ok = ok and "Pendiente de evaluación" in content and "No se han registrado hallazgos" in content
        return _result(ok, "Plantilla sin hallazgos inventados", exit_code=process.returncode,
                       required_sections=len(required))


def calculate_health_score(results: dict[str, dict[str, Any]]) -> float:
    """Porcentaje de comprobaciones aprobadas; NO es un índice de seguridad."""
    if not results:
        return 0.0
    return 100.0 * sum(item.get("status") == "pass" for item in results.values()) / len(results)


def main() -> int:
    checks = {
        "py_compile": test_python_compilation,
        "integrity": test_integrity,
        "normalize": test_normalize_findings,
        "triage": test_log_triage,
        "http_audit": test_http_audit_syntax,
        "report": test_report_skeleton,
    }
    results = {name: check() for name, check in checks.items()}
    passed = sum(item["status"] == "pass" for item in results.values())
    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Pruebas locales sintéticas; sin red ni integraciones de terceros",
        "summary": {
            "total_tests": len(results),
            "passed": passed,
            "failed": len(results) - passed,
            "checks_passed_percentage": round(calculate_health_score(results), 1),
        },
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
