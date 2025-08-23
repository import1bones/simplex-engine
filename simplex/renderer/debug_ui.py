"""
Debug UI system for OpenGL renderer.
Provides on-screen debugging information and controls for 3D development.
"""

from simplex.utils.logger import log

try:
    import OpenGL.GL as gl
    import OpenGL.GLU as glu
    import pygame
    import pygame.font
except ImportError:
    gl = None
    glu = None
    pygame = None

class DebugUI:
    """Debug UI overlay for OpenGL renderer with camera controls and info display."""
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.enabled = True
        self.font = None
        self.info_text = []
        self.camera_pos = [16, 16, 48]
        self.camera_target = [16, 16, 0]
        self.camera_speed = 0.5
        self.mouse_sensitivity = 0.1
        
    def initialize(self):
        """Initialize the debug UI system."""
        if pygame:
            pygame.font.init()
            self.font = pygame.font.Font(None, 24)
            log("DebugUI initialized", level="INFO")
    
    def handle_input(self, events):
        """Handle input for camera controls and UI toggling."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.enabled = not self.enabled
                    log(f"Debug UI {'enabled' if self.enabled else 'disabled'}", level="INFO")
                elif event.key == pygame.K_w:
                    self.camera_pos[2] -= self.camera_speed
                    self.camera_target[2] -= self.camera_speed
                elif event.key == pygame.K_s:
                    self.camera_pos[2] += self.camera_speed
                    self.camera_target[2] += self.camera_speed
                elif event.key == pygame.K_a:
                    self.camera_pos[0] -= self.camera_speed
                    self.camera_target[0] -= self.camera_speed
                elif event.key == pygame.K_d:
                    self.camera_pos[0] += self.camera_speed
                    self.camera_target[0] += self.camera_speed
                elif event.key == pygame.K_q:
                    self.camera_pos[1] += self.camera_speed
                    self.camera_target[1] += self.camera_speed
                elif event.key == pygame.K_e:
                    self.camera_pos[1] -= self.camera_speed
                    self.camera_target[1] -= self.camera_speed
    
    def update_info(self, renderer_info):
        """Update debug information display."""
        self.info_text = [
            f"FPS: {renderer_info.get('fps', 'N/A')}",
            f"Camera: {self.camera_pos}",
            f"Target: {self.camera_target}",
            f"Primitives: {renderer_info.get('primitives_rendered', 0)}",
            f"Backend: {renderer_info.get('backend', 'Unknown')}",
            "",
            "Controls:",
            "F1 - Toggle Debug UI",
            "WASD - Move Camera",
            "Q/E - Up/Down",
            "ESC - Exit"
        ]
    
    def render_2d_overlay(self, screen):
        """Render 2D debug overlay on top of 3D scene."""
        if not self.enabled or not self.font:
            return
            
        # Semi-transparent background
        overlay = pygame.Surface((300, len(self.info_text) * 25 + 20))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (10, 10))
        
        # Render text
        y_offset = 20
        for line in self.info_text:
            if line.strip():  # Skip empty lines
                text_surface = self.font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (20, y_offset))
            y_offset += 25
    
    def get_camera_position(self):
        """Get current camera position for 3D rendering."""
        return self.camera_pos
    
    def get_camera_target(self):
        """Get current camera target for 3D rendering."""
        return self.camera_target

class OpenGLDebugRenderer:
    """Enhanced OpenGL renderer with debug UI integration."""
    
    def __init__(self, opengl_renderer):
        self.renderer = opengl_renderer
        self.debug_ui = DebugUI(opengl_renderer.width, opengl_renderer.height)
        self.primitives_rendered = 0
        
    def initialize(self):
        """Initialize both OpenGL renderer and debug UI."""
        success = self.renderer.initialize()
        if success:
            self.debug_ui.initialize()
        return success
    
    def handle_events(self):
        """Handle pygame events for both rendering and debug UI."""
        events = pygame.event.get()
        self.debug_ui.handle_input(events)
        
        # Handle window close
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
        return True
    
    def render_with_debug(self):
        """Render 3D scene with debug overlay."""
        if not self.renderer.initialized:
            return
            
        # Update camera from debug UI
        camera_pos = self.debug_ui.get_camera_position()
        camera_target = self.debug_ui.get_camera_target()
        
        # Render 3D scene
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        
        # Setup 3D projection
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = self.renderer.width / self.renderer.height if self.renderer.height != 0 else 1
        glu.gluPerspective(70, aspect, 0.1, 1000.0)
        
        # Setup 3D view
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        glu.gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
                     camera_target[0], camera_target[1], camera_target[2],
                     0, 1, 0)
        
        # Render scene
        self.primitives_rendered = 0
        if self.renderer.scene_root:
            self._traverse_and_render_debug(self.renderer.scene_root)
        
        # Render some test cubes for demo
        self._render_test_world()
        
        # Render debug UI directly in OpenGL (if enabled)
        if self.debug_ui.enabled:
            self._render_debug_overlay_opengl()
        
        pygame.display.flip()
    
    def _render_debug_overlay_opengl(self):
        """Render debug overlay directly using OpenGL."""
        # Switch to 2D orthographic projection
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(0, self.renderer.width, self.renderer.height, 0, -1, 1)
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        
        # Disable depth testing for 2D overlay
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        # Update debug info
        renderer_info = {
            'fps': 60,  # TODO: Calculate actual FPS
            'primitives_rendered': self.primitives_rendered,
            'backend': 'OpenGL'
        }
        self.debug_ui.update_info(renderer_info)
        
        # Draw semi-transparent background
        gl.glColor4f(0.0, 0.0, 0.0, 0.7)  # Black with 70% opacity
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(10, 10)
        gl.glVertex2f(320, 10)
        gl.glVertex2f(320, len(self.debug_ui.info_text) * 20 + 30)
        gl.glVertex2f(10, len(self.debug_ui.info_text) * 20 + 30)
        gl.glEnd()
        
        # Draw text outline/border for better visibility
        gl.glColor3f(1.0, 1.0, 1.0)  # White text
        y_pos = 30
        for line in self.debug_ui.info_text:
            if line.strip():  # Skip empty lines
                self._draw_text_simple(line, 20, y_pos)
            y_pos += 20
        
        # Restore 3D state
        gl.glDisable(gl.GL_BLEND)
        gl.glEnable(gl.GL_DEPTH_TEST)
        
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def _draw_text_simple(self, text, x, y):
        """Draw simple text using OpenGL lines (basic bitmap-style)."""
        # This is a very basic text rendering - just draw the text info as simple shapes
        # For demonstration, we'll draw simple rectangular indicators for each line
        if "FPS:" in text:
            gl.glColor3f(0.0, 1.0, 0.0)  # Green for FPS
        elif "Camera:" in text:
            gl.glColor3f(0.0, 0.8, 1.0)  # Cyan for camera
        elif "Primitives:" in text:
            gl.glColor3f(1.0, 0.8, 0.0)  # Yellow for primitives
        elif "Backend:" in text:
            gl.glColor3f(1.0, 0.5, 0.0)  # Orange for backend
        elif "Controls:" in text or any(key in text for key in ["F1", "WASD", "Q/E", "ESC"]):
            gl.glColor3f(0.8, 0.8, 0.8)  # Light gray for controls
        else:
            gl.glColor3f(1.0, 1.0, 1.0)  # White for other text
        
        # Draw a simple colored rectangle as text indicator
        gl.glBegin(gl.GL_QUADS)
        text_width = len(text) * 6  # Approximate text width
        gl.glVertex2f(x, y - 2)
        gl.glVertex2f(x + text_width, y - 2)
        gl.glVertex2f(x + text_width, y + 12)
        gl.glVertex2f(x, y + 12)
        gl.glEnd()
        
        # Draw text outline
        gl.glColor3f(0.0, 0.0, 0.0)  # Black outline
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glVertex2f(x, y - 2)
        gl.glVertex2f(x + text_width, y - 2)
        gl.glVertex2f(x + text_width, y + 12)
        gl.glVertex2f(x, y + 12)
        gl.glEnd()
    
    def _traverse_and_render_debug(self, node, parent_transform=None):
        """Traverse scene graph and count rendered primitives."""
        if hasattr(node, 'primitive') and node.primitive in ("cube", "voxel"):
            self.renderer._draw_cube(node)
            self.primitives_rendered += 1
        if hasattr(node, 'children'):
            for child in node.children:
                self._traverse_and_render_debug(child)
    
    def _render_test_world(self):
        """Render a simple test world for debugging."""
        # Draw a simple grid of cubes
        for x in range(10, 23):
            for z in range(10, 23):
                gl.glPushMatrix()
                gl.glTranslatef(x, 10, z)
                
                # Alternate colors
                if (x + z) % 2 == 0:
                    gl.glColor3f(0.8, 0.6, 0.4)  # Light brown
                else:
                    gl.glColor3f(0.6, 0.8, 0.4)  # Light green
                
                # Draw cube
                self._draw_simple_cube()
                gl.glPopMatrix()
                self.primitives_rendered += 1
    
    def _draw_simple_cube(self):
        """Draw a simple unit cube."""
        gl.glBegin(gl.GL_QUADS)
        # Front face
        gl.glVertex3f(-0.5, -0.5,  0.5)
        gl.glVertex3f( 0.5, -0.5,  0.5)
        gl.glVertex3f( 0.5,  0.5,  0.5)
        gl.glVertex3f(-0.5,  0.5,  0.5)
        # Back face
        gl.glVertex3f(-0.5, -0.5, -0.5)
        gl.glVertex3f(-0.5,  0.5, -0.5)
        gl.glVertex3f( 0.5,  0.5, -0.5)
        gl.glVertex3f( 0.5, -0.5, -0.5)
        # Left face
        gl.glVertex3f(-0.5, -0.5, -0.5)
        gl.glVertex3f(-0.5, -0.5,  0.5)
        gl.glVertex3f(-0.5,  0.5,  0.5)
        gl.glVertex3f(-0.5,  0.5, -0.5)
        # Right face
        gl.glVertex3f(0.5, -0.5, -0.5)
        gl.glVertex3f(0.5,  0.5, -0.5)
        gl.glVertex3f(0.5,  0.5,  0.5)
        gl.glVertex3f(0.5, -0.5,  0.5)
        # Top face
        gl.glVertex3f(-0.5, 0.5, -0.5)
        gl.glVertex3f(-0.5, 0.5,  0.5)
        gl.glVertex3f( 0.5, 0.5,  0.5)
        gl.glVertex3f( 0.5, 0.5, -0.5)
        # Bottom face
        gl.glVertex3f(-0.5, -0.5, -0.5)
        gl.glVertex3f( 0.5, -0.5, -0.5)
        gl.glVertex3f( 0.5, -0.5,  0.5)
        gl.glVertex3f(-0.5, -0.5,  0.5)
        gl.glEnd()
