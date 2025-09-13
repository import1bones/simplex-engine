# simplex-engine TODO List

## Input System
- [ ] Design abstract input system API
- [ ] Implement pygame backend for input
- [ ] Support polling and state retrieval for keyboard, mouse, and gamepad
- [ ] Integrate input events with ECS and game logic
- [ ] Document API for future backend replacement

## Core Architecture
- [ ] Implement ECS core (Entity, Component, System management)
- [ ] Create base classes for Entity, Component, System
- [ ] Integrate flexible event system for ECS
- [ ] Provide serialization/deserialization for ECS objects

## Renderer
- [ ] Implement OpenGL renderer backend
- [ ] Design scene graph and rendering pipeline
- [ ] Support basic primitives and materials
- [ ] Add camera and viewport management
- [ ] Implement VBO/VAO upload and cleanup utilities

## Voxel / Minecraft Project
- [ ] Implement voxel block type system and palette
- [ ] Implement Chunk storage and access APIs
- [ ] Implement mesh generation (naive + greedy)
- [ ] Implement ChunkManager for streaming and LRU caching
- [ ] Add async mesh generation worker and GPU upload scheduler
- [ ] Implement world generation and biome systems

## Physics
- [ ] Integrate pybullet or custom AABB collision for physics simulation
- [ ] Define physics component and system interfaces
- [ ] Support collision detection and response
- [ ] Add rigid body and soft body support

## Scripting
- [ ] Implement ScriptManager for Python scripting
- [ ] Support hot-reloading of scripts
- [ ] Provide API for game logic and event hooks

## Resource Manager
- [ ] Implement ResourceManager for asset loading/unloading
- [ ] Support various resource types (textures, models, audio, scripts)
- [ ] Add resource caching and reference counting

## Audio
- [ ] Implement Audio system interface
- [ ] Support playback, stop, and audio resource management
- [ ] Integrate with resource manager for audio assets

## Engine Core
- [ ] Implement Engine main loop
- [ ] Design configuration and resource management
- [ ] Add logging and debugging utilities

## Testing & CI
- [ ] Write unit tests for core interfaces
- [ ] Add CI pipeline for tests and linters
- [ ] Document testing guidelines in docs/development/testing.md

## Examples & Demos
- [ ] Create example game project
- [ ] Provide demo scenes for video creators

---

This list is based on the current architecture and features. Update as development progresses.
