"""Safe adapters for established OSINT tools.

Third-party projects remain separate installations. ORION invokes trusted local
executables or a configured SpiderFoot service with bounded, structured input.
"""

from __future__ import annotations

import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Mapping

from .adapters import (
    TemporaryToolDirectory,
    ToolRunner,
    ToolSpec,
    collect_artifacts,
    parse_json_output,
)
from .core import BasePlugin, JsonObject, PluginContext, PluginHealth, PluginMetadata

_GENERIC_OUTPUT_SCHEMA: JsonObject = {
    "type": "object",
    "required": ["tool", "result"],
    "properties": {
        "tool": {"type": "string"},
        "result": {},
        "execution": {"type": "object"},
        "artifacts": {"type": "object"},
    },
}


def _timeout(payload: Mapping[str, Any], default: float = 120.0) -> float:
    return float(payload.get("timeout_seconds", default))


def _execution_result(tool_id: str, execution: JsonObject, artifacts: JsonObject | None = None) -> JsonObject:
    parsed = parse_json_output(str(execution.get("stdout", "")))
    result: JsonObject = {
        "tool": tool_id,
        "result": parsed if parsed is not None else execution.get("stdout", ""),
        "execution": {
            "return_code": execution["return_code"],
            "duration_ms": execution["duration_ms"],
            "stderr": execution.get("stderr", ""),
        },
    }
    if artifacts:
        result["artifacts"] = artifacts
    return result


class ExternalCommandPlugin(BasePlugin):
    """Base class for allow-listed third-party command adapters."""

    tool_spec: ToolSpec

    def __init__(self) -> None:
        self.runner = ToolRunner(self.tool_spec)

    def health(self) -> PluginHealth:
        return self.runner.health()


class SpiderFootPlugin(BasePlugin):
    metadata = PluginMetadata(
        plugin_id="spiderfoot",
        name="SpiderFoot",
        version="1.0.0",
        category="osint-automation",
        description="Controls an authorized SpiderFoot service and returns normalized scan data.",
        risk_level="medium",
        capabilities=("scan-start", "scan-list", "scan-results"),
        requires_authorization=True,
        network_access=True,
        side_effects=True,
        default_timeout_seconds=60,
        max_timeout_seconds=600,
        tags=("osint", "spiderfoot", "service-adapter", "read-mostly"),
        homepage="https://github.com/smicallef/spiderfoot",
        license="MIT",
        integration="http-api",
        input_schema={
            "type": "object",
            "required": ["operation"],
            "additionalProperties": False,
            "properties": {
                "operation": {"type": "string", "enum": ["start", "list", "results", "summary"]},
                "server_url": {"type": "string", "pattern": r"^https?://", "maxLength": 2048},
                "target": {"type": "string", "minLength": 1, "maxLength": 2048},
                "scan_id": {"type": "string", "minLength": 1, "maxLength": 128},
                "name": {"type": "string", "minLength": 1, "maxLength": 128},
                "use_case": {"type": "string", "maxLength": 128},
                "modules": {
                    "type": "array",
                    "maxItems": 250,
                    "uniqueItems": True,
                    "items": {"type": "string", "minLength": 1, "maxLength": 128},
                },
                "types": {
                    "type": "array",
                    "maxItems": 250,
                    "uniqueItems": True,
                    "items": {"type": "string", "minLength": 1, "maxLength": 128},
                },
                "timeout_seconds": {"type": "number", "minimum": 1, "maximum": 600},
            },
        },
        output_schema=_GENERIC_OUTPUT_SCHEMA,
    )

    def requests_side_effects(self, payload: JsonObject) -> bool:
        return payload.get("operation") == "start"

    def run(self, payload: JsonObject, context: PluginContext) -> JsonObject:
        del context
        operation = str(payload["operation"])
        server = str(payload.get("server_url", "http://127.0.0.1:5001")).rstrip("/")
        timeout = _timeout(payload, 60)

        if operation == "start":
            target = str(payload.get("target", "")).strip()
            if not target:
                raise ValueError("target is required for SpiderFoot start")
            fields = {
                "scanname": str(payload.get("name", f"ORION-{target}")),
                "scantarget": target,
                "modulelist": ",".join(payload.get("modules", [])),
                "typelist": ",".join(payload.get("types", [])),
                "usecase": str(payload.get("use_case", "all")),
            }
            result = self._request(f"{server}/startscan", timeout, fields)
        elif operation == "list":
            result = self._request(f"{server}/scanlist", timeout)
        else:
            scan_id = str(payload.get("scan_id", "")).strip()
            if not scan_id:
                raise ValueError(f"scan_id is required for SpiderFoot {operation}")
            endpoint = "scansummary" if operation == "summary" else "scanexportjsonmulti"
            parameters = {"id": scan_id, "by": "type"} if operation == "summary" else {"ids": scan_id}
            query = urllib.parse.urlencode(parameters)
            result = self._request(f"{server}/{endpoint}?{query}", timeout)
        return {"tool": "spiderfoot", "result": result}

    @staticmethod
    def _request(url: str, timeout: float, fields: Mapping[str, str] | None = None) -> Any:
        data = urllib.parse.urlencode(fields).encode("utf-8") if fields else None
        request = urllib.request.Request(url, data=data, method="POST" if fields else "GET")
        request.add_header("Accept", "application/json")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read(8 * 1024 * 1024).decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            body = exc.read(64 * 1024).decode("utf-8", errors="replace")
            raise RuntimeError(f"SpiderFoot HTTP {exc.code}: {body}") from exc
        parsed = parse_json_output(raw)
        return parsed if parsed is not None else raw


