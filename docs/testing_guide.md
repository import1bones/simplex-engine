# Testing Guide (MVP-3)

## Running Tests
To run all integration and edge-case tests:

```shell
python -m unittest discover tests
```

## What is Covered
- Engine integration
- Physics (rigid/soft body, event emission)
- ResourceManager (error handling)
- Input (custom backend)

## Extending Tests
- Add new test files to the `tests/` directory.
- Use `unittest` for new subsystems or edge cases.
- See `tests/test_edge_cases.py` for examples.

---
For more, see subsystem docs and code docstrings.
