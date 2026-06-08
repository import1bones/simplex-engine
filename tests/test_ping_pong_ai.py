"""Ping-pong AI behavior tests."""

import unittest

from simplex.ecs.components import InputComponent, PositionComponent, VelocityComponent
from simplex.ecs.ecs import ECS, Entity
from simplex.ecs.systems import InputSystem, MovementSystem


class PingPongAiTests(unittest.TestCase):
    def _make_world(self, ball_y=450, ball_vx=6):
        ecs = ECS()
        ecs.add_system(InputSystem(bounds=(800, 600)))
        ecs.add_system(MovementSystem(bounds=(800, 600)))

        ai = Entity("ai_paddle")
        ai.add_component(PositionComponent(750, 300, 0))
        ai.add_component(VelocityComponent(0, 0, 0))
        ai_input = InputComponent(input_type="ai")
        ai_input.speed = 6.0
        ai.add_component(ai_input)

        ball = Entity("ball")
        ball.add_component(PositionComponent(400, ball_y, 0))
        ball.add_component(VelocityComponent(ball_vx, 0, 0))

        ecs.add_entity(ai)
        ecs.add_entity(ball)
        return ecs, ai

    def test_ai_moves_toward_ball(self):
        ecs, ai = self._make_world(ball_y=450)
        for _ in range(20):
            ecs.update()
        self.assertGreater(ai.get_component("position").y, 300)

    def test_ai_tracks_ball_on_ai_side_even_when_moving_left(self):
        ecs, ai = self._make_world(ball_y=200, ball_vx=-4)
        ball = ecs.get_entity("ball")
        ball.get_component("position").x = 500
        for _ in range(15):
            ecs.update()
        self.assertLess(ai.get_component("position").y, 300)


if __name__ == "__main__":
    unittest.main()
