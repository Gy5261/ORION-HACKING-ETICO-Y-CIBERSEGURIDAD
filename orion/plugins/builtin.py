"""Plugins oficiales incluidos en ORION."""

from __future__ import annotations

import ipaddress
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable

from .core import BasePlugin, JsonObject, PluginContext, PluginMetadata


def _workers(payload: JsonObject, item_count: int) -> int:
    requested = int(payload.get("workers", 4))
    return max(1, min(requested, max(1, item_count), 32))


def _parallel_map(function: Callable[[str], JsonObject], values: Iterable[str], workers: int) -> list[JsonObject]:
    ordered_values = list(values)
    if workers == 1 or len(ordered_values) <= 1:
        return [function(value) for value in ordered_values]
    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="orion-plugin") as pool:
        return list(pool.map(function, ordered_values))


class IocEnricherPlugin(BasePlugin):
    metadata = PluginMetadata(
        plugin_id="ioc_enricher",
        name="IOC Enricher",
        version="1.0.0",
        category="osint-intelligence",
        description="Clasifica, resuelve y enriquece indicadores de compromiso con fuentes opcionales.",
        risk_level="low",
        capabilities=("ioc-classification", "dns-resolution", "threat-intelligence"),
        requires_authorization=True,
        network_access=True,
        side_effects=False,
        default_timeout_seconds=30,
        max_timeout_seconds=300,
        tags=("ioc", "osint", "defensive", "json-first"),
        input_schema={
            "type": "object",
            "required": ["iocs"],
            "additionalProperties": False,
            "properties": {
                "iocs": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 500,
                    "uniqueItems": True,
                    "items": {"type": "string", "minLength": 1, "maxLength": 2048},
                },
                "timeout": {"type": "number", "minimum": 0.1, "maximum": 30},
                "workers": {"type": "integer", "minimum": 1, "maximum": 32},
                "external_sources": {"type": "boolean"},
            },
        },
        output_schema={
            "type": "object",
            "required": ["tool", "count", "items"],
            "properties": {
                "tool": {"type": "string", "enum": ["ioc_enricher"]},
                "count": {"type": "integer", "minimum": 0},
                "items": {"type": "array"},
            },
        },
    )

    @staticmethod
    def _local_record(value: str) -> JsonObject:
        from orion.scripts import ioc_enricher as engine

        ioc_type = engine.classify_ioc(value)
        record: JsonObject = {
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
            record["local"] = engine.dns_lookup(value)
        elif ioc_type == "url":
            parsed = urllib.parse.urlparse(value)
            record["local"] = {"scheme": parsed.scheme, "host": parsed.hostname, "path": parsed.path}
            if parsed.hostname:
                record["local"]["dns"] = engine.dns_lookup(parsed.hostname)
        elif ioc_type == "hash":
            record["local"] = {"algorithm_guess": {32: "md5", 40: "sha1", 64: "sha256"}.get(len(value))}
        return record

    def run(self, payload: JsonObject, context: PluginContext) -> JsonObject:
        from orion.scripts import ioc_enricher as engine

        del context
        iocs = list(dict.fromkeys(item.strip() for item in payload["iocs"] if item.strip()))
        timeout = float(payload.get("timeout", 5.0))
        external_sources = bool(payload.get("external_sources", False))
        build = (lambda value: engine.build_record(value, timeout)) if external_sources else self._local_record
        items = _parallel_map(build, iocs, _workers(payload, len(iocs)))
        return {"tool": "ioc_enricher", "count": len(items), "items": items}


class TlsPostureAuditPlugin(BasePlugin):
    metadata = PluginMetadata(
        plugin_id="tls_posture_audit",
        name="TLS Posture Audit",
        version="1.0.0",
        category="web-network",
        description="Inspecciona negociación TLS y certificados de endpoints autorizados.",
        risk_level="low",
        capabilities=("tls-inspection", "certificate-inventory", "expiry-monitoring"),
        requires_authorization=True,
        network_access=True,
        side_effects=False,
        default_timeout_seconds=30,
        max_timeout_seconds=300,
        tags=("tls", "certificate", "defensive", "read-only"),
        input_schema={
            "type": "object",
            "required": ["targets"],
            "additionalProperties": False,
            "properties": {
                "targets": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 500,
                    "uniqueItems": True,
                    "items": {"type": "string", "minLength": 1, "maxLength": 255},
                },
                "timeout": {"type": "number", "minimum": 0.1, "maximum": 30},
                "workers": {"type": "integer", "minimum": 1, "maximum": 32},
            },
        },
        output_schema={
            "type": "object",
            "required": ["tool", "count", "items"],
            "properties": {
                "tool": {"type": "string", "enum": ["tls_posture_audit"]},
                "count": {"type": "integer", "minimum": 0},
                "items": {"type": "array"},
            },
        },
    )

    def run(self, payload: JsonObject, context: PluginContext) -> JsonObject:
        from orion.scripts import tls_posture_audit as engine

        del context
        targets = list(dict.fromkeys(item.strip() for item in payload["targets"] if item.strip()))
        timeout = float(payload.get("timeout", 5.0))

        def audit(target: str) -> JsonObject:
            try:
                return engine.audit_target(target, timeout)
            except Exception as exc:  # noqa: BLE001
                return {"target": target, "error": str(exc), "error_type": type(exc).__name__}

        items = _parallel_map(audit, targets, _workers(payload, len(targets)))
        return {"tool": "tls_posture_audit", "count": len(items), "items": items}


