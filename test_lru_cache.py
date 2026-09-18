import threading
import time
import pytest
from lru_cache import DoublyLinkedListLRUCache, LRUCache, lru_cached


@pytest.mark.parametrize("CacheClass", [DoublyLinkedListLRUCache, LRUCache])
def test_get_updates_recency(CacheClass):
    cache = CacheClass(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    cache.put("c", 3)
    assert "b" not in cache
    assert cache.get("a") == 1
    assert cache.get("c") == 3


@pytest.mark.parametrize("CacheClass", [DoublyLinkedListLRUCache, LRUCache])
def test_stored_none_is_not_a_miss(CacheClass):
    cache = CacheClass(2)
    cache.put("a", None)
    assert cache.get("a", "fallback") is None
    assert cache.hits == 1


@pytest.mark.parametrize("CacheClass", [DoublyLinkedListLRUCache, LRUCache])
def test_put_existing_key_updates_value(CacheClass):
    cache = CacheClass(2)
    cache.put("a", 1)
    cache.put("a", 10)
    assert cache.get("a") == 10
    assert len(cache) == 1


@pytest.mark.parametrize("CacheClass", [DoublyLinkedListLRUCache, LRUCache])
def test_stats_track_misses_and_evictions(CacheClass):
    cache = CacheClass(1)
    assert cache.get("missing") is None
    cache.put("a", 1)
    cache.put("b", 2)
    stats = cache.stats()
    assert stats["hits"] == 0
    assert stats["misses"] == 1
    assert stats["evictions"] == 1


@pytest.mark.parametrize("CacheClass", [DoublyLinkedListLRUCache, LRUCache])
def test_invalid_capacity(CacheClass):
    with pytest.raises(ValueError):
        CacheClass(0)


@pytest.mark.parametrize("CacheClass", [DoublyLinkedListLRUCache, LRUCache])
@pytest.mark.parametrize("capacity", [1.5, "2", True])
def test_capacity_must_be_an_integer(CacheClass, capacity):
    with pytest.raises(TypeError):
        CacheClass(capacity)


@pytest.mark.parametrize("CacheClass", [DoublyLinkedListLRUCache, LRUCache])
def test_peek_does_not_change_recency_or_statistics(CacheClass):
    cache = CacheClass(2)
    cache.put("a", 1)
    cache.put("b", 2)

    assert cache.peek("a") == 1
    assert cache.peek("missing", "fallback") == "fallback"
    stats = cache.stats()
    assert stats["hits"] == 0
    assert stats["misses"] == 0
    assert stats["evictions"] == 0

    cache.put("c", 3)
    assert "a" not in cache


@pytest.mark.parametrize("CacheClass", [DoublyLinkedListLRUCache, LRUCache])
def test_clear_and_reset_stats_have_independent_effects(CacheClass):
    cache = CacheClass(1)
    cache.put("a", 1)
    cache.get("a")
    cache.get("missing")
    cache.put("b", 2)

    cache.clear()
    assert len(cache) == 0
    stats = cache.stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert stats["evictions"] == 1

    cache.reset_stats()
    assert cache.stats() == {"hits": 0, "misses": 0, "evictions": 0, "expirations": 0}


@pytest.mark.parametrize("CacheClass", [DoublyLinkedListLRUCache, LRUCache])
def test_ttl_expiration(CacheClass):
    cache = CacheClass(capacity=5, ttl_seconds=0.05)
    cache.put("temp", "value")
    assert cache.get("temp") == "value"

    time.sleep(0.06)
    assert cache.get("temp") is None
    assert cache.stats()["expirations"] == 1


@pytest.mark.parametrize("CacheClass", [DoublyLinkedListLRUCache, LRUCache])
def test_thread_safety(CacheClass):
    cache = CacheClass(capacity=100, thread_safe=True)

    def worker(offset):
        for i in range(100):
            cache.put(f"key_{offset}_{i}", i)
            _ = cache.get(f"key_{offset}_{i}")

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(cache) <= 100
    assert cache.hits > 0


def test_lru_cached_decorator():
    call_count = 0

    @lru_cached(capacity=2)
    def compute(n: int) -> int:
        nonlocal call_count
        call_count += 1
        return n * n

    assert compute(4) == 16
    assert compute(4) == 16
    assert call_count == 1

    assert compute(5) == 25
    assert call_count == 2

    # Evict 4 by inserting 6
    assert compute(6) == 36
    assert compute(4) == 16
    assert call_count == 4
