# simplex-engine TODO List

Last updated: 2026-06-09 (main, post PR #1–#3 + agent docs).

## Status snapshot

| Item | State |
|------|--------|
| Branch | `main` — PR #1 OpenGL, #2 streaming/collision, #3 MCP merged |
| Tests | **61** (`uv run pytest tests/ -q`) |
| CI | GitHub Actions — ruff + pytest (xvfb) |
| MCP | `simplex-mcp --check` OK; Cursor `.cursor/mcp.json` |
| Voxel demo | `run_player.py` — walk, stream chunks, gravity, jump |
| Ping-pong | `run_simple.py` — AI opponent works |

## MVP next (priority order)

1. [ ] **Block place/break** — raycast → chunk edit → remesh
2. [ ] **Cross-chunk face culling** — neighbor-aware meshgen (fix border seams)
3. [ ] **Voxel-only engine profile** — `mode = "voxel"` skips ping-pong systems
4. [ ] **Clean voxel demo config** — remove/gate `demo_resource` hot-reload warnings
5. [ ] **Noise terrain** — post-MVP world generation

See also [GOOD_FIRST_ISSUES.md](../../GOOD_FIRST_ISSUES.md) and [AGENTS.md](../../AGENTS.md).

---

## Input System
- [x] Design abstract input system API
- [x] Implement pygame backend for input
- [x] Support polling and state retrieval for keyboard and mouse
- [x] Integrate input events with ECS and game logic (OpenGL renderer + InputSystem)
- [ ] Support gamepad input in voxel demo
- [ ] Document API for future backend replacement

## Core Architecture
- [x] Implement ECS core (Entity, Component, System management)
- [x] Create base classes for Entity, Component, System
- [x] Integrate flexible event system for ECS
- [x] SubsystemManager for dependency-ordered initialization
- [x] Editable package install (`pyproject.toml` + hatchling)
- [ ] Provide serialization/deserialization for ECS objects
- [ ] Separate 2D (ping-pong) and 3D (voxel) system profiles

## Renderer
- [x] Implement OpenGL renderer backend
- [x] Design scene graph and rendering pipeline (MVP)
- [x] Support basic primitives and materials
- [x] Add camera and viewport management (FPS camera)
- [x] Implement VBO upload and cleanup utilities (VBOManager)
- [x] Wire ECS MeshComponent entities into OpenGL render loop
- [x] Add numpy for PyOpenGL fast path
- [ ] Shader-based rendering pipeline (replace fixed-function GL)
- [ ] Frustum culling and draw-call batching

## Voxel / Minecraft Project
- [x] Implement voxel block type system and palette
- [x] Implement Chunk storage and access APIs
- [x] Implement mesh generation (naive + greedy)
- [x] Implement ChunkManager for LRU caching and preload/unload APIs
- [x] First-person player controller (WASD + mouse look)
- [x] Minecraft-like demos (`run.py`, `run_player.py`)
- [x] Player-driven chunk streaming (horizontal, hysteresis, Y-locked slice)
- [x] Mesh generation budget (`mesh_chunks_per_frame` in config)
- [x] World query helpers (`world_query.py` — ground height, block lookup)
- [ ] Cross-chunk face culling (fix border seams)
- [ ] Block place/break interaction
- [ ] Add async mesh generation worker and GPU upload scheduler
- [ ] Implement world generation and biome systems (noise terrain)

## Physics
- [x] Define physics component and system interfaces (MVP)
- [x] 2D AABB collision for ping-pong demo
- [x] Voxel grid collision (gravity, ground snap, jump, horizontal blocking)
- [ ] Integrate pybullet or custom 3D collision for physics simulation
- [ ] Add rigid body and soft body support

## Performance
- [x] Horizontal-only streaming (9 chunks at radius 1)
- [x] Stream on chunk boundary only (not every frame)
- [x] Chunk streaming hysteresis (avoid border thrash)
- [x] Headless performance regression tests (`tests/test_performance.py`)
- [ ] Profile and optimize immediate-mode GL fallback path

## Scripting
- [x] Implement ScriptManager for Python scripting
- [x] Support hot-reloading of scripts
- [x] Provide API for game logic and event hooks
- [ ] Script editor integration polish

## Resource Manager
- [x] Implement ResourceManager for asset loading/unloading
- [x] Support various resource types (textures, models, audio, scripts)
- [x] Add resource caching and hot-reload hooks
- [ ] Add reference counting

## Audio
- [x] Implement Audio system interface
- [x] Support playback, stop, and audio resource management
- [x] Integrate with resource manager for audio assets

## Engine Core
- [x] Implement Engine main loop
- [x] Design configuration and resource management
- [x] Add logging and debugging utilities
- [x] World config section (`streaming_radius`, `horizontal_streaming`, `mesh_chunks_per_frame`)
- [ ] Game mode selection (2D vs 3D) in config

## AI & Community
- [x] MCP server (`simplex/mcp/`, `uv run simplex-mcp`)
- [x] MCP tools: status, health_check, tests, lint, world_probe, demos
- [x] MCP resources: agents, contributing, todo, config, architecture
- [x] AGENTS.md — agent onboarding guide
- [x] CONTRIBUTING.md — contributor workflow
- [x] GOOD_FIRST_ISSUES.md — scoped starter tasks
- [x] Cursor rules (`.cursor/rules/`)
- [x] GitHub issue templates (bug, feature)
- [ ] Enable GitHub Discussions for Q&A
- [ ] Document testing guidelines in `docs/development/testing.md`

## Testing & CI
- [x] Unit tests — 61 across ECS, voxel, world, renderer, MCP, perf
- [x] CI pipeline (GitHub Actions)
- [x] pytest scoped to `tests/` only
- [x] Ping-pong AI regression test
- [x] Chunk streaming + voxel collision tests

## Examples & Demos
- [x] Ping-pong example game (AI fixed, `ecs_setup.py`)
- [x] Minecraft-like voxel demos
- [x] `run_simple.py` rename (was `test_simple.py`)
- [ ] Provide demo scenes for video creators

---

This list reflects the current codebase. Quick commands: [README](../../README.md) · [AGENTS.md](../../AGENTS.md) · `uv run simplex-mcp --check`
