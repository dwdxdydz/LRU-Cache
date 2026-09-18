"""
Performance Benchmarking Suite for LRUCache and DoublyLinkedListLRUCache.
Measures throughput (operations/second), hit rates, and latency under various access distributions.
"""

from functools import lru_cache as builtin_lru_cache
import random
import time
from lru_cache import DoublyLinkedListLRUCache, LRUCache


def benchmark_workload(name: str, cache_cls, num_ops: int = 100_000, capacity: int = 1_000):
    cache = cache_cls(capacity)
    # Generate Zipf-like access distribution (80% accesses to top 20% keys)
    hot_keys = [f"key_{i}" for i in range(200)]
    cold_keys = [f"key_{i}" for i in range(200, 5000)]

    start = time.perf_counter()
    for _ in range(num_ops):
        key = random.choice(hot_keys) if random.random() < 0.8 else random.choice(cold_keys)
        val = cache.get(key)
        if val is None:
            cache.put(key, f"val_{key}")

    elapsed = time.perf_counter() - start
    ops_per_sec = num_ops / elapsed
    stats = cache.stats()
    hit_rate = (stats["hits"] / (stats["hits"] + stats["misses"])) * 100

    print(f"┌─ {name}")
    print(f"│ Operations:   {num_ops:,}")
    print(f"│ Elapsed Time: {elapsed * 1000:.2f} ms")
    print(f"│ Throughput:   {ops_per_sec:,.0f} ops/sec")
    print(f"│ Hit Rate:     {hit_rate:.1f}% ({stats['hits']:,} hits / {stats['misses']:,} misses)")
    print(f"│ Evictions:    {stats['evictions']:,}")
    print(f"└──────────────────────────────────────────────\n")


def benchmark_builtin_functools(num_ops: int = 100_000, capacity: int = 1_000):
    @builtin_lru_cache(maxsize=capacity)
    def fetch_data(key: str) -> str:
        return f"val_{key}"

    hot_keys = [f"key_{i}" for i in range(200)]
    cold_keys = [f"key_{i}" for i in range(200, 5000)]

    start = time.perf_counter()
    for _ in range(num_ops):
        key = random.choice(hot_keys) if random.random() < 0.8 else random.choice(cold_keys)
        _ = fetch_data(key)

    elapsed = time.perf_counter() - start
    ops_per_sec = num_ops / elapsed
    info = fetch_data.cache_info()
    hit_rate = (info.hits / (info.hits + info.misses)) * 100

    print(f"┌─ Python functools.lru_cache (C-Optimized Standard Library)")
    print(f"│ Operations:   {num_ops:,}")
    print(f"│ Elapsed Time: {elapsed * 1000:.2f} ms")
    print(f"│ Throughput:   {ops_per_sec:,.0f} ops/sec")
    print(f"│ Hit Rate:     {hit_rate:.1f}%")
    print(f"└──────────────────────────────────────────────\n")


if __name__ == "__main__":
    print("\n⚡ Running LRU Cache Benchmark Suite (100,000 Operations, Skewed Distribution)...\n")
    benchmark_workload("Custom Doubly-Linked List + Hash Map (O(1) First Principles)", DoublyLinkedListLRUCache)
    benchmark_workload("OrderedDict LRU Cache (Pythonic Implementation)", LRUCache)
    benchmark_builtin_functools()
