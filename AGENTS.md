# ORION Engineering Contract

Every contributor and coding agent must read this file before changing the repository.

## Non-negotiable rules

1. Authorized defensive use only. No malware, credential theft, persistence, evasion, phishing, destructive actions, or out-of-scope access.
2. Public APIs are typed, documented, deterministic, and backwards-compatible within a major version.
3. External tools are adapters, never vendored copies. Use `shell=False`, bounded timeouts, bounded output, temporary directories, and allow-listed arguments.
4. Network access and side effects remain disabled unless the caller enables them explicitly and supplies an authorization reference.
5. A missing optional OSINT executable must produce a clear health result, not break installation or default CI.
6. Tests must not contact the internet. Mock services and create fake executables in temporary directories.
7. Keep modules focused. Prefer small contracts and composition over hidden global state.
8. Never merge code that fails `python tools/validate_repository.py`, `python -m pytest`, package build, or runtime doctor.

## Definition of done

- Input and output schemas exist.
- Error messages are actionable.
- Paths are traversal-safe.
- Processes never use a shell.
- Secrets are supplied through environment variables, never arguments or committed files.
- Documentation, static manifest, runtime manifest, CLI, MCP, and tests agree.
