"""Subsystem manager for the Simplex engine.

Provides a small factory registry that can create subsystems in dependency order
and attach them to the engine instance. Designed to be simple and easy to test.
"""

from typing import Callable, Dict, List


class SubsystemManager:
    def __init__(self, engine):
        self.engine = engine
        # name -> (factory, requires)
        self._registry: Dict[str, tuple[Callable, List[str]]] = {}
        # set of created subsystem names
        self._created = {}

    def register_factory(self, name: str, factory: Callable, requires: List[str] = None):
        if requires is None:
            requires = []
        self._registry[name] = (factory, list(requires))

    def created(self):
        return set(self._created.keys())

    def ensure(self, name: str):
        """Ensure a subsystem with the given name exists. Create dependencies first.

        Raises KeyError if no factory registered for the name. Raises RuntimeError
        on cyclic/self dependencies.
        Returns the created instance.
        """
        if name in self._created:
            return self._created[name]

        if name not in self._registry:
            raise KeyError(f"No factory registered for '{name}'")

        # detect cycles using recursion stack
        creating = set()

        def _create(n: str):
            if n in self._created:
                return self._created[n]
            if n not in self._registry:
                raise KeyError(f"No factory registered for '{n}'")
            if n in creating:
                raise RuntimeError(f"Cyclic dependency detected for '{n}'")
            creating.add(n)
            factory, deps = self._registry[n]
            # ensure dependencies
            for d in deps:
                _create(d)
            # call factory with engine argument
            inst = factory(self.engine)
            # attach to engine attribute
            try:
                setattr(self.engine, n, inst)
            except Exception:
                pass
            self._created[n] = inst
            creating.remove(n)
            return inst

        return _create(name)

    def initialize_all(self):
        # create all registered factories in an order satisfying dependencies
        for name in list(self._registry.keys()):
            self.ensure(name)
