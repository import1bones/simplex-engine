"""
Engine interface for simplex-engine.
Flexible and maintainable entry point for the engine core.
"""

from .ecs.ecs import ECS
from .renderer.renderer import Renderer
from .physics.physics import Physics
from .script.script_manager import ScriptManager
from .resource.resource_manager import ResourceManager

class Engine:
    def __init__(self):
        self.ecs = ECS()
        self.renderer = Renderer()
        self.physics = Physics()
        self.script_manager = ScriptManager()
        self.resource_manager = ResourceManager()

    def run(self):
        """Main loop for the engine MVP."""
        print("Engine starting...")
        self.resource_manager.load("example_resource")
        self.ecs.add_entity("Player")
        self.ecs.add_system("MovementSystem")
        self.script_manager.execute()
        self.physics.simulate()
        self.renderer.render()
        print("Engine stopped.")
