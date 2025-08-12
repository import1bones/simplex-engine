#!/usr/bin/env python3
"""
Basic OpenGL renderer test - minimal test to verify OpenGL backend works.
Tests initialization, basic rendering, and shutdown functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from simplex.renderer.opengl_renderer import OpenGLRenderer
from simplex.renderer.renderer import SceneNode
from simplex.renderer.material import Material
from simplex.utils.logger import log
import pygame

def test_basic_initialization():
    """Test basic OpenGL renderer initialization."""
    log("Testing basic OpenGL renderer initialization", level="INFO")
    
    try:
        # Create renderer
        renderer = OpenGLRenderer(width=800, height=600)
        
        # Try to initialize
        success = renderer.initialize()
        
        if success:
            log("✓ OpenGL renderer initialized successfully!", level="INFO")
            
            # Test basic rendering without content
            for i in range(5):
                renderer.render()
                log(f"✓ Rendered frame {i+1}", level="INFO")
            
            renderer.shutdown()
            log("✓ OpenGL renderer test completed successfully", level="INFO")
            return True
        else:
            log("✗ OpenGL renderer failed to initialize", level="ERROR")
            return False
            
    except Exception as e:
        log(f"✗ OpenGL renderer test failed with exception: {e}", level="ERROR")
        import traceback
        traceback.print_exc()
        return False

def test_scene_rendering():
    """Test OpenGL renderer with scene content."""
    log("Testing OpenGL renderer with scene content", level="INFO")
    
    try:
        # Create renderer
        renderer = OpenGLRenderer(width=800, height=600)
        
        if not renderer.initialize():
            log("✗ Failed to initialize renderer for scene test", level="ERROR")
            return False
        
        # Create test scene with colorful cubes
        root = SceneNode("root")
        colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0)]
        
        for i, color in enumerate(colors):
            material = Material(f"cube_mat_{i}", properties={"color": color})
            cube = SceneNode(f"cube_{i}", primitive="cube", material=material)
            cube.position = (i * 2, 0, 0)
            cube.size = 1
            root.add_child(cube)
        
        renderer.set_scene_root(root)
        log(f"✓ Created test scene with {len(root.children)} cubes", level="INFO")
        
        # Render frames with content
        for i in range(10):
            renderer.render()
        
        log("✓ Scene rendering test completed successfully", level="INFO")
        renderer.shutdown()
        return True
        
    except Exception as e:
        log(f"✗ Scene rendering test failed: {e}", level="ERROR")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all basic OpenGL renderer tests."""
    log("Starting OpenGL renderer basic tests", level="INFO")
    
    tests = [
        ("Basic Initialization", test_basic_initialization),
        ("Scene Rendering", test_scene_rendering)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        log(f"\n--- Running {test_name} Test ---", level="INFO")
        if test_func():
            passed += 1
            log(f"✓ {test_name} test PASSED", level="INFO")
        else:
            log(f"✗ {test_name} test FAILED", level="ERROR")
    
    log(f"\n=== Test Results: {passed}/{total} tests passed ===", level="INFO")
    
    if passed == total:
        log("🎉 All tests PASSED!", level="INFO")
        return True
    else:
        log("❌ Some tests FAILED!", level="ERROR")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
