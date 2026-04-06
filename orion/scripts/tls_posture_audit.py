#!/usr/bin/env python3
"""
tls_posture_audit.py - Recoleccion segura de postura TLS por host.

Entradas:
- hostnames por linea en --input o repetidos con --host

Salida:
- JSON con certificado, fechas, sujeto, SANs y version TLS negociada
"""

from __future__ import annotations

import argparse
import json
import socket
import ssl
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audita postura TLS de endpoints.")
    parser.add_argument("--host", action="append", default=[], help="Host o host:puerto.")
    parser.add_argument("--input", help="Archivo con un host por linea.")
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--output", help="Archivo JSON de salida.")
    return parser.parse_args()


def load_targets(args: argparse.Namespace) -> List[str]:
    targets = list(args.host)
    if args.input:
        with open(args.input, "r", encoding="utf-8") as handle:
            targets.extend(line.strip() for line in handle if line.strip())
    deduped = []
    seen = set()
    for target in targets:
        if target not in seen:
            seen.add(target)
            deduped.append(target)
    if not deduped:
        raise ValueError("Debes indicar al menos un host.")
    return deduped


def split_host_port(target: str) -> tuple[str, int]:
    if ":" in target and target.count(":") == 1:
        host, raw_port = target.rsplit(":", 1)
        return host, int(raw_port)
    return target, 443


def cert_to_json(cert: Dict[str, Any]) -> Dict[str, Any]:
    def flatten_name(items: List[tuple[str, str]]) -> Dict[str, str]:
        return {name: value for name, value in items}

    subject = [flatten_name(part) for part in cert.get("subject", [])]
    issuer = [flatten_name(part) for part in cert.get("issuer", [])]
    sans = [value for kind, value in cert.get("subjectAltName", []) if kind == "DNS"]
    not_after = cert.get("notAfter")
    expires_at = None
    days_until_expiry = None
    if not_after:
        expires_at = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        days_until_expiry = int((expires_at - datetime.now(timezone.utc)).total_seconds() // 86400)
    return {
        "subject": subject,
        "issuer": issuer,
        "subject_alt_names": sans,
        "serial_number": cert.get("serialNumber"),
        "not_before": cert.get("notBefore"),
        "not_after": not_after,
        "days_until_expiry": days_until_expiry,
    }


def audit_target(target: str, timeout: float) -> Dict[str, Any]:
    host, port = split_host_port(target)
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with socket.create_connection((host, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=host) as tls_sock:
            cert = tls_sock.getpeercert()
            cipher = tls_sock.cipher()
            return {
                "target": target,
                "version": tls_sock.version(),
                "cipher": {
                    "name": cipher[0] if cipher else None,
                    "protocol": cipher[1] if cipher else None,
                    "bits": cipher[2] if cipher else None,
                },
                "certificate": cert_to_json(cert),
                "peer_ip": tls_sock.getpeername()[0],
            }


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
        items = []
        for target in load_targets(args):
            try:
                items.append(audit_target(target, args.timeout))
            except Exception as exc:  # noqa: BLE001
                items.append({"target": target, "error": str(exc)})
        write_output({"tool": "tls_posture_audit", "items": items}, args.output)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"[tls_posture_audit] error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
