#!/usr/bin/env python3
"""
findings_ticket_sync.py - Convierte hallazgos normalizados en tickets Jira o ServiceNow.

Entradas:
- JSON normalizado con lista de findings

Modos:
- plan: solo genera payloads
- jira: genera o crea issues Jira si se usa --apply
- servicenow: genera o crea incidents si se usa --apply
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.request
from typing import Any, Dict, Iterable, List


SEVERITY_TO_PRIORITY = {
    "critical": "P1",
    "high": "P2",
    "medium": "P3",
    "low": "P4",
    "info": "P5",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sincroniza hallazgos con plataformas de tickets.")
    parser.add_argument("input", help="Archivo JSON de hallazgos.")
    parser.add_argument("--mode", choices=["plan", "jira", "servicenow"], default="plan")
    parser.add_argument("--apply", action="store_true", help="Envia tickets al backend.")
    parser.add_argument("--output", help="Archivo de salida JSON.")
    return parser.parse_args()


def load_findings(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, dict):
        for key in ("findings", "items", "results"):
            if isinstance(data.get(key), list):
                return data[key]
    if isinstance(data, list):
        return data
    raise ValueError("Formato de hallazgos no soportado.")


def normalize_severity(finding: Dict[str, Any]) -> str:
    value = str(
        finding.get("severity")
        or finding.get("risk")
        or finding.get("priority")
        or "medium"
    ).strip().lower()
    return value if value in SEVERITY_TO_PRIORITY else "medium"


def summary_for(finding: Dict[str, Any]) -> str:
    return str(
        finding.get("title")
        or finding.get("name")
        or finding.get("finding")
        or "Hallazgo sin titulo"
    ).strip()


def description_for(finding: Dict[str, Any]) -> str:
    parts = [
        f"Resumen: {summary_for(finding)}",
        f"Severidad: {normalize_severity(finding)}",
        f"Activo: {finding.get('asset') or finding.get('target') or 'n/d'}",
        f"CWE/CVE: {finding.get('cwe') or finding.get('cve') or 'n/d'}",
        f"Evidencia: {finding.get('evidence') or finding.get('details') or 'n/d'}",
        f"Remediacion: {finding.get('remediation') or finding.get('recommendation') or 'n/d'}",
    ]
    return "\n".join(parts)


def build_plan(findings: Iterable[Dict[str, Any]], mode: str) -> List[Dict[str, Any]]:
    plan = []
    for finding in findings:
        severity = normalize_severity(finding)
        payload = {
            "summary": summary_for(finding),
            "description": description_for(finding),
            "labels": ["orion-hacking", severity],
            "priority": SEVERITY_TO_PRIORITY[severity],
            "source_asset": finding.get("asset") or finding.get("target"),
        }
        if mode == "jira":
            payload["jira_fields"] = {
                "project": {"key": os.getenv("JIRA_PROJECT_KEY", "SEC")},
                "issuetype": {"name": "Task"},
                "summary": payload["summary"],
                "description": payload["description"],
                "labels": payload["labels"],
            }
        if mode == "servicenow":
            payload["servicenow_fields"] = {
                "short_description": payload["summary"],
                "description": payload["description"],
                "severity": severity,
                "category": "security",
                "subcategory": "vulnerability",
            }
        plan.append(payload)
    return plan


def post_json(url: str, payload: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def apply_jira(plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    base_url = os.environ["JIRA_BASE_URL"].rstrip("/")
    email = os.environ["JIRA_EMAIL"]
    token = os.environ["JIRA_API_TOKEN"]
    auth = base64.b64encode(f"{email}:{token}".encode("utf-8")).decode("ascii")
    headers = {"Authorization": f"Basic {auth}", "Accept": "application/json"}
    created = []
    for item in plan:
        result = post_json(f"{base_url}/rest/api/3/issue", {"fields": item["jira_fields"]}, headers)
        created.append({"summary": item["summary"], "ticket": result.get("key"), "raw": result})
    return created


def apply_servicenow(plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    instance = os.environ["SNOW_INSTANCE"].rstrip("/")
    user = os.environ["SNOW_USER"]
    password = os.environ["SNOW_PASSWORD"]
    auth = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("ascii")
    headers = {"Authorization": f"Basic {auth}", "Accept": "application/json"}
    created = []
    for item in plan:
        result = post_json(
            f"{instance}/api/now/table/incident",
            item["servicenow_fields"],
            headers,
        )
        created.append({"summary": item["summary"], "ticket": result.get("result", {}).get("number"), "raw": result})
    return created


def write_output(payload: Dict[str, Any], output: str | None) -> None:
    rendered = json.dumps(payload, indent=2, ensure_ascii=False)
    if output:
        with open(output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
    else:
        print(rendered)


def main() -> int:
    try:
        args = parse_args()
        findings = load_findings(args.input)
        plan = build_plan(findings, args.mode)
        payload: Dict[str, Any] = {"mode": args.mode, "count": len(plan), "items": plan}
        if args.apply and args.mode == "jira":
            payload["created"] = apply_jira(plan)
        elif args.apply and args.mode == "servicenow":
            payload["created"] = apply_servicenow(plan)
        write_output(payload, args.output)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"[findings_ticket_sync] error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
