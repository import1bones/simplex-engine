"""
Minimal ResourceManager implementation for MVP.
"""

from .interface import ResourceManagerInterface
from simplex.utils.logger import log

class ResourceManager(ResourceManagerInterface):
    def reload_resource(self, resource_path: str) -> None:
        """
        Reload a resource if it supports hot-reloading.
        """
        try:
            resource = self._cache.get(resource_path)
            if resource and hasattr(resource, 'reload'):
                resource.reload()
                log(f"Hot-reloaded resource: {resource_path}", level="INFO")
            else:
                log(f"Resource not hot-reloadable: {resource_path}", level="WARNING")
        except Exception as e:
            log(f"Resource reload error: {e}", level="ERROR")
    """
    Resource manager for simplex-engine MVP.
    Handles asset loading/unloading and error management.
    """
    def __init__(self):
        self._cache = {}
        self._ref_counts = {}

    def load(self, resource_path: str) -> None:
        """
        Load a resource by path. Implements caching and reference counting.
        """
        try:
            if resource_path in self._cache:
                self._ref_counts[resource_path] += 1
                log(f"Resource already loaded (refcount {self._ref_counts[resource_path]}): {resource_path}", level="INFO")
                return
            # Example: load shader resource if .glsl or .shader extension
            if resource_path.endswith('.glsl') or resource_path.endswith('.shader'):
                from .shader_resource import ShaderResource
                resource = ShaderResource(resource_path)
                resource.load()
            else:
                resource = f"Loaded({resource_path})"  # Replace with actual resource object
            self._cache[resource_path] = resource
            self._ref_counts[resource_path] = 1
            log(f"Loaded resource: {resource_path}", level="INFO")
        except Exception as e:
            log(f"Resource loading error: {e}", level="ERROR")

    def unload(self, resource_path: str) -> None:
        """
        Unload a resource by path. Decrements refcount and removes from cache if needed.
        """
        try:
            if resource_path in self._ref_counts:
                self._ref_counts[resource_path] -= 1
                log(f"Decremented refcount for {resource_path}: {self._ref_counts[resource_path]}", level="INFO")
                if self._ref_counts[resource_path] <= 0:
                    del self._cache[resource_path]
                    del self._ref_counts[resource_path]
                    log(f"Unloaded resource: {resource_path}", level="INFO")
            else:
                log(f"Resource not loaded: {resource_path}", level="WARNING")
        except Exception as e:
            log(f"Resource unloading error: {e}", level="ERROR")
