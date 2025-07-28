# Input System Architecture Solutions

When adding an input system to simplex-engine, here are two main implementation approaches to consider:

## Solution 1: Use a Python Input Library (e.g., `pygame`)
- **Description:** Integrate a mature Python library like `pygame` to handle keyboard, mouse, and gamepad input.
- **How it works:**
    - `pygame` provides event polling and input state management out of the box.
    - The engine's main loop calls `pygame.event.get()` to process input events and update game state.
    - Input events are dispatched to ECS or game logic as needed.
- **Pros:**
    - Well-tested, cross-platform, supports many input devices.
    - Easy to use and extend for more advanced input features.
- **Cons:**
    - Adds a dependency; may be heavier than needed for minimal MVP.
    - Tightly coupled to `pygame` event loop unless abstracted.

## Solution 2: Custom Event Loop with OS Hooks (e.g., `inputs`, `evdev`, or direct polling)
- **Description:** Implement a custom input system using lower-level libraries like `inputs` or `evdev` (Linux), or direct polling via OS APIs.
- **How it works:**
    - Poll input devices directly in the engine's main loop or via a dedicated thread.
    - Maintain input state and dispatch events to ECS/game logic.
    - Can be abstracted for cross-platform support.
- **Pros:**
    - Lightweight, minimal dependencies.
    - Full control over input handling and event dispatch.
- **Cons:**
    - More complex to implement and maintain.
    - May require platform-specific code for full device support.

## Next Steps
- Trade off these solutions based on project goals (simplicity, extensibility, platform support).
- Once a solution is chosen, update the architecture and TODO list accordingly.
