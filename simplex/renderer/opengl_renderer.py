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
import math

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
        # Capture mouse by default for first-person controls
        self.capture_mouse = True
        self._mouse_grabbed = False

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
            # Enable relative mouse capture by default to support FPS-style controls
            try:
                if self.capture_mouse:
                    pygame.event.set_grab(True)
                    pygame.mouse.set_visible(False)
                    # center mouse
                    try:
                        pygame.mouse.set_pos((self.width // 2, self.height // 2))
                    except Exception:
                        pass
                    self._mouse_grabbed = True
            except Exception:
                pass
            gl.glEnable(gl.GL_DEPTH_TEST)
            gl.glClearColor(0.1, 0.1, 0.1, 1.0)
            self.initialized = True
            log("OpenGLRenderer initialized", level="INFO")

            # If engine provided vbo_manager, attach here and process pending uploads
            try:
                if hasattr(self, 'engine') and getattr(self.engine, 'vbo_manager', None):
                    try:
                        self.vbo_manager = self.engine.vbo_manager
                    except Exception:
                        pass
                # Process any pending uploads queued on the engine
                if hasattr(self, 'engine') and hasattr(self.engine, '_process_pending_mesh_uploads'):
                    try:
                        self.engine._process_pending_mesh_uploads()
                    except Exception:
                        pass

                # Additionally, register to engine events to handle mesh_generated directly
                try:
                    if hasattr(self, 'engine') and getattr(self.engine, 'events', None):
                        try:
                            # Ensure idempotent registration: unregister any existing listener first
                            try:
                                self.engine.events.unregister('mesh_generated', self._on_mesh_generated)
                            except Exception:
                                pass
                            # Register a renderer-side listener for lower-latency VBO uploads
                            self.engine.events.register('mesh_generated', self._on_mesh_generated)
                            # Track that we've registered so shutdown can unregister
                            try:
                                self._registered_mesh_listener = True
                            except Exception:
                                pass
                        except Exception:
                            pass
                except Exception:
                    pass
            except Exception:
                pass

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

    def _reset_modelview_stack(self):
        """Pop leaked matrices from prior frames (glLoadIdentity does not shrink the stack)."""
        if not gl:
            return
        gl.glMatrixMode(gl.GL_MODELVIEW)
        try:
            while gl.glGetIntegerv(gl.GL_MODELVIEW_STACK_DEPTH) > 1:
                gl.glPopMatrix()
        except Exception:
            pass

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
        self._reset_modelview_stack()
        gl.glLoadIdentity()
        # Use oriented camera (yaw/pitch) when available; fall back to simple lookAt
        # Simple camera: move back to see the scene
        if self.camera and hasattr(self.camera, "position"):
            pos = self.camera.position
            # camera may expose yaw/pitch in degrees
            yaw = getattr(self.camera, 'yaw', 0.0)
            pitch = getattr(self.camera, 'pitch', 0.0)
            try:
                yaw_rad = math.radians(yaw)
                pitch_rad = math.radians(pitch)
                # forward vector from spherical coordinates (yaw around Y, pitch around X)
                fx = math.cos(pitch_rad) * math.sin(yaw_rad)
                fy = math.sin(pitch_rad)
                fz = math.cos(pitch_rad) * math.cos(yaw_rad)
                look_dist = 100.0
                tx = pos[0] + fx * look_dist
                ty = pos[1] + fy * look_dist
                tz = pos[2] + fz * look_dist
                glu.gluLookAt(pos[0], pos[1], pos[2], tx, ty, tz, 0, 1, 0)
            except Exception:
                # fallback: look towards -Z
                glu.gluLookAt(pos[0], pos[1], pos[2], pos[0], pos[1], pos[2] - 1, 0, 1, 0)
        else:
            glu.gluLookAt(5, 5, 10, 0, 0, 0, 0, 1, 0)  # Better default view

        # --- Scene traversal and rendering ---
        rendered_any = False
        if self.scene_root and getattr(self.scene_root, "children", None):
            self._traverse_and_render(self.scene_root)
            rendered_any = True
        if self._render_ecs_meshes():
            rendered_any = True
        if not rendered_any:
            self._render_default_test_content()

        pygame.display.flip()
        # Remove debug log to avoid spam
        # log("OpenGL frame rendered", level="DEBUG")

    def _poll_input_events(self):
        """Poll pygame events and forward to the engine event system.

        Called from Engine.update() before ECS so input is available the same frame.
        Returns False when the window was closed.
        """
        try:
            if not pygame:
                return True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.initialized = False
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    try:
                        if getattr(self, '_mouse_grabbed', False):
                            pygame.event.set_grab(False)
                            pygame.mouse.set_visible(True)
                            self._mouse_grabbed = False
                        else:
                            pygame.event.set_grab(True)
                            pygame.mouse.set_visible(False)
                            try:
                                pygame.mouse.set_pos((self.width // 2, self.height // 2))
                            except Exception:
                                pass
                            self._mouse_grabbed = True
                        if hasattr(self, 'engine') and getattr(self.engine, 'events', None):
                            try:
                                self.engine.events.emit(
                                    'mouse_capture_toggled',
                                    {'captured': self._mouse_grabbed},
                                )
                            except Exception:
                                pass
                    except Exception:
                        pass
                    continue
                if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    if hasattr(self, 'engine') and getattr(self.engine, 'events', None):
                        if event.key in [pygame.K_UP, pygame.K_w]:
                            game_key = 'UP'
                        elif event.key in [pygame.K_DOWN, pygame.K_s]:
                            game_key = 'DOWN'
                        elif event.key in [pygame.K_LEFT, pygame.K_a]:
                            game_key = 'LEFT'
                        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                            game_key = 'RIGHT'
                        elif event.key == pygame.K_SPACE:
                            game_key = 'SPACE'
                        else:
                            game_key = None
                        if game_key is not None:
                            evt = type('Event', (), {})()
                            evt.type = 'KEYDOWN' if event.type == pygame.KEYDOWN else 'KEYUP'
                            evt.key = game_key
                            try:
                                self.engine.events.emit('input', evt)
                            except Exception:
                                pass
                if event.type == pygame.MOUSEMOTION:
                    if hasattr(self, 'engine') and getattr(self.engine, 'events', None):
                        mevt = {'type': 'MOUSEMOTION', 'rel': event.rel, 'pos': event.pos}
                        try:
                            self.engine.events.emit('mouse', mevt)
                        except Exception:
                            pass
        except Exception:
            pass
        return True

    def _get_vbo_manager(self):
        if getattr(self, 'vbo_manager', None) is not None:
            return self.vbo_manager
        if hasattr(self, 'engine') and getattr(self.engine, 'vbo_manager', None):
            return self.engine.vbo_manager
        return None

    def _get_vbo_helpers(self):
        if hasattr(self, 'engine') and getattr(self.engine, 'vbo_helpers', None):
            return self.engine.vbo_helpers
        if create_vbo_for_mesh and delete_vbo:
            return {'create_vbo_for_mesh': create_vbo_for_mesh, 'delete_vbo': delete_vbo}
        return None

    def _ensure_mesh_gpu(self, mesh_comp):
        """Upload mesh data to GPU when a VBO manager or helpers are available."""
        if getattr(mesh_comp, 'gpu', None) is not None:
            return

        vm = self._get_vbo_manager()
        if vm:
            try:
                mesh_comp.gpu = vm.create_vbo(mesh_comp.vertices, mesh_comp.colors)
                log(
                    f"OpenGLRenderer: Uploaded mesh to GPU (count={mesh_comp.gpu.get('count') if mesh_comp.gpu else 'N/A'})",
                    level="DEBUG",
                )
                return
            except Exception as e:
                log(f"OpenGLRenderer: GPU upload failed via VBOManager: {e}", level="DEBUG")

        helpers = self._get_vbo_helpers()
        if helpers and helpers.get('create_vbo_for_mesh'):
            try:
                mesh_comp.gpu = helpers['create_vbo_for_mesh'](
                    mesh_comp.vertices, mesh_comp.colors
                )
                log(
                    f"OpenGLRenderer: Uploaded mesh to GPU (count={mesh_comp.gpu.get('count')})",
                    level="DEBUG",
                )
            except Exception as e:
                log(f"OpenGLRenderer: GPU upload failed: {e}", level="DEBUG")

    def _render_ecs_meshes(self) -> bool:
        """Draw ECS entities that carry a MeshComponent. Returns True if any mesh was drawn."""
        ecs = getattr(self, 'ecs', None)
        if not ecs or not hasattr(ecs, 'get_entities_with'):
            return False

        drawn = False
        for entity in ecs.get_entities_with('mesh'):
            mesh_comp = entity.get_component('mesh')
            if not mesh_comp or not getattr(mesh_comp, 'vertices', None):
                continue
            self._ensure_mesh_gpu(mesh_comp)
            self._draw_mesh(mesh_comp)
            drawn = True
        return drawn

    def _render_default_test_content(self):
        """Render some default content when no scene is set."""
        import time

        gl.glPushMatrix()
        try:
            gl.glColor3f(0.8, 0.4, 0.2)
            rotation = (time.time() * 50) % 360
            gl.glRotatef(rotation, 1, 1, 0)
            self._draw_unit_cube()
        finally:
            gl.glPopMatrix()

    def _traverse_and_render(self, node, parent_transform=None):
        # For now, ignore transforms and just draw cubes for primitives named 'cube' or 'voxel'
        if hasattr(node, "primitive") and node.primitive in ("cube", "voxel"):
            self._draw_cube(node)
        if hasattr(node, "children"):
            for child in node.children:
                self._traverse_and_render(child)

    def _draw_mesh_immediate(self, verts, cols):
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

    def _draw_mesh_vbo(self, mesh_comp) -> bool:
        handle = mesh_comp.gpu
        try:
            gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
            gl.glEnableClientState(gl.GL_COLOR_ARRAY)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, handle["vbo"])
            gl.glVertexPointer(3, gl.GL_FLOAT, 0, None)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, handle["vbo_color"])
            gl.glColorPointer(4, gl.GL_FLOAT, 0, None)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, handle["count"])
            return True
        except Exception as e:
            log(f"OpenGLRenderer: VBO draw failed, falling back to immediate mode: {e}", level="DEBUG")
            mesh_comp.gpu = None
            return False
        finally:
            try:
                gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
                gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
                gl.glDisableClientState(gl.GL_COLOR_ARRAY)
            except Exception:
                pass

    def _draw_mesh(self, mesh_comp):
        """Draw meshes stored in MeshComponent (VBO path with immediate-mode fallback)."""
        verts = mesh_comp.vertices or []
        cols = mesh_comp.colors or []
        if not verts or not gl:
            return

        gl.glPushMatrix()
        try:
            if getattr(mesh_comp, "origin", None):
                ox, oy, oz = mesh_comp.origin
                gl.glTranslatef(ox, oy, oz)

            if getattr(mesh_comp, "gpu", None) and self._draw_mesh_vbo(mesh_comp):
                return

            self._draw_mesh_immediate(verts, cols)
        finally:
            try:
                gl.glPopMatrix()
            except Exception:
                self._reset_modelview_stack()

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
        try:
            gl.glTranslatef(pos[0], pos[1], pos[2])
            gl.glScalef(size, size, size)
            gl.glColor3f(*color)
            self._draw_unit_cube()
        finally:
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
            # Prefer VBOManager cleanup when attached to renderer
            if hasattr(self, 'vbo_manager') and self.vbo_manager is not None:
                try:
                    self.vbo_manager.delete_all()
                except Exception:
                    pass
            elif hasattr(self, 'engine') and getattr(self.engine, 'vbo_manager', None):
                try:
                    self.engine.vbo_manager.delete_all()
                except Exception:
                    pass
            else:
                if 'delete_all_vbos' in globals():
                    from .gl_utils import delete_all_vbos
                    delete_all_vbos()
        except Exception:
            pass
        # Unregister renderer's event listener to avoid dangling references
        try:
            if hasattr(self, 'engine') and getattr(self, 'engine', None) and getattr(self.engine, 'events', None):
                try:
                    self.engine.events.unregister('mesh_generated', self._on_mesh_generated)
                except Exception:
                    pass
        except Exception:
            pass
        # restore mouse state if we grabbed it
        try:
            if pygame and getattr(self, '_mouse_grabbed', False):
                try:
                    pygame.event.set_grab(False)
                    pygame.mouse.set_visible(True)
                except Exception:
                    pass
        except Exception:
            pass
        if pygame:
            pygame.quit()
        self.initialized = False
        log("OpenGLRenderer shutdown", level="INFO")

    def _on_mesh_generated(self, event):
        """Renderer-side handler for mesh_generated events. Attempts to upload immediately.

        This provides lower-latency uploads when the OpenGL context is available. If upload
        fails or no helpers are present, leaves the mesh queued for the engine to process.
        """
        try:
            if not isinstance(event, dict):
                return
            mesh_comp = event.get('mesh')
            entity = event.get('entity')
            if not mesh_comp or getattr(mesh_comp, 'gpu', None) is not None:
                return

            # Prefer attached VBOManager
            vm = getattr(self, 'vbo_manager', None) or (hasattr(self, 'engine') and getattr(self.engine, 'vbo_manager', None)) or None
            if vm is not None:
                try:
                    handle = vm.create_vbo(mesh_comp.vertices, mesh_comp.colors)
                    if handle:
                        mesh_comp.gpu = handle
                        log(f"OpenGLRenderer: Uploaded mesh for entity {getattr(entity, 'name', entity)} via VBOManager", level="DEBUG")
                        return
                except Exception as e:
                    log(f"OpenGLRenderer: VBOManager upload failed: {e}", level="DEBUG")

            # Fallback to engine-provided helpers or module-level helpers
            helpers = None
            if hasattr(self, 'engine') and getattr(self.engine, 'vbo_helpers', None):
                helpers = getattr(self.engine, 'vbo_helpers')
            elif create_vbo_for_mesh and delete_vbo:
                helpers = {'create_vbo_for_mesh': create_vbo_for_mesh, 'delete_vbo': delete_vbo}

            if helpers and helpers.get('create_vbo_for_mesh'):
                try:
                    mesh_comp.gpu = helpers['create_vbo_for_mesh'](mesh_comp.vertices, mesh_comp.colors)
                    log(f"OpenGLRenderer: Uploaded mesh for entity {getattr(entity, 'name', entity)} via helpers", level="DEBUG")
                    return
                except Exception as e:
                    log(f"OpenGLRenderer: helper upload failed: {e}", level="DEBUG")
        except Exception as e:
            log(f"OpenGLRenderer _on_mesh_generated error: {e}", level="DEBUG")
