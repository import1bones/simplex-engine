# Minecraft-like demo (examples/minecraft-like)

Voxel world demos using the engine's OpenGL backend, chunk manager, and ECS mesh pipeline.

## Run

```bash
# Basic demo: spawn one chunk, render 5 frames
uv run python3 examples/minecraft-like/run.py

# Interactive demo: player + 3×3 chunk grid, first-person controls
uv run python3 examples/minecraft-like/run_player.py
```

## Controls (`run_player.py`)

- **WASD** — move relative to camera yaw
- **Mouse** — look around (captured by default)
- **Space** — move up
- **ESC** — toggle mouse capture
- **Ctrl+C** — quit

## What it does

- Creates an `Engine` with OpenGL renderer (see `examples/config.toml`)
- Spawns chunk entities via `Engine.spawn_chunk` / `ChunkManager`
- `ChunkMeshSystem` generates greedy meshes; `OpenGLRenderer` draws ECS `MeshComponent` entities
- `run_player.py` adds a first-person controller and interactive loop

## Requirements

- Python 3.13+, pygame, PyOpenGL
- Display server (X11 or XWayland). On Wayland, `run_player.py` auto-relaunches with `SDL_VIDEODRIVER=x11`.

## Known limitations (MVP)

- Fixed 3×3 chunk area (no player-driven streaming yet)
- Low FPS on immediate-mode GL fallback
- No voxel collision (player can move through terrain)
