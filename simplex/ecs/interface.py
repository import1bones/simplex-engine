"""
ECS (Entity-Component-System) interface for simplex-engine.
"""

from abc import ABC, abstractmethod


class ECSInterface(ABC):
    @abstractmethod
    def add_entity(self, entity):
        pass

    @abstractmethod
    def add_system(self, system):
        pass
