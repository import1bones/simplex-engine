#!/usr/bin/env python3
"""
Test runner for OpenGL renderer tests.
Runs all available tests and provides a summary.
"""

import sys
import os
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from simplex.utils.logger import log


def run_test(test_script, test_name, interactive=False):
    """Run a test script and return success status."""
    log(f"\n{'=' * 60}", level="INFO")
    log(f"Running {test_name}", level="INFO")
    log(f"{'=' * 60}", level="INFO")

    if interactive:
        log(
            "This is an interactive test - follow the on-screen instructions",
            level="INFO",
        )
        log("Press Ctrl+C here if the test window doesn't respond", level="INFO")

    try:
        # Get the directory of this script
        test_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.join(test_dir, test_script)

        # Run the test
        result = subprocess.run(
            [sys.executable, test_path],
            capture_output=not interactive,
            text=True,
            cwd=os.path.join(test_dir, "..", ".."),
        )

        if result.returncode == 0:
            log(f"✓ {test_name} PASSED", level="INFO")
            return True
        else:
            log(f"✗ {test_name} FAILED (exit code: {result.returncode})", level="ERROR")
            if not interactive and result.stderr:
                log(f"Error output: {result.stderr}", level="ERROR")
            return False

    except KeyboardInterrupt:
        log(f"✗ {test_name} INTERRUPTED by user", level="WARNING")
        return False
    except Exception as e:
        log(f"✗ {test_name} FAILED with exception: {e}", level="ERROR")
        return False


def main():
    """Run all OpenGL renderer tests."""
    log("OpenGL Renderer Test Suite", level="INFO")
    log("=" * 60, level="INFO")

    # Define available tests
    tests = [
        ("test_opengl_basic.py", "Basic OpenGL Tests", False),
        ("test_opengl_interactive.py", "Interactive Test (Manual)", True),
        ("test_opengl_minecraft.py", "Minecraft World Test (Manual)", True),
    ]

    # Ask user which tests to run
    print("\nAvailable tests:")
    for i, (script, name, interactive) in enumerate(tests, 1):
        print(f"  {i}. {name} {'(Interactive)' if interactive else '(Automated)'}")

    print(f"  {len(tests) + 1}. Run all automated tests")
    print(f"  {len(tests) + 2}. Run all tests (including interactive)")

    try:
        choice = input(f"\nSelect test to run (1-{len(tests) + 2}): ").strip()

        if not choice:
            choice = "1"  # Default to basic tests

        choice_num = int(choice)

        if 1 <= choice_num <= len(tests):
            # Run specific test
            script, name, interactive = tests[choice_num - 1]
            success = run_test(script, name, interactive)
            log(f"\n{'=' * 60}", level="INFO")
            if success:
                log("🎉 Test completed successfully!", level="INFO")
            else:
                log("❌ Test failed!", level="ERROR")

        elif choice_num == len(tests) + 1:
            # Run all automated tests
            log("Running all automated tests...", level="INFO")
            passed = 0
            total_auto = sum(1 for _, _, interactive in tests if not interactive)

            for script, name, interactive in tests:
                if not interactive:
                    if run_test(script, name, interactive):
                        passed += 1

            log(f"\n{'=' * 60}", level="INFO")
            log(f"Automated Test Results: {passed}/{total_auto} passed", level="INFO")

            if passed == total_auto:
                log("🎉 All automated tests PASSED!", level="INFO")
            else:
                log("❌ Some automated tests FAILED!", level="ERROR")

        elif choice_num == len(tests) + 2:
            # Run all tests
            log("Running all tests (including interactive)...", level="INFO")
            passed = 0
            total = len(tests)

            for script, name, interactive in tests:
                if run_test(script, name, interactive):
                    passed += 1

            log(f"\n{'=' * 60}", level="INFO")
            log(f"All Test Results: {passed}/{total} passed", level="INFO")

            if passed == total:
                log("🎉 All tests PASSED!", level="INFO")
            else:
                log("❌ Some tests FAILED!", level="ERROR")
        else:
            log("Invalid choice. Running basic tests by default.", level="WARNING")
            script, name, interactive = tests[0]
            run_test(script, name, interactive)

    except (ValueError, KeyboardInterrupt):
        log("Invalid input or interrupted. Exiting.", level="WARNING")
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