class TheHarvesterPlugin(ExternalCommandPlugin):
    tool_spec = ToolSpec(
        tool_id="theharvester",
        candidates=("theHarvester", "theharvester"),
        environment_variable="ORION_THEHARVESTER_EXECUTABLE",
        homepage="https://github.com/laramies/theHarvester",
        license="GPL-2.0-only",
    )
    metadata = PluginMetadata(
        plugin_id="theharvester",
        name="theHarvester",
        version="1.0.0",
        category="osint-reconnaissance",
        description="Collects public emails, hosts, and subdomains for an authorized domain.",
        risk_level="medium",
        capabilities=("email-discovery", "subdomain-discovery", "host-discovery"),
        network_access=True,
        tags=("osint", "domain", "external-adapter"),
        homepage=tool_spec.homepage,
        license=tool_spec.license,
        integration="subprocess",
        default_timeout_seconds=180,
        max_timeout_seconds=900,
        input_schema={
            "type": "object",
            "required": ["domain"],
            "additionalProperties": False,
            "properties": {
                "domain": {"type": "string", "pattern": r"^[A-Za-z0-9.-]+$", "maxLength": 253},
                "sources": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 50,
                    "uniqueItems": True,
                    "items": {"type": "string", "pattern": r"^[A-Za-z0-9_-]+$", "maxLength": 64},
                },
                "limit": {"type": "integer", "minimum": 1, "maximum": 5000},
                "dns_lookup": {"type": "boolean"},
                "quiet": {"type": "boolean"},
                "timeout_seconds": {"type": "number", "minimum": 1, "maximum": 900},
            },
        },
        output_schema=_GENERIC_OUTPUT_SCHEMA,
    )

    def run(self, payload: JsonObject, context: PluginContext) -> JsonObject:
        sources = payload.get("sources", ["crtsh", "duckduckgo"])
        with TemporaryToolDirectory("orion-theharvester-") as output:
            prefix = output / "results"
            arguments = [
                "-d",
                str(payload["domain"]),
                "-b",
                ",".join(sources),
                "-l",
                str(payload.get("limit", 500)),
                "-f",
                str(prefix),
            ]
            if payload.get("dns_lookup"):
                arguments.append("-n")
            if payload.get("quiet", True):
                arguments.append("-q")
            execution = self.runner.run(
                arguments,
                timeout_seconds=_timeout(payload, 180),
                environment=context.environment,
                working_directory=output,
            )
            return _execution_result("theharvester", execution, collect_artifacts(output))


