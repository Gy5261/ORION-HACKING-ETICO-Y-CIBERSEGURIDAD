"""Hardened adapters for optional third-party command-line tools."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .core import JsonObject, PluginHealth, ToolUnavailableError

_MAX_STREAM_BYTES = 2 * 1024 * 1024
_MAX_ARTIFACT_BYTES = 8 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class ToolSpec:
    """Resolution contract for an optional executable."""

    tool_id: str
    candidates: tuple[str, ...]
    environment_variable: str
    homepage: str
    license: str
    version_arguments: tuple[str, ...] = ("--version",)


@dataclass(frozen=True, slots=True)
class ResolvedTool:
    """Resolved executable prefix."""

    path: str
    command_prefix: tuple[str, ...]
    source: str


class ToolRunner:
    """Resolve and execute allow-listed tools without invoking a shell."""

    def __init__(self, spec: ToolSpec) -> None:
        self.spec = spec

    def resolve(self) -> ResolvedTool | None:
        override = os.getenv(self.spec.environment_variable)
        if override:
            path = Path(override).expanduser()
            if path.is_file():
                return self._resolved(str(path.resolve()), "environment")

        for candidate in self.spec.candidates:
            discovered = shutil.which(candidate)
            if discovered:
                return self._resolved(discovered, "path")
        return None

    @staticmethod
    def _resolved(path: str, source: str) -> ResolvedTool:
        prefix = (sys.executable, path) if path.lower().endswith(".py") else (path,)
        return ResolvedTool(path=path, command_prefix=prefix, source=source)

    def health(self) -> PluginHealth:
        resolved = self.resolve()
        if resolved is None:
            candidates = ", ".join(self.spec.candidates)
            return PluginHealth(
                available=False,
                status="optional_dependency_missing",
                message=(
                    f"{self.spec.tool_id} is not installed; set {self.spec.environment_variable} "
                    f"or install one of: {candidates}"
                ),
                details={
                    "tool": self.spec.tool_id,
                    "homepage": self.spec.homepage,
                    "license": self.spec.license,
                    "environment_variable": self.spec.environment_variable,
                },
            )
        return PluginHealth(
            available=True,
            details={
                "tool": self.spec.tool_id,
                "path": resolved.path,
                "source": resolved.source,
                "homepage": self.spec.homepage,
                "license": self.spec.license,
            },
        )

    def run(
        self,
        arguments: Sequence[str],
        *,
        timeout_seconds: float,
        environment: Mapping[str, str] | None = None,
        working_directory: str | Path | None = None,
    ) -> JsonObject:
        resolved = self.resolve()
        if resolved is None:
            raise ToolUnavailableError(self.health().message)
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        command = [*resolved.command_prefix, *[str(argument) for argument in arguments]]
        env = self._environment(environment)
        started = time.perf_counter()
        try:
            completed = subprocess.run(
                command,
                cwd=str(working_directory) if working_directory else None,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout_seconds,
                check=False,
                shell=False,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = self._decode(exc.stdout)
            stderr = self._decode(exc.stderr)
            raise TimeoutError(
                f"{self.spec.tool_id} exceeded {timeout_seconds:.1f}s; stdout={stdout!r}; stderr={stderr!r}"
            ) from exc

        duration_ms = round((time.perf_counter() - started) * 1000)
        stdout = self._decode(completed.stdout)
        stderr = self._decode(completed.stderr)
        result: JsonObject = {
            "tool": self.spec.tool_id,
            "return_code": completed.returncode,
            "duration_ms": duration_ms,
            "stdout": stdout,
            "stderr": stderr,
        }
        if completed.returncode != 0:
            raise RuntimeError(
                f"{self.spec.tool_id} exited with code {completed.returncode}: {stderr or stdout}"
            )
        return result

    @staticmethod
    def _environment(extra: Mapping[str, str] | None) -> dict[str, str]:
        allowed = {
            "PATH",
            "HOME",
            "USERPROFILE",
            "TMP",
            "TEMP",
            "LANG",
            "LC_ALL",
            "SYSTEMROOT",
            "WINDIR",
        }
        env = {key: value for key, value in os.environ.items() if key in allowed}
        env.setdefault("PYTHONUNBUFFERED", "1")
        if extra:
            for key, value in extra.items():
                if not key or not key.replace("_", "A").isalnum() or len(key) > 128:
                    raise ValueError(f"invalid environment variable name: {key!r}")
                if len(value) > 16_384:
                    raise ValueError(f"environment variable {key!r} is too large")
                env[key] = value
        return env

    @staticmethod
    def _decode(value: bytes | str | None) -> str:
        if value is None:
            return ""
        raw = value if isinstance(value, bytes) else value.encode("utf-8", errors="replace")
        if len(raw) > _MAX_STREAM_BYTES:
            raw = raw[:_MAX_STREAM_BYTES] + b"\n[ORION OUTPUT TRUNCATED]"
        return raw.decode("utf-8", errors="replace").strip()


def parse_json_output(text: str) -> Any | None:
    """Parse complete JSON or the last JSON line emitted by a tool."""

    stripped = text.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass
    for line in reversed(stripped.splitlines()):
        candidate = line.strip()
        if candidate.startswith(("{", "[")):
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                continue
    return None


def collect_artifacts(root: str | Path) -> JsonObject:
    """Collect bounded UTF-8/JSON artifacts from a temporary output directory."""

    base = Path(root).resolve()
    files: JsonObject = {}
    consumed = 0
    for path in sorted(base.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        resolved = path.resolve()
        if base not in resolved.parents:
            continue
        size = resolved.stat().st_size
        if size > _MAX_ARTIFACT_BYTES or consumed + size > _MAX_ARTIFACT_BYTES:
            files[str(resolved.relative_to(base))] = {"truncated": True, "size_bytes": size}
            continue
        consumed += size
        raw = resolved.read_bytes()
        relative = str(resolved.relative_to(base))
        if resolved.suffix.lower() == ".json":
            try:
                files[relative] = json.loads(raw.decode("utf-8"))
                continue
            except (UnicodeDecodeError, json.JSONDecodeError):
                pass
        files[relative] = raw.decode("utf-8", errors="replace")
    return files


class TemporaryToolDirectory:
    """Context manager exposing a private temporary directory to adapters."""

    def __init__(self, prefix: str) -> None:
        self._temporary = tempfile.TemporaryDirectory(prefix=prefix)
        self.path = Path(self._temporary.name)

    def __enter__(self) -> Path:
        return self.path

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self._temporary.cleanup()
