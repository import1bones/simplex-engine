# simplex-engine

Simplex Engine is a modern game engine written in Python.
We believe hardware performance will continue to improve in the future.
This project aims to deliver the best experience to our customers:
- Game players
- Game developers
- Video creators
...

We believe a simplified engine (less code complexity, more functionality) will make game and video development faster, easier, and better.

## Architecture


- Modular subsystems: ECS, Renderer, Physics, ScriptManager, ResourceManager, Audio, Input, EventSystem
- Event-driven architecture: subsystems communicate via a unified event system
- Input system: abstract API, pygame backend, handles initialization internally, emits events, backend can be swapped
- Centralized configuration management via TOML
- Multi-level logging and robust error handling

### Advantages

By using Python for all subsystems, this engine provides dynamic behavior when building game or video systems.
For example, when you write a command, you immediately see the result on your monitor. Once you confirm it works as intended, you can build for better performance.

Python offers a superior development interface, making development and debugging easier and faster.
