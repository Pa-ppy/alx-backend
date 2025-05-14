#!/usr/bin/python3
""" MRUCache module """
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRUCache class"""
    def __init__(self):
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Add item in cache using MRU replacement"""
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.order.remove(key)
        self.cache_data[key] = item
        self.order.append(key)
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            mru_key = self.order.pop()
            del self.cache_data[mru_key]
            print(f"DISCARD: {mru_key}")

    def get(self, key):
        """Get item by key and update recent use"""
        if key is None or key not in self.cache_data:
            return None
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
