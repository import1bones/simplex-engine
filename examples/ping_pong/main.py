"""
main.py - Ping-Pong Game (MVP-Sample-4)

A simple GUI ping-pong game using simplex-engine.
"""

from simplex.engine import Engine
from simplex.physics.body import RigidBody
from simplex.event.event_system import EventSystem
from simplex.resource.resource_manager import ResourceManager

# --- Game Setup ---
engine = Engine(config_path="examples/ping_pong/config.toml")

# Entities
player_paddle = RigidBody('PlayerPaddle', mass=0.0)
ai_paddle = RigidBody('AIPaddle', mass=0.0)
ball = RigidBody('Ball', mass=1.0)

engine.physics.add_rigid_body(player_paddle)
engine.physics.add_rigid_body(ai_paddle)
engine.physics.add_rigid_body(ball)

# Renderer: paddles and ball
engine.renderer.register_material(engine.resource_manager.load('material', 'player_mat'))
engine.renderer.register_material(engine.resource_manager.load('material', 'ai_mat'))
engine.renderer.register_material(engine.resource_manager.load('material', 'ball_mat'))
engine.renderer.add_primitive('cube', material='player_mat', parent=None, transform=None)
engine.renderer.add_primitive('cube', material='ai_mat', parent=None, transform=None)
engine.renderer.add_primitive('sphere', material='ball_mat', parent=None, transform=None)

# Input: map up/down to paddle
engine.input.on_event('up', lambda e: player_paddle.apply_impulse((0, 8, 0)))
engine.input.on_event('down', lambda e: player_paddle.apply_impulse((0, -8, 0)))

# AI paddle (simple follow)
def ai_follow(event):
    if ball.position[1] > ai_paddle.position[1]:
        ai_paddle.apply_impulse((0, 6, 0))
    elif ball.position[1] < ai_paddle.position[1]:
        ai_paddle.apply_impulse((0, -6, 0))
engine.events.register('physics_update', ai_follow)

# Collision: bounce and scoring
def on_collision(event):
    # Bounce logic and scoring (stub)
    pass
engine.events.register('physics_collision', on_collision)

# Score and GUI overlay (stub)
score = {'player': 0, 'ai': 0}

def render_score(event):
    # Render score overlay (stub)
    pass
engine.events.register('render', render_score)

# Game logic: win/lose, restart (stub)
def check_win(event):
    if score['player'] >= 5:
        print('You win!')
        engine.reset()
    elif score['ai'] >= 5:
        print('AI wins!')
        engine.reset()
engine.events.register('physics_update', check_win)

# --- Run Game ---
engine.run()
