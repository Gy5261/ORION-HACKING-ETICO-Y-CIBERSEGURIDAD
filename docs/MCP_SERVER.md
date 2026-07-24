# ORION MCP server

ORION 2.1 exposes the complete plugin runtime and repository catalog through the Model Context Protocol. The server is client-neutral: any host that implements MCP can discover the same tools, resources, templates and prompts without vendor-specific code.

## Installation

```bash
python -m pip install -e ".[mcp]"
```

The stable MCP Python SDK is kept behind the optional dependency so the base ORION CLI remains lightweight.

## Standard transports

### stdio

Recommended for local desktop applications, IDEs and agent processes.

```bash
orion-mcp --transport stdio
```

The process writes only MCP JSON-RPC messages to stdout. Diagnostics use stderr.

### Streamable HTTP

Recommended for remote, multi-client and browser-capable deployments.

```bash
orion-mcp \
  --transport streamable-http \
  --host 127.0.0.1 \
  --port 8000 \
  --path /mcp \
  --stateless \
  --json-response
```

Use `--stream-response` when the client expects `text/event-stream` responses. Remote interfaces such as `0.0.0.0` require `--allow-remote` explicitly.

### Legacy SSE

Available for older clients that still implement the superseded HTTP+SSE transport.

```bash
orion-mcp \
  --transport sse \
  --host 127.0.0.1 \
  --port 8000 \
  --sse-path /sse \
  --message-path /messages/
```

New deployments should prefer Streamable HTTP.

## Browser clients and CORS

Expose only trusted origins:

```bash
orion-mcp \
  --transport streamable-http \
  --cors-origin https://client.example \
  --cors-origin http://localhost:5173
```

ORION exposes `Mcp-Session-Id` and accepts the standard Streamable HTTP methods and protocol headers. `--allow-any-origin` exists for isolated development only.

## Environment configuration

All command-line defaults can be provided through environment variables:

| Variable | Purpose |
| --- | --- |
| `ORION_MCP_TRANSPORT` | `stdio`, `streamable-http` or `sse` |
| `ORION_MCP_HOST` | Bind address; defaults to `127.0.0.1` |
| `ORION_MCP_PORT` | HTTP port; defaults to `8000` |
| `ORION_MCP_PATH` | Streamable HTTP endpoint; defaults to `/mcp` |
| `ORION_MCP_SSE_PATH` | Legacy SSE endpoint |
| `ORION_MCP_MESSAGE_PATH` | Legacy SSE message endpoint |
| `ORION_MCP_STATELESS` | Stateless HTTP session mode |
| `ORION_MCP_RESPONSE_MODE` | `json` or `stream` |
| `ORION_MCP_CORS_ORIGINS` | Comma-separated trusted origins |
| `ORION_MCP_LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL` |
| `ORION_RESOURCE_ROOT` | Repository/catalog root |
| `ORION_RESOURCE_MAX_BYTES` | Maximum exposed resource size |

Inspect the resolved configuration without starting the protocol server:

```bash
orion-mcp --transport streamable-http --print-config
```

## Client-neutral configuration

Most local clients use the common `mcpServers` shape:

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

A remote descriptor uses the MCP endpoint:

```json
{
  "mcpServers": {
    "orion": {
      "url": "https://orion.example/mcp",
      "transport": "streamable-http"
    }
  }
}
```

The `orion_client_config` tool and `orion://mcp/client-config/{client}/{transport}` resource generate configurations for generic clients, Claude Desktop, Claude Code, Cursor, Windsurf, Cline, Roo Code, VS Code and GitHub Copilot. Unknown client names receive a standards-based generic descriptor instead of failing.

## MCP tools

- `orion_mcp_capabilities`: reports protocol, transports, encodings and exposed primitives.
- `orion_client_config`: generates a client-specific connection descriptor.
- `orion_list_plugins`: returns every plugin contract and optional dependency health.
- `orion_get_plugin`: returns one exact plugin contract.
- `orion_doctor`: validates plugin discovery, resources and MCP runtime metadata.
- `orion_run_plugin`: executes one plugin with explicit authorization and permissions.
- `orion_search_resources`: searches text resources and binary filenames.
- `orion_resource_links`: returns MCP resource-link descriptors.
- `orion_read_resource`: reads a UTF-8 text resource.
- `orion_read_resource_content`: returns text or base64 binary content with MIME metadata.

Dictionary and list results are emitted as structured tool output by FastMCP and retain the JSON text fallback required for older clients.

## MCP resources

- `orion://manifest`
- `orion://mcp/capabilities`
- `orion://repository/index`
- `orion://plugins/{plugin_id}`
- `orion://mcp/client-config/{client}/{transport}`
- one exact `orion://repository/<path>` resource for every permitted repository file

The catalog supports source, Markdown, JSON, JSONL, YAML, TOML, HTML, XML, CSV, shell files, images, audio and PDF resources. Text is returned as UTF-8; binary resources use MCP blob/base64 semantics. Secret-like files, caches, build outputs, symlinks, path traversal and oversized resources are blocked.

## MCP prompts

- `authorized_security_workflow`: establishes authorization and least-privilege execution rules.
- `mcp_integration_guide`: returns integration instructions and a concrete client configuration.

## Validation

CI performs real round trips with the official MCP client SDK over:

1. stdio;
2. Streamable HTTP;
3. legacy SSE.

Each session initializes, negotiates capabilities, lists tools/resources/prompts and calls `orion_mcp_capabilities`. This catches transport and schema regressions rather than validating construction only.

## Security defaults

- HTTP binds to loopback by default.
- Remote binding requires explicit confirmation.
- CORS is disabled unless trusted origins are provided.
- Plugin authorization, network permission and side-effect permission remain separate.
- Repository resources are read-only and bounded.
- SSE is retained only for backwards compatibility.
