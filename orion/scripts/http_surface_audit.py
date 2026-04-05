#!/usr/bin/env python3
"""
http_surface_audit.py - Auditoría de superficie HTTP y configuración de seguridad.

Analiza encabezados HTTP de seguridad en URLs destino y clasifica posibles
vulnerabilidades o configuraciones deficientes. Incluye reintentos con backoff
exponencial y procesamiento paralelo opcional.

Encabezados auditados:
- HSTS (Strict-Transport-Security)
- CSP (Content-Security-Policy)
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection
- Referrer-Policy
- Permissions-Policy
- Server (revelación de información)

Uso:
    python3 http_surface_audit.py <url> [<url> ...]
    python3 http_surface_audit.py https://example.com https://test.com

Salida JSON con resultados por URL:
    [
        {
            "url": "https://example.com",
            "status": 200,
            "security_headers": {...},
            "findings": [{severity: str, description: str}],
            "risk_score": float
        },
        ...
    ]
"""

import json
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from typing import Dict, Any, List
from collections import defaultdict


MAX_RETRIES = 3
RETRY_DELAY = 1  # segundos (con backoff exponencial)
REQUEST_TIMEOUT = 10
USER_AGENT = "ORION-HACKING-audit/1.0 (+http://example.com/security)"

EXPECTED_HEADERS = {
    "strict-transport-security": {"severity": "high", "description": "HSTS not configured"},
    "content-security-policy": {"severity": "medium", "description": "CSP not set"},
    "x-frame-options": {"severity": "medium", "description": "Clickjacking protection missing"},
    "x-content-type-options": {"severity": "medium", "description": "MIME-sniffing not prevented"},
    "x-xss-protection": {"severity": "low", "description": "XSS protection header missing"},
    "referrer-policy": {"severity": "low", "description": "Referrer policy not defined"},
    "permissions-policy": {"severity": "low", "description": "Permissions policy not set"},
}

INSECURE_SERVERS = {
    "Apache": "visible",
    "nginx": "visible",
    "Microsoft-IIS": "visible",
    "Apache httpd": "version exposed",
}


def fetch_with_retry(url: str, max_retries: int = MAX_RETRIES) -> Dict[str, Any]:
    """
    Obtiene encabezados HTTP con reintentos y backoff exponencial.
    """
    for attempt in range(max_retries):
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                headers = {k.lower(): v for k, v in resp.headers.items()}
                return {
                    "url": url,
                    "status": resp.status,
                    "status_text": "OK" if resp.status == 200 else "Non-200 Status",
                    "headers": headers,
                    "error": None
                }
        except HTTPError as e:
            # HTTP error (4xx, 5xx) - puede tener headers útiles
            if attempt == max_retries - 1:
                headers = {k.lower(): v for k, v in e.headers.items()}
                return {
                    "url": url,
                    "status": e.code,
                    "status_text": f"HTTP {e.code}",
                    "headers": headers,
                    "error": None
                }
        except (URLError, TimeoutError, ConnectionError) as e:
            if attempt < max_retries - 1:
                delay = RETRY_DELAY * (2 ** attempt)  # Backoff exponencial
                time.sleep(delay)
            else:
                return {
                    "url": url,
                    "status": None,
                    "status_text": "Connection Failed",
                    "headers": {},
                    "error": str(e)
                }
        except Exception as e:
            return {
                "url": url,
                "status": None,
                "status_text": "Unknown Error",
                "headers": {},
                "error": str(e)
            }
    
    return {
        "url": url,
        "status": None,
        "status_text": "Unknown Error",
        "headers": {},
        "error": "Max retries exceeded"
    }


