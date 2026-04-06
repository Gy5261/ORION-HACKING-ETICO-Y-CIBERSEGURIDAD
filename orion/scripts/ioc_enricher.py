#!/usr/bin/env python3
"""
ioc_enricher.py - Enriquecimiento seguro de IOCs con servicios opcionales.

Entradas:
- --ioc VALUE (repetible)
- --input FILE.json con lista de IOCs

Servicios opcionales por variables de entorno:
- VT_API_KEY
- ABUSEIPDB_API_KEY
- SHODAN_API_KEY
- OTX_API_KEY

Salida:
- JSON normalizado con clasificacion local, resolucion DNS y enriquecimiento externo opcional
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterable, List


HASH_RE = re.compile(r"^[A-Fa-f0-9]{32}$|^[A-Fa-f0-9]{40}$|^[A-Fa-f0-9]{64}$")
DOMAIN_RE = re.compile(r"^(?=.{1,253}$)([a-zA-Z0-9-]{1,63}\.)+[A-Za-z]{2,63}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enriquece IOCs de forma segura.")
    parser.add_argument("--ioc", action="append", default=[], help="IOC individual.")
    parser.add_argument("--input", help="Archivo JSON con lista de IOCs.")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout de red.")
    parser.add_argument("--output", help="Archivo JSON de salida. Por defecto stdout.")
    return parser.parse_args()


def load_iocs(args: argparse.Namespace) -> List[str]:
    values = list(args.ioc)
    if args.input:
        data = json.loads(open(args.input, "r", encoding="utf-8").read())
        if isinstance(data, list):
            values.extend(str(item) for item in data)
        else:
            raise ValueError("El archivo de entrada debe contener una lista JSON.")
    deduped = []
    seen = set()
    for value in values:
        cleaned = value.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            deduped.append(cleaned)
    if not deduped:
        raise ValueError("No se recibieron IOCs.")
    return deduped


def classify_ioc(value: str) -> str:
    try:
        ipaddress.ip_address(value)
        return "ip"
    except ValueError:
        pass
    if HASH_RE.match(value):
        return "hash"
    if DOMAIN_RE.match(value):
        return "domain"
    if value.startswith("http://") or value.startswith("https://"):
        return "url"
    return "unknown"


def dns_lookup(value: str) -> Dict[str, Any]:
    result: Dict[str, Any] = {"resolved_ips": [], "reverse_dns": None}
    try:
        _, _, addrs = socket.gethostbyname_ex(value)
        result["resolved_ips"] = sorted(set(addrs))
    except OSError as exc:
        result["dns_error"] = str(exc)
    if result["resolved_ips"]:
        try:
            result["reverse_dns"] = socket.gethostbyaddr(result["resolved_ips"][0])[0]
        except OSError:
            pass
    return result


def fetch_json(url: str, headers: Dict[str, str], timeout: float) -> Dict[str, Any]:
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read().decode("utf-8")
    return json.loads(payload)


def safe_fetch(label: str, fn) -> Dict[str, Any]:
    try:
        data = fn()
        return {"ok": True, "source": label, "data": data}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "source": label, "error": f"HTTP {exc.code}"}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "source": label, "error": str(exc)}


def enrich_external(ioc_type: str, value: str, timeout: float) -> Dict[str, Any]:
    integrations: Dict[str, Any] = {}

    vt_key = os.getenv("VT_API_KEY")
    if vt_key:
        encoded = urllib.parse.quote(value, safe="")
        url = f"https://www.virustotal.com/api/v3/search?query={encoded}"
        integrations["virustotal"] = safe_fetch(
            "virustotal",
            lambda: fetch_json(url, {"x-apikey": vt_key}, timeout),
        )

    abuse_key = os.getenv("ABUSEIPDB_API_KEY")
    if abuse_key and ioc_type == "ip":
        query = urllib.parse.urlencode({"ipAddress": value, "maxAgeInDays": 90})
        url = f"https://api.abuseipdb.com/api/v2/check?{query}"
        integrations["abuseipdb"] = safe_fetch(
            "abuseipdb",
            lambda: fetch_json(url, {"Key": abuse_key, "Accept": "application/json"}, timeout),
        )

    shodan_key = os.getenv("SHODAN_API_KEY")
    if shodan_key and ioc_type == "ip":
        url = f"https://api.shodan.io/shodan/host/{value}?key={shodan_key}"
        integrations["shodan"] = safe_fetch(
            "shodan",
            lambda: fetch_json(url, {}, timeout),
        )

    otx_key = os.getenv("OTX_API_KEY")
    if otx_key and ioc_type in {"domain", "ip", "hash"}:
        section = {"domain": "domain", "ip": "IPv4", "hash": "file"}[ioc_type]
        url = f"https://otx.alienvault.com/api/v1/indicators/{section}/{value}/general"
        integrations["alienvault_otx"] = safe_fetch(
            "alienvault_otx",
            lambda: fetch_json(url, {"X-OTX-API-KEY": otx_key}, timeout),
        )

    return integrations


def build_record(value: str, timeout: float) -> Dict[str, Any]:
    ioc_type = classify_ioc(value)
    record: Dict[str, Any] = {
        "value": value,
        "type": ioc_type,
        "observed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "local": {},
        "external": {},
    }
    if ioc_type == "ip":
        ip = ipaddress.ip_address(value)
        record["local"] = {
            "version": ip.version,
            "is_private": ip.is_private,
            "is_global": ip.is_global,
            "is_multicast": ip.is_multicast,
            "is_reserved": ip.is_reserved,
        }
    elif ioc_type == "domain":
        record["local"] = dns_lookup(value)
    elif ioc_type == "url":
        parsed = urllib.parse.urlparse(value)
        record["local"] = {
            "scheme": parsed.scheme,
            "host": parsed.hostname,
            "path": parsed.path,
        }
        if parsed.hostname:
            record["local"]["dns"] = dns_lookup(parsed.hostname)
    elif ioc_type == "hash":
        record["local"] = {"algorithm_guess": {32: "md5", 40: "sha1", 64: "sha256"}.get(len(value))}
    record["external"] = enrich_external(ioc_type, value, timeout)
    return record


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
        iocs = load_iocs(args)
        payload = {
            "tool": "ioc_enricher",
            "count": len(iocs),
            "items": [build_record(ioc, args.timeout) for ioc in iocs],
        }
        write_output(payload, args.output)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"[ioc_enricher] error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
