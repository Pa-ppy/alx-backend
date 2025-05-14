#!/usr/bin/python3
""" LFUCache module """
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFUCache class"""
    def __init__(self):
        super().__init__()
        self.freq = {}
        self.order = []

    def put(self, key, item):
        """Add item in cache using LFU replacement"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq[key] += 1
            self.order.remove(key)
            self.order.append(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_freq = min(self.freq.values())
                lfu_keys = [k for k in self.order if self.freq[k] == min_freq]
                discard_key = lfu_keys[0]
                self.order.remove(discard_key)
                del self.cache_data[discard_key]
                del self.freq[discard_key]
                print(f"DISCARD: {discard_key}")

            self.cache_data[key] = item
            self.freq[key] = 1
            self.order.append(key)

    def get(self, key):
        """Get item by key and update usage frequency"""
        if key is None or key not in self.cache_data:
            return None
        self.freq[key] += 1
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
