# Getting Started with Simplex Engine

Welcome to Simplex Engine! This section will guide you through installation, setup, and creating your first game.

## What is Simplex Engine?

Simplex Engine is a modern, lightweight game engine built in Python. It features:
- **Entity-Component-System (ECS)** architecture for flexible game object management
- **Event-driven** communication between systems
- **Hot-reloading** for rapid development
- **Multiple backends** for rendering, physics, and audio
- **Simple API** that's easy to learn and use

## Quick Start Path

Follow this recommended learning path:

### 1. 📦 [Installation & Setup](./installation.md)
Get Simplex Engine installed and running on your system.

### 2. 🎮 [Your First Project](./first-project.md)
Create a simple "Hello World" project to verify everything works.

### 3. 🏓 [Ping Pong Tutorial](./ping-pong-tutorial.md)
Build a complete Ping Pong game step-by-step. This tutorial covers:
- Creating entities and components
- Implementing game systems
- Handling input
- Physics and collision detection
- Scoring and game state

### 4. ⚙️ [Configuration Guide](./configuration.md)
Learn how to configure the engine for your specific needs.

## Prerequisites

Before you begin, you should have:
- **Python 3.8+** installed on your system
- Basic knowledge of **Python programming**
- Familiarity with **object-oriented programming** concepts
- A **text editor** or IDE (VS Code, PyCharm, etc.)

## Getting Help

If you run into issues:
1. Check the [Troubleshooting](#troubleshooting) section below
2. Review the [API Reference](../api/complete.md)
3. Look at the [Examples](../examples/) for working code
4. [File an issue](https://github.com/import1bones/simplex-engine/issues) if you find a bug

## Troubleshooting

### Common Issues

**Import Error: No module named 'simplex'**
- Make sure you've installed the engine: `uv add simplex-engine`
- Verify you're using the correct Python environment

**Pygame not found**
- Install pygame: `uv add pygame`
- Some systems require additional dependencies

**Permission errors**
- On Linux/Mac, you might need to install system packages
- Check the [Installation Guide](./installation.md) for platform-specific instructions

### Getting More Help

- **Documentation**: Browse the [Core Concepts](../core-concepts/README.md)
- **Examples**: Check [working examples](../examples/)
- **Community**: Join discussions on GitHub
- **Bug Reports**: [Create an issue](https://github.com/import1bones/simplex-engine/issues)

## What's Next?

Once you've completed the getting started guides:
- Explore [Core Concepts](../core-concepts/README.md) to understand the engine deeply
- Learn about specific [Systems & Features](../systems/)
- Try more complex [Examples & Tutorials](../examples/)
- Dive into [Advanced Topics](../advanced/) for sophisticated features

---

Ready to begin? Start with [Installation & Setup](./installation.md)!
