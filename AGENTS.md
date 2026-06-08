# AGENTS.md — AI agent guide for simplex-engine

Instructions for coding agents (Cursor, Claude, Copilot, etc.) working in this repository.

## Project

**simplex-engine** — Python ECS game engine focused on a Minecraft-like voxel demo.

- Python **3.13+**, package manager: **uv**
- Core: `simplex/` — ECS, OpenGL renderer, chunk streaming, voxel collision
- Examples: `examples/minecraft-like/`, `examples/ping_pong/`
- Tests: `tests/` only (pytest `testpaths = ["tests"]`)

## First commands

```bash
uv sync
uv run simplex-mcp --check    # MCP smoke test
uv run pytest tests/ -q       # 57+ tests
uv run ruff check simplex/ tests/
uv run python3 examples/minecraft-like/run_player.py   # needs display
```

## MCP (preferred for agents)

Enable **simplex-engine** in Cursor MCP (`.cursor/mcp.json`). Use tools before guessing:

| Tool | When to use |
|------|-------------|
| `project_status` | Branch, dirty state, test count |
| `health_check` | Pre-PR: lint + tests |
| `engine_capabilities` | What subsystems exist |
| `world_probe` | Headless chunk/ground check (no GPU) |
| `demo_instructions` | How to run a demo |
| `good_first_issues` | Scoped contributor tasks |
| `run_tests` / `run_lint` | CI commands |

Resources: `simplex://agents`, `simplex://contributing`, `simplex://good-first-issues`, `simplex://docs/todo`

## Architecture (where to edit)

| Area | Path |
|------|------|
| Engine loop | `simplex/engine.py` |
| ECS systems | `simplex/ecs/` |
| Voxel meshing | `simplex/voxel/meshgen.py`, `chunk.py` |
| Streaming | `simplex/ecs/chunk_streaming_system.py`, `simplex/world/chunk_manager.py` |
| Collision | `simplex/ecs/voxel_collision_system.py`, `simplex/world/world_query.py` |
| OpenGL draw | `simplex/renderer/opengl_renderer.py` |
| Config | `examples/config.toml` |
| MCP | `simplex/mcp/` |

## Coding rules

1. **Minimal diff** — fix the requested problem only; match existing style.
2. **Tests** — run `uv run pytest tests/ -q` before finishing; add tests for real behavior.
3. **Lint** — `uv run ruff check simplex/ tests/`.
4. **No commits** unless the user asks.
5. **Chunk coords** — `spawn_chunk((x,0,z))` uses chunk indices; mesh origin = index × 16.
6. **ECS update order** matters: input → movement → collision → game systems → render.
7. **Examples** — add `sys.path` bootstrap like `run_player.py` if script is under `examples/`.

## MVP priorities (feature work)

1. **Block place/break** — raycast → `ChunkManager` → remesh (highest gameplay value)
2. **Cross-chunk face culling** — neighbor-aware meshgen (fix border seams)
3. **Engine profile** — `mode = "voxel"` skips ping-pong systems in `engine.py`
4. Noise terrain / biomes — post-MVP

## PR checklist

- [ ] `uv run ruff check simplex/ tests/`
- [ ] `uv run pytest tests/ -q`
- [ ] Focused commit message (why, not just what)
- [ ] Update `docs/todo/todo.md` if completing a listed item

## Demos

| Demo | Command | Notes |
|------|---------|-------|
| Voxel FPS | `uv run python3 examples/minecraft-like/run_player.py` | WASD, mouse, Space, ESC |
| Ping-pong | `uv run python3 examples/ping_pong/run_simple.py` | Arrows / W/S |

Wayland: `run_player.py` auto-relaunches with `SDL_VIDEODRIVER=x11`.
