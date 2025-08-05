# Resource Usage Analytics & Error Reporting (MVP-3)

The ResourceManager now tracks detailed usage analytics and error logs for all resource operations.

## Features
- Tracks loads, unloads, cache size, and reference counts.
- Logs all resource actions (load, unload, errors) with timestamps.
- Records and exposes recent errors for debugging.
- Analytics available via `get_usage_analytics()`.

## Usage Example
```python
from simplex.resource.resource_manager import ResourceManager
rm = ResourceManager()
rm.load('assets/texture.png')
rm.unload('assets/texture.png')
print(rm.get_usage_analytics())
```

## Analytics Output Example
```
{
  'load_count': 5,
  'unload_count': 2,
  'cache_size': 3,
  'ref_counts': {'foo': 1},
  'recent_errors': [...],
  'usage_log': [...]
}
```

## Notes
- All errors are logged and accessible for debugging.
- Usage analytics can be used for profiling, debugging, and live monitoring.
