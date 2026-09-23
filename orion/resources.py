"""Bounded, read-only repository resources; private control and evidence files are excluded."""
from __future__ import annotations

import base64
import mimetypes
import os
import stat
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from orion.plugins.core import JsonObject, PluginRegistry, dumps_json

_TEXT_SUFFIXES = {".cfg", ".css", ".csv", ".html", ".ini", ".js", ".json", ".md", ".ps1", ".py",
                  ".sh", ".svg", ".toml", ".ts", ".tsx", ".txt", ".xml", ".yaml", ".yml"}
_BINARY_SUFFIXES = {".gif", ".jpeg", ".jpg", ".mp3", ".ogg", ".pdf", ".png", ".wav", ".webp"}
_ALLOWED_SUFFIXES = _TEXT_SUFFIXES | _BINARY_SUFFIXES
_EXCLUDED_PARTS = {"__pycache__", "build", "dist", "node_modules", "evidence", "engagements", "audit", "private"}
_EXCLUDED_NAMES = {"credentials.json", "secrets.json", "approval.json", "lab-approval.json"}
_DEFAULT_MAX_RESOURCE_BYTES = 2 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class ResourceDescriptor:
    uri: str
    path: str
    name: str
    media_type: str
    size_bytes: int
    binary: bool

    def to_dict(self) -> JsonObject:
        return asdict(self)


