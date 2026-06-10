"""Block place/break via camera raycast."""

from simplex.ecs.ecs import Entity, System
from simplex.utils.logger import log
from simplex.voxel.voxel import BLOCK_AIR, BLOCK_DIRT
from simplex.world.world_query import (
    get_block_id_at_world,
    raycast_blocks,
    set_block_id_at_world,
    view_direction_from_yaw_pitch,
)


class BlockInteractionSystem(System):
    """Left-click break, right-click place blocks along the camera view ray."""

    MAX_REACH = 8.0
    PLAYER_RADIUS = 0.35
    PLAYER_HEIGHT = 1.8

    def __init__(self, event_system=None, engine=None, place_block_id: int = BLOCK_DIRT):
        super().__init__("block_interaction")
        self.event_system = event_system
        self.engine = engine
        self.place_block_id = int(place_block_id)
        self.required_components = []
        self._pending_clicks: list[str] = []
        self._listener_registered = False

    def _ensure_listener(self):
        if self._listener_registered or not self.event_system:
            return
        try:
            self.event_system.register("mouse_button", self._on_mouse_button)
            self._listener_registered = True
        except Exception:
            pass

    def _on_mouse_button(self, event):
        button = None
        pressed = True
        if isinstance(event, dict):
            button = event.get("button")
            pressed = event.get("pressed", True)
        else:
            button = getattr(event, "button", None)
            pressed = getattr(event, "pressed", True)
        if not pressed or button not in ("LEFT", "RIGHT"):
            return
        self._pending_clicks.append(button)

    def update(self, entities: list[Entity]) -> None:
        self._ensure_listener()
        if not self._pending_clicks:
            return
        clicks = self._pending_clicks
        self._pending_clicks = []
        for button in clicks:
            self._handle_click(button)

    def _handle_click(self, button: str):
        cm = getattr(self.engine, "chunk_manager", None) if self.engine else None
        ecs = getattr(self.engine, "ecs", None) if self.engine else None
        cam = getattr(self.engine, "camera_follow", None) if self.engine else None
        if cm is None or ecs is None or cam is None:
            return

        origin = getattr(cam, "position", None)
        if not origin:
            return
        yaw = float(getattr(cam, "yaw", 0.0))
        pitch = float(getattr(cam, "pitch", 0.0))
        direction = view_direction_from_yaw_pitch(yaw, pitch)

        result = raycast_blocks(cm, origin, direction, max_distance=self.MAX_REACH)
        if not result.get("hit"):
            return

        if button == "LEFT":
            bx, by, bz = result["block"]
            if set_block_id_at_world(cm, ecs, bx, by, bz, BLOCK_AIR):
                log(f"BlockInteraction: broke block at ({bx}, {by}, {bz})", level="DEBUG")
            return

        if button == "RIGHT":
            px, py, pz = result["prev"]
            if self._overlaps_player(px, py, pz):
                return
            if get_block_id_at_world(cm, px, py, pz) != BLOCK_AIR:
                return
            if set_block_id_at_world(cm, ecs, px, py, pz, self.place_block_id):
                log(f"BlockInteraction: placed block at ({px}, {py}, {pz})", level="DEBUG")

    def _overlaps_player(self, bx: int, by: int, bz: int) -> bool:
        """Rough AABB overlap between block cell and player body."""
        if not self.engine or not getattr(self.engine, "ecs", None):
            return False
        player = self.engine.ecs.get_entity("Player")
        if not player:
            return False
        pos = player.get_component("position")
        if not pos:
            return False
        half = self.PLAYER_RADIUS
        height = self.PLAYER_HEIGHT
        player_min = (pos.x - half, pos.y, pos.z - half)
        player_max = (pos.x + half, pos.y + height, pos.z + half)
        block_min = (float(bx), float(by), float(bz))
        block_max = (float(bx + 1), float(by + 1), float(bz + 1))
        return (
            player_min[0] < block_max[0]
            and player_max[0] > block_min[0]
            and player_min[1] < block_max[1]
            and player_max[1] > block_min[1]
            and player_min[2] < block_max[2]
            and player_max[2] > block_min[2]
        )
