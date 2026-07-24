"""Read-only resource catalog shared by the CLI and MCP server."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from orion.plugins.core import JsonObject, PluginRegistry, dumps_json

_ALLOWED_SUFFIXES = {".md", ".json", ".py", ".toml", ".yml", ".yaml", ".txt"}
_EXCLUDED_PARTS = {
    ".git",
    ".github",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}
_MAX_RESOURCE_BYTES = 512 * 1024


@dataclass(frozen=True, slots=True)
class ResourceDescriptor:
    uri: str
    path: str
    name: str
    media_type: str
    size_bytes: int

    def to_dict(self) -> JsonObject:
        return asdict(self)


class ResourceCatalog:
    """Bounded, path-safe catalog of repository knowledge resources."""

    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root).resolve() if root else self._default_root()

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

    def list(self) -> tuple[ResourceDescriptor, ...]:
        descriptors: list[ResourceDescriptor] = []
        for path in self._iter_files():
            relative = path.relative_to(self.root).as_posix()
            descriptors.append(
                ResourceDescriptor(
                    uri=f"orion://repository/{relative}",
                    path=relative,
                    name=path.name,
                    media_type=self._media_type(path),
                    size_bytes=path.stat().st_size,
                )
            )
        return tuple(descriptors)

    def index(self) -> JsonObject:
        registry = PluginRegistry()
        return {
            "project": "ORION-HACKING-ETICO-Y-CIBERSEGURIDAD",
            "manifest_uri": "orion://manifest",
            "plugin_count": len(registry.list()),
            "plugins": [
                {
                    "plugin_id": plugin.metadata.plugin_id,
                    "resource_uri": f"orion://plugins/{plugin.metadata.plugin_id}",
                }
                for plugin in registry.list()
            ],
            "resources": [descriptor.to_dict() for descriptor in self.list()],
        }

    def read(self, relative_path: str) -> str:
        path = self._resolve(relative_path)
        if not path.is_file() or path.suffix.lower() not in _ALLOWED_SUFFIXES:
            raise FileNotFoundError(f"resource not found: {relative_path}")
        size = path.stat().st_size
        if size > _MAX_RESOURCE_BYTES:
            raise ValueError(f"resource exceeds {_MAX_RESOURCE_BYTES} bytes: {relative_path}")
        return path.read_text(encoding="utf-8", errors="replace")

    def search(self, query: str, limit: int = 20) -> list[JsonObject]:
        normalized = query.strip().casefold()
        if len(normalized) < 2:
            raise ValueError("query must contain at least two characters")
        bounded_limit = max(1, min(limit, 100))
        matches: list[JsonObject] = []
        for descriptor in self.list():
            if len(matches) >= bounded_limit:
                break
            try:
                text = self.read(descriptor.path)
            except (OSError, ValueError):
                continue
            position = text.casefold().find(normalized)
            if position < 0 and normalized not in descriptor.path.casefold():
                continue
            start = max(0, position - 160) if position >= 0 else 0
            end = min(len(text), position + len(normalized) + 320) if position >= 0 else 320
            matches.append(
                {
                    "uri": descriptor.uri,
                    "path": descriptor.path,
                    "snippet": text[start:end].replace("\n", " ").strip(),
                }
            )
        return matches

    def manifest_json(self) -> str:
        return dumps_json(PluginRegistry().manifest())

    def plugin_json(self, plugin_id: str) -> str:
        plugin = PluginRegistry().get(plugin_id)
        payload = plugin.metadata.to_dict()
        payload["health"] = plugin.health().to_dict()
        return dumps_json(payload)

    def _iter_files(self) -> Iterable[Path]:
        for path in sorted(self.root.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue
            relative_parts = path.relative_to(self.root).parts
            if any(part in _EXCLUDED_PARTS for part in relative_parts):
                continue
            if path.suffix.lower() not in _ALLOWED_SUFFIXES:
                continue
            if path.stat().st_size > _MAX_RESOURCE_BYTES:
                continue
            yield path.resolve()

    def _resolve(self, relative_path: str) -> Path:
        candidate = (self.root / relative_path).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError as exc:
            raise ValueError("resource path escapes repository root") from exc
        return candidate

    @staticmethod
    def _media_type(path: Path) -> str:
        return {
            ".md": "text/markdown",
            ".json": "application/json",
            ".py": "text/x-python",
            ".toml": "application/toml",
            ".yml": "application/yaml",
            ".yaml": "application/yaml",
        }.get(path.suffix.lower(), "text/plain")
