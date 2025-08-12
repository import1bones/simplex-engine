#!/usr/bin/env python3
"""
Advanced OpenGL renderer test with Minecraft-like world generation.
Tests large-scale voxel rendering and world generation capabilities.
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

def create_minecraft_world(size=16, height_variation=4):
    """Create a Minecraft-like world with different block types."""
    root = SceneNode("minecraft_world")
    
    # Block materials with realistic colors
    materials = {
        'grass': Material("grass", properties={"color": (0.4, 0.8, 0.2)}),
        'dirt': Material("dirt", properties={"color": (0.6, 0.4, 0.2)}),
        'stone': Material("stone", properties={"color": (0.5, 0.5, 0.5)}),
        'water': Material("water", properties={"color": (0.2, 0.4, 0.8)}),
        'sand': Material("sand", properties={"color": (0.9, 0.8, 0.6)}),
        'wood': Material("wood", properties={"color": (0.7, 0.5, 0.3)}),
        'leaves': Material("leaves", properties={"color": (0.2, 0.6, 0.2)})
    }
    
    block_count = 0
    
    # Generate terrain
    for x in range(size):
        for z in range(size):
            # Simple height map with some variation
            base_height = 3
            height_offset = int(height_variation * ((x + z) % 8) / 8)
            terrain_height = base_height + height_offset
            
            # Generate blocks column by column
            for y in range(terrain_height):
                # Determine block type based on height and position
                if y == terrain_height - 1:
                    # Top layer
                    if terrain_height <= 3:
                        block_type = 'sand'  # Beach areas
                    else:
                        block_type = 'grass'
                elif y >= terrain_height - 3:
                    block_type = 'dirt'
                else:
                    block_type = 'stone'
                
                # Add some water at low elevations
                if terrain_height == 3 and (x + z) % 11 == 0:
                    block_type = 'water'
                
                # Create the block
                block = SceneNode(
                    name=f"block_{x}_{y}_{z}",
                    primitive="voxel",
                    material=materials[block_type]
                )
                block.position = (x, y, z)
                block.size = 1
                root.add_child(block)
                block_count += 1
            
            # Occasionally add trees
            if (x % 5 == 0 and z % 4 == 0 and terrain_height > 4):
                # Tree trunk
                for tree_y in range(2):
                    trunk = SceneNode(
                        name=f"trunk_{x}_{terrain_height + tree_y}_{z}",
                        primitive="voxel",
                        material=materials['wood']
                    )
                    trunk.position = (x, terrain_height + tree_y, z)
                    trunk.size = 1
                    root.add_child(trunk)
                    block_count += 1
                
                # Tree leaves
                for lx in range(-1, 2):
                    for lz in range(-1, 2):
                        if abs(lx) + abs(lz) <= 1:  # Cross pattern
                            leaves = SceneNode(
                                name=f"leaves_{x+lx}_{terrain_height + 2}_{z+lz}",
                                primitive="voxel",
                                material=materials['leaves']
                            )
                            leaves.position = (x + lx, terrain_height + 2, z + lz)
                            leaves.size = 1
                            root.add_child(leaves)
                            block_count += 1
    
    log(f"Generated Minecraft-like world: {size}x{size} terrain with {block_count} blocks", level="INFO")
    return root, block_count

def main():
    """Test large-scale voxel world rendering."""
    log("Starting Minecraft-like world rendering test", level="INFO")
    
    # Create OpenGL renderer with larger window
    renderer = OpenGLRenderer(width=1280, height=720, title="Simplex Engine - Minecraft World Test")
    
    # Wrap with debug renderer
    debug_renderer = OpenGLDebugRenderer(renderer)
    
    # Initialize
    if not debug_renderer.initialize():
        log("Failed to initialize OpenGL debug renderer", level="ERROR")
        return False
    
    # Create world (start small for performance)
    world_size = 16
    log(f"Generating {world_size}x{world_size} Minecraft-like world...", level="INFO")
    
    start_gen = time.time()
    world, block_count = create_minecraft_world(size=world_size)
    gen_time = time.time() - start_gen
    
    renderer.set_scene_root(world)
    log(f"✓ World generated in {gen_time:.2f}s ({block_count} blocks)", level="INFO")
    
    log("=== Minecraft World Test Started ===", level="INFO")
    log("You should see a procedurally generated world with:", level="INFO")
    log("  - Grass and dirt terrain", level="INFO")
    log("  - Stone underneath", level="INFO") 
    log("  - Sand and water in low areas", level="INFO")
    log("  - Occasional trees with wood trunks and leaves", level="INFO")
    log("Use WASD/Q/E to fly around and explore!", level="INFO")
    
    # Performance test render loop
    clock = pygame.time.Clock()
    running = True
    frame_count = 0
    start_time = time.time()
    
    try:
        while running:
            # Handle events
            running = debug_renderer.handle_events()
            
            # Render frame
            debug_renderer.render_with_debug()
            
            frame_count += 1
            
            # Log performance every 5 seconds
            if frame_count % 300 == 0:
                elapsed = time.time() - start_time
                fps = frame_count / elapsed if elapsed > 0 else 0
                log(f"Performance: {fps:.1f} FPS rendering {block_count} blocks", level="INFO")
            
            # Limit framerate
            clock.tick(60)
        
        # Final performance report
        elapsed = time.time() - start_time
        avg_fps = frame_count / elapsed if elapsed > 0 else 0
        log(f"✓ Minecraft world test completed:", level="INFO")
        log(f"  Blocks rendered: {block_count}", level="INFO")
        log(f"  Frames rendered: {frame_count}", level="INFO")
        log(f"  Duration: {elapsed:.1f}s", level="INFO")
        log(f"  Average FPS: {avg_fps:.1f}", level="INFO")
        
    except Exception as e:
        log(f"✗ Minecraft world test failed: {e}", level="ERROR")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        renderer.shutdown()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
