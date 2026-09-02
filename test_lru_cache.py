import pytest

from lru_cache import LRUCache


def test_get_updates_recency():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    cache.put("c", 3)
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_put_existing_key_updates_value():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("a", 10)
    assert cache.get("a") == 10
    assert len(cache) == 1


def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)