class ResourceCatalog:
    """Publish a trusted read-only tree, never an arbitrary home or assessment directory.

    Name filtering is defense in depth, not secret detection. The operator must keep
    private data outside the published tree and deny untrusted writers to its parents.
    """
    def __init__(self, root: str | Path | None = None, max_resource_bytes: int | None = None) -> None:
        self.root = Path(root).resolve() if root else self._default_root()
        limit = max_resource_bytes if max_resource_bytes is not None else int(
            os.getenv("ORION_RESOURCE_MAX_BYTES", str(_DEFAULT_MAX_RESOURCE_BYTES)))
        if type(limit) is not int or not 1 <= limit <= 16 * 1024 * 1024:
            raise ValueError("max_resource_bytes must be between 1 byte and 16 MiB")
        self.max_resource_bytes = limit

    @staticmethod
    def _default_root() -> Path:
        override = os.getenv("ORION_RESOURCE_ROOT")
        if override:
            return Path(override).expanduser().resolve()
        source_root = Path(__file__).resolve().parents[1]
        if (source_root / "pyproject.toml").is_file():
            return source_root
        working_root = Path.cwd().resolve()
        if (working_root / "orion").is_dir() and (working_root / "README.md").is_file():
            return working_root
        return Path(__file__).resolve().parent

    @staticmethod
    def _excluded_part(part: str) -> bool:
        lowered = part.casefold()
        return lowered.startswith(".") or lowered in _EXCLUDED_PARTS or lowered.endswith(".egg-info")

    def _published(self, path: Path) -> bool:
        relative = path.relative_to(self.root)
        if any(self._excluded_part(part) for part in relative.parts):
            return False
        if path.name.casefold() in _EXCLUDED_NAMES or path.suffix.casefold() not in _ALLOWED_SUFFIXES:
            return False
        for variable in ("ORION_LAB_APPROVAL_FILE", "ORION_AUDIT_DATABASE"):
            raw = os.getenv(variable)
            if raw:
                private = str(Path(raw).expanduser().resolve())
                if str(path) in {private, private + "-journal", private + "-wal", private + "-shm"}:
                    return False
        return True

    def _resolve(self, relative_path: str) -> Path:
        if not isinstance(relative_path, str) or not relative_path or "\x00" in relative_path:
            raise ValueError("resource path must be a nonempty relative path")
        relative = Path(relative_path)
        if relative.is_absolute() or ".." in relative.parts or "\\" in relative_path:
            raise ValueError("resource path escapes repository root or is not canonical")
        candidate = self.root / relative
        cursor = candidate
        while cursor != self.root:
            if cursor.is_symlink():
                raise ValueError("symbolic links are not published resources")
            cursor = cursor.parent
        resolved = candidate.resolve()
        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise ValueError("resource path escapes repository root") from exc
        return resolved

    def descriptor(self, relative_path: str) -> ResourceDescriptor:
        path = self._resolve(relative_path)
        if not self._published(path):
            raise FileNotFoundError("resource is not published")
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_size > self.max_resource_bytes:
            raise ValueError("resource is not a bounded regular file")
        relative = path.relative_to(self.root).as_posix()
        return ResourceDescriptor(uri=f"orion://repository/{relative}", path=relative, name=path.name,
                                  media_type=self._media_type(path), size_bytes=info.st_size,
                                  binary=path.suffix.lower() in _BINARY_SUFFIXES)

    def _iter_files(self) -> Iterable[Path]:
        count = 0
        for current, directories, filenames in os.walk(self.root, followlinks=False):
            directories[:] = sorted(name for name in directories if not self._excluded_part(name)
                                    and not (Path(current) / name).is_symlink())
            for name in sorted(filenames):
                if count >= 5000:
                    return
                path = Path(current) / name
                try:
                    descriptor = self.descriptor(path.relative_to(self.root).as_posix())
                except (OSError, ValueError):
                    continue
                count += 1
                yield self.root / descriptor.path

    def list(self) -> tuple[ResourceDescriptor, ...]:
        descriptors = []
        for path in self._iter_files():
            try:
                descriptors.append(self.descriptor(path.relative_to(self.root).as_posix()))
            except (OSError, ValueError):
                continue
        return tuple(sorted(descriptors, key=lambda item: item.path))

    def read_bytes(self, relative_path: str) -> bytes:
        descriptor = self.descriptor(relative_path)
        path = self._resolve(descriptor.path)
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        with os.fdopen(os.open(path, flags), "rb") as handle:
            if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
                raise ValueError("resource changed to a non-regular file")
            data = handle.read(self.max_resource_bytes + 1)
        if len(data) > self.max_resource_bytes:
            raise ValueError("resource exceeds the actual read-byte limit")
        return data

    def read(self, relative_path: str) -> str:
        if self.descriptor(relative_path).binary:
            raise ValueError("resource is binary")
        return self.read_bytes(relative_path).decode("utf-8", errors="replace")

    def read_mcp(self, relative_path: str) -> str | bytes:
        return self.read_bytes(relative_path) if self.descriptor(relative_path).binary else self.read(relative_path)

    def payload(self, relative_path: str) -> JsonObject:
        descriptor = self.descriptor(relative_path)
        data = self.read_bytes(relative_path)
        result: JsonObject = {"uri": descriptor.uri, "path": descriptor.path, "mimeType": descriptor.media_type,
                              "size": len(data), "encoding": "base64" if descriptor.binary else "utf-8"}
        if descriptor.binary:
            result["blob"] = base64.b64encode(data).decode("ascii")
        else:
            result["text"] = data.decode("utf-8", errors="replace")
        return result

    def search(self, query: str, limit: int = 20) -> list[JsonObject]:
        normalized = query.strip().casefold()
        if not 2 <= len(normalized) <= 512:
            raise ValueError("query must contain 2 to 512 characters")
        results: list[JsonObject] = []
        for descriptor in self.list():
            if len(results) >= max(1, min(limit, 100)):
                break
            if descriptor.binary:
                if normalized in descriptor.path.casefold():
                    results.append({"uri": descriptor.uri, "path": descriptor.path,
                                    "mimeType": descriptor.media_type, "snippet": "binary resource"})
                continue
            try:
                text = self.read(descriptor.path)
            except (OSError, ValueError):
                continue
            position = text.casefold().find(normalized)
            if position < 0 and normalized not in descriptor.path.casefold():
                continue
            start = max(0, position - 160) if position >= 0 else 0
            end = min(len(text), position + len(normalized) + 320) if position >= 0 else 320
            results.append({"uri": descriptor.uri, "path": descriptor.path, "mimeType": descriptor.media_type,
                            "snippet": text[start:end].replace("\n", " ").strip()})
        return results

    def index(self) -> JsonObject:
        registry = PluginRegistry(load_external=False)
        return {"project": "ORION-HACKING-ETICO-Y-CIBERSEGURIDAD", "manifest_uri": "orion://manifest",
                "mcp_capabilities_uri": "orion://mcp/capabilities", "plugin_count": len(registry.list()),
                "plugins": [{"plugin_id": item.metadata.plugin_id,
                             "resource_uri": f"orion://plugins/{item.metadata.plugin_id}"} for item in registry.list()],
                "resources": [item.to_dict() for item in self.list()]}

    def manifest_json(self) -> str:
        return dumps_json(PluginRegistry(load_external=False).manifest())

    def plugin_json(self, plugin_id: str) -> str:
        plugin = PluginRegistry(load_external=False).get(plugin_id)
        result = plugin.metadata.to_dict()
        result["health"] = plugin.health().to_dict()
        return dumps_json(result)

    @staticmethod
    def _media_type(path: Path) -> str:
        explicit = {".md": "text/markdown", ".py": "text/x-python", ".toml": "application/toml",
                    ".yaml": "application/yaml", ".yml": "application/yaml"}
        if path.suffix.lower() in explicit:
            return explicit[path.suffix.lower()]
        guessed, _ = mimetypes.guess_type(path.name)
        return guessed or ("application/octet-stream" if path.suffix.lower() in _BINARY_SUFFIXES else "text/plain")
