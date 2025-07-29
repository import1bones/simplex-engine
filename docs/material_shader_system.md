# Material & Shader System (MVP-3)

The Renderer now supports a material/shader system with user extensibility.

## Features
- Register custom shaders and materials at runtime.
- Assign materials (by name or object) to primitives in the scene graph.
- Materials reference shaders and can have custom properties.

## Usage Example
```python
from simplex.renderer.renderer import Renderer
from simplex.renderer.material import Shader, Material

renderer = Renderer()

# Register a custom shader and material
my_shader = Shader('basic', source='void main() { ... }')
my_material = Material('red', shader=my_shader, properties={'color': (1,0,0)})
renderer.register_shader(my_shader)
renderer.register_material(my_material)

# Add a primitive with the custom material
renderer.add_primitive('cube', material='red')
renderer.render()
```

## Notes
- Materials can be referenced by name or passed as objects.
- Shaders are extensible and can be loaded from source files.
- See `simplex/renderer/material.py` for extensibility patterns.
