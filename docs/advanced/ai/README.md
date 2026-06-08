# AI-native integration (MCP)

Simplex Engine ships a [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server so AI assistants in Cursor and other MCP clients can inspect, test, and probe the engine without guessing project layout.

## Enable in Cursor

The repo includes `.cursor/mcp.json`. After `uv sync`, open **Cursor Settings → MCP** and enable the **simplex-engine** server (or reload the window).

Equivalent root-level config: `mcp.json`.

## Run manually

```bash
uv sync
uv run simplex-mcp
# or
uv run python -m simplex.mcp
```

The server uses stdio transport (default for Cursor).

## Tools

| Tool | Purpose |
|------|---------|
| `project_status` | Git branch, dirty state, Python version, test count |
| `engine_capabilities` | Subsystems, demos, lint/test commands |
| `list_demos` | Runnable example scripts |
| `run_tests` | Execute pytest (optional path / extra args) |
| `run_lint` | Run ruff on `simplex/` and `tests/` |
| `world_probe` | Headless chunk load + ground height (no GPU) |

## Resources

| URI | Content |
|-----|---------|
| `simplex://docs/todo` | `docs/todo/todo.md` |
| `simplex://config` | `examples/config.toml` |
| `simplex://readme` | Project README |
| `simplex://architecture` | Architecture overview |

## SDK / automation

To drive Cursor agents programmatically with MCP enabled, see the [Cursor SDK](https://cursor.com/docs/sdk/overview) and pass MCP server config in the agent environment.

## Extend

Add tools in `simplex/mcp/tools.py` and register them in `simplex/mcp/server.py`. Keep tool implementations headless and testable — see `tests/test_mcp_tools.py`.
