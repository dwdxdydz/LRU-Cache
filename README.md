# LRU Cache

## What is this?

This project implements an **LRU (Least Recently Used) Cache** in Python.

A cache stores frequently used data so that it can be accessed quickly.

When the cache becomes full, the item that has not been used for the longest time is removed.

## Simple example

Imagine the cache can hold 3 items:

```
Put A
[A]

Put B
[A, B]

Put C
[A, B, C]

Use A
[B, C, A]

Put D
[C, A, D]
     ↑
     B was removed because it was least recently used
```

## Main idea

The cache needs two important operations:

- `get(key)` — retrieve a value
- `put(key, value)` — add or update a value

The implementation is designed to make these operations **O(1) average time**.

## Files

- `lru_cache.py` — cache implementation
- `test_lru_cache.py` — automated tests
- `benchmark.py` — performance comparison

## Run it

Run tests:

```bash
pytest -q
```

Run the benchmark:

```bash
python benchmark.py
```

## Important terms

**Cache:** temporary storage for data that is expensive or slow to calculate/fetch.

**LRU:** Least Recently Used.

**O(1):** operation takes approximately constant time as the input size grows.

**Eviction:** removing an item from the cache.

**Hit:** requested data is already in the cache.

**Miss:** requested data is not in the cache.

## What this project demonstrates

- Data structures
- Algorithms
- Hash-map based lookup
- Cache design
- Time-complexity analysis
- Testing
- Benchmarking
