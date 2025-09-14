"""ChunkManager: simple streaming and LRU cache for chunk entities.

Provides a minimal API to create/load/unload chunks and attach them to the ECS
as entities with ChunkComponent. Intended as a starting point for Minecraft-like
streaming workflows.
"""

from collections import OrderedDict
from typing import Tuple, Dict, Optional

from simplex.utils.logger import log
from simplex.voxel.chunk import Chunk
from simplex.ecs.ecs import Entity
from simplex.ecs.components import ChunkComponent


class ChunkManager:
    def __init__(self, ecs, event_system=None, chunk_size: Tuple[int, int, int] = (16, 16, 16), cache_size: int = 64):
        self.ecs = ecs
        self.event_system = event_system
        self.chunk_size = tuple(chunk_size)
        self.cache_size = int(cache_size)
        # maps chunk_pos -> {'chunk': Chunk, 'entity_name': str}
        self._chunks: Dict[Tuple[int, int, int], Dict] = {}
        # LRU ordering of positions (most recent at end)
        self._lru = OrderedDict()
        log(f"ChunkManager created (chunk_size={self.chunk_size}, cache_size={self.cache_size})", level="INFO")

    def _evict_if_needed(self):
        while len(self._chunks) > self.cache_size:
            # pop oldest
            pos, _ = self._lru.popitem(last=False)
            log(f"ChunkManager: Evicting chunk at {pos}", level="INFO")
            self.unload_chunk(pos)

    def _register_access(self, pos: Tuple[int, int, int]):
        # move pos to end
        if pos in self._lru:
            try:
                self._lru.pop(pos)
            except KeyError:
                pass
        self._lru[pos] = True

    def _generate_chunk(self, position: Tuple[int, int, int]) -> Chunk:
        """Create and populate a Chunk instance with a simple heightmap."""
        chunk = Chunk(position, size=self.chunk_size)
        sx, sy, sz = chunk.size
        # simple deterministic heightmap based on chunk coords
        cx, cy, cz = position
        base_height = sy // 4
        # fill with dirt up to base_height
        for x in range(sx):
            for z in range(sz):
                height = base_height
                # small variation using coordinates
                height += (abs(cx) + abs(cz) + x + z) % (max(1, sy // 8))
                if height >= sy:
                    height = sy - 1
                for y in range(height):
                    chunk.set_block_id(x, y, z, 1)  # dirt
        chunk.dirty = True
        return chunk

    def create_chunk(self, position: Tuple[int, int, int]) -> Optional[Entity]:
        """Create a chunk, attach a ChunkComponent on an ECS entity, and return the entity."""
        pos = tuple(position)
        if pos in self._chunks:
            # ensure LRU updated
            self._register_access(pos)
            info = self._chunks[pos]
            return self.ecs.get_entity(info.get("entity_name"))

        try:
            chunk = self._generate_chunk(pos)
            entity_name = f"chunk_{pos[0]}_{pos[1]}_{pos[2]}"
            e = Entity(entity_name)
            chunk_comp = ChunkComponent(position=pos, size=chunk.size, chunk=chunk)
            e.add_component(chunk_comp)
            self.ecs.add_entity(e)
            # register
            self._chunks[pos] = {"chunk": chunk, "entity_name": entity_name}
            self._register_access(pos)
            log(f"ChunkManager: Created and registered chunk entity {entity_name}", level="INFO")
            self._evict_if_needed()
            return e
        except Exception as exc:
            log(f"ChunkManager.create_chunk failed: {exc}", level="ERROR")
            return None

    def get_chunk(self, position: Tuple[int, int, int]) -> Optional[Chunk]:
        pos = tuple(position)
        info = self._chunks.get(pos)
        if info:
            self._register_access(pos)
            return info.get("chunk")
        return None

    def unload_chunk(self, position: Tuple[int, int, int]) -> bool:
        pos = tuple(position)
        info = self._chunks.pop(pos, None)
        try:
            if pos in self._lru:
                try:
                    self._lru.pop(pos)
                except KeyError:
                    pass
            if info:
                entity_name = info.get("entity_name")
                if entity_name and self.ecs.get_entity(entity_name):
                    self.ecs.remove_entity(entity_name)
                log(f"ChunkManager: Unloaded chunk at {pos}", level="INFO")
                return True
            return False
        except Exception as exc:
            log(f"ChunkManager.unload_chunk failed: {exc}", level="ERROR")
            return False

    def ensure_loaded(self, position: Tuple[int, int, int]) -> Optional[Entity]:
        """Ensure chunk at position is loaded and return the entity."""
        if position in self._chunks:
            return self.create_chunk(position)
        return self.create_chunk(position)

    def list_loaded(self):
        return list(self._chunks.keys())

    def preload_area(self, center: Tuple[int, int, int], radius: int = 1):
        """Ensure all chunks within `radius` (Manhattan) of center are loaded.

        Uses create_chunk for each position and then evicts if cache exceeded.
        """
        cx, cy, cz = center

        # Build positions list (center first) to ensure center is created
        positions = []
        positions.append((cx, cy, cz))
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    pos = (cx + dx, cy + dy, cz + dz)
                    if pos == (cx, cy, cz):
                        continue
                    positions.append(pos)

        for pos in positions:
            try:
                self.create_chunk(pos)
            except Exception:
                # ignore generation failures for individual positions
                pass

        # If center somehow wasn't created (e.g., failures), try once more
        if (cx, cy, cz) not in self._chunks:
            try:
                self.create_chunk((cx, cy, cz))
            except Exception:
                pass

        # mark center as most recently used so eviction prefers other chunks
        try:
            self._register_access((cx, cy, cz))
        except Exception:
            pass

        # after loading, ensure we don't exceed cache
        self._evict_if_needed()

    def unload_outside_area(self, center: Tuple[int, int, int], radius: int = 1):
        """Unload any loaded chunk whose max(|dx|,|dy|,|dz|) > radius.

        Useful to prune chunks outside streaming radius.
        """
        cx, cy, cz = center
        to_unload = []
        for pos in list(self._chunks.keys()):
            dx = abs(pos[0] - cx)
            dy = abs(pos[1] - cy)
            dz = abs(pos[2] - cz)
            if max(dx, dy, dz) > radius:
                to_unload.append(pos)

        for pos in to_unload:
            self.unload_chunk(pos)

    def ensure_area_loaded(self, center: Tuple[int, int, int], radius: int = 1):
        """Convenience: preload area then unload outside it.
        """
        self.preload_area(center, radius)
        self.unload_outside_area(center, radius)
