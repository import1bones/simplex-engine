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

## TODO (Status as of July 2025)

### 1. Project Setup
- [x] Create `examples/ping_pong/` directory
- [x] Scaffold main game script (`main.py`)
- [x] Add config file for game settings (e.g., paddle speed, ball speed)

### 2. Game Entities & ECS
- [x] Define paddle and ball entities (ECS)
- [x] Add components: position, velocity, render, input, score
- [x] Register systems: movement, collision, scoring, rendering (basic, not full ECS)


### 3. Physics & Collision
- [~] Use Physics subsystem for ball movement and paddle collision (**partially: ECS/engine structure in place, but CLI loop handles movement/collision manually**)
- [~] Emit collision events for scoring and bounce (**partially: event system in place, but collisions handled in CLI loop, not via event system**)

### 4. Input Handling
- [x] Map keyboard input to paddle movement (**via engine event system in CLI**)
- [x] Support two-player or AI paddle (**AI paddle implemented**)

### 5. Rendering & GUI
- [~] Render paddles, ball, and background (**CLI ASCII only; no GUI renderer yet**)
- [~] Overlay score and win/lose messages (simple text) (**CLI only**)

### 6. Game Logic
- [x] Implement start, pause, and restart logic (**basic win/lose, restart via engine.reset()**)
- [x] Handle win/lose conditions and reset


### 7. Testing & Polish
- [ ] Add basic tests for game logic (optional)
- [ ] Polish gameplay (tuning, feedback)
- [ ] Document code and usage in `README.md`

---
## MVP-4 Status Summary (July 2025)

**CLI/architecture verification is complete:**
- Paddle control, input, and event system are fully tested in the CLI sample.
- ECS/entity structure, event system, and basic game logic are in place and working.

**Not yet possible (engine work required):**
- Physics/collision and scoring are not handled by the engine’s physics/collision subsystems or event system.
- No real GUI rendering; only CLI ASCII output is available.

**Next steps for full GUI MVP:**
1. Move all ball/paddle movement and collision logic into the engine’s physics and event subsystems.
2. Implement collision event emission and handling for scoring and bounce.
3. Build a real GUI renderer for paddles, ball, background, and overlays.
4. Add polish, tests, and documentation.

**Conclusion:**
MVP-4 is complete for CLI/architecture verification. For a true GUI MVP, further engine subsystem work is required.

---
**Target:**
The goal is a GUI ping-pong game using simplex-engine, demonstrating real-world use of all core subsystems:
- Input/events, ECS, physics, collision, rendering, scoring, and game logic should all be handled by the engine (not manual CLI logic).

**Current status:**
- CLI sample now verifies input and event system integration (paddle control via engine events).
- Physics/collision and rendering are still handled manually in the CLI loop.
- Next steps: move all movement/collision/score logic into engine subsystems and event system, and implement a real GUI renderer.
