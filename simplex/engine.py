"""
Engine interface for simplex-engine.
Flexible and maintainable entry point for the engine core with proper subsystem coordination.
"""

from typing import Optional, Dict, Any
from .ecs.ecs import ECS
from .renderer.renderer import Renderer
from .physics.physics import Physics
from .script.script_manager import ScriptManager
from .resource.resource_manager import ResourceManager
from .audio.audio import Audio
from .event.event_system import EventSystem
from .config import Config
from .input.input import Input
from .utils.logger import log


class Engine:
    """
    Main engine coordinator that manages all subsystems with proper initialization order
    and dependency injection. Provides a unified interface for game development.
    """

    def __init__(self, config_path: str = "examples/config.toml"):
        self._running = False
        self._initialized = False

        # Phase 1: Core systems initialization (no dependencies)
        self.config = Config(config_path)
        self.events = EventSystem()

        # Phase 2: Primary subsystems (depend on core systems)
        self.ecs = ECS(event_system=self.events)
        self.resource_manager = ResourceManager()

        # Phase 3: Secondary subsystems (may depend on primary systems)
        self.renderer = Renderer(
            event_system=self.events, resource_manager=self.resource_manager
        )
        self.physics = Physics(event_system=self.events, ecs=self.ecs)
        self.audio = Audio(
            event_system=self.events, resource_manager=self.resource_manager
        )
        self.script_manager = ScriptManager(event_system=self.events, engine=self)
        self.input = Input(backend="pygame", event_system=self.events)

        # Phase 4: System integration and event wiring
        self._initialize_subsystems()
        self._setup_event_handlers()
        self._setup_hot_reloading(config_path)

        self._initialized = True
        log("Engine initialized successfully", level="INFO")

    def _initialize_subsystems(self):
        """Initialize subsystems with proper dependency injection."""
        # Initialize ECS with common game systems
        from .ecs.systems import (
            MovementSystem,
            CollisionSystem,
            InputSystem,
            ScoringSystem,
        )

        # Get bounds from config
        bounds = (
            self.config.get("renderer", {}).get("width", 800),
            self.config.get("renderer", {}).get("height", 600),
        )

        # Register core ECS systems
        movement_system = MovementSystem(event_system=self.events, bounds=bounds)
        collision_system = CollisionSystem(event_system=self.events, bounds=bounds)
        input_system = InputSystem(event_system=self.events)
        scoring_system = ScoringSystem(event_system=self.events, bounds=bounds)

        self.ecs.add_system(movement_system)
        self.ecs.add_system(collision_system)
        self.ecs.add_system(input_system)
        self.ecs.add_system(scoring_system)

        # Register chunk systems for voxel world support (creates chunks and generates meshes)
        try:
            from .ecs.chunk_system import ChunkSystem, ChunkMeshSystem

            chunk_system = ChunkSystem(event_system=self.events)
            chunk_mesh_system = ChunkMeshSystem(event_system=self.events)
            self.ecs.add_system(chunk_system)
            self.ecs.add_system(chunk_mesh_system)
            log("Engine: Chunk systems registered", level="INFO")
        except Exception as e:
            log(f"Engine: Failed to register chunk systems: {e}", level="WARNING")

        # Initialize renderer with config
        renderer_config = self.config.get("renderer", {})
        # Default to OpenGL backend for 3D/voxel support
        if "backend" not in renderer_config:
            renderer_config["backend"] = "opengl"
        if renderer_config.get("enabled", True):
            self.renderer.initialize(renderer_config)

        # Initialize physics with config
        physics_config = self.config.get("physics", {})
        if physics_config.get("enabled", True):
            self.physics.initialize(physics_config)

    def _setup_event_handlers(self):
        """Set up event handlers for cross-system communication."""
        # Input event forwarding
        self.events.register("input", self._handle_input_event)

        # Physics collision events
        self.events.register("physics_collision", self._handle_physics_collision)

        # Score events
        self.events.register("score", self._handle_score_event)

        # System lifecycle events
        self.events.register("system_error", self._handle_system_error)

    def _handle_input_event(self, event):
        """Handle input events and forward to appropriate systems."""
        try:
            # Forward to ECS input systems
            for system in self.ecs.systems:
                if hasattr(system, "_handle_input_event"):
                    system._handle_input_event(event)
        except Exception as e:
            log(f"Error handling input event: {e}", level="ERROR")

    def _handle_physics_collision(self, event):
        """Handle physics collision events."""
        try:
            if isinstance(event, dict):
                if (
                    event.get("type") == "boundary"
                    and "ball" in event.get("entity", "").lower()
                ):
                    # Ball hit boundary - handle scoring or bouncing
                    if event.get("side") in ["left", "right"]:
                        # Potential scoring event
                        self.events.emit("potential_score", event)
                elif event.get("type") == "entity":
                    # Entity collision - handle ball paddle collision
                    entities = [event.get("entity_a"), event.get("entity_b")]
                    if any("ball" in str(e).lower() for e in entities) and any(
                        "paddle" in str(e).lower() for e in entities
                    ):
                        self.events.emit("ball_paddle_collision", event)
        except Exception as e:
            log(f"Error handling physics collision: {e}", level="ERROR")

    def _handle_score_event(self, event):
        """Handle scoring events."""
        try:
            if isinstance(event, dict) and "scorer" in event:
                log(
                    f"Score Event: {event['scorer']} scored! Current score: {event.get('score', {})}",
                    level="INFO",
                )
                # Emit to other systems that might care about scoring
                self.events.emit("game_score_update", event)
        except Exception as e:
            log(f"Error handling score event: {e}", level="ERROR")

    def _handle_system_error(self, event):
        """Handle system error events."""
        if isinstance(event, dict):
            system_name = event.get("system", "Unknown")
            error = event.get("error", "Unknown error")
            log(f"System Error in {system_name}: {error}", level="ERROR")

    def _setup_hot_reloading(self, config_path):
        """Set up hot-reloading features if available."""
        try:
            # Script plugin registration
            try:
                from examples.mvp.scripts.plugin_example import script_event_logger

                self.script_manager.on("on_load", script_event_logger)
                self.script_manager.on("on_reload", script_event_logger)
            except ImportError:
                log("Script plugin not found, skipping", level="DEBUG")

            # Resource hot-reloader
            try:
                from simplex.resource.resource_hot_reloader import ResourceHotReloader

                demo_resource = self.config.get("demo_resource", "example_resource")
                demo_sound = self.config.get("audio", {}).get(
                    "demo_sound", "examples/mvp/demo_sound.wav"
                )
                self.resource_hot_reloader = ResourceHotReloader(
                    self.resource_manager,
                    watch_paths=[demo_resource, demo_sound],
                    poll_interval=1.0,
                )
            except ImportError:
                log("ResourceHotReloader not available", level="DEBUG")

            # Config hot-reloader
            try:
                from simplex.config.config_hot_reloader import ConfigHotReloader

                self.config_hot_reloader = ConfigHotReloader(
                    self.config,
                    config_path,
                    event_system=self.events,
                    poll_interval=1.0,
                )
            except ImportError:
                log("ConfigHotReloader not available", level="DEBUG")

        except Exception as e:
            log(f"Hot-reloading setup failed: {e}", level="DEBUG")

    def update(self, delta_time: float = 0.016):
        """
        Update all engine subsystems in the correct order.

        Args:
            delta_time: Time elapsed since last update in seconds
        """
        if not self._initialized:
            log("Engine not initialized, cannot update", level="WARNING")
            return

        try:
            # Update order is important for proper data flow
            # 1. Input processing
            self.input.poll()

            # 2. Script updates (may modify entities)
            self.script_manager.update(delta_time)

            # 3. ECS systems update (game logic)
            self.ecs.update()

            # 4. Physics simulation
            self.physics.simulate()

            # 5. Audio processing
            self.audio.update(delta_time)

            # 6. Rendering (should be last)
            self.renderer.render()

            # 7. Hot-reload checks (development only)
            if hasattr(self, "resource_hot_reloader"):
                self.resource_hot_reloader.run_once()
            if hasattr(self, "config_hot_reloader"):
                self.config_hot_reloader.run_once()

        except Exception as e:
            log(f"Engine update error: {e}", level="ERROR")
            self.events.emit("system_error", {"system": "Engine", "error": str(e)})

    def run(self):
        """
        Main loop for the engine - basic MVP implementation.
        For production games, use update() in a proper game loop.
        """
        if not self._initialized:
            log("Engine not initialized, cannot run", level="ERROR")
            return

        log("Engine starting...", level="INFO")
        self._running = True

        try:
            # Example: use configuration
            demo_resource = self.config.get("demo_resource", "example_resource")
            self.resource_manager.load(demo_resource)

            # Example ECS usage
            self.ecs.add_entity("Player")
            self.ecs.add_system("MovementSystem")

            # Run one update cycle for MVP demonstration
            self.update()

            # Audio demo: load and play a sound if enabled in config
            audio_enabled = self.config.get("audio", {}).get("enabled", False)
            if audio_enabled:
                sound_path = self.config.get("audio", {}).get(
                    "demo_sound", "examples/mvp/demo_sound.wav"
                )
                self.audio.load(sound_path)
                self.audio.play(sound_path)

            # Hot-reload demo script (edit examples/mvp/demo_script.py to test)
            self.script_manager.hot_reload()

            log("Engine MVP cycle completed", level="INFO")

        except Exception as e:
            log(f"Engine run error: {e}", level="ERROR")
        finally:
            self._running = False
            log("Engine stopped", level="INFO")

    def shutdown(self):
        """Clean shutdown of all engine subsystems."""
        if not self._initialized:
            return

        log("Engine shutting down...", level="INFO")
        self._running = False

        try:
            # Shutdown in reverse order of initialization
            if hasattr(self, "input"):
                self.input.shutdown()
            if hasattr(self, "renderer"):
                self.renderer.shutdown()
            if hasattr(self, "physics"):
                self.physics.shutdown()
            if hasattr(self, "audio"):
                self.audio.shutdown()
            if hasattr(self, "script_manager"):
                self.script_manager.shutdown()
            if hasattr(self, "ecs"):
                self.ecs.shutdown()
            if hasattr(self, "events"):
                self.events.shutdown()

        except Exception as e:
            log(f"Error during engine shutdown: {e}", level="ERROR")
        finally:
            self._initialized = False
            log("Engine shutdown complete", level="INFO")

    @property
    def is_running(self) -> bool:
        """Check if engine is currently running."""
        return self._running

    @property
    def is_initialized(self) -> bool:
        """Check if engine is properly initialized."""
        return self._initialized
