# MVP (Minimum Viable Product) Task List for simplex-engine

## MVP Definition
The MVP for simplex-engine is the minimal set of features required to build and run a simple interactive game scene, demonstrating the engine's core capabilities and extensibility.

## Sorted MVP Task List

### 1. Core Engine Loop
- [x] Implement Engine main loop
- [x] Centralize and extend configuration management (document usage)
- [x] Integrate unified event system for subsystem communication (support extensibility)
### 2. ECS (Entity-Component-System)
- [x] Implement ECS core (Entity, Component, System management)

### 3. Input System
- [x] Design abstract Input system API
- [x] Implement pygame backend for input
- [x] Support polling and state retrieval for keyboard, mouse, and gamepad
- [x] Integrate input events with ECS and game logic
- [x] Document API for future backend replacement

### 4. Renderer
- [x] Add camera and viewport management

### 4. Physics
- [x] Integrate pybullet for physics simulation

// ...existing code...
### 6. Resource Manager
- [x] Implement ResourceManager for asset loading (textures, models)
- [x] Plan and implement robust error handling for resource management and event flows

## MVP Analysis

The minimal set of MVP features includes:
- Engine main loop
- ECS core (Entity, Component, System)
- Input System (abstract API, pygame backend)
- Renderer (basic primitives, camera)
- Physics (basic simulation)
- ScriptManager (game logic API)
- ResourceManager (basic asset loading)
- Unified event system for subsystem communication (extensible)
- Centralized configuration management (documented)
- Robust error handling in resource, input, and event systems
- Example projects and demo scenes for validation and onboarding

Audio and advanced features (hot-reloading, advanced materials, demo scenes) are not required for the MVP but can be added after the core is functional.

## MVP UML Design

```mermaid
classDiagram
    class Engine {
        +ECS ecs
        +Renderer renderer
        +Physics physics
        +ScriptManager scriptManager
        +ResourceManager resourceManager
        +run()
    }
    class ECS {
        +Entity[] entities
        +System[] systems
        +addEntity()
        +addSystem()
    Engine --> Input
    }
    class Renderer {
        +render()
    }
    class Physics {
        +simulate()
    }
    class ScriptManager {
        +execute()
    }
    class ResourceManager {
        +load()
    }
    Engine --> ECS
    Engine --> Renderer
    Engine --> Physics
    Engine --> ScriptManager
    Engine --> ResourceManager
    ECS --> Entity
    ECS --> System
```

---
This MVP list and design focus on delivering a functional, extensible engine foundation. Update as development progresses.
