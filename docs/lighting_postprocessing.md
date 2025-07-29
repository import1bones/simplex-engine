# Lighting & Post-Processing Effects (MVP-3)

The Renderer now supports basic lighting and post-processing effect stubs.

## Features
- Built-in light types: Directional, Point, Ambient
- Add lights to the scene and apply them to primitives
- Post-processing effect pipeline (e.g., Grayscale, Blur stubs)

## Usage Example
```python
from simplex.renderer.renderer import Renderer, DirectionalLight, PointLight, AmbientLight, GrayscaleEffect, BlurEffect

renderer = Renderer()
renderer.add_light(DirectionalLight(direction=(1,0,0), color=(1,1,1), intensity=0.8))
renderer.add_light(PointLight(position=(0,1,0), color=(1,0,0), intensity=1.0))
renderer.add_light(AmbientLight(color=(0.2,0.2,0.2), intensity=0.5))

renderer.add_post_effect(GrayscaleEffect())
renderer.add_post_effect(BlurEffect())

renderer.render()
```

## Notes
- Lighting and post-processing are currently stubs for extensibility and demo purposes.
- Real engines would implement actual shading and framebuffer effects.
- See `simplex/renderer/renderer.py` for extensibility patterns.
