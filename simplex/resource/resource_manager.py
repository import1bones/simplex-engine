"""
Minimal ResourceManager implementation for MVP.
"""

from .interface import ResourceManagerInterface
from simplex.utils.logger import log

class ResourceManager(ResourceManagerInterface):
    def reload(self, resource_path: str) -> None:
        """Alias for reload_resource for hot-reloader compatibility."""
        self.reload_resource(resource_path)
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
            self._error_log.append(("reload", resource_path, str(e)))
    """
    Resource manager for simplex-engine MVP.
    Handles asset loading/unloading and error management.
    """
    def __init__(self):
        self._cache = {}
        self._ref_counts = {}
        self._load_count = 0
        self._unload_count = 0
        self._error_log = []  # (action, resource_path, error)

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
            self._load_count += 1
            log(f"Loaded resource: {resource_path}", level="INFO")
        except Exception as e:
            log(f"Resource loading error: {e}", level="ERROR")
            self._error_log.append(("load", resource_path, str(e)))

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
                    self._unload_count += 1
                    log(f"Unloaded resource: {resource_path}", level="INFO")
            else:
                log(f"Resource not loaded: {resource_path}", level="WARNING")
        except Exception as e:
            log(f"Resource unloading error: {e}", level="ERROR")
            self._error_log.append(("unload", resource_path, str(e)))
    def get_usage_analytics(self):
        """Return resource usage statistics and recent errors."""
        return {
            "load_count": self._load_count,
            "unload_count": self._unload_count,
            "cache_size": len(self._cache),
            "ref_counts": dict(self._ref_counts),
            "recent_errors": list(self._error_log[-10:]),
        }
