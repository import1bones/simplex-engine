# MVP-Sample-4: GUI Ping-Pong Game TODO List

## Goal
Build a simple GUI ping-pong game using simplex-engine, demonstrating real-world use of all core subsystems.

## Features
- Player paddle (keyboard/gamepad control)
- AI or second player paddle
- Ball with physics and collision
- Score display (basic GUI overlay)
- Game start/restart logic
- Win/lose conditions

## TODO

### 1. Project Setup
- [ ] Create `examples/ping_pong/` directory
- [ ] Scaffold main game script (`main.py`)
- [ ] Add config file for game settings (e.g., paddle speed, ball speed)

### 2. Game Entities & ECS
- [ ] Define paddle and ball entities (ECS)
- [ ] Add components: position, velocity, render, input, score
- [ ] Register systems: movement, collision, scoring, rendering

### 3. Physics & Collision
- [ ] Use Physics subsystem for ball movement and paddle collision
- [ ] Emit collision events for scoring and bounce

### 4. Input Handling
- [ ] Map keyboard/gamepad input to paddle movement
- [ ] Support two-player or AI paddle

### 5. Rendering & GUI
- [ ] Render paddles, ball, and background
- [ ] Overlay score and win/lose messages (simple text)

### 6. Game Logic
- [ ] Implement start, pause, and restart logic
- [ ] Handle win/lose conditions and reset

### 7. Testing & Polish
- [ ] Add basic tests for game logic (optional)
- [ ] Polish gameplay (tuning, feedback)
- [ ] Document code and usage in `README.md`

---
This MVP will serve as a reference for building simple games with simplex-engine and as a template for future projects.
