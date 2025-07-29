# MVP-3 (Sprint 3 / Extensibility & Advanced Features): TODO List for simplex-engine

## MVP-3: Completed

- [x] ScriptManager plugin/event system (observable, extensible)
- [x] Script hot-reloading and plugin demo (see plugin_example.py)
- [x] Integrate in-engine script editor (CLI-based, flexible interface; complete and tested)
- [x] Support additional resource types (shaders; demo shader hot-reloadable; extensible for more)
- [x] Implement resource hot-reloading for assets (shaders, scripts; demo complete)
- [x] Prototype plugin system for user-defined subsystems (script/event plugins, resource hot-reloader)
- [x] Refactor for improved modularity and testability (logging, event hooks, plugin registration)
- [x] Document advanced scripting patterns and event hooks (see code and plugin_example.py)
- [x] All MVP-3 features implemented, tested, and demoed (resource hot-reload, plugin/event system, CLI script editor)
- [x] Documentation and developer workflow updated
- [x] Ready for feedback, onboarding, and next sprint planning

## MVP-3: In Progress / Open

### Scripting & Tooling
- [x] Add script debugging and error reporting (tracebacks and recent errors now logged and accessible)

### Advanced Resource Management
- [x] Add resource usage analytics and error reporting (see docs/resource_analytics.md)

### Input & Event System
- [x] Add support for gamepad and touch input (see docs/input_touch_gamepad.md)
- [x] Implement event priorities and propagation (bubbling/capturing) (see docs/event_priorities_propagation.md)
- [x] Document event system extensibility and advanced usage (see docs/event_system_advanced.md)

### Engine Core & Flexibility
- [x] Add configuration hot-reloading (live config changes) (see docs/config_hot_reload.md)

### Renderer Enhancements
- [x] Add support for lighting and basic post-processing effects (see docs/lighting_postprocessing.md)
- [x] Implement material/shader system with user extensibility (see docs/material_shader_system.md)
- [x] Expand scene graph for hierarchical transforms and instancing (see docs/scene_graph_hierarchical_instancing.md)

### Physics System Expansion
- [x] Integrate advanced physics features (rigid body, soft body, collision response) (see docs/advanced_physics_features.md)
- [x] Expose physics events to ECS and scripting (see docs/physics_events_ecs_scripting.md)
- [x] Add physics-based demo scene and documentation (see docs/physics_demo_scene.md)

### Testing & Documentation
- [x] Expand integration and edge-case tests for all subsystems (see docs/testing_guide.md)
- [x] Update and expand onboarding, architecture, and API docs (see docs/onboarding_architecture.md, docs/architecture.md, docs/api_reference.md)
- [x] Provide advanced example projects and usage guides (see docs/full_integration_demo.md, docs/advanced_example_platformer.md)

---
Sprint 3 TODOs focus on extensibility, advanced features, and developer experience, preparing the engine for real-world projects and community contributions.

---
**Next Steps:**
- Prioritize physics and resource hot-reloading
- Expand renderer and scripting capabilities
- Continue improving modularity, documentation, and onboarding
- Gather feedback from early users and iterate on extensibility features
