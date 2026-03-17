import time
from typing import Any, Optional

class TTLCache:
    """Simple dict-based TTL cache."""

    def __init__(self, maxsize: int = 100, ttl: int = 3600):
        self.maxsize = maxsize
        self.ttl = ttl
        self._cache: dict[str, tuple[float, Any]] = {}

    def _normalize_key(self, key: str) -> str:
        return key.strip().lower()

    def get(self, key: str) -> Optional[Any]:
        normalized = self._normalize_key(key)
        if normalized in self._cache:
            timestamp, value = self._cache[normalized]
            if time.time() - timestamp < self.ttl:
                return value
            del self._cache[normalized]
        return None

    def set(self, key: str, value: Any) -> None:
        normalized = self._normalize_key(key)
        # Evict oldest if at capacity
        if len(self._cache) >= self.maxsize and normalized not in self._cache:
            oldest_key = min(self._cache, key=lambda k: self._cache[k][0])
            del self._cache[oldest_key]
        self._cache[normalized] = (time.time(), value)

    def clear(self) -> None:
        self._cache.clear()

# Cache instances
retrieval_cache = TTLCache(maxsize=100, ttl=3600)
generation_cache = TTLCache(maxsize=100, ttl=3600)