class FindingsTicketSyncPlugin(BasePlugin):
    metadata = PluginMetadata(
        plugin_id="findings_ticket_sync",
        name="Findings Ticket Sync",
        version="1.0.0",
        category="automation-reporting",
        description="Convierte hallazgos normalizados en planes o tickets Jira/ServiceNow.",
        risk_level="medium",
        capabilities=("finding-normalization", "ticket-planning", "ticket-creation"),
        requires_authorization=True,
        network_access=False,
        side_effects=True,
        default_timeout_seconds=60,
        max_timeout_seconds=600,
        tags=("jira", "servicenow", "reporting", "dry-run-default"),
        input_schema={
            "type": "object",
            "required": ["findings"],
            "additionalProperties": False,
            "properties": {
                "findings": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 1000,
                    "items": {"type": "object"},
                },
                "mode": {"type": "string", "enum": ["plan", "jira", "servicenow"]},
                "apply": {"type": "boolean"},
            },
        },
        output_schema={
            "type": "object",
            "required": ["tool", "mode", "count", "items"],
            "properties": {
                "tool": {"type": "string", "enum": ["findings_ticket_sync"]},
                "mode": {"type": "string"},
                "count": {"type": "integer", "minimum": 0},
                "items": {"type": "array"},
                "created": {"type": "array"},
            },
        },
    )

    def run(self, payload: JsonObject, context: PluginContext) -> JsonObject:
        from orion.scripts import findings_ticket_sync as engine

        findings = payload["findings"]
        mode = str(payload.get("mode", "plan"))
        apply = bool(payload.get("apply", False))
        plan = engine.build_plan(findings, mode)
        result: JsonObject = {
            "tool": "findings_ticket_sync",
            "mode": mode,
            "count": len(plan),
            "items": plan,
        }
        if apply:
            if mode == "plan":
                raise ValueError("apply=true no es válido cuando mode=plan")
            if not context.allow_network:
                raise PermissionError("La creación de tickets también requiere allow_network=true")
            result["created"] = engine.apply_jira(plan) if mode == "jira" else engine.apply_servicenow(plan)
        return result


BUILTIN_PLUGINS: tuple[type[BasePlugin], ...] = (
    IocEnricherPlugin,
    TlsPostureAuditPlugin,
    FindingsTicketSyncPlugin,
)
