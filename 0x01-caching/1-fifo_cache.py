#!/usr/bin/env python3
"""1‑fifo_cache

Defines class FIFOCache: a fixed‑size cache with FIFO eviction strategy.
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """Cache that discards the *oldest* stored key when full (FIFO)."""

    def __init__(self):
        """Initialise the underlying dict and insertion order tracker."""
        super().__init__()
        self._order = []          # Insertion order queue (oldest ⇒ first)

    def put(self, key, item):
        """Store *item* under *key*, evicting oldest key if capacity exceeded.

        If *key* or *item* is ``None`` nothing happens.
        """
        if key is None or item is None:
            return

        if key not in self.cache_data and len(
            self.cache_data
        ) >= self.MAX_ITEMS:
            discard = self._order.pop(0)      # first‑in key
            del self.cache_data[discard]
            print(f"DISCARD: {discard}")

        # If key already exists we overwrite but keep its original position
        if key not in self._order:
            self._order.append(key)

        self.cache_data[key] = item

    def get(self, key):
        """Return the value linked to *key* or ``None``."""
        if key is None:
            return None
        return self.cache_data.get(key)
