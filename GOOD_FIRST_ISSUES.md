# Good first issues

Scoped tasks for new contributors and AI agents. Each item lists likely files.

## Gameplay (MVP)

### 1. Block place / break
**Goal:** Left-click break, right-click place block at raycast hit.  
**Files:** new `simplex/ecs/block_interaction_system.py`, `simplex/world/world_query.py`, `run_player.py` input wiring.  
**Tests:** headless raycast + chunk dirty flag.

### 2. Cross-chunk face culling
**Goal:** No visible seams at chunk borders.  
**Files:** `simplex/voxel/meshgen.py`, `ChunkMeshSystem` (pass neighbor chunks).  
**Tests:** `tests/voxel/test_meshgen.py` border cases.

### 3. Disable hot-reload in voxel demo
**Goal:** Remove startup warnings from `demo_resource` in `examples/config.toml`.  
**Files:** `examples/config.toml`, optional `engine.py` guard.

## Engine

### 4. Voxel-only engine profile
**Goal:** `mode = "voxel"` in config skips ping-pong ECS systems.  
**Files:** `simplex/engine.py`, `examples/config.toml`.  
**Tests:** engine init registers fewer systems in voxel mode.

### 5. Jump via Space in collision system
**Goal:** Document/fix Space as jump (verify in `run_player.py`).  
**Files:** `simplex/ecs/voxel_collision_system.py`, demo README.

## Community / AI

### 6. Expand MCP `demo_instructions`
**Goal:** Return controls + prerequisites per demo name.  
**Files:** `simplex/mcp/tools.py`, `tests/test_mcp_tools.py`.

### 7. Sync docs/todo/todo.md
**Goal:** Mark streaming, collision, MCP, numpy VBO as done.  
**Files:** `docs/todo/todo.md`, `README.md` planned section.

### 8. GitHub issue templates
**Goal:** Bug + feature templates under `.github/ISSUE_TEMPLATE/`.  
**Files:** `.github/ISSUE_TEMPLATE/*.md`.

## Rendering (harder)

### 9. Frustum culling for chunk meshes
**Files:** `simplex/renderer/opengl_renderer.py`.

### 10. Shader-based chunk material
**Files:** `simplex/renderer/`, `examples/mvp/demo_shader.glsl`.
