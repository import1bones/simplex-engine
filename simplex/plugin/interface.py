from abc import ABC, abstractmethod

class PluginInterface(ABC):
    """Base interface for all engine plugins."""
    @abstractmethod
    def on_load(self, engine):
        """Called when the plugin is loaded. Engine instance is passed for integration."""
        pass

    @abstractmethod
    def on_unload(self):
        """Called when the plugin is unloaded."""
        pass
