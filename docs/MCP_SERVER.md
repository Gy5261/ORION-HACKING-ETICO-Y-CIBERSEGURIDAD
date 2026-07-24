# ORION MCP server

Install MCP support:

```bash
python -m pip install -e ".[mcp]"
```

Run over stdio:

```bash
orion-mcp
```

Run with Streamable HTTP:

```bash
orion-mcp --transport streamable-http
```

## MCP tools

- `orion_list_plugins`: returns contracts and dependency health.
- `orion_doctor`: validates discovery and optional tools.
- `orion_run_plugin`: executes one plugin with explicit authorization and permissions.
- `orion_search_resources`: searches documentation, playbooks, references, schemas, samples, and source.
- `orion_read_resource`: reads one bounded repository file using a traversal-safe relative path.

## MCP resources

- `orion://manifest`
- `orion://repository/index`
- `orion://plugins/{plugin_id}`
- one exact `orion://repository/<path>` resource for every readable repository file

The server registers every text resource found by the catalog. The catalog is read-only, blocks path traversal, excludes caches and binaries, and limits each resource to 512 KiB. Set `ORION_RESOURCE_ROOT` when the server must expose a checkout outside the current working directory.

## Client configuration

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
