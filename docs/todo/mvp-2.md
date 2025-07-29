# MVP-2 (Sprint 2 / MCP+): TODO List for simplex-engine

## Sprint 2 TODOs

### Audio System
- [x] Implement Audio subsystem (play, stop, resource management)
- [x] Integrate with ResourceManager for audio assets
- [x] Add basic sound playback to demo scenes (mocked in tests, demo scene integration in progress)

### Advanced Scripting & Hot-Reloading
- [x] Add hot-reloading for Python scripts
- [x] Enable dynamic updates to game logic without restarting the engine

### Demo Scene Expansion & Example Projects
- [x] Expand MVP demo in `examples/mvp/` to showcase all subsystems, including audio and advanced scripting (initial version complete, further expansion planned)
- [x] Add onboarding documentation and usage examples

### Resource Manager Enhancements
- [x] Add resource caching and reference counting
- [ ] Support more resource types (e.g., shaders, advanced materials)

### Renderer Improvements
- [x] Add support for advanced primitives, materials, and effects (scaffolded, basic support implemented)
- [x] Implement basic scene graph

### Input System Extensibility
- [x] Prototype a lightweight or platform-specific backend (pygame, abstraction in place)
- [x] Document backend swap process and limitations

### Testing & Documentation
- [x] Write unit tests for new features and subsystems (all major subsystems covered, file-independent)
- [x] Update architecture, design, and decision docs
- [x] Document configuration options and event types

---
Sprint 2 TODOs focus on expanding engine capabilities, improving user/developer experience, and validating extensibility for future growth.

---
**Next Steps:**
- Expand demo scene with more advanced features and onboarding
- Further enhance renderer (materials, effects)
- Add more resource types (e.g., shaders)
- Continue improving documentation and onboarding
- Add more integration and edge-case tests as new features are added
