# LRU Cache

A compact Python implementation of a fixed-capacity **Least Recently Used (LRU) cache** with tests covering eviction and recency behavior.

## Design

The cache uses Python's `OrderedDict` to maintain insertion/access order. Reads promote the accessed key to the most-recent position; when capacity is exceeded, the least-recent entry is evicted.

### Complexity

- `get`: O(1) average case
- `put`: O(1) average case
- Space: O(capacity)

## Run Tests

```bash
python -m pytest -q
```

## Tech Stack

**Python · Data Structures · Caching · Unit Testing**

## Resume Description

**LRU Cache | Python, Data Structures, Pytest**

Implemented a fixed-capacity LRU cache with O(1) average-case lookup, insertion, recency updates, and eviction using an ordered hash-map abstraction. Added unit tests covering least-recently-used eviction, key updates, and invalid-capacity handling.
