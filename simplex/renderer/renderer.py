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
    Renderer system for simplex-engine with proper dependency injection.
    Handles rendering, advanced primitives, materials, and scene graph.
    """
    def __init__(self, event_system=None, resource_manager=None):
        from .material import Material, Shader
        
        self.event_system = event_system
        self.resource_manager = resource_manager
        self._initialized = False
        
        # Core rendering components
        self.scene_root = SceneNode("root")
        self.lights = []  # List of light sources
        self.post_effects = []  # List of post-processing effects
        self.materials = {}  # name -> Material
        self.shaders = {}   # name -> Shader
        
        # Rendering state
        self.config = {}
        self.backend = None
        
        log("Renderer created", level="INFO")
    
    def initialize(self, config=None):
        """Initialize renderer with configuration."""
        self.config = config or {}
        
        # Initialize rendering backend based on config
        backend_type = self.config.get("backend", "debug")
        
        if backend_type == "pygame":
            self._initialize_pygame_backend()
        elif backend_type == "opengl":
            self._initialize_opengl_backend()
        else:
            # Default debug backend
            self._initialize_debug_backend()
        
        self._initialized = True
        log(f"Renderer initialized with {backend_type} backend", level="INFO")
    
    def _initialize_pygame_backend(self):
        """Initialize pygame rendering backend."""
        try:
            import pygame
            pygame.init()
            
            width = self.config.get("width", 800)
            height = self.config.get("height", 600)
            
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption(self.config.get("title", "Simplex Engine"))
            
            self.backend = "pygame"
            log("Pygame backend initialized", level="INFO")
        except ImportError:
            log("Pygame not available, falling back to debug backend", level="WARNING")
            self._initialize_debug_backend()
    
    def _initialize_opengl_backend(self):
        """Initialize OpenGL rendering backend."""
        try:
            # Placeholder for OpenGL initialization
            log("OpenGL backend not yet implemented, using debug backend", level="WARNING")
            self._initialize_debug_backend()
        except ImportError:
            log("OpenGL not available, falling back to debug backend", level="WARNING")
            self._initialize_debug_backend()
    
    def _initialize_debug_backend(self):
        """Initialize debug rendering backend (console output)."""
        self.backend = "debug"
        log("Debug backend initialized", level="INFO")

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
        if not self._initialized:
            log("Renderer not initialized, skipping render", level="WARNING")
            return
            
        try:
            if self.backend == "pygame":
                self._render_pygame()
            elif self.backend == "opengl":
                self._render_opengl()
            else:
                self._render_debug()
                
        except Exception as e:
            log(f"Renderer error: {e}", level="ERROR")
            if self.event_system:
                self.event_system.emit('system_error', {'system': 'Renderer', 'error': str(e)})
    
    def _render_pygame(self):
        """Render using pygame backend."""
        import pygame
        
        # Clear screen
        self.screen.fill((0, 0, 0))  # Black background
        
        # Render scene graph
        def render_node(node, global_transform):
            if node.primitive and hasattr(node, 'position'):
                # Simple primitive rendering for pygame
                color = (255, 255, 255)  # White default
                if node.material and hasattr(node.material, 'color'):
                    color = node.material.color
                    
                # Draw primitive based on type
                if node.primitive == 'rectangle':
                    pygame.draw.rect(self.screen, color, 
                                   (node.position.x, node.position.y, node.width, node.height))
                elif node.primitive == 'circle':
                    pygame.draw.circle(self.screen, color, 
                                     (int(node.position.x), int(node.position.y)), node.radius)
        
        self.scene_root.traverse(render_node)
        
        # Update display
        pygame.display.flip()
        log("Pygame frame rendered", level="DEBUG")
    
    def _render_opengl(self):
        """Render using OpenGL backend."""
        # Placeholder for OpenGL rendering
        log("OpenGL rendering not implemented", level="DEBUG")
    
    def _render_debug(self):
        """Render using debug backend."""
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
    
    def shutdown(self):
        """Clean shutdown of renderer."""
        if self.backend == "pygame":
            try:
                import pygame
                pygame.quit()
            except:
                pass
        
        self._initialized = False
        log("Renderer shutdown", level="INFO")
