"""Local-only HTTP boundary and explicit MCP protocol compatibility reporting."""
from __future__ import annotations

import asyncio
import time
from importlib import metadata
from typing import Any
from urllib.parse import urlsplit


def require_local_configuration(config: Any) -> None:
    """Refuse unauthenticated remote bindings and wildcard browser origins."""
    if config.transport != "stdio" and config.host not in {"localhost", "127.0.0.1", "::1"}:
        raise ValueError("controlled MCP is local-only; remote OAuth deployment is not implemented")
    if "*" in config.cors_origins:
        raise ValueError("wildcard CORS is forbidden in the controlled profile")
    for origin in config.cors_origins:
        parsed = urlsplit(origin)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("CORS origins must be explicit HTTP(S) origins without credentials")
        if parsed.path or parsed.query or parsed.fragment or any(ord(char) < 33 for char in origin):
            raise ValueError("CORS origins must not contain paths, queries, fragments or whitespace")
        try:
            parsed.port
        except ValueError as exc:
            raise ValueError("invalid CORS origin port") from exc
    for path in (config.streamable_http_path, config.sse_path, config.message_path):
        if not path.startswith("/") or path.startswith("//") or any(char in path for char in "?#\\"):
            raise ValueError("MCP paths must be local absolute URL paths")
        if any(ord(char) < 33 for char in path) or ".." in path.split("/"):
            raise ValueError("MCP paths must not contain traversal or control characters")


def protocol_audit() -> dict[str, Any]:
    """Report the SDK baseline without presenting an SDK version as conformance proof."""
    try:
        import mcp.types as types
        sdk_version: str | None = metadata.version("mcp")
        latest: str | None = getattr(types, "LATEST_PROTOCOL_VERSION", None)
    except (ImportError, metadata.PackageNotFoundError):
        sdk_version, latest = None, None
    return {
        "requested_specification": "2026-07-28", "sdk_version": sdk_version,
        "sdk_declared_latest_protocol": latest,
        "orion_protocol_era": "initialize-handshake",
        "conforms_to_2026_07_28": False,
        "verification": "transport round trips are not full protocol conformance tests",
        "migration_requirements": [
            "server/discover and per-request protocol/capability metadata",
            "resultType on all results and required cache metadata",
            "modern HTTP method/name header validation",
            "modern cancellation and subscriptions semantics",
            "independent conformance tests before advertising the new revision",
        ],
        "remote_oauth_implemented": False,
        "unsupported_features": ["tasks extension", "MRTR", "MCP Apps", "skills-over-MCP extension"],
        "reference": "https://modelcontextprotocol.io/specification/2026-07-28/changelog",
    }


class LocalHttpGuard:
    """ASGI guard: exact Host/Origin validation and bounded request-body buffering.

    Response streams are not buffered. This is not authentication or a firewall.
    """
    def __init__(self, app: Any, config: Any, max_body_bytes: int = 1024 * 1024) -> None:
        require_local_configuration(config)
        self.app = app
        self.max_body_bytes = max_body_bytes
        self.hosts = {f"127.0.0.1:{config.port}", f"localhost:{config.port}", f"[::1]:{config.port}"}
        if config.port == 80:
            self.hosts.update({"127.0.0.1", "localhost", "[::1]"})
        self.origins = {f"http://{host}" for host in self.hosts} | set(config.cors_origins)

    @staticmethod
    async def _reject(send: Any, status: int, message: str) -> None:
        body = message.encode("utf-8")
        await send({"type": "http.response.start", "status": status,
                    "headers": [(b"content-type", b"text/plain; charset=utf-8"),
                                (b"cache-control", b"no-store"), (b"content-length", str(len(body)).encode())]})
        await send({"type": "http.response.body", "body": body})

    async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        pairs = [(key.lower(), value) for key, value in scope.get("headers", [])]
        headers = dict(pairs)
        for name in (b"host", b"origin", b"content-length"):
            if sum(key == name for key, _ in pairs) > 1:
                await self._reject(send, 400, "duplicate security-sensitive header")
                return
        host = headers.get(b"host", b"").decode("latin-1").lower()
        origin = headers.get(b"origin")
        if host not in self.hosts:
            await self._reject(send, 403, "invalid Host")
            return
        if origin is not None and origin.decode("latin-1") not in self.origins:
            await self._reject(send, 403, "invalid Origin")
            return
        length = headers.get(b"content-length")
        if length is not None:
            if not length.isdigit():
                await self._reject(send, 400, "invalid Content-Length")
                return
            if int(length) > self.max_body_bytes:
                await self._reject(send, 413, "request body too large")
                return
        if scope.get("method") not in {"POST", "PUT", "PATCH"}:
            await self.app(scope, receive, send)
            return
        body = bytearray()
        deadline = time.monotonic() + 10.0
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                await self._reject(send, 408, "request body deadline exceeded")
                return
            try:
                message = await asyncio.wait_for(receive(), timeout=remaining)
            except asyncio.TimeoutError:
                await self._reject(send, 408, "request body deadline exceeded")
                return
            if message["type"] == "http.disconnect":
                return
            body.extend(message.get("body", b""))
            if len(body) > self.max_body_bytes:
                await self._reject(send, 413, "request body too large")
                return
            if not message.get("more_body", False):
                break
        delivered = False

        async def bounded_receive() -> Any:
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": bytes(body), "more_body": False}
            return await receive()

        await self.app(scope, bounded_receive, send)
