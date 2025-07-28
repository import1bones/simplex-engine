"""
Script manager interface for simplex-engine.
"""
from abc import ABC, abstractmethod

class ScriptManagerInterface(ABC):
    @abstractmethod
    def execute(self):
        pass
