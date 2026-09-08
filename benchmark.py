"""Simple workload benchmark for the custom LRU implementation."""

import time

from lru_cache import LRUCache


def benchmark(operations: int = 100_000, capacity: int = 10_000) -> float:
    cache = LRUCache(capacity)
    start = time.perf_counter()
    for key in range(operations):
        cache.put(key, key)
        cache.get(key)
    elapsed = time.perf_counter() - start
    print(f"operations={operations:,} elapsed={elapsed:.4f}s stats={cache.stats()}")
    return elapsed


if __name__ == "__main__":
    benchmark()
