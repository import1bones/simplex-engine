"""
main.py - Ping-Pong Game (MVP-Sample-4)

A simple GUI ping-pong game using simplex-engine.
"""

from simplex.engine import Engine
from simplex.physics.body import RigidBody
from simplex.event.event_system import EventSystem

from simplex.renderer.material import Material

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
player_mat = Material('player_mat', properties={'color': (1, 1, 1)})
ai_mat = Material('ai_mat', properties={'color': (0, 1, 0)})
ball_mat = Material('ball_mat', properties={'color': (1, 0, 0)})
engine.renderer.register_material(player_mat)
engine.renderer.register_material(ai_mat)
engine.renderer.register_material(ball_mat)
engine.renderer.add_primitive('cube', material='player_mat', parent=None, transform=None)
engine.renderer.add_primitive('cube', material='ai_mat', parent=None, transform=None)
engine.renderer.add_primitive('sphere', material='ball_mat', parent=None, transform=None)


# Input: handle key events for paddle movement
def handle_input(event):
    # Accept both pygame-style and CLI events
    if hasattr(event, 'type') and (event.type == 'KEYDOWN' or (hasattr(event, 'type') and event.type == 'KEYDOWN')):
        # Accept both string and pygame constants for key
        if getattr(event, 'key', None) in ('UP', 'K_UP'):
            player_paddle.apply_impulse((0, 8, 0))
        elif getattr(event, 'key', None) in ('DOWN', 'K_DOWN'):
            player_paddle.apply_impulse((0, -8, 0))
engine.events.register('input', handle_input)

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

# Ball state: position and velocity
ball.position = (400, 300, 0)  # Start in the middle (assuming 800x600)
ball.velocity = (-6, 4, 0)     # Initial velocity (left and up)

# Paddle positions (X fixed, Y moves)
player_paddle.position = (50, 300, 0)
ai_paddle.position = (750, 300, 0)

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


# --- CLI/Log-Based Ping-Pong Loop ---
import time
import sys
import os
# Non-blocking keyboard input for Linux/macOS
import termios
import tty
import select
TICKS = 100  # Number of simulation steps

def render_ascii(player_y, ai_y, ball_x, ball_y, width=80, height=24):
    # Map game coordinates to ASCII grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    # Paddles: 4 chars tall
    py = int(player_y * (height-1) / 600)
    ay = int(ai_y * (height-1) / 600)
    for dy in range(-2, 2):
        if 0 <= py+dy < height:
            grid[py+dy][2] = '|'
        if 0 <= ay+dy < height:
            grid[ay+dy][width-3] = '|'
    # Ball
    bx = int(ball_x * (width-1) / 800)
    by = int(ball_y * (height-1) / 600)
    if 0 <= by < height and 0 <= bx < width:
        grid[by][bx] = 'O'
    # Render
    return '\n'.join(''.join(row) for row in grid)


# Helper for non-blocking input (Linux/macOS)
def get_key():
    dr, dw, de = select.select([sys.stdin], [], [], 0)
    if dr:
        return sys.stdin.read(1)
    return None

# Save terminal settings
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
tty.setcbreak(fd)
print("Controls: 'w' = up, 's' = down. Press Ctrl+C to quit.")
try:
    for tick in range(TICKS):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Tick {tick+1} | Player {score['player']} : {score['ai']} AI\n")

        # Poll input and emit events via simplex-engine
        key = get_key()
        if key == 'w':
            event = type('Event', (), {})()
            event.type = 'KEYDOWN'
            event.key = 'UP'
            engine.events.emit('input', event)
        elif key == 's':
            event = type('Event', (), {})()
            event.type = 'KEYDOWN'
            event.key = 'DOWN'
            engine.events.emit('input', event)

        # Let engine update physics and AI
        engine.events.emit('physics_update', None)

        # Ball movement (simulate physics step)
        bx, by, bz = ball.position
        vx, vy, vz = ball.velocity
        bx += vx
        by += vy

        # Collision with top/bottom
        if by <= 0 or by >= 600:
            vy = -vy
            by = max(0, min(by, 600))

        # Collision with paddles
        # Player paddle (left)
        if bx <= player_paddle.position[0] + 10 and abs(by - player_paddle.position[1]) < 60:
            vx = abs(vx)
        # AI paddle (right)
        elif bx >= ai_paddle.position[0] - 10 and abs(by - ai_paddle.position[1]) < 60:
            vx = -abs(vx)

        # Score: ball passes left or right
        if bx < 0:
            score['ai'] += 1
            bx, by = 400, 300
            vx, vy = -6, 4
        elif bx > 800:
            score['player'] += 1
            bx, by = 400, 300
            vx, vy = 6, 4

        ball.position = (bx, by, bz)
        ball.velocity = (vx, vy, vz)

        # ASCII render
        print(render_ascii(player_paddle.position[1], ai_paddle.position[1], ball.position[0], ball.position[1]))
        print(f"\nPlayer paddle: y={player_paddle.position[1]:.0f} | AI paddle: y={ai_paddle.position[1]:.0f} | Ball: x={ball.position[0]:.0f} y={ball.position[1]:.0f}")
        print(f"Score: Player {score['player']} | AI {score['ai']}")
        sys.stdout.flush()

        # Win/lose check
        if score['player'] >= 5:
            print('You win!')
            break
        elif score['ai'] >= 5:
            print('AI wins!')
            break
        time.sleep(0.08)
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
print("Simulation complete.")
