# ⚡ LRU Cache

## What is this project?

This project is a Python implementation of an **LRU Cache (Least Recently Used Cache)**.

A cache is temporary storage used to keep information that may be needed again soon. Keeping frequently used information in a cache can make an application faster because it avoids repeating expensive work.

An LRU cache has a fixed size. When the cache becomes full, it removes the item that has not been used for the longest time.

## A simple example

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

## Why use a cache?

Imagine an application needs the same information several times.

Without a cache:

```text
Request → expensive operation → result
Request → expensive operation → result
Request → expensive operation → result
```

With a cache:

```text
First request  → expensive operation → save result
Second request → return saved result
Third request  → return saved result
```

The second and third requests can be faster because the result is already available.

## How does this cache work?

When a value is requested:

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
Remove least recently used item
   ↓
Store new value
```

## Main features

- Fixed maximum capacity.
- Automatically removes the least recently used item.
- Fast `get()` and `put()` operations.
- Tracks cache hits, misses and evictions.
- Correctly handles a stored `None` value.
- `peek()` reads a value without changing its usage order.
- `clear()` removes stored values.
- `reset_stats()` resets usage counters.
- Includes automated tests.
- Includes a performance benchmark.

## Main operations

```text
get(key)          → Get a value from the cache.
put(key, value)   → Add or update a value.
peek(key)         → Read a value without changing its usage order.
clear()           → Remove all cached values.
reset_stats()     → Reset hit/miss/eviction counters.
```

## Why is it fast?

The implementation uses Python's `OrderedDict` to keep track of item order efficiently.

The average complexity is:

```text
get  → O(1)
put  → O(1)
peek → O(1)
```

`O(1)` means that the amount of work stays roughly constant as the number of stored items increases.

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

## Main technologies

- **Python** — implementation language
- **OrderedDict** — keeps cached items in usage order
- **Pytest** — automated testing

## Technical terms explained

**Cache** — Temporary storage for information that may be needed again. The purpose is usually to avoid repeating expensive work.

**LRU (Least Recently Used)** — A rule for deciding which item to remove when a cache is full. The item that has not been used for the longest time is removed first.

**Eviction** — Removing an item from the cache to make room for another item.

**Cache hit** — The requested item is already in the cache, so the program can return it immediately.

**Cache miss** — The requested item is not in the cache, so the program cannot return it from cached storage.

**MRU (Most Recently Used)** — The item that was used most recently. In this project, a successful `get()` makes that item the most recently used.

**OrderedDict** — A Python dictionary-like data structure that keeps track of item order. It is useful here because the cache needs to know which item is oldest and newest.

**O(1)** — A way of describing algorithm efficiency. It means the operation takes roughly the same amount of work regardless of how many items are stored.

**O(capacity)** — The amount of memory used grows with the maximum number of items the cache can hold.

**API** — The set of functions or methods that another piece of code can use to interact with a component. Here, methods such as `get()`, `put()` and `peek()` form the cache interface.

**Benchmark** — A test that measures how quickly code performs under a particular workload.

**Unit test** — A small automated test that checks whether one part of a program behaves correctly.

**Edge case** — An unusual or boundary situation that can expose bugs. This project tests cases such as storing `None` and using invalid capacities.

## What does this project demonstrate?

This small project takes an important computer-science data structure and turns it into a reusable Python component:

**Data structure → API design → edge cases → efficiency → testing → benchmarking**

It demonstrates **Python, data structures, algorithmic complexity, API design, testing and performance measurement** skills.

## Future improvements

- Compare performance with Python's built-in `functools.lru_cache`.
- Test with larger workloads.
- Add optional TTL (time-to-live) support.
- Add an optional thread-safe implementation.
