"""
Minimal ResourceManager implementation for MVP.
"""

from .interface import ResourceManagerInterface
from simplex.utils.logger import log

class ResourceManager(ResourceManagerInterface):
    """
    Resource manager for simplex-engine MVP.
    Handles asset loading/unloading and error management.
    """
    def load(self, resource_path: str) -> None:
        """
        Load a resource by path. Logs at INFO level and handles errors.
        """
        try:
            log(f"Loading resource: {resource_path}", level="INFO")
            # Future: actual resource loading logic
        except Exception as e:
            log(f"Resource loading error: {e}", level="ERROR")

    def unload(self, resource_path: str) -> None:
        """
        Unload a resource by path. Logs at INFO level and handles errors.
        """
        try:
            log(f"Unloading resource: {resource_path}", level="INFO")
            # Future: actual resource unloading logic
        except Exception as e:
            log(f"Resource unloading error: {e}", level="ERROR")
