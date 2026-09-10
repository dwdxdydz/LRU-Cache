# ⚡ LRU Cache

## What is this project?

An **LRU Cache** is a small storage area that keeps recently used information so it can be retrieved quickly.

This project is a Python implementation of an LRU cache.

A simple example is a website that repeatedly needs the same information. Instead of calculating or downloading the information every time, the program can temporarily keep it in the cache.

The cache has a fixed size. When it becomes full, it removes the item that has been unused for the longest time.

## Example

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

This is what **Least Recently Used (LRU)** means.

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

For example:

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

- Fixed maximum capacity.
- Automatically removes old/unused items.
- Fast `get()` and `put()` operations.
- Tracks cache hits, misses and evictions.
- Correctly handles a stored `None` value.
- `peek()` lets you inspect a value without changing its usage order.
- `clear()` removes stored values.
- `reset_stats()` resets usage counters.
- Includes automated tests.
- Includes a small performance benchmark.

## Main operations

```text
get(key)
→ Get a value from the cache.

put(key, value)
→ Add or update a value.

peek(key)
→ Look at a value without marking it as recently used.

clear()
→ Remove everything from the cache.

reset_stats()
→ Reset hit/miss/eviction counters.
```

## Why is it fast?

The implementation uses Python's `OrderedDict`, which allows the cache to quickly move recently used items and remove the oldest item.

Average complexity:

```text
get  → O(1)
put  → O(1)
peek → O(1)
```

`O(1)` means the operation takes roughly the same amount of work even as the cache gets larger.

## Run the tests

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

- **Python** — implementation
- **OrderedDict** — stores the cache in usage order
- **Pytest** — automated testing

## What I learned

This project demonstrates how a common computer-science data structure works in practice.

It focuses on:

- Data structures
- Algorithm efficiency
- API design
- Edge cases
- Unit testing
- Performance measurement

## Future improvements

- Compare performance with Python's built-in `functools.lru_cache`.
- Add larger benchmark workloads.
- Add optional time-based expiration (TTL).
- Add an optional thread-safe implementation.
