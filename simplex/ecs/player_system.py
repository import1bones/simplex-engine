"""Player controller system: first-person movement using the engine input pipeline.

This system updates entities that have 'position' and 'velocity' components.
It consumes input from the unified InputSystem (preferred) which receives events
forwarded by renderers (e.g. `SimpleRenderer` -> EventSystem -> InputSystem).

Behavior notes:
- The controller prefers to read `InputSystem.input_state` from the engine's ECS.
- If `EventSystem` or `InputSystem` are missing on the engine, the controller will
  attempt to create and register them automatically (best-effort). This is a
  compatibility convenience; for production use prefer registering subsystems via
  `engine.scheduler.register_factory(...)` and calling `engine.scheduler.initialize_all()`
  during engine startup so subsystem topology is explicit and deterministic.

This class intentionally does NOT query pygame directly; use the renderer->event
pipeline to drive input.
"""

from simplex.ecs.ecs import System
from simplex.utils.logger import log
import math

# Try to import InputSystem and EventSystem to use the unified pipeline
try:
    from simplex.ecs.systems import InputSystem
except Exception:
    InputSystem = None

try:
    from simplex.event.event_system import EventSystem
except Exception:
    EventSystem = None


class FirstPersonController(System):
    def __init__(self, event_system=None, engine=None, speed: float = 5.0):
        super().__init__("player_control")
        self.event_system = event_system
        self.engine = engine
        self.speed = speed
        # Mouse look state (degrees)
        self.yaw = 0.0
        self.pitch = 0.0
        self.mouse_sensitivity = 0.15
        self._mouse_listener_registered = False
        # controller requires position and velocity to operate
        self.required_components = ["position", "velocity"]

    def _ensure_event_system(self):
        """Ensure engine has an event system; create a lightweight one if missing.

        Creation is best-effort and logged at INFO so the application developer can
        see when implicit subsystem creation occurs. Prefer using engine.scheduler
        to register and create subsystems explicitly.
        """
        if not self.engine:
            return None
        if getattr(self.engine, 'events', None) is None:
            if EventSystem is not None:
                try:
                    self.engine.events = EventSystem()
                    log("PlayerController: created EventSystem on engine", level="INFO")
                except Exception as e:
                    log(f"PlayerController: failed to create EventSystem: {e}", level="ERROR")
                    return None
            else:
                # Minimal fallback event system
                class _StubEvents:
                    def __init__(self):
                        self._handlers = {}
                    def register(self, name, fn):
                        self._handlers.setdefault(name, []).append(fn)
                    def emit(self, name, data):
                        for fn in self._handlers.get(name, []):
                            try:
                                fn(data)
                            except Exception:
                                pass
                self.engine.events = _StubEvents()
                log("PlayerController: installed stub EventSystem on engine (fallback)", level="INFO")
        return self.engine.events

    def _ensure_input_system(self):
        """Ensure an InputSystem exists on the engine.ecs; create and register if missing.

        This will prefer an existing InputSystem instance (or any system exposing
        `input_state`). If none exists the controller will attempt to create a
        real InputSystem (if available in the codebase) and register it with the
        ECS. Creation is logged at INFO level.
        """
        if not self.engine or not getattr(self.engine, 'ecs', None):
            return None

        # look for existing InputSystem
        for s in getattr(self.engine.ecs, 'systems', []):
            if InputSystem is not None and isinstance(s, InputSystem):
                return s
            if hasattr(s, 'input_state'):
                return s

        # not found: create one if we have an event system
        events = self._ensure_event_system()
        if events is None:
            log("PlayerController: no EventSystem available to attach InputSystem", level="ERROR")
            return None

        if InputSystem is not None:
            try:
                input_sys = InputSystem(event_system=events)
                # register with ECS
                try:
                    self.engine.ecs.add_system(input_sys)
                    log("PlayerController: created and registered InputSystem on ECS", level="INFO")
                except Exception:
                    # best-effort: attach to ecs.systems list if add_system not present
                    if hasattr(self.engine.ecs, 'systems') and isinstance(self.engine.ecs.systems, list):
                        self.engine.ecs.systems.append(input_sys)
                        log("PlayerController: appended InputSystem to ecs.systems (fallback)", level="INFO")
                return input_sys
            except Exception as e:
                log(f"PlayerController: failed to create InputSystem: {e}", level="ERROR")
                return None

        # No InputSystem implementation available
        log("PlayerController: InputSystem implementation not available in project", level="ERROR")
        return None

    def _delta_time(self) -> float:
        if self.engine and getattr(self.engine, "_last_delta_time", None):
            return float(self.engine._last_delta_time)
        return 1.0 / 60.0

    def _ensure_mouse_listener(self):
        """Ensure the controller is registered to receive mouse events from the engine EventSystem."""
        events = self._ensure_event_system()
        if events is None:
            return None
        if not getattr(self, '_mouse_listener_registered', False):
            try:
                events.register('mouse', self._on_mouse)
                self._mouse_listener_registered = True
                log("PlayerController: registered mouse listener", level="DEBUG")
            except Exception:
                pass
        return events

    def _process_entities(self, entities):
        # Prefer the engine's InputSystem (unified pipeline). Do NOT query pygame here.
        input_sys = None
        try:
            input_sys = self._ensure_input_system()
        except Exception as e:
            log(f"PlayerController: error ensuring input system: {e}", level="ERROR")

        if input_sys is None:
            # Nothing to do without a unified input system
            log("PlayerController: no InputSystem available; skipping input processing", level="DEBUG")
            return

        input_state = getattr(input_sys, 'input_state', None)
        if input_state is None:
            log("PlayerController: InputSystem has no input_state; skipping", level="DEBUG")
            return

        # Ensure mouse listener is attached so mouse deltas update yaw/pitch
        try:
            self._ensure_mouse_listener()
        except Exception:
            pass

        for entity in entities:
            pos = entity.get_component("position")
            vel = entity.get_component("velocity")

            if not pos or not vel:
                continue

            # Simple movement in local camera-relative X/Z plane and space for up
            dx = 0.0
            dz = 0.0

            # InputSystem uses abstracted key names (e.g. 'UP','DOWN','LEFT','RIGHT','SPACE')
            if input_state.get('UP'):
                dz += 1
            if input_state.get('DOWN'):
                dz -= 1
            if input_state.get('LEFT'):
                dx += 1
            if input_state.get('RIGHT'):
                dx -= 1
            # Jump is handled by VoxelCollisionSystem when on ground.

            # Transform input (dx,dz) by current yaw to move relative to view
            if dx != 0 or dz != 0:
                # compute forward and right vectors from yaw
                yaw_rad = math.radians(self.yaw)
                forward_x = math.sin(yaw_rad)
                forward_z = math.cos(yaw_rad)
                right_x = math.cos(yaw_rad)
                right_z = -math.sin(yaw_rad)

                # combine
                move_x = forward_x * dz + right_x * dx
                move_z = forward_z * dz + right_z * dx
                mag = (move_x * move_x + move_z * move_z) ** 0.5
                if mag != 0:
                    ndx, ndz = move_x / mag, move_z / mag
                else:
                    ndx, ndz = 0.0, 0.0

                step = self.speed * self._delta_time()
                pos.x += ndx * step
                pos.z += ndz * step

            # Update camera follow object if present on engine
            try:
                if self.engine:
                    # ensure camera_follow exists
                    if not hasattr(self.engine, 'camera_follow') or self.engine.camera_follow is None:
                        # lightweight camera object
                        class _Cam:
                            def __init__(self):
                                self.position = (0, 0, 0)
                                self.yaw = 0.0
                                self.pitch = 0.0
                        self.engine.camera_follow = _Cam()
                    cam = self.engine.camera_follow
                    # set camera position a bit above player and push orientation
                    cam.position = (pos.x, pos.y + 1.6, pos.z)
                    cam.yaw = self.yaw
                    cam.pitch = self.pitch
            except Exception as e:
                log(f"PlayerController: failed to update camera: {e}", level="DEBUG")

    def _on_mouse(self, event):
        """Handle mouse motion events forwarded via EventSystem. Expects a dict with 'rel'."""
        try:
            rel = None
            if isinstance(event, dict):
                rel = event.get('rel')
            else:
                # pygame Event-like object
                rel = getattr(event, 'rel', None)
            if not rel:
                return
            dx, dy = rel[0], rel[1]
            # Update yaw/pitch (invert Y so moving mouse up looks up)
            self.yaw += dx * self.mouse_sensitivity
            self.pitch -= dy * self.mouse_sensitivity
            # clamp pitch to avoid gimbal
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0
        except Exception:
            pass
