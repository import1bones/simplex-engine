"""
Engine interface for simplex-engine.
Flexible and maintainable entry point for the engine core.
"""

from .ecs.ecs import ECS
from .renderer.renderer import Renderer
from .physics.physics import Physics
from .script.script_manager import ScriptManager
from .resource.resource_manager import ResourceManager
from .audio.audio import Audio
from .event.event_system import EventSystem
from .config import Config


from .input.input import Input

class Engine:
    def __init__(self, config_path: str = "examples/config.toml"):
        self.config = Config(config_path)
        self.ecs = ECS()
        self.renderer = Renderer()
        self.physics = Physics()
        self.script_manager = ScriptManager()
        self.resource_manager = ResourceManager()
        self.audio = Audio()
        self.events = EventSystem()
        self.input = Input(backend="pygame", event_system=self.events)

        # Register an event listener for 'input'
        self.events.register('input', self.handle_input_event)

    def handle_input_event(self, data):
        # Example handler for input events
        print(f"Input event received: {data}")

    def run(self):
        """Main loop for the engine MVP-2."""
        print("Engine starting...")
        # Example: use configuration
        demo_resource = self.config.get("demo_resource", "example_resource")
        self.resource_manager.load(demo_resource)
        self.ecs.add_entity("Player")
        self.ecs.add_system("MovementSystem")
        self.script_manager.execute()
        self.physics.simulate()
        self.renderer.render()

        # Audio demo: load and play a sound if enabled in config
        audio_enabled = self.config.get("audio", {}).get("enabled", False)
        if audio_enabled:
            sound_path = self.config.get("audio", {}).get("demo_sound", "examples/mvp/demo_sound.wav")
            self.audio.load(sound_path)
            self.audio.play(sound_path)

        # Hot-reload demo script (edit examples/mvp/demo_script.py to test)
        self.script_manager.hot_reload("examples/mvp/demo_script.py")

        # Poll input and handle events (would be in a loop in a real engine)
        self.input.poll()

        print("Engine stopped.")
