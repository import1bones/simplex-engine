"""
MVP-2 Demo Scene for simplex-engine
Demonstrates: resource loading, audio playback, hot-reloading, and event-driven input.
"""

from simplex.engine import Engine


def main():
    engine = Engine(config_path="examples/config.toml")
    engine.run()


if __name__ == "__main__":
    main()
