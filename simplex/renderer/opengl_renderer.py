"""
OpenGL renderer backend for simplex-engine.
Provides 3D rendering capabilities for voxel/world rendering (Minecraft-like).
"""

from simplex.renderer.interface import RendererInterface
from simplex.renderer.material import Material, Shader
from simplex.utils.logger import log

try:
    import OpenGL.GL as gl
    import OpenGL.GLU as glu
    import pygame
    from pygame.locals import DOUBLEBUF, OPENGL
except ImportError:
    gl = None
    glu = None
    pygame = None

try:
    from .gl_utils import create_vbo_for_mesh, delete_vbo
except Exception:
    create_vbo_for_mesh = None
    delete_vbo = None


class OpenGLRenderer(RendererInterface):
    def __init__(self, width=800, height=600, title="Simplex Engine - OpenGL Renderer"):
        self.width = width
        self.height = height
        self.title = title
        self.screen = None
        self.initialized = False
        self.scene_root = None
        self.materials = {}
        self.shaders = {}
        self.lights = []
        self.post_effects = []
        self.camera = None

    def initialize(self):
        if not gl or not pygame:
            log(
                "PyOpenGL or pygame not available, cannot initialize OpenGLRenderer",
                level="ERROR",
            )
            return False
        try:
            # Check if pygame is already initialized
            if not pygame.get_init():
                pygame.init()

            # Try to initialize OpenGL context
            # If display is already initialized, try to quit and reinitialize
            if pygame.display.get_init():
                pygame.display.quit()

            pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
            pygame.display.set_caption(self.title)
            gl.glEnable(gl.GL_DEPTH_TEST)
            gl.glClearColor(0.1, 0.1, 0.1, 1.0)
            self.initialized = True
            log("OpenGLRenderer initialized", level="INFO")
            return True
        except Exception as e:
            log(f"Failed to initialize OpenGL renderer: {e}", level="ERROR")
            self.initialized = False
            return False

    def set_scene_root(self, scene_root):
        self.scene_root = scene_root

    def register_shader(self, shader: Shader):
        self.shaders[shader.name] = shader
        log(f"Registered OpenGL shader: {shader}", level="INFO")

    def register_material(self, material: Material):
        self.materials[material.name] = material
        log(f"Registered OpenGL material: {material}", level="INFO")

    def add_light(self, light):
        self.lights.append(light)
        log(f"Added OpenGL light: {light}", level="INFO")

    def add_post_effect(self, effect):
        self.post_effects.append(effect)
        log(f"Added OpenGL post-processing effect: {effect}", level="INFO")

    def set_camera(self, camera):
        self.camera = camera

    def render(self):
        if not self.initialized:
            log("OpenGLRenderer not initialized, skipping render", level="WARNING")
            return
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # --- Camera/projection setup (simple perspective) ---
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = self.width / self.height if self.height != 0 else 1
        glu.gluPerspective(70, aspect, 0.1, 1000.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        # Simple camera: move back to see the scene
        if self.camera and hasattr(self.camera, "position"):
            pos = self.camera.position
            glu.gluLookAt(pos[0], pos[1], pos[2], 0, 0, 0, 0, 1, 0)
        else:
            glu.gluLookAt(5, 5, 10, 0, 0, 0, 0, 1, 0)  # Better default view

        # --- Scene traversal and rendering ---
        if self.scene_root:
            self._traverse_and_render(self.scene_root)
        else:
            # Render a default test cube if no scene
            self._render_default_test_content()

        pygame.display.flip()
        # Remove debug log to avoid spam
        # log("OpenGL frame rendered", level="DEBUG")

    def _render_default_test_content(self):
        """Render some default content when no scene is set."""
        # Draw a simple rotating cube at origin
        gl.glPushMatrix()
        gl.glColor3f(0.8, 0.4, 0.2)  # Orange color

        # Simple rotation based on time
        import time

        rotation = (time.time() * 50) % 360
        gl.glRotatef(rotation, 1, 1, 0)

        self._draw_unit_cube()
        gl.glPopMatrix()

    def _traverse_and_render(self, node, parent_transform=None):
        # Draw mesh component if present
        if hasattr(node, "components"):
            mesh_comp = (
                node.get_component("mesh") if hasattr(node, "get_component") else None
            )
            if mesh_comp and getattr(mesh_comp, "vertices", None):
                # If GPU handle not present, attempt upload now (context guaranteed here)
                if getattr(mesh_comp, "gpu", None) is None and create_vbo_for_mesh:
                    try:
                        mesh_comp.gpu = create_vbo_for_mesh(mesh_comp.vertices, mesh_comp.colors)
                        log(f"OpenGLRenderer: Uploaded mesh to GPU (count={mesh_comp.gpu.get('count')})", level="DEBUG")
                    except Exception as e:
                        log(f"OpenGLRenderer: GPU upload failed: {e}", level="DEBUG")
                self._draw_mesh(mesh_comp)

        # For now, ignore transforms and just draw cubes for primitives named 'cube' or 'voxel'
        if hasattr(node, "primitive") and node.primitive in ("cube", "voxel"):
            self._draw_cube(node)
        if hasattr(node, "children"):
            for child in node.children:
                self._traverse_and_render(child)

    def _draw_mesh(self, mesh_comp):
        """Immediate-mode fallback to draw meshes stored in MeshComponent.

        Honors mesh_comp.origin to place chunk meshes in world space.
        If VBOs are available, upload once and draw using VBOs.
        """
        verts = mesh_comp.vertices or []
        cols = mesh_comp.colors or []
        if not verts:
            return

        # If a GPU handle exists, draw using VBOs
        if getattr(mesh_comp, "gpu", None) and gl and create_vbo_for_mesh:
            handle = mesh_comp.gpu
            gl.glPushMatrix()
            if getattr(mesh_comp, "origin", None):
                ox, oy, oz = mesh_comp.origin
                gl.glTranslatef(ox, oy, oz)
            # Bind vertex VBO
            gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
            gl.glEnableClientState(gl.GL_COLOR_ARRAY)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, handle["vbo"])
            gl.glVertexPointer(3, gl.GL_FLOAT, 0, None)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, handle["vbo_color"])
            gl.glColorPointer(4, gl.GL_FLOAT, 0, None)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, handle["count"])
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
            gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
            gl.glDisableClientState(gl.GL_COLOR_ARRAY)
            gl.glPopMatrix()
            return

        # Otherwise fallback to immediate-mode draw
        gl.glPushMatrix()
        # Apply mesh world origin translation
        if getattr(mesh_comp, "origin", None):
            ox, oy, oz = mesh_comp.origin
            gl.glTranslatef(ox, oy, oz)
        gl.glBegin(gl.GL_TRIANGLES)
        vcount = len(verts) // 3
        for i in range(vcount):
            r, g, b, a = (1.0, 1.0, 1.0, 1.0)
            if len(cols) >= (i + 1) * 4:
                r = cols[i * 4 + 0]
                g = cols[i * 4 + 1]
                b = cols[i * 4 + 2]
                a = cols[i * 4 + 3]
            gl.glColor4f(r, g, b, a)
            gl.glVertex3f(verts[i * 3 + 0], verts[i * 3 + 1], verts[i * 3 + 2])
        gl.glEnd()
        gl.glPopMatrix()

    def _draw_cube(self, node):
        # Draw a simple colored cube at node.position (default at origin)
        pos = getattr(node, "position", (0, 0, 0))
        size = getattr(node, "size", 1)
        color = (1.0, 1.0, 1.0)
        if (
            hasattr(node, "material")
            and node.material
            and hasattr(node.material, "properties")
        ):
            color = node.material.properties.get("color", color)
        gl.glPushMatrix()
        gl.glTranslatef(pos[0], pos[1], pos[2])
        gl.glScalef(size, size, size)
        gl.glColor3f(*color)
        self._draw_unit_cube()
        gl.glPopMatrix()

    def _draw_unit_cube(self):
        """Draw a unit cube centered at origin."""
        gl.glBegin(gl.GL_QUADS)
        # Front face
        gl.glVertex3f(-0.5, -0.5, 0.5)
        gl.glVertex3f(0.5, -0.5, 0.5)
        gl.glVertex3f(0.5, 0.5, 0.5)
        gl.glVertex3f(-0.5, 0.5, 0.5)
        # Back face
        gl.glVertex3f(-0.5, -0.5, -0.5)
        gl.glVertex3f(-0.5, 0.5, -0.5)
        gl.glVertex3f(0.5, 0.5, -0.5)
        gl.glVertex3f(0.5, -0.5, -0.5)
        # Left face
        gl.glVertex3f(-0.5, -0.5, -0.5)
        gl.glVertex3f(-0.5, -0.5, 0.5)
        gl.glVertex3f(-0.5, 0.5, 0.5)
        gl.glVertex3f(-0.5, 0.5, -0.5)
        # Right face
        gl.glVertex3f(0.5, -0.5, -0.5)
        gl.glVertex3f(0.5, 0.5, -0.5)
        gl.glVertex3f(0.5, 0.5, 0.5)
        gl.glVertex3f(0.5, -0.5, 0.5)
        # Top face
        gl.glVertex3f(-0.5, 0.5, -0.5)
        gl.glVertex3f(-0.5, 0.5, 0.5)
        gl.glVertex3f(0.5, 0.5, 0.5)
        gl.glVertex3f(0.5, 0.5, -0.5)
        # Bottom face
        gl.glVertex3f(-0.5, -0.5, -0.5)
        gl.glVertex3f(0.5, -0.5, -0.5)
        gl.glVertex3f(0.5, -0.5, 0.5)
        gl.glVertex3f(-0.5, -0.5, 0.5)
        gl.glEnd()

    def shutdown(self):
        # Clean up VBOs created via gl_utils
        try:
            if 'delete_all_vbos' in globals():
                from .gl_utils import delete_all_vbos
                delete_all_vbos()
        except Exception:
            pass
        if pygame:
            pygame.quit()
        self.initialized = False
        log("OpenGLRenderer shutdown", level="INFO")
