# LRU Cache

A fixed-capacity **Least Recently Used cache** implemented with Python's `OrderedDict`, with edge-case tests, cache statistics, and a small performance benchmark.

## Design

Accessing an item promotes it to the most-recent position. When capacity is exceeded, the least-recent item is evicted.

- `get`: O(1) average case
- `put`: O(1) average case
- Space: O(capacity)
- Tracks hits, misses, and evictions
- Correctly distinguishes a missing key from a stored `None`
- Provides `peek` for inspection without changing recency or statistics
- Validates capacity eagerly (positive integers only)

## API notes

- `get(key, default=None)` returns a value, promotes a hit to most-recently
  used, and records a hit or miss.
- `peek(key, default=None)` returns a value without promoting it or changing
  statistics. This is useful for diagnostics and conditional logic.
- `clear()` removes values but retains statistics, while `reset_stats()` resets
  counters without removing values. Keeping these operations separate makes
  reporting windows explicit.

## Run

```bash
python -m pytest -q
python benchmark.py
```

## Resume value

Demonstrates practical data-structure design, API semantics, unit testing, complexity analysis, and lightweight performance measurement.
