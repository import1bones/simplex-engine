# Scene Graph: Hierarchical Transforms & Instancing (MVP-3)

The scene graph now supports hierarchical transforms and instancing for efficient rendering.

## Features
- Each `SceneNode` can have a local transform and parent/child relationships.
- Global transforms are calculated by traversing the hierarchy (stub: placeholder for matrix math).
- Instancing: render multiple instances of a primitive efficiently by setting `instance_count`.

## Usage Example
```python
from simplex.renderer.renderer import Renderer

renderer = Renderer()

# Add a parent node with a transform
parent = renderer.add_primitive('cube', transform=(0,0,0), instance_count=1)
# Add a child node with its own transform
child = renderer.add_primitive('sphere', parent=parent, transform=(1,0,0), instance_count=5)

renderer.render()
```

## Notes
- Real engines would use 4x4 matrices for transforms and multiply them for global transforms.
- Instancing is logged and ready for efficient rendering backends.
- See `simplex/renderer/renderer.py` for extensibility patterns.
