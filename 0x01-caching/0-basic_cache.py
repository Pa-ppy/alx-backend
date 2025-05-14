#!/usr/bin/env python3
"""0‑basic_cache

Defines class BasicCache: an unlimited‑size key/value cache that inherits
from BaseCaching.
"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """A trivial cache that never evicts anything."""

    def put(self, key, item):
        """Store *item* in the cache under *key*.

        If *key* or *item* is ``None`` nothing happens.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """Return the value linked to *key* or ``None``."""
        if key is None:
            return None
        return self.cache_data.get(key)
