"""
Core ECS components for simplex-engine.
Defines reusable components for common game entity needs.
"""

from simplex.ecs.ecs import Component


class PositionComponent(Component):
    """Component for entity position in 3D space."""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__("position")
        self.x = x
        self.y = y
        self.z = z

    @property
    def position(self):
        return (self.x, self.y, self.z)

    @position.setter
    def position(self, value):
        self.x, self.y, self.z = value


class VelocityComponent(Component):
    """Component for entity velocity in 3D space."""

    def __init__(self, vx=0.0, vy=0.0, vz=0.0):
        super().__init__("velocity")
        self.vx = vx
        self.vy = vy
        self.vz = vz

    @property
    def velocity(self):
        return (self.vx, self.vy, self.vz)

    @velocity.setter
    def velocity(self, value):
        self.vx, self.vy, self.vz = value


class RenderComponent(Component):
    """Component for entity rendering properties."""

    def __init__(self, primitive="cube", material=None, color=(1, 1, 1)):
        super().__init__("render")
        self.primitive = primitive
        self.material = material
        self.color = color
        self.visible = True


class CollisionComponent(Component):
    """Component for entity collision properties."""

    def __init__(self, width=10.0, height=10.0, depth=10.0, mass=1.0):
        super().__init__("collision")
        self.width = width
        self.height = height
        self.depth = depth
        self.mass = mass
        self.is_static = mass == 0.0


class InputComponent(Component):
    """Component for entities that respond to input."""

    def __init__(self, input_type="player"):
        super().__init__("input")
        self.input_type = input_type  # 'player', 'ai', etc.
        self.speed = 10.0


class ScoreComponent(Component):
    """Component for tracking score."""

    def __init__(self, score=0):
        super().__init__("score")
        self.score = score


class VoxelComponent(Component):
    """Component for a single voxel/block reference on an entity.

    Holds a block id and optional metadata/properties. Systems will
    interpret block ids using the voxel palette defined in
    `simplex.voxel.voxel`.
    """

    def __init__(self, block_id: int = 0, properties: dict | None = None):
        super().__init__("voxel")
        self.block_id = int(block_id)
        self.properties = properties or {}


class ChunkComponent(Component):
    """Component that attaches chunk data to an entity.

    Stores a reference to a `Chunk` instance (from `simplex.voxel.chunk`) or
    lazily holds chunk parameters. `chunk` may be None initially and filled
    by a world/streaming system.
    """

    def __init__(
        self, position: tuple = (0, 0, 0), size: tuple = (16, 16, 16), chunk=None
    ):
        super().__init__("chunk")
        self.position = tuple(position)
        self.size = tuple(size)
        self.chunk = (
            chunk  # expected to be a simplex.voxel.chunk.Chunk instance or None
        )
        self.dirty = True

    def mark_dirty(self):
        self.dirty = True

    def clear_dirty(self):
        self.dirty = False

    def has_chunk(self) -> bool:
        return self.chunk is not None

    def attach_chunk(self, chunk):
        """Attach a Chunk instance (or None) to this component and mark dirty."""
        self.chunk = chunk
        self.mark_dirty()


class MeshComponent(Component):
    """Component that stores a generated mesh (vertices/colors) or a renderer handle.

    vertices: flat list of floats (x,y,z) per vertex
    colors: flat list of floats (r,g,b,a) per vertex
    mesh_id / gpu: optional renderer-side handle or dict with VBO info
    origin: world-space offset to apply when rendering (x,y,z)
    """

    def __init__(
        self,
        vertices=None,
        colors=None,
        mesh_id: str | None = None,
        origin: tuple = (0, 0, 0),
    ):
        super().__init__("mesh")
        self.vertices = vertices or []
        self.colors = colors or []
        self.mesh_id = mesh_id
        self.origin = tuple(origin)
        self.gpu = None  # renderer may attach {'vbo': int, 'count': int, ...}
