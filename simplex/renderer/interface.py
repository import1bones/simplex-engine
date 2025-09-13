"""
Renderer interface for simplex-engine.
"""

from abc import ABC, abstractmethod


class RendererInterface(ABC):
    @abstractmethod
    def render(self):
        pass
