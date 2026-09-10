# ⚡ LRU Cache

## What is this project?

An **LRU Cache (Least Recently Used Cache)** is a small storage area that keeps recently used information so it can be retrieved quickly.

This project is a Python implementation of an LRU cache.

For example, a website may repeatedly need the same information. Instead of doing the expensive work every time, the program can temporarily keep the result in a cache.

The cache has a fixed size. When it becomes full, it removes the item that has been unused for the longest time.

## Simple example

Imagine the cache can store only 3 items:

```text
Add A
Add B
Add C

Cache:
A B C
```

Now A is used again:

```text
Use A

Cache:
B C A   ← A is now the most recently used
```

Now D is added:

```text
Add D

Cache:
C A D

B is removed because B was used least recently.
```

That is the **Least Recently Used** rule.

## How does it work?

```text
Request a value
      ↓
Is it in the cache?
   ↙          ↘
 Yes           No
  ↓             ↓
Return it     Return default
  ↓
Mark it as recently used
```

When a new value is added:

```text
Add value
   ↓
Cache full?
   ↓ Yes
Remove least recently used value
   ↓
Store new value
```

## Why use a cache?

Caching can make applications faster because frequently used information can be returned without doing the expensive work again.

```text
Without cache:
Request → expensive operation → result
Request → expensive operation → result
Request → expensive operation → result

With cache:
Request → expensive operation → save result
Request → return saved result
Request → return saved result
```

## Features

- Fixed maximum capacity
- Automatically removes the least recently used item
- Fast `get()` and `put()` operations
- Tracks cache hits, misses and evictions
- Correctly handles a stored `None` value
- `peek()` reads a value without changing its usage order
- `clear()` removes stored values
- `reset_stats()` resets usage counters
- Automated tests
- Performance benchmark

## Main operations

```text
get(key)   → Get a value from the cache.
put(key, value) → Add or update a value.
peek(key)  → Look at a value without marking it as recently used.
clear()    → Remove everything from the cache.
reset_stats() → Reset hit/miss/eviction counters.
```

## Why is it fast?

The implementation uses Python's `OrderedDict` to keep track of item order efficiently.

The average complexity is:

```text
get  → O(1)
put  → O(1)
peek → O(1)
```

## Run the project

Run the tests:

```bash
python -m pytest -q
```

Run the benchmark:

```bash
python benchmark.py
```

## Project structure

```text
lru_cache.py       → LRU cache implementation
test_lru_cache.py  → Automated tests
benchmark.py       → Performance benchmark
README.md          → Project documentation
```

## Technical terms explained

**Cache** — Temporary storage for information that may be needed again soon. The goal is to avoid repeating expensive work.

**LRU (Least Recently Used)** — A rule for deciding what to remove when a cache is full: remove the item that has not been used for the longest time.

**Eviction** — Removing an item from the cache to make room for another item.

**Cache hit** — The requested item is already in the cache, so it can be returned immediately.

**Cache miss** — The requested item is not in the cache.

**OrderedDict** — A Python dictionary-like data structure that keeps track of item order. It is useful here because the cache needs to know which item is oldest and which is newest.

**O(1)** — A measure of algorithm efficiency. It means the amount of work for the operation stays roughly constant as the number of stored items grows.

**O(capacity)** — The memory used grows with the maximum number of items the cache can store.

**API** — The set of functions or methods that other code can use to interact with a component. Here, `get()`, `put()` and `peek()` form the main cache interface.

**Benchmark** — A performance test that measures how quickly code performs under a particular workload.

**Unit test** — A small automated test that checks whether one part of a program behaves correctly.

## What does this project demonstrate?

This small project covers an important computer-science concept and shows how it can be turned into a usable Python component:

**Data structure → API design → edge cases → efficiency → testing → benchmarking**

It demonstrates **Python, data structures, algorithmic complexity, API design, testing and performance measurement**.

## Future improvements

- Compare performance with Python's built-in `functools.lru_cache`
- Test with larger workloads
- Add optional TTL (time-to-live) support
- Add an optional thread-safe implementation
