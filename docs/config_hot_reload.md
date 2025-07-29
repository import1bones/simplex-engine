# Config Hot-Reloading (MVP-3)

The engine now supports live configuration hot-reloading. When the config file (e.g., `examples/config.toml`) is changed, the engine automatically reloads the config and emits a `config_reload` event.

## How it works
- The `ConfigHotReloader` watches the config file for changes (using polling).
- When a change is detected, it reloads the config and emits a `config_reload` event via the EventSystem (if present).
- Subsystems can listen for this event to update their settings live.

## Usage Example
```python
from simplex.config.config_hot_reloader import ConfigHotReloader

config = Config('examples/config.toml')
events = EventSystem()
reloader = ConfigHotReloader(config, 'examples/config.toml', event_system=events)

def on_config_reload(new_config):
    print('Config reloaded! New value:', new_config.get('some_key'))

events.register('config_reload', on_config_reload)

# In your main loop or tick:
reloader.run_once()  # or reloader.run_forever() in a background thread
```

## Extending
- You can change the polling interval or use a different event name.
- Subsystems can subscribe to `config_reload` to update their state.

## Notes
- The config file must be valid TOML after edits.
- The engine demo calls `run_once()` on each tick; for continuous watching, use `run_forever()` in a thread.
