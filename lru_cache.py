"""
Production-Grade & Algorithmic LRU (Least Recently Used) Cache Implementations.

Features:
1. DoublyLinkedListLRUCache: First-principles implementation using Sentinel Node Doubly-Linked List + Hash Map.
2. LRUCache: High-performance OrderedDict-backed implementation.
3. Thread-Safety: Optional RLock protection for concurrent environments.
4. TTL Support: Optional per-entry or cache-wide Time-To-Live expiration.
5. Function Decorator: @lru_cached decorator matching functools semantics with telemetry.
"""

from __future__ import annotations

from collections import OrderedDict
from functools import wraps
import threading
import time
from typing import Callable, Generic, Optional, TypeVar, Union, overload

K = TypeVar("K")
V = TypeVar("V")
D = TypeVar("D")
_MISSING = object()


class _Node(Generic[K, V]):
    """Internal doubly-linked list node storing key, value, and TTL metadata."""
    __slots__ = ("key", "value", "expires_at", "prev", "next")

    def __init__(
        self,
        key: Optional[K] = None,
        value: Optional[V] = None,
        expires_at: Optional[float] = None,
    ):
        self.key = key
        self.value = value
        self.expires_at = expires_at
        self.prev: Optional[_Node[K, V]] = None
        self.next: Optional[_Node[K, V]] = None


class DoublyLinkedListLRUCache(Generic[K, V]):
    """First-principles LRU Cache using a Doubly Linked List and Hash Map.

    Guarantees strict O(1) constant time complexity for get(), put(), and peek().
    Uses sentinel pseudo-head and pseudo-tail nodes to eliminate boundary checks.
    """

    def __init__(
        self,
        capacity: int,
        ttl_seconds: Optional[float] = None,
        thread_safe: bool = False,
    ):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be an integer")
        if capacity <= 0:
            raise ValueError("capacity must be greater than zero")

        self.capacity = capacity
        self.ttl_seconds = ttl_seconds
        self.thread_safe = thread_safe
        self._lock = threading.RLock() if thread_safe else None

        # Hash map: key -> _Node
        self._lookup: dict[K, _Node[K, V]] = {}

        # Sentinel nodes for O(1) list manipulation
        self._head: _Node[K, V] = _Node()
        self._tail: _Node[K, V] = _Node()
        self._head.next = self._tail
        self._tail.prev = self._head

        # Telemetry stats
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expirations = 0

    def _remove_node(self, node: _Node[K, V]) -> None:
        """Unlink a node from its current position in O(1)."""
        prev_node = node.prev
        next_node = node.next
        if prev_node:
            prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node

    def _add_to_head(self, node: _Node[K, V]) -> None:
        """Insert a node right after the sentinel head (most recently used) in O(1)."""
        node.prev = self._head
        node.next = self._head.next
        if self._head.next:
            self._head.next.prev = node
        self._head.next = node

    def _move_to_head(self, node: _Node[K, V]) -> None:
        """Promote an existing node to the MRU position in O(1)."""
        self._remove_node(node)
        self._add_to_head(node)

    def _pop_tail(self) -> _Node[K, V]:
        """Remove and return the least recently used node in O(1)."""
        lru = self._tail.prev
        if lru and lru is not self._head:
            self._remove_node(lru)
            return lru
        raise KeyError("Cache is empty")

    def _is_expired(self, node: _Node[K, V]) -> bool:
        if node.expires_at is None:
            return False
        return time.time() > node.expires_at

    def get(self, key: K, default: Union[D, object] = None) -> Union[V, D, object]:
        """Retrieve value by key and promote to MRU. Returns default on cache miss."""
        if self._lock:
            with self._lock:
                return self._get_unlocked(key, default)
        return self._get_unlocked(key, default)

    def _get_unlocked(self, key: K, default: object) -> object:
        node = self._lookup.get(key)
        if node is None:
            self.misses += 1
            return default

        if self._is_expired(node):
            self._remove_node(node)
            del self._lookup[key]
            self.expirations += 1
            self.misses += 1
            return default

        self.hits += 1
        self._move_to_head(node)
        return node.value

    def peek(self, key: K, default: object = None) -> object:
        """Retrieve value without updating recency order or incrementing hit/miss stats."""
        if self._lock:
            with self._lock:
                return self._peek_unlocked(key, default)
        return self._peek_unlocked(key, default)

    def _peek_unlocked(self, key: K, default: object) -> object:
        node = self._lookup.get(key)
        if node is None or self._is_expired(node):
            return default
        return node.value

    def put(self, key: K, value: V, ttl_seconds: Optional[float] = None) -> None:
        """Insert or update a key-value pair. Evicts LRU item if capacity is exceeded."""
        if self._lock:
            with self._lock:
                self._put_unlocked(key, value, ttl_seconds)
        else:
            self._put_unlocked(key, value, ttl_seconds)

    def _put_unlocked(self, key: K, value: V, ttl_seconds: Optional[float] = None) -> None:
        effective_ttl = ttl_seconds if ttl_seconds is not None else self.ttl_seconds
        expires_at = (time.time() + effective_ttl) if effective_ttl is not None else None

        if key in self._lookup:
            node = self._lookup[key]
            node.value = value
            node.expires_at = expires_at
            self._move_to_head(node)
            return

        new_node = _Node(key=key, value=value, expires_at=expires_at)
        self._lookup[key] = new_node
        self._add_to_head(new_node)

        if len(self._lookup) > self.capacity:
            lru_node = self._pop_tail()
            if lru_node.key in self._lookup:
                del self._lookup[lru_node.key]
            self.evictions += 1

    def clear(self) -> None:
        """Flush all cache entries while preserving statistics."""
        if self._lock:
            with self._lock:
                self._clear_unlocked()
        else:
            self._clear_unlocked()

    def _clear_unlocked(self) -> None:
        self._lookup.clear()
        self._head.next = self._tail
        self._tail.prev = self._head

    def reset_stats(self) -> None:
        """Reset hit, miss, and eviction counters."""
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expirations = 0

    def stats(self) -> dict[str, int]:
        """Return diagnostic metrics."""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "expirations": self.expirations,
        }

    def __len__(self) -> int:
        return len(self._lookup)

    def __contains__(self, key: K) -> bool:
        if self._lock:
            with self._lock:
                return self._contains_unlocked(key)
        return self._contains_unlocked(key)

    def _contains_unlocked(self, key: K) -> bool:
        node = self._lookup.get(key)
        if node is None:
            return False
        if self._is_expired(node):
            return False
        return True


