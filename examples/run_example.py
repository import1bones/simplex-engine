"""Simple example runner for the Simplex Engine examples directory.

Usage:
    python3 examples/run_example.py           # list examples and prompt
    python3 examples/run_example.py demo_chunk  # run specific example by name

This runner executes example scripts in a subprocess using the current
Python interpreter and ensures PYTHONPATH includes the project root so
examples can import the `simplex` package.
"""

import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "examples"


def discover_examples():
    examples = {}
    for dirpath, dirnames, filenames in os.walk(EXAMPLES_DIR):
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            if fn.startswith("__"):
                continue
            full = Path(dirpath) / fn
            # key: relative path from examples without .py, use underscores for name
            rel = full.relative_to(EXAMPLES_DIR).with_suffix("")
            name = "_".join(rel.parts)
            examples[name] = str(full)
            # also add a short alias using the file stem if not already present
            stem = full.stem
            if stem not in examples:
                examples[stem] = str(full)
    return examples


def run_example(path: str):
    env = os.environ.copy()
    # Ensure project root is on PYTHONPATH so scripts import simplex
    env["PYTHONPATH"] = str(ROOT)
    print(f"Running example: {path}")
    proc = subprocess.run([sys.executable, path], env=env)
    return proc.returncode


def main():
    examples = discover_examples()
    if not examples:
        print("No examples found in examples/")
        return 1

    if len(sys.argv) >= 2:
        name = sys.argv[1]
        if name not in examples:
            print(f"Example '{name}' not found. Available examples:")
            for k in sorted(examples):
                print("  ", k)
            return 2
        return_code = run_example(examples[name])
        return return_code

    # No arg: list and interactive choose
    print("Available examples:")
    for i, k in enumerate(sorted(examples.keys()), start=1):
        print(f"  {i}. {k}")
    try:
        choice = input("Choose an example number (or press Enter to cancel): ")
        if not choice.strip():
            print("Cancelled")
            return 0
        idx = int(choice) - 1
        name = sorted(examples.keys())[idx]
    except Exception:
        print("Invalid choice")
        return 3

    return_code = run_example(examples[name])
    return return_code


if __name__ == "__main__":
    sys.exit(main())
