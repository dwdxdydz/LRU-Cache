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


@pytest.mark.parametrize("capacity", [1.5, "2", True])
def test_capacity_must_be_an_integer(capacity):
    with pytest.raises(TypeError):
        LRUCache(capacity)


def test_peek_does_not_change_recency_or_statistics():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)

    assert cache.peek("a") == 1
    assert cache.peek("missing", "fallback") == "fallback"
    assert cache.stats() == {"hits": 0, "misses": 0, "evictions": 0}

    cache.put("c", 3)
    assert "a" not in cache


def test_clear_and_reset_stats_have_independent_effects():
    cache = LRUCache(1)
    cache.put("a", 1)
    cache.get("a")
    cache.get("missing")
    cache.put("b", 2)

    cache.clear()
    assert len(cache) == 0
    assert cache.stats() == {"hits": 1, "misses": 1, "evictions": 1}

    cache.reset_stats()
    assert cache.stats() == {"hits": 0, "misses": 0, "evictions": 0}
