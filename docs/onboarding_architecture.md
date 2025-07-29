# Onboarding & Architecture Guide (MVP-3)

Welcome to simplex-engine! This guide will help you get started, understand the architecture, and extend the engine.

## Getting Started
- Install dependencies: see `pyproject.toml`
- Run a demo: `python examples/physics_demo.py`
- Explore subsystems: see `simplex/` modules

## Architecture Overview
- **Engine**: Orchestrates all subsystems
- **ECS**: Entity-Component-System for game logic
- **Renderer**: Scene graph, materials, lighting, post-processing
- **Physics**: Rigid/soft bodies, collision events
- **ResourceManager**: Asset loading, hot-reloading, analytics
- **Input**: Keyboard, gamepad, touch
- **EventSystem**: Priorities, bubbling/capturing, extensibility
- **ScriptManager**: Plugins, hot-reloading, CLI editor

## Extending the Engine
- Add new subsystems as plugins
- Register custom events, resources, or input backends
- Use the CLI script editor for rapid prototyping

## Docs & Examples
- See `docs/` for advanced usage and subsystem guides
- See `examples/` for demo scenes and integration patterns

---
For API details, see code docstrings and subsystem markdown docs.
