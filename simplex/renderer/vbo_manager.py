"""VBOManager: central VBO handle manager for the engine.

Provides a small API used by renderers to create/delete VBOs and guarantees
cleanup on shutdown. Uses helpers from gl_utils when available.
"""
from typing import Any, Dict, List, Optional


class VBOManager:
    def __init__(self, helpers: Optional[Dict[str, Any]] = None):
        # helpers expected to be {'create_vbo_for_mesh': func, 'delete_vbo': func}
        self.helpers = helpers or {}
        self._handles: List[Dict[str, Any]] = []

    def create_vbo(self, vertices: List[float], colors: List[float]) -> Optional[Dict[str, Any]]:
        """Create a VBO for the provided mesh data and track the handle.

        Returns the handle dict from create_vbo_for_mesh or None on failure.
        """
        create_fn = self.helpers.get('create_vbo_for_mesh')
        if not create_fn:
            return None
        try:
            handle = create_fn(vertices, colors)
            if handle:
                self._handles.append(handle)
            return handle
        except Exception:
            return None

    def delete_vbo(self, handle: Dict[str, Any]) -> None:
        """Delete a single VBO handle using the helper and remove it from tracking."""
        delete_fn = self.helpers.get('delete_vbo')
        if not delete_fn or not handle:
            return
        try:
            delete_fn(handle)
        except Exception:
            pass
        try:
            self._handles.remove(handle)
        except ValueError:
            pass

    def delete_all(self) -> None:
        """Delete all tracked VBOs."""
        delete_fn = self.helpers.get('delete_vbo')
        if not delete_fn:
            self._handles.clear()
            return
        for h in list(self._handles):
            try:
                delete_fn(h)
            except Exception:
                pass
        self._handles.clear()

    def shutdown(self) -> None:
        """Alias for cleanup on engine shutdown."""
        self.delete_all()
