# MVP-2 Demo Scene: Quick Start

This demo showcases the core features of simplex-engine MVP-2:
- Resource loading and caching
- Audio playback (requires a .wav file at examples/mvp/demo_sound.wav)
- Script hot-reloading (edit demo_script.py and rerun demo_scene.py)
- Event-driven input system

## How to Run

1. Ensure you have all dependencies installed (see project README).
2. Place a .wav file at `examples/mvp/demo_sound.wav` for audio playback.
3. Run the demo scene:

   ```bash
   python -m examples.mvp.demo_scene
   ```

4. Edit `demo_script.py` and rerun the demo to see hot-reloading in action.

## Customization
- Edit `config.toml` to change engine settings, audio, and resource paths.
- Add your own scripts and assets to expand the demo.

---
For more details, see the main project documentation.
