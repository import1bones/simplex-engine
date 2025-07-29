import importlib.util
import os
from .interface import PluginInterface

class PluginManager:
    """Discovers and loads plugins from a directory."""
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = []

    def discover_and_load(self, engine):
        if not os.path.isdir(self.plugin_dir):
            return
        for fname in os.listdir(self.plugin_dir):
            if fname.endswith(".py") and not fname.startswith("__"):
                path = os.path.join(self.plugin_dir, fname)
                spec = importlib.util.spec_from_file_location(fname[:-3], path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, PluginInterface) and obj is not PluginInterface:
                        plugin = obj()
                        plugin.on_load(engine)
                        self.plugins.append(plugin)

    def unload_all(self):
        for plugin in self.plugins:
            plugin.on_unload()
        self.plugins.clear()
