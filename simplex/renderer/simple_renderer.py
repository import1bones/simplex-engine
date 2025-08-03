"""
Simple 2D GUI renderer for simplex-engine using pygame.
Provides basic 2D rendering capabilities to replace the stub renderer.
"""

import pygame
import sys
from simplex.renderer.interface import RendererInterface
from simplex.utils.logger import log


class SimpleRenderer(RendererInterface):
    """
    Simple 2D renderer using pygame for basic GUI output.
    Replaces the stub renderer with actual visual output.
    """
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = None
        self.clock = None
        self.initialized = False
        self.entities_to_render = []
        
    def initialize(self):
        """Initialize pygame and create display."""
        if not self.initialized:
            try:
                pygame.init()
                self.screen = pygame.display.set_mode((self.width, self.height))
                pygame.display.set_caption("Simplex Engine - Ping Pong")
                self.clock = pygame.time.Clock()
                self.initialized = True
                log("SimpleRenderer initialized with pygame", level="INFO")
            except Exception as e:
                log(f"Failed to initialize SimpleRenderer: {e}", level="ERROR")
                self.initialized = False
    
    def add_entity_to_render(self, entity):
        """Add an ECS entity to the render list."""
        if entity not in self.entities_to_render:
            self.entities_to_render.append(entity)
    
    def render(self):
        """Render the current frame."""
        if not self.initialized:
            self.initialize()
        
        if not self.initialized:
            return
        
        try:
            # Clear screen (black background)
            self.screen.fill((0, 0, 0))
            
            # Render all entities
            for entity in self.entities_to_render:
                self._render_entity(entity)
            
            # Render UI elements (score, etc.)
            self._render_ui()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
            
            # Handle pygame events (for window closing)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
        except Exception as e:
            log(f"Rendering error: {e}", level="ERROR")
    
    def _render_entity(self, entity):
        """Render a single ECS entity."""
        position_comp = entity.get_component('position')
        render_comp = entity.get_component('render')
        collision_comp = entity.get_component('collision')
        
        if not all([position_comp, render_comp]):
            return
        
        # Get entity properties
        x, y = int(position_comp.x), int(position_comp.y)
        color = self._convert_color(render_comp.color)
        
        # Determine size from collision component or defaults
        if collision_comp:
            width = int(collision_comp.width)
            height = int(collision_comp.height)
        else:
            width = height = 20
        
        # Render based on primitive type
        if render_comp.primitive == 'sphere':
            # Render as circle
            radius = max(width, height) // 2
            pygame.draw.circle(self.screen, color, (x, y), radius)
        else:
            # Render as rectangle (cube, default)
            rect = pygame.Rect(x - width//2, y - height//2, width, height)
            pygame.draw.rect(self.screen, color, rect)
    
    def _render_ui(self):
        """Render UI elements like score."""
        try:
            # Simple score display (we'll get score from scoring system later)
            font = pygame.font.Font(None, 36)
            score_text = font.render("Player: 0  AI: 0", True, (255, 255, 255))
            self.screen.blit(score_text, (self.width // 2 - 80, 20))
            
            # Center line
            pygame.draw.line(self.screen, (255, 255, 255), 
                           (self.width // 2, 0), (self.width // 2, self.height), 2)
                           
        except Exception as e:
            log(f"UI rendering error: {e}", level="ERROR")
    
    def _convert_color(self, color):
        """Convert normalized color (0-1) to pygame color (0-255)."""
        if isinstance(color, tuple) and len(color) >= 3:
            return (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
        return (255, 255, 255)  # Default white
    
    def update_score(self, player_score, ai_score):
        """Update score display."""
        self.player_score = player_score
        self.ai_score = ai_score
    
    def shutdown(self):
        """Clean shutdown of renderer."""
        if self.initialized:
            pygame.quit()
            self.initialized = False
