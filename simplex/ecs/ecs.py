"""
Minimal ECS implementation for MVP.
"""

from .interface import ECSInterface
from simplex.utils.logger import log



class Component:
    """Base class for all components."""
    def __init__(self, name):
        self.name = name

class Entity:
    """Entity holds components."""
    def __init__(self, name):
        self.name = name
        self.components = {}

    def add_component(self, component):
        log(f"Adding component {component.name} to entity {self.name}")
        self.components[component.name] = component

    def get_component(self, name):
        return self.components.get(name)



class System:
    """Base class for all systems."""
    def __init__(self, name):
        self.name = name
    def update(self, entities):
        """Override in subclass to process entities."""
        pass


class ECS(ECSInterface):
    """ECS core implementation."""
    def __init__(self):
        self.entities = []
        self.systems = []

    def add_entity(self, entity):
        if isinstance(entity, str):
            entity = Entity(entity)
        log(f"Adding entity: {entity.name}")
        self.entities.append(entity)

    def add_system(self, system):
        if isinstance(system, str):
            system = System(system)
        log(f"Adding system: {system.name}")
        self.systems.append(system)

    def update(self):
        """Run all systems on all entities."""
        for system in self.systems:
            log(f"Running system: {system.name}")
            system.update(self.entities)
    
    def get_entities_with(self, *component_names):
        """Get entities that have all specified components."""
        result = []
        for entity in self.entities:
            if all(entity.get_component(name) for name in component_names):
                result.append(entity)
        return result
    
    def get_entity(self, name):
        """Get entity by name."""
        for entity in self.entities:
            if entity.name == name:
                return entity
        return None