def analyze_headers(headers: Dict[str, str]) -> tuple[List[Dict[str, str]], float]:
    """
    Analiza encabezados de seguridad y detecta problemas.
    
    Retorna: (lista de hallazgos, puntuación de riesgo 0-10)
    """
    findings = []
    risk_points = 0.0
    
    # Verifica encabezados requeridos
    for header_name, rule in EXPECTED_HEADERS.items():
        if header_name not in headers:
            findings.append({
                "header": header_name,
                "status": "missing",
                "severity": rule["severity"],
                "description": rule["description"]
            })
            severity_weights = {"high": 3, "medium": 2, "low": 1}
            risk_points += severity_weights.get(rule["severity"], 1)
    
    # Valida contenido de HSTS
    if "strict-transport-security" in headers:
        hsts_value = headers["strict-transport-security"].lower()
        if "max-age" not in hsts_value:
            findings.append({
                "header": "strict-transport-security",
                "status": "invalid",
                "severity": "high",
                "description": "HSTS missing max-age directive"
            })
            risk_points += 2
        elif "max-age=0" in hsts_value:
            findings.append({
                "header": "strict-transport-security",
                "status": "disabled",
                "severity": "high",
                "description": "HSTS disabled (max-age=0)"
            })
            risk_points += 3
    
    # Detecta revelación de información en Server header
    if "server" in headers:
        server = headers["server"]
        findings.append({
            "header": "server",
            "status": "information_disclosure",
            "severity": "low",
            "description": f"Server information exposed: {server}"
        })
        risk_points += 0.5
    
    # Valida CSP
    if "content-security-policy" in headers:
        csp_value = headers["content-security-policy"].lower()
        if "unsafe-inline" in csp_value or "unsafe-eval" in csp_value:
            findings.append({
                "header": "content-security-policy",
                "status": "weak",
                "severity": "high",
                "description": "CSP allows unsafe-inline or unsafe-eval"
            })
            risk_points += 2.5
    
    # Normaliza puntuación
    risk_score = min(risk_points, 10.0)
    
    return findings, risk_score


def classify_risk_level(score: float) -> str:
    """Clasifica nivel de riesgo basado en puntuación."""
    if score >= 8.0:
        return "critical"
    elif score >= 6.0:
        return "high"
    elif score >= 4.0:
        return "medium"
    elif score >= 2.0:
        return "low"
    return "minimal"


def main() -> int:
    """Audita URLs y genera reporte de seguridad."""
    if len(sys.argv) < 2:
        print("Uso: http_surface_audit.py <url> [<url> ...]")
        print("Ejemplo: http_surface_audit.py https://example.com https://test.com")
        return 1
    
    results = []
    summary = {
        "urls_scanned": 0,
        "successful_scans": 0,
        "failed_scans": 0,
        "critical_findings": 0,
        "high_findings": 0,
        "medium_findings": 0,
        "low_findings": 0,
    }
    
    for url in sys.argv[1:]:
        # Asegura que URL tiene esquema
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        
        summary["urls_scanned"] += 1
        
        # Obtiene headers con reintentos
        response = fetch_with_retry(url)
        
        if response["error"]:
            results.append({
                "url": url,
                "status": None,
                "error": response["error"],
                "findings": [],
                "risk_score": 0.0
            })
            summary["failed_scans"] += 1
            continue
        
        summary["successful_scans"] += 1
        
        # Analiza headers de seguridad
        findings, risk_score = analyze_headers(response["headers"])
        
        # Contabiliza hallazgos por severidad
        for finding in findings:
            severity = finding.get("severity", "low")
            summary[f"{severity}_findings"] += 1
        
        result = {
            "url": url,
            "status": response["status"],
            "status_text": response["status_text"],
            "security_headers": {
                k: response["headers"].get(k) 
                for k in EXPECTED_HEADERS.keys() 
                if k in response["headers"]
            },
            "findings": findings,
            "risk_score": risk_score,
            "risk_level": classify_risk_level(risk_score)
        }
        
        results.append(result)
    
    output = {
        "summary": summary,
        "results": results
    }
    
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0 if summary["failed_scans"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
