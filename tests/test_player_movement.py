import unittest

from simplex.ecs.chunk_streaming_system import ChunkStreamingSystem
from simplex.ecs.ecs import ECS, Entity
from simplex.ecs.components import PositionComponent, VelocityComponent
from simplex.ecs.player_system import FirstPersonController
from simplex.ecs.voxel_collision_system import VoxelCollisionSystem
from simplex.ecs.systems import InputSystem
from simplex.event.event_system import EventSystem
from simplex.world.chunk_manager import ChunkManager


class PlayerMovementTests(unittest.TestCase):
    def setUp(self):
        self.ecs = ECS()
        self.events = EventSystem()
        self.input_sys = InputSystem(event_system=self.events)
        self.ecs.add_system(self.input_sys)

        class _Engine:
            pass

        self.engine = _Engine()
        self.engine.ecs = self.ecs
        self.engine.events = self.events
        self.engine.chunk_manager = ChunkManager(
            self.ecs, chunk_size=(16, 16, 16), cache_size=32
        )
        self.engine._last_delta_time = 1.0 / 60.0

        self.player = Entity("Player")
        self.player.add_component(PositionComponent(0.5, 8.0, 0.5))
        self.player.add_component(VelocityComponent())
        self.ecs.add_entity(self.player)

        self.ecs.add_system(
            ChunkStreamingSystem(
                engine=self.engine,
                radius=1,
                horizontal_only=True,
                stream_y_chunk=0,
            )
        )
        self.ecs.add_system(FirstPersonController(event_system=self.events, engine=self.engine))
        self.ecs.add_system(VoxelCollisionSystem(engine=self.engine))

    def test_forward_moves_z_and_stays_above_ground(self):
        self.input_sys.input_state["UP"] = True
        for _ in range(120):
            self.ecs.update()
        pos = self.player.get_component("position")
        self.assertGreater(pos.z, 0.4)
        self.assertGreater(pos.y, 0.0)

    def test_strafe_moves_x(self):
        self.input_sys.input_state["LEFT"] = True
        for _ in range(120):
            self.ecs.update()
        pos = self.player.get_component("position")
        self.assertGreater(pos.x, 0.4)


if __name__ == "__main__":
    unittest.main()
