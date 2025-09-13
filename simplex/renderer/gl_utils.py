"""OpenGL helper utilities for creating VBOs/VAOs and uploading mesh data.

This module provides minimal helpers used by the OpenGL renderer to
upload vertex and color buffers. It uses PyOpenGL functions and ctypes
to create typed buffers acceptable by glBufferData.
"""

from typing import Dict, Any, List

try:
    import OpenGL.GL as gl
    import ctypes
except Exception:
    gl = None
    ctypes = None

# Track allocated handles so we can cleanup on shutdown
_ALLOCATED_HANDLES = []


def create_vbo_for_mesh(vertices: List[float], colors: List[float]) -> Dict[str, Any]:
    """Create VBOs for vertex and color arrays and return a small handle dict.

    Returns: {'vbo': int, 'vbo_color': int, 'count': int}
    """
    if not gl:
        raise RuntimeError("PyOpenGL not available")

    # Convert to GLfloat arrays
    vert_count = len(vertices) // 3
    # Create ctypes arrays from Python lists
    GLfloatArrayType = (gl.GLfloat * len(vertices))
    colorArrayType = (gl.GLfloat * len(colors))
    vert_array = GLfloatArrayType(*vertices)
    col_array = colorArrayType(*colors)

    # Create VBO for vertices
    vbo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, ctypes.sizeof(vert_array), vert_array, gl.GL_STATIC_DRAW)

    # Create VBO for colors
    vbo_color = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_color)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, ctypes.sizeof(col_array), col_array, gl.GL_STATIC_DRAW)

    # Unbind
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    handle = {'vbo': vbo, 'vbo_color': vbo_color, 'count': vert_count}
    _ALLOCATED_HANDLES.append(handle)
    return handle


def delete_vbo(handle: Dict[str, Any]) -> None:
    if not gl or not handle:
        return
    try:
        if 'vbo' in handle and handle['vbo']:
            gl.glDeleteBuffers(1, [handle['vbo']])
        if 'vbo_color' in handle and handle['vbo_color']:
            gl.glDeleteBuffers(1, [handle['vbo_color']])
    except Exception:
        pass
    try:
        _ALLOCATED_HANDLES.remove(handle)
    except ValueError:
        pass


def delete_all_vbos() -> None:
    """Delete all allocated VBO handles tracked by this module."""
    if not gl:
        _ALLOCATED_HANDLES.clear()
        return
    for h in list(_ALLOCATED_HANDLES):
        try:
            delete_vbo(h)
        except Exception:
            pass
    _ALLOCATED_HANDLES.clear()
