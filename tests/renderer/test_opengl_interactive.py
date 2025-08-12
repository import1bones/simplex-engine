#!/usr/bin/env python3
"""
Interactive OpenGL renderer test with debug UI and camera controls.
This test creates a visual window for manual testing and debugging.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from simplex.renderer.opengl_renderer import OpenGLRenderer
from simplex.renderer.debug_ui import OpenGLDebugRenderer
from simplex.renderer.renderer import SceneNode
from simplex.renderer.material import Material
from simplex.utils.logger import log
import time
import pygame

def create_test_scene():
    """Create a simple test scene with colorful cubes."""
    root = SceneNode("test_scene")
    
    # Create colorful test cubes in a line
    colors = [
        (1.0, 0.0, 0.0, "Red"),
        (0.0, 1.0, 0.0, "Green"), 
        (0.0, 0.0, 1.0, "Blue"),
        (1.0, 1.0, 0.0, "Yellow"),
        (1.0, 0.0, 1.0, "Magenta"),
        (0.0, 1.0, 1.0, "Cyan")
    ]
    
    for i, (r, g, b, name) in enumerate(colors):
        material = Material(f"{name.lower()}_mat", properties={"color": (r, g, b)})
        cube = SceneNode(f"cube_{name.lower()}", primitive="cube", material=material)
        cube.position = (i * 3, 0, 0)
        cube.size = 1
        root.add_child(cube)
    
    log(f"Created test scene with {len(root.children)} colored cubes", level="INFO")
    return root

def main():
    """Interactive test with debug UI and camera controls."""
    log("Starting interactive OpenGL renderer test", level="INFO")
    
    # Create OpenGL renderer
    renderer = OpenGLRenderer(width=1024, height=768, title="Simplex Engine - Interactive Test")
    
    # Wrap with debug renderer for UI and controls
    debug_renderer = OpenGLDebugRenderer(renderer)
    
    # Initialize
    if not debug_renderer.initialize():
        log("Failed to initialize OpenGL debug renderer", level="ERROR")
        return False
    
    # Create test scene
    scene = create_test_scene()
    renderer.set_scene_root(scene)
    
    log("=== Interactive Test Started ===", level="INFO")
    log("Controls:", level="INFO")
    log("  WASD - Move camera", level="INFO")
    log("  Q/E - Up/Down", level="INFO")
    log("  F1 - Toggle debug UI", level="INFO")
    log("  ESC - Exit", level="INFO")
    log("Close the window or press ESC to end the test", level="INFO")
    
    # Main render loop
    clock = pygame.time.Clock()
    running = True
    frame_count = 0
    start_time = time.time()
    
    try:
        while running:
            # Handle events and get continue status
            running = debug_renderer.handle_events()
            
            # Render frame with debug overlay
            debug_renderer.render_with_debug()
            
            frame_count += 1
            
            # Log performance occasionally
            if frame_count % 180 == 0:  # Every 3 seconds at 60fps
                elapsed = time.time() - start_time
                fps = frame_count / elapsed if elapsed > 0 else 0
                log(f"Performance: {fps:.1f} FPS, {frame_count} frames rendered", level="INFO")
            
            # Limit framerate
            clock.tick(60)
        
        elapsed = time.time() - start_time
        avg_fps = frame_count / elapsed if elapsed > 0 else 0
        log(f"✓ Interactive test completed: {frame_count} frames in {elapsed:.1f}s (avg {avg_fps:.1f} FPS)", level="INFO")
        
    except Exception as e:
        log(f"✗ Interactive test failed: {e}", level="ERROR")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        renderer.shutdown()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
