# ORION 2.0 Plugin System

ORION converts security capabilities into typed, discoverable, auditable plugins. The runtime is the source of truth for CLI, MCP, manifests, tests, and external integrations.

## Architecture

```text
orion/
├── cli.py                  # CLI
├── resources.py            # read-only MCP resource catalog
├── mcp/server.py           # FastMCP server
├── plugins/
│   ├── core.py             # contracts, policy, registry, runtime
│   ├── adapters.py         # hardened subprocess adapters
│   ├── builtin.py          # native plugins
│   └── osint.py            # external OSINT integrations
└── scripts/                # existing native engines
```

## Stable contract

Every plugin implements `BasePlugin`, publishes immutable `PluginMetadata`, exposes `health()`, and returns JSON-compatible data.

```python
from orion.plugins import BasePlugin, PluginContext, PluginMetadata


class ExamplePlugin(BasePlugin):
    metadata = PluginMetadata(
        plugin_id="example_plugin",
        name="Example Plugin",
        version="1.0.0",
        category="defensive",
        description="Read-only authorized defensive example.",
        risk_level="low",
        capabilities=("example",),
        input_schema={"type": "object"},
        output_schema={"type": "object"},
    )

    def run(self, payload: dict, context: PluginContext) -> dict:
        return {"ok": True}
```

Metadata declares authorization, network access, request-specific side effects, timeouts, schemas, tags, integration type, homepage, and license.

## Execution policy

The runtime validates, in order:

1. plugin identifier;
2. input schema;
3. authorization reference;
4. network permission;
5. request-specific side-effect permission;
6. optional dependency health;
7. output schema;
8. normalized result metadata.

Every result contains plugin ID and version, request UUID, actor, duration, warnings, data, or a structured error.

## External tools

External projects are not copied into ORION. Adapters resolve trusted local executables, use `shell=False`, reject arbitrary arguments, bound execution time and output, isolate artifacts in temporary directories, and expose missing dependencies through health checks.

Supported adapters:

- SpiderFoot;
- theHarvester;
- Sherlock;
- OSINT-SPY;
- PhoneInfoga;
- Photon.

See [OSINT integrations](OSINT_INTEGRATIONS.md).

## CLI

```bash
orion plugins list --health
orion plugins describe photon --health
orion plugins doctor
orion plugins doctor --strict
orion plugins export-manifest --output skills/skills.json
```

```bash
orion plugins run photon \
  --input samples/plugins/photon.json \
  --authorization TOR-2026-ORION-001 \
  --allow-network
```

The default doctor treats missing third-party executables as optional. `--strict` requires every integration to be installed.

## MCP

The MCP server exposes plugin discovery, health, execution, repository search, manifests, plugin resources, and bounded read-only access to repository text resources.

```bash
python -m pip install -e ".[mcp]"
orion-mcp
```

See [MCP server](MCP_SERVER.md).

## Quality gate

```bash
python tools/validate_repository.py
python -m pytest
orion plugins doctor
python -m build
```

The validator checks the exact plugin set, authorization metadata, subprocess policy, static/runtime manifest synchronization, and resource path isolation.

## Compatibility

- Python 3.10–3.13;
- no mandatory third-party runtime dependencies;
- optional MCP dependency;
- JSON-first interfaces;
- standard Python entry points;
- source checkout, editable installation, wheel, containers, and MCP clients.
