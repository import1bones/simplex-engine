"""
Minimal Renderer implementation for MVP.
"""

from .interface import RendererInterface
from simplex.utils.logger import log


# --- MVP-2: Scene Graph and Advanced Rendering Scaffold ---
class SceneNode:
    def __init__(self, name, children=None, transform=None, primitive=None, material=None, parent=None, instance_count=1):
        self.name = name
        self.children = children if children else []
        self.transform = transform  # Local transform (e.g., 4x4 matrix or tuple)
        self.primitive = primitive  # e.g., 'cube', 'sphere', etc.
        self.material = material    # Placeholder for material properties
        self.parent = parent
        self.instance_count = instance_count  # For instancing repeated objects

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def traverse(self, action, parent_transform=None):
        # Calculate global transform (stub: just pass local for now)
        global_transform = self.get_global_transform(parent_transform)
        action(self, global_transform)
        for child in self.children:
            child.traverse(action, global_transform)

    def get_global_transform(self, parent_transform=None):
        # Stub: combine parent and local transform (real engine would multiply matrices)
        if parent_transform is None:
            return self.transform
        # Placeholder: just return local for now
        return self.transform

class DirectionalLight:
    def __init__(self, direction, color=(1,1,1), intensity=1.0):
        self.type = 'directional'
        self.direction = direction
        self.color = color
        self.intensity = intensity
    def __repr__(self):
        return f"<DirectionalLight dir={self.direction} color={self.color} intensity={self.intensity}>"

class PointLight:
    def __init__(self, position, color=(1,1,1), intensity=1.0):
        self.type = 'point'
        self.position = position
        self.color = color
        self.intensity = intensity
    def __repr__(self):
        return f"<PointLight pos={self.position} color={self.color} intensity={self.intensity}>"

class AmbientLight:
    def __init__(self, color=(1,1,1), intensity=1.0):
        self.type = 'ambient'
        self.color = color
        self.intensity = intensity
    def __repr__(self):
        return f"<AmbientLight color={self.color} intensity={self.intensity}>"

class GrayscaleEffect:
    def __repr__(self):
        return "<GrayscaleEffect>"

class BlurEffect:
    def __repr__(self):
        return "<BlurEffect>"

class Renderer(RendererInterface):
    """
    Renderer system for simplex-engine MVP-2.
    Handles rendering, advanced primitives, materials, and scene graph.
    """
    def __init__(self):
        from .material import Material, Shader
        self.scene_root = SceneNode("root")
        self.lights = []  # List of light sources
        self.post_effects = []  # List of post-processing effects
        self.materials = {}  # name -> Material
        self.shaders = {}   # name -> Shader

    def register_shader(self, shader):
        self.shaders[shader.name] = shader
        log(f"Registered shader: {shader}", level="INFO")

    def register_material(self, material):
        self.materials[material.name] = material
        log(f"Registered material: {material}", level="INFO")

    def add_light(self, light):
        self.lights.append(light)
        log(f"Added light: {light}", level="INFO")

    def add_post_effect(self, effect):
        self.post_effects.append(effect)
        log(f"Added post-processing effect: {effect}", level="INFO")

    def add_primitive(self, primitive, material=None, parent=None, transform=None, instance_count=1):
        # Allow material to be a name or Material object
        mat_obj = material
        if isinstance(material, str):
            mat_obj = self.materials.get(material)
        node = SceneNode(name=primitive, primitive=primitive, material=mat_obj, transform=transform, instance_count=instance_count)
        if parent is None:
            self.scene_root.add_child(node)
        else:
            parent.add_child(node)
        log(f"Added primitive: {primitive} with material: {mat_obj} (instances: {instance_count})", level="INFO")
        return node

    def render(self) -> None:
        """
        Render the current scene graph with lighting and post-processing effects.
        Handles errors gracefully and logs at INFO level.
        """
        try:
            def render_node(node, global_transform):
                if node.primitive:
                    log(f"Rendering primitive: {node.primitive} with material: {node.material} (instances: {node.instance_count}) transform: {global_transform}", level="INFO")
                    # Lighting: apply all lights to primitive (stub)
                    for light in self.lights:
                        if getattr(light, 'type', None) == 'directional':
                            log(f"Applying directional light {light.direction} to {node.primitive}", level="DEBUG")
                        elif getattr(light, 'type', None) == 'point':
                            log(f"Applying point light {light.position} to {node.primitive}", level="DEBUG")
                        elif getattr(light, 'type', None) == 'ambient':
                            log(f"Applying ambient light to {node.primitive}", level="DEBUG")
            self.scene_root.traverse(render_node)
            log("Rendering scene with scene graph and camera.", level="INFO")
            # Post-processing: apply all post effects (stub)
            for effect in self.post_effects:
                log(f"Applying post-processing effect: {effect}", level="INFO")
            # Future: integrate with pyopengl or other graphics libraries
        except Exception as e:
            log(f"Renderer error: {e}", level="ERROR")
