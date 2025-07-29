"""
Minimal Renderer implementation for MVP.
"""

from .interface import RendererInterface
from simplex.utils.logger import log


# --- MVP-2: Scene Graph and Advanced Rendering Scaffold ---
class SceneNode:
    def __init__(self, name, children=None, transform=None, primitive=None, material=None):
        self.name = name
        self.children = children if children else []
        self.transform = transform  # Placeholder for transformation matrix
        self.primitive = primitive  # e.g., 'cube', 'sphere', etc.
        self.material = material    # Placeholder for material properties

    def add_child(self, node):
        self.children.append(node)

    def traverse(self, action):
        action(self)
        for child in self.children:
            child.traverse(action)

class Renderer(RendererInterface):
    """
    Renderer system for simplex-engine MVP-2.
    Handles rendering, advanced primitives, materials, and scene graph.
    """
    def __init__(self):
        self.scene_root = SceneNode("root")

    def add_primitive(self, primitive, material=None, parent=None):
        node = SceneNode(primitive, material=material)
        if parent is None:
            self.scene_root.add_child(node)
        else:
            parent.add_child(node)
        log(f"Added primitive: {primitive} with material: {material}", level="INFO")
        return node

    def render(self) -> None:
        """
        Render the current scene graph.
        Handles errors gracefully and logs at INFO level.
        """
        try:
            def render_node(node):
                if node.primitive:
                    log(f"Rendering primitive: {node.primitive} with material: {node.material}", level="INFO")
            self.scene_root.traverse(render_node)
            log("Rendering scene with scene graph and camera.", level="INFO")
            # Future: integrate with puopengl or other graphics libraries
        except Exception as e:
            log(f"Renderer error: {e}", level="ERROR")
