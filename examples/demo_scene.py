"""
Demo scene entry point for simplex-engine.
Demonstrates subsystem interactions and event-driven architecture.
"""

from simplex.engine import Engine


def main():
    engine = Engine(config_path="examples/config.toml")
    engine.run()


if __name__ == "__main__":
    main()
