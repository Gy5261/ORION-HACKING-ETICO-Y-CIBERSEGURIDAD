"""Hardened adapters for optional third-party command-line tools."""

from __future__ import annotations

import json
import math
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, Mapping, Sequence

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

    @staticmethod
    def _drain(pipe: BinaryIO, buffer: bytearray, overflow: list[bool]) -> None:
        """Always drain pipes; retain only bounded output in memory."""
        try:
            while True:
                chunk = pipe.read(65536)
                if not chunk:
                    break
                available = max(0, _MAX_STREAM_BYTES - len(buffer))
                buffer.extend(chunk[:available])
                if len(chunk) > available:
                    overflow[0] = True
        finally:
            pipe.close()

    @staticmethod
    def _stop_process(process: subprocess.Popen[bytes]) -> None:
        """Stop a dedicated process group on POSIX; kill the child on Windows."""
        if os.name == "posix":
            try:
                os.killpg(process.pid, signal.SIGKILL)
                return
            except ProcessLookupError:
                return
        try:
            process.kill()
        except ProcessLookupError:
            pass

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
        if type(timeout_seconds) not in {int, float} or not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be finite and positive")
        command = [*resolved.command_prefix, *[str(argument) for argument in arguments]]
        if any("\x00" in argument for argument in command):
            raise ValueError("NUL bytes are not allowed in tool arguments")
        env = self._environment(environment)
        started = time.perf_counter_ns()

        process = subprocess.Popen(
            command,
            cwd=str(working_directory) if working_directory else None,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            start_new_session=os.name == "posix",
            creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) if os.name == "nt" else 0,
        )
        assert process.stdout is not None and process.stderr is not None
        stdout_bytes, stderr_bytes = bytearray(), bytearray()
        stdout_overflow, stderr_overflow = [False], [False]
        readers = (
            threading.Thread(target=self._drain, args=(process.stdout, stdout_bytes, stdout_overflow),
                             name="orion-tool-stdout", daemon=True),
            threading.Thread(target=self._drain, args=(process.stderr, stderr_bytes, stderr_overflow),
                             name="orion-tool-stderr", daemon=True),
        )
        for reader in readers:
            reader.start()
        timed_out = False
        try:
            return_code = process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            self._stop_process(process)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._stop_process(process)
            return_code = process.returncode

        for reader in readers:
            reader.join(timeout=2)
        if any(reader.is_alive() for reader in readers):
            self._stop_process(process)
            for reader in readers:
                reader.join(timeout=2)
            raise RuntimeError(f"{self.spec.tool_id} retained open subprocess output handles")
        duration_ms = round((time.perf_counter_ns() - started) / 1_000_000)

        stdout = self._decode(bytes(stdout_bytes))
        stderr = self._decode(bytes(stderr_bytes))
        if stdout_overflow[0]:
            stdout += "\n[ORION STDOUT TRUNCATED AT 2 MiB]"
        if stderr_overflow[0]:
            stderr += "\n[ORION STDERR TRUNCATED AT 2 MiB]"
        if timed_out:
            raise TimeoutError(
                f"{self.spec.tool_id} exceeded {timeout_seconds:.1f}s; "
                f"stdout={stdout[:512]!r}; stderr={stderr[:512]!r}"
            )

        result: JsonObject = {
            "tool": self.spec.tool_id,
            "return_code": return_code,
            "duration_ms": duration_ms,
            "stdout": stdout,
            "stderr": stderr,
            "stdout_truncated": stdout_overflow[0],
            "stderr_truncated": stderr_overflow[0],
        }
        if return_code != 0:
            raise RuntimeError(
                f"{self.spec.tool_id} exited with code {return_code}: {(stderr or stdout)[:2048]}"
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
            if len(extra) > 32:
                raise ValueError("too many tool environment overrides")
            blocked = {"PATH", "PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP",
                       "PYTHONINSPECT", "LD_PRELOAD", "LD_LIBRARY_PATH",
                       "ORION_LAB_APPROVAL_FILE", "ORION_AUDIT_DATABASE", "ORION_EMERGENCY_STOP"}
            for key, value in extra.items():
                if not isinstance(key, str) or not key or not key.replace("_", "A").isalnum() or len(key) > 128:
                    raise ValueError(f"invalid environment variable name: {key!r}")
                normalized = key.upper()
                if normalized in blocked or normalized.startswith(("DYLD_", "LD_", "PYTHON")):
                    raise ValueError(f"protected environment variable cannot be overridden: {key!r}")
                if not isinstance(value, str) or len(value) > 4096 or "\x00" in value:
                    raise ValueError(f"invalid environment variable value for {key!r}")
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
