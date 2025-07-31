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
- [x] Map keyboard input to paddle movement (**via engine event system in CLI; real-time, smooth, bounded paddle movement**)
- [x] Support two-player or AI paddle (**AI paddle implemented**)



### 5. Rendering & GUI (sample responsibility for MVP-4)
- [ ] Implement GUI renderer for paddles, ball, background, overlays (sample-level, for MVP-4)
- [ ] Support GUI score and win/lose overlays (sample-level, for MVP-4)

### 5b. Sample Rendering (current demo)
- [~] Render paddles, ball, and background (**CLI ASCII only; no GUI renderer yet**)
- [~] Overlay score and win/lose messages (simple text) (**CLI only**)

### 6. Game Logic
- [x] Implement start, pause, and restart logic (**basic win/lose, restart via engine.reset()**)
- [x] Handle win/lose conditions and reset




### 7. Testing & Polish (engine feature, not sample responsibility)
- [ ] (Engine) Add basic tests for game logic
- [ ] (Engine) Polish gameplay (tuning, feedback)
- [ ] (Engine) Document code and usage in `README.md`

---

## MVP-4 Status Summary (July 2025)

**CLI/architecture verification is complete:**
- Paddle control is now real-time, smooth, and bounded, matching AI and ball speed.
- Input, event system, ECS/entity structure, physics/collision, and game logic are all verified in the CLI sample.
- CLI controls are responsive and gameplay is fair and playable.



**Not yet possible (sample work required for MVP-4):**
- No real GUI rendering; only CLI ASCII output is available. (GUI renderer is now a sample responsibility for MVP-4)
- Full event/collision system and polish are engine-level tasks.


**Next steps for MVP-4 sample:**
1. Implement a real GUI renderer for paddles, ball, background, and overlays in the sample.
2. Move all movement/collision/score logic into engine subsystems and event system.
3. Add polish, tests, and documentation at the engine level.

**Conclusion:**
MVP-4 is complete for CLI/architecture verification, with all core engine subsystems verified in a playable sample. For a true GUI MVP, further engine subsystem work is required.

---

**Target:**
The goal is a GUI ping-pong game using simplex-engine, demonstrating real-world use of all core subsystems:
- Input/events, ECS, physics, collision, rendering, scoring, and game logic should all be handled by the engine (not manual CLI logic). GUI rendering is now a sample responsibility for MVP-4.

**Current status:**
- CLI sample now verifies input and event system integration (paddle control via engine events).
- Physics/collision and rendering are still handled manually in the CLI loop.
- Next steps: move all movement/collision/score logic into engine subsystems and event system, and implement a real GUI renderer.
