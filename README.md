# ORION 2.0 — Authorized Security Runtime

ORION is a typed plugin and MCP runtime for defensive security, authorized audits, OSINT, evidence collection, and finding management.

## Runtime

```bash
python -m pip install -e ".[mcp]"
orion plugins list --health
orion plugins doctor
```

Every execution requires an authorization reference. Network and external changes are separate explicit permissions.

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

## MCP

```bash
orion-mcp
```

The MCP server exposes all registered plugins plus a read-only catalog of ORION playbooks, references, documentation, schemas, samples, and source files.

Documentation:

- [Plugin architecture](docs/PLUGIN_SYSTEM.md)
- [OSINT integrations](docs/OSINT_INTEGRATIONS.md)
- [MCP server](docs/MCP_SERVER.md)
- [Engineering contract](AGENTS.md)

## CI

A single deterministic workflow validates source policy, contracts, nine-plugin registration, tests, Python 3.10–3.13 compatibility, MCP construction, wheel build, clean installation, and runtime smoke tests.

## Legal and ethical scope

Use ORION only on systems, identities, domains, numbers, and services for which you have explicit authorization or a lawful public-source research basis. An authorization string recorded by the runtime does not replace legal permission, Rules of Engagement, or Terms of Reference.