class SherlockPlugin(ExternalCommandPlugin):
    tool_spec = ToolSpec(
        tool_id="sherlock",
        candidates=("sherlock",),
        environment_variable="ORION_SHERLOCK_EXECUTABLE",
        homepage="https://github.com/sherlock-project/sherlock",
        license="MIT",
    )
    metadata = PluginMetadata(
        plugin_id="sherlock",
        name="Sherlock",
        version="1.0.0",
        category="osint-identity",
        description="Checks public username presence across configured public services.",
        risk_level="medium",
        capabilities=("username-enumeration", "public-profile-discovery"),
        network_access=True,
        tags=("osint", "username", "external-adapter"),
        homepage=tool_spec.homepage,
        license=tool_spec.license,
        integration="subprocess",
        default_timeout_seconds=180,
        max_timeout_seconds=900,
        input_schema={
            "type": "object",
            "required": ["usernames"],
            "additionalProperties": False,
            "properties": {
                "usernames": {
                    "type": "array",
                    "minItems": 1,
                    "maxItems": 100,
                    "uniqueItems": True,
                    "items": {"type": "string", "minLength": 1, "maxLength": 64},
                },
                "sites": {
                    "type": "array",
                    "maxItems": 300,
                    "uniqueItems": True,
                    "items": {"type": "string", "minLength": 1, "maxLength": 128},
                },
                "request_timeout": {"type": "number", "minimum": 1, "maximum": 60},
                "timeout_seconds": {"type": "number", "minimum": 1, "maximum": 900},
            },
        },
        output_schema=_GENERIC_OUTPUT_SCHEMA,
    )

    def run(self, payload: JsonObject, context: PluginContext) -> JsonObject:
        with TemporaryToolDirectory("orion-sherlock-") as output:
            arguments = [
                *[str(item) for item in payload["usernames"]],
                "--print-found",
                "--no-color",
                "--folderoutput",
                str(output),
                "--timeout",
                str(payload.get("request_timeout", 10)),
            ]
            for site in payload.get("sites", []):
                arguments.extend(["--site", str(site)])
            execution = self.runner.run(
                arguments,
                timeout_seconds=_timeout(payload, 180),
                environment=context.environment,
            )
            return _execution_result("sherlock", execution, collect_artifacts(output))


class OsintSpyPlugin(ExternalCommandPlugin):
    tool_spec = ToolSpec(
        tool_id="osint-spy",
        candidates=("osint-spy.py", "osint-spy"),
        environment_variable="ORION_OSINT_SPY_EXECUTABLE",
        homepage="https://github.com/SharadKumar97/OSINT-SPY",
        license="GPL-3.0",
    )
    metadata = PluginMetadata(
        plugin_id="osint_spy",
        name="OSINT-SPY",
        version="1.0.0",
        category="osint-aggregation",
        description="Runs the legacy OSINT-SPY public-data modes through a constrained adapter.",
        risk_level="medium",
        capabilities=("domain-lookup", "email-lookup", "ip-lookup", "device-lookup"),
        network_access=True,
        tags=("osint", "legacy", "external-adapter"),
        homepage=tool_spec.homepage,
        license=tool_spec.license,
        integration="subprocess",
        default_timeout_seconds=120,
        max_timeout_seconds=600,
        input_schema={
            "type": "object",
            "required": ["target_type", "value"],
            "additionalProperties": False,
            "properties": {
                "target_type": {"type": "string", "enum": ["domain", "email", "ip", "device"]},
                "value": {"type": "string", "minLength": 1, "maxLength": 512},
                "timeout_seconds": {"type": "number", "minimum": 1, "maximum": 600},
            },
        },
        output_schema=_GENERIC_OUTPUT_SCHEMA,
    )

    def run(self, payload: JsonObject, context: PluginContext) -> JsonObject:
        resolved = self.runner.resolve()
        working_directory = Path(resolved.path).parent if resolved else None
        execution = self.runner.run(
            [f"--{payload['target_type']}", str(payload["value"]), "--json"],
            timeout_seconds=_timeout(payload, 120),
            environment=context.environment,
            working_directory=working_directory,
        )
        return _execution_result("osint_spy", execution)


