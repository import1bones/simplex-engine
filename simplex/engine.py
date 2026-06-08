"""
Engine interface for simplex-engine.
Flexible and maintainable entry point for the engine core with proper subsystem coordination.
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
from .scheduler.manager import SubsystemManager
from .utils.logger import log


class Engine:
    """
    Main engine coordinator that manages all subsystems with proper initialization order
    and dependency injection. Provides a unified interface for game development.
    """

    def __init__(self, config_path: str = "examples/config.toml"):
        self._running = False
        self._initialized = False
        # pending mesh uploads (entity, mesh_comp) queued until VBO manager/context ready
        self._pending_mesh_uploads = []

        # Phase 1: Core systems initialization (no dependencies)
        self.config = Config(config_path)

        # Create scheduler to manage subsystem factories
        self.scheduler = SubsystemManager(self)

        # Register common subsystem factories (idempotent)
        self.scheduler.register_factory('events', lambda eng: EventSystem(), requires=[])
        self.scheduler.register_factory('ecs', lambda eng: ECS(event_system=getattr(eng, 'events', None) or EventSystem()), requires=['events'])
        self.scheduler.register_factory('resource_manager', lambda eng: ResourceManager(), requires=[])
        self.scheduler.register_factory('renderer', lambda eng: Renderer(event_system=getattr(eng, 'events', None) or EventSystem(), resource_manager=getattr(eng, 'resource_manager', None) or ResourceManager()), requires=['events','resource_manager'])
        self.scheduler.register_factory('physics', lambda eng: Physics(event_system=getattr(eng, 'events', None) or EventSystem(), ecs=getattr(eng, 'ecs', None) or ECS()), requires=['events','ecs'])
        self.scheduler.register_factory('audio', lambda eng: Audio(event_system=getattr(eng, 'events', None) or EventSystem(), resource_manager=getattr(eng, 'resource_manager', None) or ResourceManager()), requires=['events','resource_manager'])
        self.scheduler.register_factory('script_manager', lambda eng: ScriptManager(event_system=getattr(eng, 'events', None) or EventSystem(), engine=eng), requires=['events'])
        self.scheduler.register_factory('input', lambda eng: Input(backend='pygame', event_system=getattr(eng, 'events', None) or EventSystem()), requires=['events'])

        # Register optional subsystems: ChunkManager (world streaming) and VBO helpers
        def _make_chunk_manager(eng):
            try:
                from simplex.world.chunk_manager import ChunkManager
                return ChunkManager(eng.ecs, event_system=getattr(eng, 'events', None), chunk_size=(16,16,16), cache_size=64)
            except Exception:
                return None

        def _make_vbo_helpers(eng):
            try:
                from simplex.renderer.gl_utils import create_vbo_for_mesh, delete_vbo
                return {'create_vbo_for_mesh': create_vbo_for_mesh, 'delete_vbo': delete_vbo}
            except Exception:
                return None

        self.scheduler.register_factory('chunk_manager', _make_chunk_manager, requires=['ecs','events'])
        self.scheduler.register_factory('vbo_helpers', _make_vbo_helpers, requires=['renderer'])

        # VBOManager factory: depends on vbo_helpers (so renderer initialization must happen first)
        def _make_vbo_manager(eng):
            try:
                from simplex.renderer.vbo_manager import VBOManager
                helpers = getattr(eng, 'vbo_helpers', None) or {}
                return VBOManager(helpers=helpers)
            except Exception:
                return None

        self.scheduler.register_factory('vbo_manager', _make_vbo_manager, requires=['vbo_helpers'])

        # Initialize registered subsystems (will attach engine.events, engine.ecs, etc.)
        self.scheduler.initialize_all()

        # For backward compatibility if scheduler didn't create them, fall back to explicit creation
        self.events = getattr(self, 'events', EventSystem())
        self.ecs = getattr(self, 'ecs', ECS(event_system=self.events))
        self.resource_manager = getattr(self, 'resource_manager', ResourceManager())
        self.renderer = getattr(self, 'renderer', Renderer(event_system=self.events, resource_manager=self.resource_manager))
        self.physics = getattr(self, 'physics', Physics(event_system=self.events, ecs=self.ecs))
        self.audio = getattr(self, 'audio', Audio(event_system=self.events, resource_manager=self.resource_manager))
        self.script_manager = getattr(self, 'script_manager', ScriptManager(event_system=self.events, engine=self))
        self.input = getattr(self, 'input', Input(backend='pygame', event_system=self.events))

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
        input_system = InputSystem(event_system=self.events, bounds=bounds)
        scoring_system = ScoringSystem(event_system=self.events, bounds=bounds)

        self.ecs.add_system(movement_system)
        self.ecs.add_system(collision_system)
        self.ecs.add_system(input_system)
        self.ecs.add_system(scoring_system)

        # Register player controller (first-person)
        try:
            from simplex.ecs.player_system import FirstPersonController

            player_ctrl = FirstPersonController(event_system=self.events, engine=self)
            self.ecs.add_system(player_ctrl)
            log("Engine: Player controller registered", level="INFO")
        except Exception:
            log("Engine: Player controller not available", level="DEBUG")

        # Voxel collision + chunk streaming (after player movement)
        world_config = self.config.get("world", {})
        streaming_radius = int(world_config.get("streaming_radius", 1))
        horizontal_streaming = bool(world_config.get("horizontal_streaming", True))
        try:
            from simplex.ecs.voxel_collision_system import VoxelCollisionSystem
            from simplex.ecs.chunk_streaming_system import ChunkStreamingSystem

            self.ecs.add_system(VoxelCollisionSystem(event_system=self.events, engine=self))
            self.ecs.add_system(
                ChunkStreamingSystem(
                    event_system=self.events,
                    engine=self,
                    radius=streaming_radius,
                    horizontal_only=horizontal_streaming,
                )
            )
            log("Engine: Voxel collision and chunk streaming registered", level="INFO")
        except Exception as e:
            log(f"Engine: Failed to register voxel systems: {e}", level="WARNING")

        # Register chunk systems for voxel world support (creates chunks and generates meshes)
        try:
            from .ecs.chunk_system import ChunkSystem, ChunkMeshSystem

            mesh_budget = int(world_config.get("mesh_chunks_per_frame", 2))
            chunk_system = ChunkSystem(event_system=self.events)
            chunk_mesh_system = ChunkMeshSystem(
                event_system=self.events,
                max_chunks_per_frame=mesh_budget,
            )
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

            # Ensure VBO helpers are available after renderer (OpenGL) initialization
            try:
                if getattr(self, 'vbo_helpers', None) is None:
                    try:
                        vh = self.scheduler.ensure('vbo_helpers')
                        if vh:
                            self.vbo_helpers = vh
                            # also attach helpers to opengl renderer if present
                            if hasattr(self.renderer, 'opengl_renderer'):
                                try:
                                    self.renderer.opengl_renderer.vbo_helpers = vh
                                except Exception:
                                    pass
                            log("Engine: VBO helpers attached", level="INFO")
                    except KeyError:
                        # factory not registered or available; skip
                        pass
            except Exception:
                pass

        # Initialize physics with config
        physics_config = self.config.get("physics", {})
        if physics_config.get("enabled", True):
            self.physics.initialize(physics_config)

        # Expose ECS to renderer so renderer backends can draw ECS-attached meshes
        try:
            # Renderer may choose to read self.renderer.ecs when rendering
            self.renderer.ecs = self.ecs
            # If OpenGL renderer exists, also attach ECS reference there
            if hasattr(self.renderer, "opengl_renderer"):
                try:
                    self.renderer.opengl_renderer.ecs = self.ecs
                    # expose engine to opengl renderer for accessing vbo helpers
                    try:
                        self.renderer.opengl_renderer.engine = self
                    except Exception:
                        pass
                    # attach vbo_manager to opengl renderer if available
                    try:
                        if getattr(self, 'vbo_manager', None) is None:
                            try:
                                vm = self.scheduler.ensure('vbo_manager')
                                if vm:
                                    self.vbo_manager = vm
                            except Exception:
                                vm = None
                        if getattr(self, 'vbo_manager', None) and hasattr(self.renderer, 'opengl_renderer'):
                            try:
                                self.renderer.opengl_renderer.vbo_manager = self.vbo_manager
                                # Process any pending uploads immediately now that a VBO manager is present
                                try:
                                    self._process_pending_mesh_uploads()
                                    log("Engine: Processed pending mesh uploads after attaching VBO manager", level="DEBUG")
                                except Exception:
                                    pass
                            except Exception:
                                pass
                    except Exception:
                        pass
                except Exception:
                    pass
        except Exception:
            pass

        # ChunkManager should be provided by the scheduler if available; preserve
        # backward compatibility by leaving existing attribute if not created.
        self.chunk_manager = getattr(self, 'chunk_manager', None)
        if self.chunk_manager is not None:
            log("Engine: ChunkManager initialized (from scheduler)", level="INFO")
        else:
            log("Engine: ChunkManager not available", level="DEBUG")

    def _setup_event_handlers(self):
        """Set up event handlers for cross-system communication."""
        # Input event forwarding
        self.events.register("input", self._handle_input_event)

        # Mesh generated events: attempt GPU upload via VBO manager when available
        self.events.register("mesh_generated", self._handle_mesh_generated)

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
                    level="DEBUG",
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

    def _handle_mesh_generated(self, event):
        """Attempt to upload a mesh to GPU when a mesh is generated.

        If a VBO manager is available and renderer/context is ready, upload
        immediately and attach the GPU handle to the MeshComponent. Otherwise
        queue the mesh for later upload.
        """
        try:
            if not isinstance(event, dict):
                return
            mesh_comp = event.get("mesh")
            entity = event.get("entity")
            if not mesh_comp:
                return

            # Try immediate upload via vbo_manager
            vm = getattr(self, 'vbo_manager', None) or getattr(self.renderer, 'vbo_manager', None) or None
            if vm is not None:
                try:
                    handle = vm.create_vbo(mesh_comp.vertices, mesh_comp.colors)
                    if handle:
                        mesh_comp.gpu = handle
                        # log successful upload
                        log(f"Engine: Uploaded mesh for entity {getattr(entity, 'name', entity)} to GPU", level="DEBUG")
                        return
                except Exception as e:
                    log(f"Engine: VBO upload failed: {e}", level="DEBUG")

            # Not uploaded: queue for later processing
            self._pending_mesh_uploads.append((entity, mesh_comp))
            log("Engine: Queued mesh for later GPU upload", level="DEBUG")
        except Exception as e:
            log(f"Engine: mesh_generated handler error: {e}", level="DEBUG")

    def _process_pending_mesh_uploads(self):
        """Process any queued mesh uploads if a VBO manager becomes available."""
        if not self._pending_mesh_uploads:
            return
        vm = getattr(self, 'vbo_manager', None) or getattr(self.renderer, 'vbo_manager', None) or None
        if vm is None:
            return
        remaining = []
        for entity, mesh_comp in list(self._pending_mesh_uploads):
            try:
                handle = vm.create_vbo(mesh_comp.vertices, mesh_comp.colors)
                if handle:
                    mesh_comp.gpu = handle
                    log(f"Engine: Uploaded queued mesh for entity {getattr(entity, 'name', entity)} to GPU", level="DEBUG")
                else:
                    remaining.append((entity, mesh_comp))
            except Exception:
                remaining.append((entity, mesh_comp))
        self._pending_mesh_uploads = remaining

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

    def get_opengl_renderer(self):
        """Return the active OpenGLRenderer (facade child or direct attachment)."""
        renderer = getattr(self, "renderer", None)
        if renderer is None:
            return None
        ogl = getattr(renderer, "opengl_renderer", None)
        if ogl is not None:
            return ogl
        try:
            from .renderer.opengl_renderer import OpenGLRenderer

            if isinstance(renderer, OpenGLRenderer):
                return renderer
        except Exception:
            pass
        return None

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
            self._last_delta_time = delta_time
            # Update order is important for proper data flow
            # 1. Input processing (OpenGL renderer owns pygame display + events)
            ogl = self.get_opengl_renderer()
            if ogl and getattr(ogl, "initialized", False):
                if not ogl._poll_input_events():
                    return
            else:
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
            # Sync camera_follow to renderer camera before rendering
            try:
                if getattr(self, 'camera_follow', None) is not None:
                    try:
                        # Prefer renderer API to set camera
                        if hasattr(self.renderer, 'set_camera'):
                            self.renderer.set_camera(self.camera_follow)
                    except Exception:
                        pass
            except Exception:
                pass

            self.renderer.render()

            # 7. Hot-reload checks (development only)
            if hasattr(self, "resource_hot_reloader"):
                self.resource_hot_reloader.run_once()
            if hasattr(self, "config_hot_reloader"):
                self.config_hot_reloader.run_once()

            # Process any pending mesh uploads after main update
            self._process_pending_mesh_uploads()

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

    def spawn_chunk(self, position=(0, 0, 0), size=(16, 16, 16)):
        """Convenience method: create a chunk entity and add it to ECS.

        Returns the created Entity instance.
        """
        try:
            from simplex.ecs.ecs import Entity
            from simplex.ecs.components import ChunkComponent

            # Prefer using ChunkManager if available
            if hasattr(self, "chunk_manager") and self.chunk_manager is not None:
                ent = self.chunk_manager.create_chunk(tuple(position))
                if ent:
                    log(f"Engine: Spawned chunk via ChunkManager at {position}", level="INFO")
                    return ent

            e = Entity(f"chunk_{position[0]}_{position[1]}_{position[2]}")
            chunk_comp = ChunkComponent(position=tuple(position), size=tuple(size))
            e.add_component(chunk_comp)
            self.ecs.add_entity(e)
            log(f"Engine: Spawned chunk entity at {position}", level="INFO")
            return e
        except Exception as exc:
            log(f"Engine.spawn_chunk failed: {exc}", level="ERROR")
            return None

    def set_camera(self, camera):
        """Attach a camera object to the renderer. Supports OpenGL backend and debug UI.

        The camera should expose a `position` attribute (tuple) and optional `target`.
        """
        try:
            ogl = self.get_opengl_renderer()
            if ogl is not None:
                try:
                    ogl.set_camera(camera)
                    log("Engine: Camera set on OpenGL renderer", level="INFO")
                    return True
                except Exception as e:
                    log(f"Engine: Failed to set camera on opengl_renderer: {e}", level="WARNING")

            # Fallback: if renderer exposes set_camera, call it
            if hasattr(self.renderer, "set_camera"):
                try:
                    self.renderer.set_camera(camera)
                    log("Engine: Camera set on renderer", level="INFO")
                    return True
                except Exception as e:
                    log(f"Engine: Failed to set camera on renderer: {e}", level="WARNING")

            log("Engine: No renderer camera API available", level="WARNING")
            return False
        except Exception as exc:
            log(f"Engine.set_camera error: {exc}", level="ERROR")
            return False

    @property
    def is_running(self) -> bool:
        """Check if engine is currently running."""
        return self._running

    @property
    def is_initialized(self) -> bool:
        """Check if engine is properly initialized."""
        return self._initialized

    camera_follow = None

    def spawn_player(self, name: str = "Player", position=(0, 2, 0)):
        """Spawn a simple player entity with position and velocity and set camera_follow."""
        try:
            from simplex.ecs.ecs import Entity
            from simplex.ecs.components import PositionComponent, VelocityComponent

            e = Entity(name)
            pos = PositionComponent(*position)
            vel = VelocityComponent(0.0, 0.0, 0.0)
            e.add_component(pos)
            e.add_component(vel)
            self.ecs.add_entity(e)
            # camera follow object is a lightweight container
            class CamObj:
                def __init__(self, position=(0,0,0)):
                    self.position = position

            cam = CamObj((position[0], position[1] + 1.6, position[2]))
            self.camera_follow = cam
            log(f"Engine: Spawned player '{name}' at {position}", level="INFO")
            return e
        except Exception as exc:
            log(f"Engine.spawn_player failed: {exc}", level="ERROR")
            return None
