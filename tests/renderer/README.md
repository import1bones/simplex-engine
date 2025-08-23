# OpenGL Renderer Test Suite

This directory contains tests for the OpenGL renderer backend of Simplex Engine.

## Test Files

### `test_opengl_basic.py`
**Automated test** - Tests basic OpenGL renderer functionality:
- ✅ Renderer initialization
- ✅ Basic rendering without content
- ✅ Scene rendering with colored cubes
- ✅ Proper shutdown

Run with: `python tests/renderer/test_opengl_basic.py`

### `test_opengl_interactive.py` 
**Interactive test** - Manual testing with debug UI:
- 🎮 Interactive camera controls (WASD, Q/E)
- 🖥️ Debug UI overlay (toggle with F1)
- 🎨 Colorful test cubes
- 📊 Real-time performance monitoring

Run with: `python tests/renderer/test_opengl_interactive.py`

### `test_opengl_minecraft.py`
**Minecraft world test** - Large-scale voxel rendering:
- 🌍 Procedural terrain generation (16x16 blocks)
- 🏔️ Multiple block types (grass, dirt, stone, water, sand)
- 🌳 Tree generation with wood and leaves
- 📈 Performance testing with hundreds of blocks

Run with: `python tests/renderer/test_opengl_minecraft.py`

### `run_tests.py`
**Test runner** - Interactive test selection menu:
- Choose individual tests or run all
- Separate automated vs interactive tests
- Progress reporting and results summary

Run with: `python tests/renderer/run_tests.py`

## Quick Start

1. **Run all automated tests:**
   ```bash
   python tests/renderer/run_tests.py
   # Select option 4 (Run all automated tests)
   ```

2. **Interactive testing:**
   ```bash
   python tests/renderer/test_opengl_interactive.py
   ```

3. **Minecraft world demo:**
   ```bash
   python tests/renderer/test_opengl_minecraft.py
   ```

## Controls (Interactive Tests)

- **WASD** - Move camera around
- **Q/E** - Move camera up/down  
- **F1** - Toggle debug UI overlay
- **ESC** - Exit test
- **Mouse** - Close window to exit

## Requirements

- PyOpenGL and PyOpenGL_accelerate
- pygame
- Working OpenGL graphics drivers

## Test Results

The tests verify:
- ✅ OpenGL context creation
- ✅ 3D projection and camera setup
- ✅ Voxel/cube rendering
- ✅ Material and color system
- ✅ Scene graph traversal
- ✅ Debug UI functionality
- ✅ Performance with large numbers of blocks

## Troubleshooting

If tests fail:
1. Check that OpenGL drivers are installed
2. Verify pygame and PyOpenGL are installed: `pip list | grep -i opengl`
3. Try running basic test first: `python tests/renderer/test_opengl_basic.py`
4. Check the logs for specific error messages

## Performance Expectations

- **Basic test**: Should run at 60+ FPS
- **Interactive test**: 60 FPS with 6 cubes
- **Minecraft test**: 30+ FPS with 1000+ blocks (depends on hardware)

The OpenGL renderer is optimized for real-time Minecraft-like voxel worlds.
