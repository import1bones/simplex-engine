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
        key = getattr(event, 'key', None)
        # Clamp paddle movement within bounds 0 to 600
        PADDLE_SPEED = 18  # Increased speed for more responsive play
        if key in ('UP', 'K_UP', 'w'):
            x, y, z = player_paddle.position
            new_y = min(y + PADDLE_SPEED, 600)
            player_paddle.position = (x, new_y, z)
        elif key in ('DOWN', 'K_DOWN', 's'):
            x, y, z = player_paddle.position
            new_y = max(y - PADDLE_SPEED, 0)
            player_paddle.position = (x, new_y, z)
engine.events.register('input', handle_input)


# AI paddle and ball/physics/collision/scoring logic in engine events
def ai_and_physics_update(event):
    # AI paddle follows ball
    if ball.position[1] > ai_paddle.position[1]:
        ai_paddle.apply_impulse((0, 6, 0))
    elif ball.position[1] < ai_paddle.position[1]:
        ai_paddle.apply_impulse((0, -6, 0))

    # Ball movement (physics step)
    bx, by, bz = ball.position
    vx, vy, vz = ball.velocity
    bx += vx
    by += vy

    # Collision with top/bottom
    if by <= 0 or by >= 600:
        vy = -vy
        by = max(0, min(by, 600))
        # Emit collision event for wall
        wall_event = type('Event', (), {})()
        wall_event.type = 'collision'
        wall_event.object = 'wall'
        engine.events.emit('physics_collision', wall_event)

    # Collision with paddles
    hit_paddle = False
    # Player paddle (left)
    if bx <= player_paddle.position[0] + 10 and abs(by - player_paddle.position[1]) < 60:
        vx = abs(vx)
        hit_paddle = 'player'
    # AI paddle (right)
    elif bx >= ai_paddle.position[0] - 10 and abs(by - ai_paddle.position[1]) < 60:
        vx = -abs(vx)
        hit_paddle = 'ai'
    if hit_paddle:
        paddle_event = type('Event', (), {})()
        paddle_event.type = 'collision'
        paddle_event.object = hit_paddle
        engine.events.emit('physics_collision', paddle_event)

    # Score: ball passes left or right
    scored = None
    if bx < 0:
        score['ai'] += 1
        bx, by = 400, 300
        vx, vy = -6, 4
        scored = 'ai'
    elif bx > 800:
        score['player'] += 1
        bx, by = 400, 300
        vx, vy = 6, 4
        scored = 'player'
    if scored:
        score_event = type('Event', (), {})()
        score_event.type = 'score'
        score_event.object = scored
        engine.events.emit('score', score_event)

    ball.position = (bx, by, bz)
    ball.velocity = (vx, vy, vz)

engine.events.register('physics_update', ai_and_physics_update)

# Collision: bounce and scoring (for logging/demo)
def on_collision(event):
    if hasattr(event, 'object'):
        if event.object == 'wall':
            print('[Event] Ball bounced off wall!')
        elif event.object == 'player':
            print('[Event] Ball hit player paddle!')
        elif event.object == 'ai':
            print('[Event] Ball hit AI paddle!')
engine.events.register('physics_collision', on_collision)

# Score event (for logging/demo)
def on_score(event):
    if hasattr(event, 'object'):
        print(f'[Event] {event.object.capitalize()} scores!')
engine.events.register('score', on_score)

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
import threading
try:
    tick = 0
    state = {'running': True, 'last_key': None, 'w_down': False, 's_down': False}
    FRAME_TIME = 1.0 / 60  # 60 FPS
    INPUT_POLL_INTERVAL = 0.005  # 5ms

    def input_thread():
        while state['running']:
            key = get_key()
            if key:
                # Track key state for continuous movement
                if key == 'w':
                    state['w_down'] = True
                elif key == 's':
                    state['s_down'] = True
                elif key == 'q':
                    state['running'] = False
                # Key up simulation (if user presses other key, release previous)
                if key not in ('w', 's'):
                    state['w_down'] = False
                    state['s_down'] = False
            else:
                # No key pressed, release both
                state['w_down'] = False
                state['s_down'] = False
            time.sleep(INPUT_POLL_INTERVAL)

    t = threading.Thread(target=input_thread, daemon=True)
    t.start()

    while state['running']:
        tick += 1
        frame_start = time.time()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Tick {tick} | Player {score['player']} : {score['ai']} AI\n")

        # Handle input (continuous movement)
        if state['w_down']:
            event = type('Event', (), {})()
            event.type = 'KEYDOWN'
            event.key = 'UP'
            engine.events.emit('input', event)
        if state['s_down']:
            event = type('Event', (), {})()
            event.type = 'KEYDOWN'
            event.key = 'DOWN'
            engine.events.emit('input', event)

        # Let engine update physics, AI, ball, collision, and scoring
        engine.events.emit('physics_update', None)

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

        # Maintain frame rate
        elapsed = time.time() - frame_start
        if elapsed < FRAME_TIME:
            time.sleep(FRAME_TIME - elapsed)
finally:
    state['running'] = False
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
print("Simulation complete.")
