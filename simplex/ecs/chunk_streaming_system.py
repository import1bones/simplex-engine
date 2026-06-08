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
        stream_y_chunk: int = 0,
        hysteresis: float = 4.0,
    ):
        super().__init__("chunk_streaming")
        self.event_system = event_system
        self.engine = engine
        self.radius = int(radius)
        self.horizontal_only = horizontal_only
        self.stream_y_chunk = int(stream_y_chunk)
        self.hysteresis = float(hysteresis)
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
        if self.horizontal_only:
            cy = self.stream_y_chunk
        else:
            cy = math.floor(pos.y / sy)

        cx = self._stable_chunk_index(pos.x, sx, 0)
        cz = self._stable_chunk_index(pos.z, sz, 2)
        center = (cx, cy, cz)

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

    def _stable_chunk_index(self, coord: float, size: int, axis: int) -> int:
        """Floor to chunk index with hysteresis so border jitter does not reload."""
        raw = math.floor(coord / size)
        if self._last_center is None:
            return raw

        last = self._last_center[axis]
        if raw == last:
            return last

        if raw > last:
            boundary = (last + 1) * size
            if coord < boundary + self.hysteresis:
                return last
        else:
            boundary = last * size
            if coord > boundary - self.hysteresis:
                return last
        return raw
