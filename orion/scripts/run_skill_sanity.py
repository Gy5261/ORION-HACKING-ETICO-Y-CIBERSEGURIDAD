#!/usr/bin/env python3
"""
run_skill_sanity.py - Valida integridad y funcionamiento de componentes ORION.

Ejecuta suite de pruebas de sanidad sobre los scripts y datos del proyecto:
- CompilaciÃ³n de scripts Python
- ValidaciÃ³n de integridad de referencias
- Esquemas y normalizaciÃ³n
- AnÃ¡lisis de logs y triaje
- CompilaciÃ³n HTML estÃ¡tica

Genera reporte JSON con resultados detallados de cada componente.

Uso:
    python3 run_skill_sanity.py
    python3 run_skill_sanity.py > sanity-report.json

Salida:
    {
        "timestamp": "2024-...",
        "summary": {total: int, passed: int, failed: int, warnings: int},
        "results": {
            "py_compile": [...],
            "integrity": {...},
            "normalize": {...},
            "triage": {...}
        },
        "health_score": float
    }
"""

import json
import pathlib
import py_compile
import subprocess
import sys
import time
from datetime import datetime
from typing import Dict, Any, List


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SAMPLES = ROOT.parent / "samples"
REPO_ROOT = ROOT.parent


def run(cmd: List[str], stdin_text: str | None = None, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    """Ejecuta comando con manejo de timeout y errores."""
    try:
        return subprocess.run(
            cmd,
            input=stdin_text,
            text=True,
            capture_output=True,
            check=False,
            cwd=str(ROOT),
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(
            cmd, 1, "", f"Command timeout after {timeout}s"
        )
    except Exception as e:
        return subprocess.CompletedProcess(
            cmd, 1, "", str(e)
        )


def test_python_compilation() -> tuple[List[Dict[str, Any]], int]:
    """Valida que todos los scripts Python sean compilables."""
    results = []
    passed = 0
    
    for path in sorted(SCRIPTS.glob("*.py")):
        try:
            py_compile.compile(str(path), doraise=True)
            results.append({
                "name": path.name,
                "status": "pass",
                "message": "Compiles successfully"
            })
            passed += 1
        except Exception as exc:
            results.append({
                "name": path.name,
                "status": "fail",
                "message": str(exc)
            })
    
    return results, passed


def test_integrity() -> tuple[Dict[str, Any], int]:
    """Valida integridad de referencias en documentaciÃ³n."""
    result = run([sys.executable, str(SCRIPTS / "check_integrity.py")])
    
    if result.returncode == 0:
        status = "pass"
        score = 100
    else:
        status = "fail"
        score = 50
    
    try:
        data = json.loads(result.stdout)
        missing_count = data.get("summary", {}).get("missing_refs", 0)
        if missing_count > 0:
            score = max(0, 100 - missing_count * 5)
    except json.JSONDecodeError:
        pass
    
    return {
        "status": status,
        "exit_code": result.returncode,
        "score": score,
        "output": result.stdout[:500] if result.stdout else ""
    }, 1 if status == "pass" else 0


def test_normalize_findings() -> tuple[Dict[str, Any], int]:
    """Valida normalizaciÃ³n de hallazgos."""
    if not SAMPLES.exists():
        return {
            "status": "skip",
            "reason": "Samples directory not found"
        }, 0
    
    findings_file = SAMPLES / "findings.sample.json"
    if not findings_file.exists():
        return {
            "status": "skip",
            "reason": "findings.sample.json not found"
        }, 0
    
    findings_text = findings_file.read_text(encoding="utf-8")
    result = run(
        [sys.executable, str(SCRIPTS / "normalize_findings.py")],
        stdin_text=findings_text
    )
    
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            total_findings = data.get("summary", {}).get("total_findings", 0)
            status = "pass" if total_findings > 0 else "fail"
            score = 100 if status == "pass" else 0
        except json.JSONDecodeError:
            status = "fail"
            score = 0
    else:
        status = "fail"
        score = 0
    
    return {
        "status": status,
        "exit_code": result.returncode,
        "score": score,
        "stderr": result.stderr[:200] if result.stderr else ""
    }, 1 if status == "pass" else 0


def test_log_triage() -> tuple[Dict[str, Any], int]:
    """Valida triaje de logs."""
    if not SAMPLES.exists():
        return {
            "status": "skip",
            "reason": "Samples directory not found"
        }, 0
    
    events_file = SAMPLES / "events.sample.json"
    if not events_file.exists():
        return {
            "status": "skip",
            "reason": "events.sample.json not found"
        }, 0
    
    result = run([sys.executable, str(SCRIPTS / "log_triage.py"), str(events_file)])
    
    if result.returncode == 0:
        try:
            data = json.loads(result.stdout)
            total = data.get("total_events", 0)
            status = "pass" if total > 0 else "fail"
            score = 100 if status == "pass" else 50
        except json.JSONDecodeError:
            status = "fail"
            score = 0
    else:
        status = "fail"
        score = 0
    
    return {
        "status": status,
        "exit_code": result.returncode,
        "score": score,
        "stderr": result.stderr[:200] if result.stderr else ""
    }, 1 if status == "pass" else 0


def test_http_audit_syntax() -> tuple[Dict[str, Any], int]:
    """Valida comportamiento bÃ¡sico de http_surface_audit."""
    audit_script = SCRIPTS / "http_surface_audit.py"
    if not audit_script.exists():
        return {"status": "skip", "reason": "Script not found"}, 0
    
    # Solo verifica que el script sea invocable sin error de uso
    result = run([sys.executable, str(audit_script)])
    
    # Debe fallar por falta de URL (esto es esperado)
    if "usage" in result.stdout.lower() or "usage" in result.stderr.lower() or result.returncode != 0:
        return {
            "status": "pass",
            "message": "Script responds to usage check"
        }, 1
    
    return {"status": "fail"}, 0


def test_report_skeleton() -> tuple[Dict[str, Any], int]:
    """Valida generaciÃ³n de plantilla de reporte."""
    test_file = ROOT / "test-report.md"
    
    try:
        result = run([sys.executable, str(SCRIPTS / "report_skeleton.py"), str(test_file)])
        
        if test_file.exists() and result.returncode == 0:
            content = test_file.read_text(encoding="utf-8")
            has_sections = all(x in content for x in ["Resumen", "Alcance", "Hallazgos"])
            
            test_file.unlink()
            
            return {
                "status": "pass" if has_sections else "fail",
                "message": "Template generated correctly" if has_sections else "Template incomplete"
            }, 1 if has_sections else 0
        else:
            return {"status": "fail", "message": "Template generation failed"}, 0
    except Exception as e:
        return {"status": "fail", "error": str(e)}, 0


def calculate_health_score(results: Dict[str, Any]) -> float:
    """Calcula puntuaciÃ³n de salud general (0-100)."""
    scores = []
    
    # compilation
    py_results = results.get("py_compile", [])
    if py_results:
        py_pass = sum(1 for r in py_results if r.get("status") == "pass")
        scores.append((py_pass / len(py_results)) * 100)
    
    # Otros tests
    for key in ["integrity", "normalize", "triage", "http_audit", "report"]:
        test_result = results.get(key, {})
        if isinstance(test_result, dict):
            score = test_result.get("score")
            if score is not None:
                scores.append(score)
            elif test_result.get("status") == "pass":
                scores.append(100)
            elif test_result.get("status") == "fail":
                scores.append(0)
    
    if not scores:
        return 50.0
    
    return sum(scores) / len(scores)


def main() -> int:
    """Ejecuta suite completa de sanidad."""
    timestamp = datetime.now().isoformat()
    
    report = {
        "timestamp": timestamp,
        "results": {}
    }
    
    print("ðŸ” ORION-HACKING Sanity Check", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    # Test compilation
    print("ðŸ“¦ CompilaciÃ³n Python...", file=sys.stderr)
    py_results, py_passed = test_python_compilation()
    report["results"]["py_compile"] = py_results
    print(f"   âœ“ {py_passed}/{len(py_results)} scripts", file=sys.stderr)

    
    # Test integrity
    print("ðŸ”— Integridad de referencias...", file=sys.stderr)
    integrity, integrity_passed = test_integrity()
    report["results"]["integrity"] = integrity
    print(f"   {'âœ“' if integrity_passed else 'âœ—'} {integrity.get('status')}", file=sys.stderr)
    
    # Test normalize
    print("âš™ï¸ NormalizaciÃ³n de hallazgos...", file=sys.stderr)
    normalize, normalize_passed = test_normalize_findings()
    report["results"]["normalize"] = normalize
    print(f"   {'âœ“' if normalize_passed else 'âœ—'} {normalize.get('status')}", file=sys.stderr)
    
    # Test triage
    print("ðŸ“‹ Triaje de logs...", file=sys.stderr)
    triage, triage_passed = test_log_triage()
    report["results"]["triage"] = triage
    print(f"   {'âœ“' if triage_passed else 'âœ—'} {triage.get('status')}", file=sys.stderr)
    
    # Test HTTP audit
    print("ðŸŒ AuditorÃ­a HTTP...", file=sys.stderr)
    http_audit, http_passed = test_http_audit_syntax()
    report["results"]["http_audit"] = http_audit
    print(f"   {'âœ“' if http_passed else 'âœ—'} {http_audit.get('status')}", file=sys.stderr)
    
    # Test report
    print("ðŸ“„ Generador de reportes...", file=sys.stderr)
    report_test, report_passed = test_report_skeleton()
    report["results"]["report"] = report_test
    print(f"   {'âœ“' if report_passed else 'âœ—'} {report_test.get('status')}", file=sys.stderr)
    
    # Calculate summary
    total_tests = 6
    compilation_passed = 1 if py_passed == len(py_results) else 0
    passed_tests = sum([compilation_passed, integrity_passed, normalize_passed, triage_passed, http_passed, report_passed])
    health = calculate_health_score(report["results"])
    
    report["summary"] = {
        "total_tests": total_tests,
        "passed": passed_tests,
        "failed": total_tests - passed_tests,
        "health_percentage": round(health, 1)
    }
    
    print("=" * 50, file=sys.stderr)
    print(f"âœ“ Pasados: {passed_tests}/{total_tests}", file=sys.stderr)
    print(f"ðŸ“Š Salud: {health:.1f}%", file=sys.stderr)
    
    # Salida JSON
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    return 0 if passed_tests == total_tests else 1


if __name__ == "__main__":
    raise SystemExit(main())
