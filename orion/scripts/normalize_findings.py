#!/usr/bin/env python3
"""
normalize_findings.py - Normaliza hallazgos de seguridad a esquema estándar.

Lee JSON desde stdin con estructura variable y lo convierte a formato normalizado
consistente para reportes. Valida campos requeridos y aplica transformaciones.

Entrada JSON (variable):
    [
        {
            "title": "Hallazgo",
            "severity": "high|medium|low|info",
            "asset": "target",
            "evidence": "prueba",
            "recommendation": "solución",
            "cvss": 7.5,
            "cwe": "CWE-123",
            "status": "open|closed|mitigated"
        },
        ...
    ]

Salida normalizada:
    [
        {
            "title": str,
            "severity": "critical|high|medium|low|info",
            "asset": str,
            "evidence": str,
            "recommendation": str,
            "cvss": float | null,
            "cwe": str | null,
            "status": "open|closed|mitigated",
            "remediation_effort": int,
            "risk_score": float
        }
    ]

Uso:
    cat findings.json | python3 normalize_findings.py
    python3 normalize_findings.py < findings.json
"""

import json
import sys
from typing import Dict, Any, List


def normalize_severity(severity_input: Any) -> str:
    """Normaliza severity a 5 niveles estándar."""
    if not severity_input:
        return "info"
    
    sev = str(severity_input).lower().strip()
    
    # Mapeos comunes
    critical_aliases = ["critical", "critical", "urgent", "blocker"]
    high_aliases = ["high", "major", "important"]
    medium_aliases = ["medium", "moderate", "normal"]
    low_aliases = ["low", "minor", "trivial", "info"]
    
    if sev in critical_aliases:
        return "critical"
    elif sev in high_aliases:
        return "high"
    elif sev in medium_aliases:
        return "medium"
    elif sev in low_aliases:
        return "low"
    
    return "info"


def normalize_status(status_input: Any) -> str:
    """Normaliza estado a valores estándar."""
    if not status_input:
        return "open"
    
    status = str(status_input).lower().strip()
    if status in ("closed", "fixed", "resolved", "remediated"):
        return "closed"
    elif status in ("mitigated", "partial", "accepted"):
        return "mitigated"
    
    return "open"


def calculate_remediation_effort(finding: Dict[str, Any]) -> int:
    """
    Estima esfuerzo de remediación (1-10).
    
    Basado en:
    - Severity del hallazgo
    - Presencia de recomendaciones
    - Complejidad percibida
    """
    effort = 5  # baseline
    
    severity = normalize_severity(finding.get("severity"))
    if severity == "critical":
        effort = 9
    elif severity == "high":
        effort = 7
    elif severity == "medium":
        effort = 5
    elif severity == "low":
        effort = 2
    
    # Ajustes
    recommendation = str(finding.get("recommendation", "")).lower()
    if "install" in recommendation or "patch" in recommendation:
        effort = max(effort - 1, 1)
    elif "architecture" in recommendation or "redesign" in recommendation:
        effort = min(effort + 3, 10)
    
    return effort


def calculate_risk_score(finding: Dict[str, Any]) -> float:
    """
    Calcula puntuación de riesgo (0.0-10.0).
    
    Basado en CVSS si está disponible, sino en tabla de severidades.
    """
    cvss = finding.get("cvss")
    if cvss is not None:
        try:
            return float(cvss)
        except (ValueError, TypeError):
            pass
    
    severity = normalize_severity(finding.get("severity"))
    severity_scores = {
        "critical": 9.5,
        "high": 7.5,
        "medium": 5.0,
        "low": 2.5,
        "info": 1.0
    }
    
    return severity_scores.get(severity, 5.0)


def normalize_finding(raw_finding: Any) -> Dict[str, Any] | None:
    """
    Normaliza un hallazgo individual.
    
    Valida campos mínimos requeridos y aplicatransformaciones.
    """
    if not isinstance(raw_finding, dict):
        return None
    
    # Campos requeridos
    title = raw_finding.get("title", "").strip()
    if not title:
        return None
    
    asset = str(raw_finding.get("asset", "")).strip()
    evidence = str(raw_finding.get("evidence", "")).strip()
    recommendation = str(raw_finding.get("recommendation", "")).strip()
    
    # Campos opcionales
    cwe = raw_finding.get("cwe")
    if cwe:
        cwe = str(cwe).strip()
        if not cwe.upper().startswith("CWE"):
            cwe = f"CWE-{cwe}"
    
    cvss = None
    if raw_finding.get("cvss") is not None:
        try:
            cvss = float(raw_finding.get("cvss"))
            cvss = max(0.0, min(10.0, cvss))  # Clamp 0-10
        except (ValueError, TypeError):
            pass
    
    normalized = {
        "title": title,
        "severity": normalize_severity(raw_finding.get("severity")),
        "asset": asset or "unspecified",
        "evidence": evidence or "no evidence provided",
        "recommendation": recommendation or "investigate further",
        "cvss": cvss,
        "cwe": cwe if cwe else None,
        "status": normalize_status(raw_finding.get("status")),
    }
    
    # Campos calculados
    normalized["remediation_effort"] = calculate_remediation_effort(normalized)
    normalized["risk_score"] = calculate_risk_score(normalized)
    
    return normalized


def main() -> int:
    """Lee JSON desde stdin, normaliza y emite resultado."""
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}), file=sys.stderr)
        return 1
    
    if not isinstance(data, list):
        data = [data]
    
    normalized_findings: List[Dict[str, Any]] = []
    
    for item in data:
        normalized = normalize_finding(item)
        if normalized:
            normalized_findings.append(normalized)
    
    # Ordena por risk_score descendente
    normalized_findings.sort(
        key=lambda x: (
            {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}.get(x["severity"], 5),
            -x["risk_score"]
        )
    )
    
    result = {
        "summary": {
            "total_findings": len(normalized_findings),
            "by_severity": {
                "critical": sum(1 for f in normalized_findings if f["severity"] == "critical"),
                "high": sum(1 for f in normalized_findings if f["severity"] == "high"),
                "medium": sum(1 for f in normalized_findings if f["severity"] == "medium"),
                "low": sum(1 for f in normalized_findings if f["severity"] == "low"),
                "info": sum(1 for f in normalized_findings if f["severity"] == "info"),
            },
            "open_findings": sum(1 for f in normalized_findings if f["status"] == "open"),
            "avg_risk_score": sum(f["risk_score"] for f in normalized_findings) / max(len(normalized_findings), 1)
        },
        "findings": normalized_findings
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
