# API Reference (MVP-3)

This document provides a high-level API overview for the main subsystems of simplex-engine. For detailed usage, see code docstrings and subsystem markdown docs.

## Engine
- `Engine()`
- `Engine.run()`
- `Engine.events`: EventSystem instance
- `Engine.physics`: Physics instance
- `Engine.renderer`: Renderer instance
- `Engine.resource_manager`: ResourceManager instance
- `Engine.input`: Input instance
- `Engine.script_manager`: ScriptManager instance

## ECS
- `ECS.add_entity(entity)`
- `ECS.add_system(system)`
- `ECS.get_entities_with(component_type)`

## Renderer
- `Renderer.add_primitive(name, material=None, ...)`
- `Renderer.register_material(material)`
- `Renderer.render()`

## Physics
- `Physics.add_rigid_body(body)`
- `Physics.simulate()`
- `Physics.on_event(event_type, handler)`

## ResourceManager
- `ResourceManager.load(resource_type, name)`
- `ResourceManager.unload(name)`
- `ResourceManager.hot_reload(name)`
- `ResourceManager.get_usage_analytics()`

## Input
- `Input.poll()`
- `Input.on_event(event_type, handler)`

## EventSystem
- `EventSystem.register(event_type, handler, priority=0)`
- `EventSystem.emit(event_type, data)`
- `EventSystem.set_priority(event_type, priority)`

## ScriptManager
- `ScriptManager.load_script(path)`
- `ScriptManager.reload_script(name)`
- `ScriptManager.register_plugin(plugin)`
- `ScriptManager.open_cli_editor()`

---
For advanced usage, see subsystem markdown docs and code docstrings.
