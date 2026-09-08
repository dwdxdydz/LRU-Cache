import pytest

from lru_cache import LRUCache


def test_get_updates_recency():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    cache.put("c", 3)
    assert "b" not in cache
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_stored_none_is_not_a_miss():
    cache = LRUCache(2)
    cache.put("a", None)
    assert cache.get("a", "fallback") is None
    assert cache.hits == 1


def test_put_existing_key_updates_value():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("a", 10)
    assert cache.get("a") == 10
    assert len(cache) == 1


def test_stats_track_misses_and_evictions():
    cache = LRUCache(1)
    assert cache.get("missing") is None
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.stats() == {"hits": 0, "misses": 1, "evictions": 1}


def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)
