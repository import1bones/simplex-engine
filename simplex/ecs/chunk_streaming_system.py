"""Load and unload chunks around the player."""

import math

from simplex.ecs.ecs import System
from simplex.utils.logger import log


class ChunkStreamingSystem(System):
    """Stream chunks in a radius around the player when they cross chunk boundaries."""

    def __init__(
        self,
        event_system=None,
        engine=None,
        radius: int = 1,
        horizontal_only: bool = True,
    ):
        super().__init__("chunk_streaming")
        self.event_system = event_system
        self.engine = engine
        self.radius = int(radius)
        self.horizontal_only = horizontal_only
        self.required_components = ["position"]
        self._last_center = None

    def _process_entities(self, entities):
        cm = getattr(self.engine, "chunk_manager", None) if self.engine else None
        if cm is None:
            return

        player = None
        for entity in entities:
            if entity.name == "Player":
                player = entity
                break
        if player is None:
            return

        pos = player.get_component("position")
        if not pos:
            return

        sx, sy, sz = cm.chunk_size
        center = (
            math.floor(pos.x / sx),
            math.floor(pos.y / sy),
            math.floor(pos.z / sz),
        )

        if center == self._last_center:
            return

        self._last_center = center
        cm.ensure_area_loaded(
            center, radius=self.radius, horizontal_only=self.horizontal_only
        )
        log(
            f"ChunkStreamingSystem: loaded area radius={self.radius} "
            f"horizontal={self.horizontal_only} at {center}",
            level="DEBUG",
        )
