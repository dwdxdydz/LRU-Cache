# ⚡ LRU Cache

A fixed-capacity **Least Recently Used (LRU) cache** implemented with Python's `OrderedDict`, including edge-case tests, cache statistics, and a lightweight performance benchmark.

## Design

```text
get(key)
  ↓
Found? ── Yes → return value + promote to MRU
  │
 No → record miss + return default

put(key, value)
  ↓
Store / update value
  ↓
Capacity exceeded?
  ↓ Yes
Evict least-recently-used item
```

## Complexity

- `get`: O(1) average case
- `put`: O(1) average case
- `peek`: O(1) average case
- Space: O(capacity)

## Features

- Fixed capacity
- LRU eviction
- Hit, miss, and eviction statistics
- Correct handling of a stored `None` value
- `peek()` for inspection without changing recency/statistics
- `clear()` and `reset_stats()` with explicit semantics
- Eager capacity validation
- Automated tests
- Performance benchmark

## API

- `get(key, default=None)` — returns a value and promotes a hit to most-recently-used
- `put(key, value)` — inserts or updates an item
- `peek(key, default=None)` — reads without changing recency/statistics
- `clear()` — removes cached values while retaining statistics
- `reset_stats()` — resets counters without removing cached values

## Run

```bash
python -m pytest -q
python benchmark.py
```

## Portfolio value

Demonstrates **data-structure design, Python API design, algorithmic complexity, unit testing, edge-case handling, performance measurement, and software engineering fundamentals**.

## Future improvements

- Compare performance with `functools.lru_cache`
- Larger benchmark workloads
- Optional TTL support
- Optional thread-safe implementation
