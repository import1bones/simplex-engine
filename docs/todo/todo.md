# simplex-engine TODO List

Last updated after OpenGL voxel backend merge (PR #1).

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
- [ ] Provide serialization/deserialization for ECS objects
- [ ] Separate 2D (ping-pong) and 3D (voxel) system profiles

## Renderer
- [x] Implement OpenGL renderer backend
- [x] Design scene graph and rendering pipeline (MVP)
- [x] Support basic primitives and materials
- [x] Add camera and viewport management (FPS camera)
- [x] Implement VBO upload and cleanup utilities (VBOManager)
- [x] Wire ECS MeshComponent entities into OpenGL render loop
- [ ] Shader-based rendering pipeline (replace fixed-function GL)
- [ ] Frustum culling and draw-call batching
- [ ] Add numpy for PyOpenGL fast path

## Voxel / Minecraft Project
- [x] Implement voxel block type system and palette
- [x] Implement Chunk storage and access APIs
- [x] Implement mesh generation (naive + greedy)
- [x] Implement ChunkManager for LRU caching and preload/unload APIs
- [x] First-person player controller (WASD + mouse look)
- [x] Minecraft-like demos (`run.py`, `run_player.py`)
- [ ] Player-driven chunk streaming (load/unload from player position)
- [ ] Cross-chunk face culling (fix border seams)
- [ ] Block place/break interaction
- [ ] Add async mesh generation worker and GPU upload scheduler
- [ ] Implement world generation and biome systems (noise terrain)

## Physics
- [x] Define physics component and system interfaces (MVP)
- [x] 2D AABB collision for ping-pong demo
- [ ] Voxel AABB collision (player stands on terrain)
- [ ] Integrate pybullet or custom 3D collision for physics simulation
- [ ] Add rigid body and soft body support

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
- [ ] Game mode selection (2D vs 3D) in config

## Testing & CI
- [x] Write unit tests for core interfaces (36 tests)
- [x] Add CI pipeline for tests and linters (GitHub Actions)
- [ ] Document testing guidelines in docs/development/testing.md

## Examples & Demos
- [x] Ping-pong example game
- [x] Minecraft-like voxel demos
- [ ] Provide demo scenes for video creators

---

This list reflects the current codebase. See [README](../../README.md) for quick-start commands.