class LRUCache(Generic[K, V]):
    """Standard-library OrderedDict-based LRU Cache.

    Provides O(1) performance with Pythonic elegance and full telemetry.
    """

    def __init__(
        self,
        capacity: int,
        ttl_seconds: Optional[float] = None,
        thread_safe: bool = False,
    ):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be an integer")
        if capacity <= 0:
            raise ValueError("capacity must be greater than zero")

        self.capacity = capacity
        self.ttl_seconds = ttl_seconds
        self.thread_safe = thread_safe
        self._lock = threading.RLock() if thread_safe else None

        self._items: OrderedDict[K, tuple[V, Optional[float]]] = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expirations = 0

    def _is_expired(self, expires_at: Optional[float]) -> bool:
        if expires_at is None:
            return False
        return time.time() > expires_at

    @overload
    def get(self, key: K) -> Optional[V]: ...

    @overload
    def get(self, key: K, default: D) -> Union[V, D]: ...

    def get(self, key: K, default: object = None) -> object:
        """Return value and promote to MRU. Increments hit/miss counters."""
        if self._lock:
            with self._lock:
                return self._get_unlocked(key, default)
        return self._get_unlocked(key, default)

    def _get_unlocked(self, key: K, default: object) -> object:
        item = self._items.get(key, _MISSING)
        if item is _MISSING:
            self.misses += 1
            return default

        val, expires_at = item
        if self._is_expired(expires_at):
            del self._items[key]
            self.expirations += 1
            self.misses += 1
            return default

        self.hits += 1
        self._items.move_to_end(key)
        return val

    def peek(self, key: K, default: object = None) -> object:
        """Return value without changing recency or statistics."""
        if self._lock:
            with self._lock:
                return self._peek_unlocked(key, default)
        return self._peek_unlocked(key, default)

    def _peek_unlocked(self, key: K, default: object) -> object:
        item = self._items.get(key, _MISSING)
        if item is _MISSING:
            return default
        val, expires_at = item
        if self._is_expired(expires_at):
            return default
        return val

    def put(self, key: K, value: V, ttl_seconds: Optional[float] = None) -> None:
        """Store key-value pair and evict oldest if full."""
        if self._lock:
            with self._lock:
                self._put_unlocked(key, value, ttl_seconds)
        else:
            self._put_unlocked(key, value, ttl_seconds)

    def _put_unlocked(self, key: K, value: V, ttl_seconds: Optional[float] = None) -> None:
        effective_ttl = ttl_seconds if ttl_seconds is not None else self.ttl_seconds
        expires_at = (time.time() + effective_ttl) if effective_ttl is not None else None

        if key in self._items:
            self._items.move_to_end(key)
        self._items[key] = (value, expires_at)

        if len(self._items) > self.capacity:
            self._items.popitem(last=False)
            self.evictions += 1

    def clear(self) -> None:
        """Remove all items."""
        if self._lock:
            with self._lock:
                self._items.clear()
        else:
            self._items.clear()

    def reset_stats(self) -> None:
        """Reset diagnostics."""
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expirations = 0

    def stats(self) -> dict[str, int]:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "expirations": self.expirations,
        }

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, key: K) -> bool:
        if self._lock:
            with self._lock:
                return self._contains_unlocked(key)
        return self._contains_unlocked(key)

    def _contains_unlocked(self, key: K) -> bool:
        item = self._items.get(key, _MISSING)
        if item is _MISSING:
            return False
        _, expires_at = item
        if self._is_expired(expires_at):
            return False
        return True


def lru_cached(capacity: int = 128, ttl_seconds: Optional[float] = None, thread_safe: bool = True):
    """Function decorator for memorizing function call results with an LRU cache."""
    def decorator(fn: Callable):
        cache = LRUCache(capacity=capacity, ttl_seconds=ttl_seconds, thread_safe=thread_safe)

        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            val = cache.get(key, _MISSING)
            if val is not _MISSING:
                return val
            result = fn(*args, **kwargs)
            cache.put(key, result)
            return result

        wrapper.cache = cache
        wrapper.cache_info = cache.stats
        wrapper.cache_clear = cache.clear
        return wrapper
    return decorator
