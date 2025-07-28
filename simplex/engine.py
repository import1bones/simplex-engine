"""
Engine interface for simplex-engine.
Flexible and maintainable entry point for the engine core.
"""
from .ecs.interface import ECSInterface
from .renderer.interface import RendererInterface
from .physics.interface import PhysicsInterface
from .script.interface import ScriptManagerInterface

class Engine:
    def __init__(self, ecs: ECSInterface, renderer: RendererInterface, physics: PhysicsInterface, script_manager: ScriptManagerInterface):
        self.ecs = ecs
        self.renderer = renderer
        self.physics = physics
        self.script_manager = script_manager

    def run(self):
        """Main loop for the engine."""
        pass
