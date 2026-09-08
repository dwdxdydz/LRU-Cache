from collections import OrderedDict
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")
_MISSING = object()


class LRUCache(Generic[K, V]):
    """Fixed-capacity least-recently-used cache.

    ``get`` and ``put`` are O(1) average-case operations. The implementation
    also exposes hit/miss/eviction statistics for benchmarking and debugging.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be greater than zero")
        self.capacity = capacity
        self._items: OrderedDict[K, V] = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def get(self, key: K, default=None):
        value = self._items.get(key, _MISSING)
        if value is _MISSING:
            self.misses += 1
            return default
        self.hits += 1
        self._items.move_to_end(key)
        return value

    def put(self, key: K, value: V) -> None:
        if key in self._items:
            self._items.move_to_end(key)
        self._items[key] = value
        if len(self._items) > self.capacity:
            self._items.popitem(last=False)
            self.evictions += 1

    def clear(self) -> None:
        self._items.clear()

    def stats(self) -> dict[str, int]:
        return {"hits": self.hits, "misses": self.misses, "evictions": self.evictions}

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, key: K) -> bool:
        return key in self._items
