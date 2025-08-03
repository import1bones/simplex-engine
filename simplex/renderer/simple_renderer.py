"""
Simple 2D GUI renderer for simplex-engine using pygame.
Provides basic 2D rendering capabilities with debug overlay and development tools.
"""

import pygame
import sys
from simplex.renderer.interface import RendererInterface
from simplex.utils.logger import log
from simplex.debug import DebugOverlay, DebugStats, DevToolsManager


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
        self.engine_events = None  # Reference to engine event system
        
        # Debug and development tools
        self.debug_overlay = DebugOverlay()
        self.debug_stats = DebugStats()
        self.dev_tools = DevToolsManager()
        self.player_score = 0
        self.ai_score = 0
        
    def initialize(self):
        """Initialize pygame and create display."""
        if not self.initialized:
            try:
                pygame.init()
                pygame.display.init()  # Ensure display subsystem is initialized
                self.screen = pygame.display.set_mode((self.width, self.height))
                pygame.display.set_caption("Simplex Engine - Ping Pong")
                self.clock = pygame.time.Clock()
                pygame.font.init()  # Initialize font subsystem
                
                # Initialize debug tools
                self.debug_overlay.initialize()
                
                self.initialized = True
                log("SimpleRenderer initialized with pygame", level="INFO")
            except Exception as e:
                log(f"Failed to initialize SimpleRenderer: {e}", level="ERROR")
                self.initialized = False
    
    def add_entity_to_render(self, entity):
        """Add an ECS entity to the render list."""
        if entity not in self.entities_to_render:
            self.entities_to_render.append(entity)
    
    def set_engine_events(self, engine_events):
        """Set reference to engine event system for input forwarding."""
        self.engine_events = engine_events
    
    def render(self):
        """Render the current frame."""
        if not self.initialized:
            self.initialize()
        
        if not self.initialized:
            return
        
        try:
            # Update debug statistics
            self.debug_stats.update()
            fps = self.debug_stats.get_fps()
            self.debug_overlay.update_fps(fps)
            
            # Update debug overlay with engine stats
            stats = self.debug_stats.get_stats()
            stats.update(self.dev_tools.get_dev_stats())
            stats['Entities'] = len(self.entities_to_render)
            self.debug_overlay.update_stats(stats)
            
            # Clear previous debug lines
            self.debug_overlay.clear_debug_lines()
            self.debug_overlay.add_debug_line(f"Resolution: {self.width}x{self.height}")
            
            # Clear screen (black background)
            self.screen.fill((0, 0, 0))
            
            # Render all entities
            for entity in self.entities_to_render:
                self._render_entity(entity)
            
            # Render UI elements (score, etc.)
            self._render_ui()
            
            # Render debug overlay if enabled
            if self.dev_tools.debug_enabled:
                self.debug_overlay.render(self.screen)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
            
            # Handle pygame events (for window closing and debug input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Handle debug keys first
                    self._handle_debug_keys(event)
                    # Forward game input to engine event system
                    self._handle_game_input(event)
                elif event.type == pygame.KEYUP:
                    # Forward game input key releases to engine event system
                    self._handle_game_input(event)
                    
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
            # Score display
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Player: {self.player_score}  AI: {self.ai_score}", True, (255, 255, 255))
            self.screen.blit(score_text, (self.width // 2 - 100, 20))
            
            # Center line
            pygame.draw.line(self.screen, (255, 255, 255), 
                           (self.width // 2, 0), (self.width // 2, self.height), 2)
            
            # Pause indicator
            if self.dev_tools.pause_system.is_paused():
                pause_font = pygame.font.Font(None, 48)
                pause_text = pause_font.render("PAUSED", True, (255, 255, 0))
                text_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2))
                # Semi-transparent background
                overlay = pygame.Surface((text_rect.width + 20, text_rect.height + 20))
                overlay.set_alpha(180)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (text_rect.x - 10, text_rect.y - 10))
                self.screen.blit(pause_text, text_rect)
                           
        except Exception as e:
            log(f"UI rendering error: {e}", level="ERROR")
            
    def _handle_debug_keys(self, event):
        """Handle debug key presses."""
        try:
            key_name = pygame.key.name(event.key).upper()
            
            # Map pygame keys to debug system
            if event.key == pygame.K_F1:
                self.dev_tools.handle_debug_input('F1')
            elif event.key == pygame.K_F2:
                self.dev_tools.handle_debug_input('F2')
            elif event.key == pygame.K_F3:
                self.dev_tools.handle_debug_input('F3')
            elif event.key == pygame.K_F4:
                self.dev_tools.handle_debug_input('F4')
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                
        except Exception as e:
            log(f"Debug key handling error: {e}", level="ERROR")
    
    def _handle_game_input(self, event):
        """Forward game input events to the engine event system."""
        try:
            if hasattr(self, 'engine_events') and self.engine_events:
                # Convert pygame key events to engine input events
                if event.key in [pygame.K_UP, pygame.K_w]:
                    game_event = type('Event', (), {})()
                    game_event.type = 'KEYDOWN' if event.type == pygame.KEYDOWN else 'KEYUP'
                    game_event.key = 'UP'
                    self.engine_events.emit('input', game_event)
                    log(f"Input event emitted: {game_event.type} {game_event.key}", level="INFO")
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    game_event = type('Event', (), {})()
                    game_event.type = 'KEYDOWN' if event.type == pygame.KEYDOWN else 'KEYUP'
                    game_event.key = 'DOWN'
                    self.engine_events.emit('input', game_event)
                    log(f"Input event emitted: {game_event.type} {game_event.key}", level="INFO")
                    
        except Exception as e:
            log(f"Game input handling error: {e}", level="ERROR")
    
    def _convert_color(self, color):
        """Convert normalized color (0-1) to pygame color (0-255)."""
        if isinstance(color, tuple) and len(color) >= 3:
            return (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
        return (255, 255, 255)  # Default white
    
    def update_score(self, player_score, ai_score):
        """Update score display."""
        self.player_score = player_score
        self.ai_score = ai_score
    
    def should_update_systems(self):
        """Check if ECS systems should update (for pause functionality)."""
        return self.dev_tools.pause_system.should_update()
        
    def is_paused(self):
        """Check if the engine is paused."""
        return self.dev_tools.pause_system.is_paused()
    
    def shutdown(self):
        """Clean shutdown of renderer."""
        if self.initialized:
            pygame.quit()
            self.initialized = False
