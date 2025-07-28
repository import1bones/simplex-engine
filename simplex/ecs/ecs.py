"""
Minimal ECS implementation for MVP.
"""

from .interface import ECSInterface
from simplex.utils.logger import log


class Entity:
    def __init__(self, name):
        self.name = name


class System:
    def __init__(self, name):
        self.name = name

class ECS(ECSInterface):
    def __init__(self):
        self.entities = []
        self.systems = []

    def add_entity(self, entity):
        log(f"Adding entity: {entity.name}")
        self.entities.append(entity)

    def add_system(self, system):
        log(f"Adding system: {system.name}")
        self.systems.append(system)
