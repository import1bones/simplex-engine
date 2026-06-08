"""ECS systems for handling chunks and mesh generation."""

from simplex.ecs.ecs import System
from simplex.utils.logger import log
from simplex.voxel.chunk import Chunk
from simplex.voxel.meshgen import generate_naive_mesh
from simplex.ecs.components import MeshComponent


class ChunkSystem(System):
    """System responsible for creating and managing Chunk instances.

    For now it provides a simple API to create a chunk entity at a
    chunk coordinate and fill it with simple test content.
    """

    def __init__(self, event_system=None):
        super().__init__("chunk")
        self.event_system = event_system
        self.required_components = ["chunk"]

    def _process_entities(self, entities):
        for entity in entities:
            chunk_comp = entity.get_component("chunk")
            if not chunk_comp.has_chunk():
                # Create a new empty chunk and attach
                chunk = Chunk(chunk_comp.position, size=chunk_comp.size)
                # Fill with a simple heightmap for testing
                sx, sy, sz = chunk.size
                for x in range(sx):
                    for z in range(sz):
                        height = sy // 4  # flat layer at 1/4 height
                        for y in range(height):
                            chunk.set_block_id(x, y, z, 1)  # dirt
                chunk_comp.attach_chunk(chunk)
                log(
                    f"ChunkSystem: Created chunk at {chunk_comp.position}", level="DEBUG"
                )


class ChunkMeshSystem(System):
    """System that generates meshes for dirty chunks and attaches MeshComponents."""

    def __init__(self, event_system=None, max_chunks_per_frame: int = 2):
        super().__init__("chunk_mesh")
        self.event_system = event_system
        self.max_chunks_per_frame = max(1, int(max_chunks_per_frame))
        self.required_components = ["chunk"]

    def _process_entities(self, entities):
        meshed = 0
        for entity in entities:
            if meshed >= self.max_chunks_per_frame:
                break
            chunk_comp = entity.get_component("chunk")
            if chunk_comp and chunk_comp.has_chunk() and chunk_comp.dirty:
                # Use greedy mesh generator for fewer vertices when available
                try:
                    from simplex.voxel.meshgen import generate_greedy_mesh

                    verts, cols = generate_greedy_mesh(chunk_comp.chunk)
                except Exception:
                    verts, cols = generate_naive_mesh(chunk_comp.chunk)
                mesh_comp = entity.get_component("mesh")
                # compute world-space origin from chunk coordinates and chunk size
                chunk_obj = chunk_comp.chunk
                origin = (
                    chunk_comp.position[0] * chunk_obj.size[0],
                    chunk_comp.position[1] * chunk_obj.size[1],
                    chunk_comp.position[2] * chunk_obj.size[2],
                )
                if not mesh_comp:
                    mesh_comp = MeshComponent(
                        vertices=verts, colors=cols, origin=origin
                    )
                    entity.add_component(mesh_comp)
                else:
                    mesh_comp.vertices = verts
                    mesh_comp.colors = cols
                    mesh_comp.origin = origin

                # GPU upload is handled by the renderer (context required). Leave mesh_comp.gpu unset.

                chunk_comp.clear_dirty()
                meshed += 1
                log(
                    f"ChunkMeshSystem: Generated mesh for chunk {chunk_comp.position} (verts={len(verts) // 3})",
                    level="DEBUG",
                )

                # Emit event so renderers or VBO managers can upload the mesh when context is available
                try:
                    if self.event_system:
                        self.event_system.emit("mesh_generated", {"entity": entity, "mesh": mesh_comp})
                except Exception:
                    pass
