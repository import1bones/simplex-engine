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

            on_ground = self._on_ground.get(entity.name, False)

            if input_state.get("SPACE") or input_state.get("JUMP"):
                if on_ground:
                    pos.y += self.JUMP_SPEED * dt
                    on_ground = False

            if not on_ground:
                pos.y -= self.GRAVITY * dt

            if on_ground and feet_on_ground(cm, pos.x, pos.y, pos.z):
                pass
            else:
                ground_y = find_ground_height(
                    cm, pos.x, pos.y, pos.z, self.PLAYER_RADIUS
                )
                if ground_y is not None and pos.y <= ground_y:
                    pos.y = ground_y
                    on_ground = True
                elif not feet_on_ground(cm, pos.x, pos.y, pos.z):
                    on_ground = False

            current = (pos.x, pos.y, pos.z)
            if current != self._last_pos.get(entity.name):
                self._resolve_horizontal(cm, pos)
                self._last_pos[entity.name] = current

            head_y = pos.y + self.PLAYER_HEIGHT
            if is_solid_at_world(cm, pos.x, head_y, pos.z):
                pos.y -= 0.1

            self._on_ground[entity.name] = on_ground

    def _resolve_horizontal(self, chunk_manager, pos):
        """Block horizontal movement into solid voxels at body height."""
        body_y = pos.y + self.PLAYER_HEIGHT * 0.5
        r = self.PLAYER_RADIUS
        checks = (
            (pos.x + r, body_y, pos.z),
            (pos.x - r, body_y, pos.z),
            (pos.x, body_y, pos.z + r),
            (pos.x, body_y, pos.z - r),
        )
        for wx, wy, wz in checks:
            if is_solid_at_world(chunk_manager, wx, wy, wz):
                if abs(wx - pos.x) > abs(wz - pos.z):
                    pos.x -= 0.05 if wx > pos.x else -0.05
                else:
                    pos.z -= 0.05 if wz > pos.z else -0.05