class PhoneInfogaPlugin(ExternalCommandPlugin):
    tool_spec = ToolSpec(
        tool_id="phoneinfoga",
        candidates=("phoneinfoga",),
        environment_variable="ORION_PHONEINFOGA_EXECUTABLE",
        homepage="https://github.com/sundowndev/phoneinfoga",
        license="GPL-3.0",
    )
    metadata = PluginMetadata(
        plugin_id="phoneinfoga",
        name="PhoneInfoga",
        version="1.0.0",
        category="osint-phone",
        description="Normalizes authorized PhoneInfoga scans of international telephone numbers.",
        risk_level="medium",
        capabilities=("phone-validation", "country-inference", "public-number-recon"),
        network_access=True,
        tags=("osint", "phone", "external-adapter"),
        homepage=tool_spec.homepage,
        license=tool_spec.license,
        integration="subprocess",
        default_timeout_seconds=120,
        max_timeout_seconds=600,
        input_schema={
            "type": "object",
            "required": ["number"],
            "additionalProperties": False,
            "properties": {
                "number": {"type": "string", "pattern": r"^\+?[0-9 ()-]{6,32}$"},
                "timeout_seconds": {"type": "number", "minimum": 1, "maximum": 600},
            },
        },
        output_schema=_GENERIC_OUTPUT_SCHEMA,
    )

    def run(self, payload: JsonObject, context: PluginContext) -> JsonObject:
        execution = self.runner.run(
            ["scan", "-n", str(payload["number"])],
            timeout_seconds=_timeout(payload, 120),
            environment=context.environment,
        )
        return _execution_result("phoneinfoga", execution)


class PhotonPlugin(ExternalCommandPlugin):
    tool_spec = ToolSpec(
        tool_id="photon",
        candidates=("photon", "photon.py"),
        environment_variable="ORION_PHOTON_EXECUTABLE",
        homepage="https://github.com/s0md3v/Photon",
        license="GPL-3.0",
    )
    metadata = PluginMetadata(
        plugin_id="photon",
        name="Photon",
        version="1.0.0",
        category="osint-web",
        description="Crawls an authorized web target and normalizes public URLs, emails, files, and profiles.",
        risk_level="medium",
        capabilities=("web-crawling", "url-extraction", "email-extraction", "file-discovery"),
        network_access=True,
        tags=("osint", "crawler", "web", "external-adapter"),
        homepage=tool_spec.homepage,
        license=tool_spec.license,
        integration="subprocess",
        default_timeout_seconds=180,
        max_timeout_seconds=900,
        input_schema={
            "type": "object",
            "required": ["url"],
            "additionalProperties": False,
            "properties": {
                "url": {"type": "string", "pattern": r"^https?://", "maxLength": 2048},
                "depth": {"type": "integer", "minimum": 1, "maximum": 5},
                "threads": {"type": "integer", "minimum": 1, "maximum": 20},
                "delay": {"type": "number", "minimum": 0, "maximum": 30},
                "request_timeout": {"type": "number", "minimum": 1, "maximum": 60},
                "only_urls": {"type": "boolean"},
                "timeout_seconds": {"type": "number", "minimum": 1, "maximum": 900},
            },
        },
        output_schema=_GENERIC_OUTPUT_SCHEMA,
    )

    def run(self, payload: JsonObject, context: PluginContext) -> JsonObject:
        resolved = self.runner.resolve()
        working_directory = Path(resolved.path).parent if resolved else None
        with TemporaryToolDirectory("orion-photon-") as output:
            arguments = [
                "-u",
                str(payload["url"]),
                "-l",
                str(payload.get("depth", 2)),
                "-t",
                str(payload.get("threads", 4)),
                "-d",
                str(payload.get("delay", 0)),
                "--timeout",
                str(payload.get("request_timeout", 6)),
                "-o",
                str(output),
                "-e",
                "json",
            ]
            if payload.get("only_urls"):
                arguments.append("--only-urls")
            execution = self.runner.run(
                arguments,
                timeout_seconds=_timeout(payload, 180),
                environment=context.environment,
                working_directory=working_directory,
            )
            return _execution_result("photon", execution, collect_artifacts(output))


OSINT_PLUGINS: tuple[type[BasePlugin], ...] = (
    SpiderFootPlugin,
    TheHarvesterPlugin,
    SherlockPlugin,
    OsintSpyPlugin,
    PhoneInfogaPlugin,
    PhotonPlugin,
)
