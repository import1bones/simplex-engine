"""
Debug overlay for displaying engine statistics and debug information.
"""
import pygame
import time
from typing import Dict, Any, List


class DebugOverlay:
    """Renders debug information over the game view."""
    
    def __init__(self):
        self.enabled = True
        self.font = None
        self.fps_history = []
        self.max_fps_history = 60
        self.stats = {}
        self.debug_lines = []
        
    def initialize(self):
        """Initialize pygame font for debug text."""
        try:
            pygame.font.init()
            self.font = pygame.font.Font(None, 24)
        except Exception as e:
            print(f"Warning: Could not initialize debug font: {e}")
            
    def toggle(self):
        """Toggle debug overlay visibility."""
        self.enabled = not self.enabled
        
    def update_fps(self, fps: float):
        """Update FPS tracking."""
        self.fps_history.append(fps)
        if len(self.fps_history) > self.max_fps_history:
            self.fps_history.pop(0)
            
    def update_stats(self, stats: Dict[str, Any]):
        """Update engine statistics."""
        self.stats.update(stats)
        
    def add_debug_line(self, text: str):
        """Add a debug text line."""
        self.debug_lines.append(text)
        
    def clear_debug_lines(self):
        """Clear all debug lines."""
        self.debug_lines.clear()
        
    def render(self, screen: pygame.Surface):
        """Render debug overlay on screen."""
        if not self.enabled or not self.font:
            return
            
        # Create semi-transparent overlay
        overlay = pygame.Surface((300, screen.get_height()))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        
        y_offset = 10
        line_height = 25
        
        # FPS information
        if self.fps_history:
            current_fps = self.fps_history[-1]
            avg_fps = sum(self.fps_history) / len(self.fps_history)
            min_fps = min(self.fps_history)
            max_fps = max(self.fps_history)
            
            fps_text = self.font.render(f"FPS: {current_fps:.1f}", True, (255, 255, 255))
            avg_text = self.font.render(f"Avg: {avg_fps:.1f}", True, (255, 255, 255))
            range_text = self.font.render(f"Min/Max: {min_fps:.1f}/{max_fps:.1f}", True, (255, 255, 255))
            
            overlay.blit(fps_text, (10, y_offset))
            y_offset += line_height
            overlay.blit(avg_text, (10, y_offset))
            y_offset += line_height
            overlay.blit(range_text, (10, y_offset))
            y_offset += line_height
            
        # Engine statistics
        y_offset += 10
        stats_title = self.font.render("Engine Stats:", True, (200, 200, 255))
        overlay.blit(stats_title, (10, y_offset))
        y_offset += line_height
        
        for key, value in self.stats.items():
            stat_text = self.font.render(f"{key}: {value}", True, (255, 255, 255))
            overlay.blit(stat_text, (10, y_offset))
            y_offset += line_height
            
        # Debug lines
        if self.debug_lines:
            y_offset += 10
            debug_title = self.font.render("Debug Info:", True, (255, 200, 200))
            overlay.blit(debug_title, (10, y_offset))
            y_offset += line_height
            
            for line in self.debug_lines:
                debug_text = self.font.render(line, True, (255, 255, 255))
                overlay.blit(debug_text, (10, y_offset))
                y_offset += line_height
                
        # Controls help
        y_offset += 10
        help_title = self.font.render("Debug Controls:", True, (255, 255, 200))
        overlay.blit(help_title, (10, y_offset))
        y_offset += line_height
        
        controls = [
            "F1: Toggle Debug",
            "F2: Toggle Pause",
            "F3: Step Frame",
            "ESC: Quit"
        ]
        
        for control in controls:
            control_text = self.font.render(control, True, (255, 255, 255))
            overlay.blit(control_text, (10, y_offset))
            y_offset += line_height
            
        screen.blit(overlay, (screen.get_width() - 300, 0))


class DebugStats:
    """Collects and manages debug statistics."""
    
    def __init__(self):
        self.frame_count = 0
        self.start_time = time.time()
        self.last_frame_time = time.time()
        self.frame_times = []
        
    def update(self):
        """Update frame statistics."""
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        self.frame_times.append(frame_time)
        
        # Keep only last 60 frames
        if len(self.frame_times) > 60:
            self.frame_times.pop(0)
            
        self.frame_count += 1
        self.last_frame_time = current_time
        
    def get_fps(self) -> float:
        """Get current FPS."""
        if not self.frame_times:
            return 0.0
        return 1.0 / self.frame_times[-1] if self.frame_times[-1] > 0 else 0.0
        
    def get_average_fps(self) -> float:
        """Get average FPS over recent frames."""
        if not self.frame_times:
            return 0.0
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
        
    def get_stats(self) -> Dict[str, Any]:
        """Get all debug statistics."""
        uptime = time.time() - self.start_time
        return {
            'Frames': self.frame_count,
            'Uptime': f"{uptime:.1f}s",
            'Frame Time': f"{self.frame_times[-1] * 1000:.1f}ms" if self.frame_times else "0ms"
        }
