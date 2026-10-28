"""High-performance in-memory LRU cache with TTL for scan results."""

import time
from collections import OrderedDict
from typing import Any, Optional

class CacheEntry:
    def __init__(self, value: Any, ttl: int):
        self.value = value
        self.expires_at = time.time() + ttl

    def is_expired(self) -> bool:
        return time.time() > self.expires_at

class LRUScanCache:
    """Least-Recently Used (LRU) Cache with Time-To-Live expiration."""

    def __init__(self, max_items: int = 1000, default_ttl: int = 3600):
        self.max_items = max_items
        self.default_ttl = default_ttl
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.hits: int = 0
        self.misses: int = 0

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            self.misses += 1
            return None
        entry = self._cache[key]
        if entry.is_expired():
            del self._cache[key]
            self.misses += 1
            return None
        self._cache.move_to_end(key)
        self.hits += 1
        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        if key in self._cache:
            del self._cache[key]
        elif len(self._cache) >= self.max_items:
            self._cache.popitem(last=False)
        self._cache[key] = CacheEntry(value, ttl or self.default_ttl)

    def stats(self) -> dict:
        total = self.hits + self.misses
        hit_ratio = (self.hits / total * 100.0) if total > 0 else 0.0
        return {
            "size": len(self._cache),
            "max_items": self.max_items,
            "hits": self.hits,
            "misses": self.misses,
            "hit_ratio_percent": round(hit_ratio, 2)
        }

    def clear(self) -> None:
        self._cache.clear()
        self.hits = 0
        self.misses = 0

global_cache = LRUScanCache()
