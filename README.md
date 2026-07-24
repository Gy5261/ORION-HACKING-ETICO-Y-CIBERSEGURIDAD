# ORION 2.1 — Universal MCP Security Runtime

ORION is a typed plugin and MCP runtime for defensive security, authorized audits, OSINT, evidence collection and finding management.

## Runtime

```bash
python -m pip install -e ".[mcp]"
orion plugins list --health
orion plugins doctor
```

Every execution requires an authorization reference. Network access and external changes are separate explicit permissions.

```bash
orion plugins run ioc_enricher \
  --input samples/plugins/ioc-enricher.json \
  --authorization TOR-2026-ORION-001 \
  --allow-network
```

## Plugins

Native plugins:

- `ioc_enricher`
- `tls_posture_audit`
- `findings_ticket_sync`

External OSINT adapters:

- `spiderfoot`
- `theharvester`
- `sherlock`
- `osint_spy`
- `phoneinfoga`
- `photon`

External projects are not copied into this repository. ORION resolves trusted local installations, runs them without a shell, limits execution time and output, and normalizes results into JSON.

## Universal MCP integration

Local AI clients and IDEs can use stdio:

```bash
orion-mcp --transport stdio
```

Remote and browser-capable clients can use Streamable HTTP:

```bash
orion-mcp \
  --transport streamable-http \
  --host 127.0.0.1 \
  --port 8000 \
  --path /mcp \
  --stateless \
  --json-response
```

Legacy SSE remains available for older clients:

```bash
orion-mcp --transport sse
```

ORION exposes tools, structured tool results with text fallback, prompts, resource templates, exact repository resources, resource links, UTF-8 text and base64 binary content. The `orion_client_config` tool generates connection descriptors for generic MCP hosts, Claude Desktop, Claude Code, Cursor, Windsurf, Cline, Roo Code, VS Code and GitHub Copilot.

Generic local configuration:

```json
{
  "mcpServers": {
    "orion": {
      "command": "orion-mcp",
      "args": ["--transport", "stdio"]
    }
  }
}
```

## Documentation

- [Plugin architecture](docs/PLUGIN_SYSTEM.md)
- [OSINT integrations](docs/OSINT_INTEGRATIONS.md)
- [MCP server and interoperability](docs/MCP_SERVER.md)
- [Engineering contract](AGENTS.md)

## CI

The deterministic CI pipeline installs the official MCP SDK and performs real client/server round trips over stdio, Streamable HTTP and legacy SSE. It also validates source compilation, repository policies, plugin registration and runtime health.

## Legal and ethical scope

Use ORION only on systems, identities, domains, numbers and services for which you have explicit authorization or a lawful public-source research basis. An authorization string recorded by the runtime does not replace legal permission, Rules of Engagement or Terms of Reference.
