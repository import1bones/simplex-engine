"""
Physics system interface for simplex-engine.
"""

from abc import ABC, abstractmethod


class PhysicsInterface(ABC):
    @abstractmethod
    def simulate(self):
        pass
