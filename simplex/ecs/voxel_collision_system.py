"""Voxel grid collision and gravity for the player."""

from simplex.ecs.ecs import System
from simplex.ecs.systems import InputSystem
from simplex.world.world_query import (
    feet_on_ground,
    find_ground_height,
    is_solid_at_world,
)


class VoxelCollisionSystem(System):
    """Keep the player on terrain with gravity and simple horizontal blocking."""

    PLAYER_HEIGHT = 1.8
    PLAYER_RADIUS = 0.3
    GRAVITY = 24.0
    JUMP_SPEED = 8.0
    MIN_WORLD_Y = -32.0

    def __init__(self, event_system=None, engine=None):
        super().__init__("voxel_collision")
        self.event_system = event_system
        self.engine = engine
        self.required_components = ["position"]
        self._on_ground: dict[str, bool] = {}
        self._input_system = None
        self._last_pos: dict[str, tuple] = {}

    def _get_input_system(self):
        if self._input_system is not None:
            return self._input_system
        if not self.engine or not getattr(self.engine, "ecs", None):
            return None
        for system in self.engine.ecs.systems:
            if isinstance(system, InputSystem):
                self._input_system = system
                return system
            if hasattr(system, "input_state"):
                self._input_system = system
                return system
        return None

    def _delta_time(self) -> float:
        if self.engine and getattr(self.engine, "_last_delta_time", None):
            return float(self.engine._last_delta_time)
        return 1.0 / 60.0

    def _body_blocked(self, chunk_manager, x: float, y: float, z: float) -> bool:
        r = self.PLAYER_RADIUS
        samples_y = (
            y + 0.2,
            y + self.PLAYER_HEIGHT * 0.5,
            y + self.PLAYER_HEIGHT - 0.2,
        )
        for body_y in samples_y:
            for wx, wy, wz in (
                (x + r, body_y, z),
                (x - r, body_y, z),
                (x, body_y, z + r),
                (x, body_y, z - r),
            ):
                if is_solid_at_world(chunk_manager, wx, wy, wz):
                    return True
        return False

    def _process_entities(self, entities):
        cm = getattr(self.engine, "chunk_manager", None) if self.engine else None
        if cm is None:
            return

        input_sys = self._get_input_system()
        input_state = getattr(input_sys, "input_state", {}) if input_sys else {}
        dt = self._delta_time()

        for entity in entities:
            if entity.name != "Player":
                continue

            pos = entity.get_component("position")
            if not pos:
                continue

            prev = self._last_pos.get(entity.name, (pos.x, pos.y, pos.z))
            on_ground = self._on_ground.get(entity.name, False)

            if input_state.get("SPACE") or input_state.get("JUMP"):
                if on_ground:
                    pos.y += self.JUMP_SPEED * dt
                    on_ground = False

            if not on_ground:
                pos.y -= self.GRAVITY * dt

            ground_y = find_ground_height(
                cm, pos.x, pos.y, pos.z, self.PLAYER_RADIUS
            )
            if ground_y is not None and pos.y <= ground_y:
                pos.y = ground_y
                on_ground = True
            elif on_ground and feet_on_ground(cm, pos.x, pos.y, pos.z):
                pass
            else:
                on_ground = False

            if (pos.x, pos.z) != (prev[0], prev[2]):
                self._resolve_horizontal(cm, pos, prev)

            self._push_out_of_solids(cm, pos, on_ground, ground_y)

            if pos.y < self.MIN_WORLD_Y:
                if ground_y is not None:
                    pos.y = ground_y
                    on_ground = True
                else:
                    pos.y = 8.0
                    pos.x, pos.z = prev[0], prev[2]
                    on_ground = False

            self._on_ground[entity.name] = on_ground
            self._last_pos[entity.name] = (pos.x, pos.y, pos.z)

    def _resolve_horizontal(self, chunk_manager, pos, prev):
        """Revert axis movement that entered a solid block."""
        if self._body_blocked(chunk_manager, pos.x, pos.y, pos.z):
            if not self._body_blocked(chunk_manager, prev[0], pos.y, pos.z):
                pos.x = prev[0]
            elif not self._body_blocked(chunk_manager, pos.x, pos.y, prev[2]):
                pos.z = prev[2]
            else:
                pos.x, pos.z = prev[0], prev[2]

    def _push_out_of_solids(self, chunk_manager, pos, on_ground: bool, ground_y: float | None):
        """Push the player up if clipped into terrain after landing (not while falling)."""
        if not on_ground:
            if ground_y is None or pos.y > ground_y + 0.25:
                return
        for _ in range(8):
            if not self._body_blocked(chunk_manager, pos.x, pos.y, pos.z):
                break
            pos.y += 0.15
