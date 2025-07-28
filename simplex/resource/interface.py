"""
Resource manager interface for simplex-engine.
"""
from abc import ABC, abstractmethod

class ResourceManagerInterface(ABC):
    @abstractmethod
    def load(self, resource_path: str):
        pass

    @abstractmethod
    def unload(self, resource_path: str):
        pass
