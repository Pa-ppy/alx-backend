#!/usr/bin/env python3
"""2‑lifo_cache

Defines class LIFOCache: a fixed‑size cache with LIFO eviction strategy.
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Cache that discards the *most recently* stored key when full (LIFO).

    Updating an existing key is treated as a fresh insertion, so that key
    becomes the newest and is therefore the first candidate for discarding.
    """

    def __init__(self):
        """Initialise the underlying dict and insertion order tracker."""
        super().__init__()
        self._stack = []          # Acts like a stack (newest ⇒ last element)

    def put(self, key, item):
        """Store *item* under *key*, evicting last key before insertion when
        capacity is exceeded.

        If *key* or *item* is ``None`` nothing happens.
        """
        if key is None or item is None:
            return

        # Remove existing key to refresh its position in the stack
        if key in self.cache_data:
            self._stack.remove(key)
        elif len(self.cache_data) >= self.MAX_ITEMS:
            discard = self._stack.pop()       # last‑in key
            del self.cache_data[discard]
            print(f"DISCARD: {discard}")

        self.cache_data[key] = item
        self._stack.append(key)

    def get(self, key):
        """Return the value linked to *key* or ``None``."""
        if key is None:
            return None
        return self.cache_data.get(key)
