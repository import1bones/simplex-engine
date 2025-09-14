# Minecraft-like demo (examples/minecraft-like)

Minimal example that demonstrates spawning a chunk and rendering it with the engine’s OpenGL backend.

How to run:

```
PYTHONPATH=. python3 examples/minecraft-like/run.py
```

What it does:
- Creates an Engine instance
- Attaches a simple camera
- Spawns a chunk entity using `Engine.spawn_chunk`
- Runs a short update loop so chunk systems generate meshes and the renderer can draw

Notes:
- Requires PyOpenGL and pygame for OpenGL rendering. If those are missing the renderer falls back to debug backend.
- This demo is intentionally small; it’s a starting point for the Minecraft-like workflow. After you confirm, I will implement additional features (chunk streaming, greedy meshing improvements, player/camera controls).
