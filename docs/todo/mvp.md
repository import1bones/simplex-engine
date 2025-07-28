# MVP (Minimum Viable Product) Task List for simplex-engine

## MVP Definition
The MVP for simplex-engine is the minimal set of features required to build and run a simple interactive game scene, demonstrating the engine's core capabilities and extensibility.

## Sorted MVP Task List

### 1. Core Engine Loop
- [ ] Implement Engine main loop
### 2. ECS (Entity-Component-System)
- [ ] Implement ECS core (Entity, Component, System management)

### 3. Input System
- [ ] Design abstract Input system API
- [ ] Implement pygame backend for input
- [ ] Support polling and state retrieval for keyboard, mouse, and gamepad
- [ ] Integrate input events with ECS and game logic
- [ ] Document API for future backend replacement

### 4. Renderer
- [ ] Add camera and viewport management

### 4. Physics
- [ ] Integrate pybullet for physics simulation

- Input System (abstract API, pygame backend)
### 6. Resource Manager
- [ ] Implement ResourceManager for asset loading (textures, models)

## MVP Analysis

The minimal set of MVP features includes:
- Engine main loop
        +Input input
- ECS core (Entity, Component, System)
- Renderer (basic primitives, camera)
- Physics (basic simulation)
- ScriptManager (game logic API)
- ResourceManager (basic asset loading)

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
