## Input System
- [ ] Design abstract Input system API
- [ ] Implement pygame backend for input
- [ ] Support polling and state retrieval for keyboard, mouse, and gamepad
- [ ] Integrate input events with ECS and game logic
- [ ] Document API for future backend replacement
# simplex-engine TODO List

## Core Architecture
- [ ] Implement ECS core (Entity, Component, System management)
- [ ] Create base classes for Entity, Component, System
- [ ] Integrate flexible event system for ECS
- [ ] Provide serialization/deserialization for ECS objects

## Renderer
- [ ] Implement Renderer using puopengl
- [ ] Design scene graph and rendering pipeline
- [ ] Support basic primitives and materials
- [ ] Add camera and viewport management

## Physics
- [ ] Integrate pybullet for physics simulation
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

## Flexibility & Maintainability
- [ ] Ensure modular design for all subsystems
- [ ] Write unit tests for core interfaces
- [ ] Document public APIs and architecture

## Example & Demo
- [ ] Create example game project
- [ ] Provide demo scenes for video creators

---
This list is based on the current architecture and features. Update as development progresses.
