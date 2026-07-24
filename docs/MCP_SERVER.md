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
- `orion_search_resources`: searches repository documentation, playbooks, references, schemas, and source.

## MCP resources

- `orion://manifest`
- `orion://repository/index`
- `orion://plugins/{plugin_id}`
- `orion://repository/{path}`

The resource catalog is read-only, blocks path traversal, excludes caches and binaries, and limits each resource to 512 KiB.

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
