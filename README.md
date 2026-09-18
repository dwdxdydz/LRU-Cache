# ⚡ High-Performance LRU Cache (Least Recently Used)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://pytest.org/)
[![Complexity](https://img.shields.io/badge/Time%20Complexity-O(1)%20Strict-blueviolet.svg)](#algorithmic-complexity)
[![CI](https://github.com/dwdxdydz/LRU-Cache/actions/workflows/ci.yml/badge.svg)](https://github.com/dwdxdydz/LRU-Cache/actions)

A production-grade, strictly $O(1)$ constant-time **Least Recently Used (LRU) Cache** implementation in Python featuring both a first-principles **Doubly-Linked List + Hash Map** architecture and an **OrderedDict** variant, with thread-safety, TTL support, and function decorator capabilities.

---

## 🏛️ Architecture: Doubly-Linked List + Hash Map

```
             ┌────────────────────────────────────────────────────────┐
             │                   Hash Map (dict)                      │
             │   Key A ──> Node A       Key B ──> Node B              │
             └──────┬───────────────────────┬─────────────────────────┘
                    │                       │
                    ▼                       ▼
    [ Sentinel Head ] <───> [ Node B (MRU) ] <───> [ Node A (LRU) ] <───> [ Sentinel Tail ]
     (Most Recent)                                                          (Least Recent)
```

### Why Doubly-Linked List + Hash Map?
- **Hash Map**: Provides instantaneous $O(1)$ key lookup.
- **Doubly-Linked List**: Enables $O(1)$ arbitrary node extraction and insertion without shifting array elements.
- **Sentinel Nodes**: Eliminates edge cases (null checks) when inserting at head or evicting at tail.

---

## 🚀 Features

- **Strict $O(1)$ Operations**: $O(1)$ time complexity for `get()`, `put()`, `peek()`, and eviction.
- **Two Implementations**:
  - `DoublyLinkedListLRUCache`: Custom node pointer mechanics (demonstrating algorithmic first-principles).
  - `LRUCache`: High-performance `OrderedDict` standard-library implementation.
- **Thread-Safety**: Optional reentrant lock (`threading.RLock`) for concurrent environments.
- **Time-To-Live (TTL)**: Optional per-entry or cache-wide automatic expiration.
- **`@lru_cached` Decorator**: Function memoization with `.cache_info()` and `.cache_clear()` helpers.
- **Telemetry & Diagnostics**: Real-time hit, miss, eviction, and expiration counters.

---

## 📊 Algorithmic Complexity

| Operation | Time Complexity | Space Complexity | Description |
| :--- | :---: | :---: | :--- |
| **`get(key)`** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Hash lookup + promote node to head |
| **`put(key, val)`** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Hash insert + insert at head + optional tail pop |
| **`peek(key)`** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Read without altering recency |
| **`clear()`** | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Reset internal pointers |

---

## 💻 Usage

```python
from lru_cache import DoublyLinkedListLRUCache, LRUCache, lru_cached

# 1. Custom Doubly-Linked List LRU Cache
cache = DoublyLinkedListLRUCache(capacity=3, thread_safe=True)
cache.put("user_1", {"name": "Alice"})
cache.put("user_2", {"name": "Bob"})
cache.put("user_3", {"name": "Charlie"})

# Access user_1 (promotes to Most-Recently Used)
print(cache.get("user_1"))  # => {'name': 'Alice'}

# Insert 4th item (evicts user_2, since user_1 was recently accessed)
cache.put("user_4", {"name": "David"})
print(cache.get("user_2"))  # => None (evicted!)

# Check telemetry
print(cache.stats())
# => {'hits': 1, 'misses': 1, 'evictions': 1, 'expirations': 0}

# 2. Function Memoization Decorator
@lru_cached(capacity=128, ttl_seconds=60)
def expensive_query(query_id: int):
    # Simulating heavy query / computation
    return f"Result for {query_id}"
```

---

## ⚡ Benchmarks

Run the built-in benchmark suite:

```bash
python benchmark.py
```

*Sample Results (100,000 operations, 80/20 Zipfian access skew):*

```text
┌─ Custom Doubly-Linked List + Hash Map (O(1) First Principles)
│ Operations:   100,000
│ Elapsed Time: 38.42 ms
│ Throughput:   2,602,811 ops/sec
│ Hit Rate:     79.8% (79,842 hits / 20,158 misses)
│ Evictions:    19,158
└──────────────────────────────────────────────
```

---

## 🧪 Testing

```bash
pytest -v
```

---

## 📄 License
MIT License.
