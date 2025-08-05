"""
Enhanced ECS implementation for simplex-engine.
Provides proper component management and system organization.
"""

from .interface import ECSInterface
from simplex.utils.logger import log
from typing import Dict, List, Set, Optional, Type


class Component:
    """Base class for all components."""
    def __init__(self, name: str):
        self.name = name
        
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"


class Entity:
    """Entity holds components and provides component management."""
    def __init__(self, name: str):
        self.name = name
        self.components: Dict[str, Component] = {}
        self._component_types: Set[str] = set()

    def add_component(self, component: Component) -> None:
        """Add a component to this entity."""
        if not isinstance(component, Component):
            raise TypeError(f"Expected Component, got {type(component)}")
            
        log(f"Adding component {component.name} to entity {self.name}", level="DEBUG")
        self.components[component.name] = component
        self._component_types.add(component.name)

    def get_component(self, name: str) -> Optional[Component]:
        """Get a component by name."""
        return self.components.get(name)
        
    def has_component(self, name: str) -> bool:
        """Check if entity has a component."""
        return name in self._component_types
        
    def has_components(self, *names: str) -> bool:
        """Check if entity has all specified components."""
        return all(name in self._component_types for name in names)

    def remove_component(self, name: str) -> Optional[Component]:
        """Remove and return a component by name."""
        if name in self.components:
            component = self.components.pop(name)
            self._component_types.discard(name)
            log(f"Removed component {name} from entity {self.name}", level="DEBUG")
            return component
        return None
        
    def get_components(self) -> Dict[str, Component]:
        """Get all components on this entity."""
        return self.components.copy()

    def __repr__(self):
        return f"Entity(name='{self.name}', components={list(self._component_types)})"


class System:
    """Base class for all systems with proper entity filtering."""
    def __init__(self, name: str):
        self.name = name
        self.required_components: List[str] = []
        
    def update(self, entities: List[Entity]) -> None:
        """Override in subclass to process entities."""
        # Filter entities that have required components
        filtered_entities = self._filter_entities(entities)
        if filtered_entities:
            self._process_entities(filtered_entities)
    
    def _filter_entities(self, entities: List[Entity]) -> List[Entity]:
        """Filter entities that have all required components."""
        if not self.required_components:
            return entities
        return [entity for entity in entities if entity.has_components(*self.required_components)]
    
    def _process_entities(self, entities: List[Entity]) -> None:
        """Override this method in subclasses instead of update()."""
        pass
        
    def __repr__(self):
        return f"System(name='{self.name}', required_components={self.required_components})"


class ECS(ECSInterface):
    """Enhanced ECS core implementation with proper system management."""
    def __init__(self, event_system=None):
        self.event_system = event_system
        self.entities: List[Entity] = []
        self.systems: List[System] = []
        self._entity_lookup: Dict[str, Entity] = {}
        log("ECS created", level="INFO")

    def add_entity(self, entity) -> None:
        """Add an entity to the ECS."""
        if isinstance(entity, str):
            entity = Entity(entity)
        elif not isinstance(entity, Entity):
            raise TypeError(f"Expected Entity or str, got {type(entity)}")
            
        if entity.name in self._entity_lookup:
            log(f"Entity {entity.name} already exists, replacing", level="WARNING")
            self.remove_entity(entity.name)
            
        log(f"Adding entity: {entity.name}", level="INFO")
        self.entities.append(entity)
        self._entity_lookup[entity.name] = entity

    def add_system(self, system) -> None:
        """Add a system to the ECS."""
        if isinstance(system, str):
            system = System(system)
        elif not isinstance(system, System):
            raise TypeError(f"Expected System or str, got {type(system)}")
            
        log(f"Adding system: {system.name}", level="INFO")
        self.systems.append(system)

    def remove_entity(self, name: str) -> Optional[Entity]:
        """Remove an entity by name."""
        if name in self._entity_lookup:
            entity = self._entity_lookup.pop(name)
            self.entities.remove(entity)
            log(f"Removed entity: {name}", level="INFO")
            return entity
        return None

    def update(self) -> None:
        """Run all systems on filtered entities."""
        for system in self.systems:
            log(f"Running system: {system.name}", level="DEBUG")
            try:
                system.update(self.entities)
            except Exception as e:
                log(f"Error in system {system.name}: {e}", level="ERROR")
                if self.event_system:
                    self.event_system.emit('system_error', {'system': system.name, 'error': str(e)})
    
    def shutdown(self):
        """Clean shutdown of ECS."""
        self.systems.clear()
        self.entities.clear()
        self._entity_lookup.clear()
        log("ECS shutdown", level="INFO")
    
    def get_entities_with(self, *component_names: str) -> List[Entity]:
        """Get entities that have all specified components."""
        return [entity for entity in self.entities if entity.has_components(*component_names)]
    
    def get_entity(self, name: str) -> Optional[Entity]:
        """Get entity by name (O(1) lookup)."""
        return self._entity_lookup.get(name)
        
    def clear(self) -> None:
        """Clear all entities and systems."""
        self.entities.clear()
        self.systems.clear()
        self._entity_lookup.clear()
        log("ECS cleared", level="INFO")
        
    def get_system(self, name: str) -> Optional[System]:
        """Get a system by name."""
        for system in self.systems:
            if system.name == name:
                return system
        return None
    
    def shutdown(self) -> None:
        """Clean shutdown of ECS."""
        self.clear()
        log("ECS shutdown", level="INFO")
        
    def __repr__(self):
        return f"ECS(entities={len(self.entities)}, systems={len(self.systems)})"
