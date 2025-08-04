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
        # Initialize core systems first
        self.config = Config(config_path)
        self.events = EventSystem()  # Initialize event system first
        
        # Initialize subsystems with event system available
        self.ecs = ECS()
        self.renderer = Renderer()
        self.physics = Physics()
        self.script_manager = ScriptManager()
        self.resource_manager = ResourceManager()
        self.audio = Audio()
        self.input = Input(backend="pygame", event_system=self.events)
        
        # Register core event handlers
        self.events.register('input', self._handle_input_event)
        
        # Initialize optional hot-reloading features
        self._setup_hot_reloading(config_path)
        
    def _handle_input_event(self, data):
        """Default input event handler."""
        # This can be overridden by game-specific logic
        pass
        
    def _setup_hot_reloading(self, config_path):
        """Set up hot-reloading features if available."""
        # Script plugin registration
        try:
            from examples.mvp.scripts.plugin_example import script_event_logger
            self.script_manager.on("on_load", script_event_logger)
            self.script_manager.on("on_reload", script_event_logger)
        except Exception as e:
            from simplex.utils.logger import log
            log(f"Script plugin registration failed: {e}", level="DEBUG")
            
        # Resource hot-reloader
        try:
            from simplex.resource.resource_hot_reloader import ResourceHotReloader
            demo_resource = self.config.get("demo_resource", "example_resource")
            demo_sound = self.config.get("audio", {}).get("demo_sound", "examples/mvp/demo_sound.wav")
            self.resource_hot_reloader = ResourceHotReloader(
                self.resource_manager,
                watch_paths=[demo_resource, demo_sound],
                poll_interval=1.0
            )
        except Exception as e:
            from simplex.utils.logger import log
            log(f"ResourceHotReloader initialization failed: {e}", level="DEBUG")
            
        # Config hot-reloader
        try:
            from simplex.config.config_hot_reloader import ConfigHotReloader
            self.config_hot_reloader = ConfigHotReloader(
                self.config,
                config_path,
                event_system=self.events,
                poll_interval=1.0
            )
        except Exception as e:
            from simplex.utils.logger import log
            log(f"ConfigHotReloader initialization failed: {e}", level="DEBUG")

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
        self.script_manager.hot_reload()

        # Resource hot-reload demo (edit demo resource or sound to test)
        if hasattr(self, "resource_hot_reloader"):
            self.resource_hot_reloader.run_once()

        # Config hot-reload demo (edit config file to test)
        if hasattr(self, "config_hot_reloader"):
            self.config_hot_reloader.run_once()

        # Poll input and handle events (would be in a loop in a real engine)
        self.input.poll()

        print("Engine stopped.")
