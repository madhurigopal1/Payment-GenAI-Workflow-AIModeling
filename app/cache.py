"""A process-local TTL cache for the MVP demo; not suitable for production."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any


@dataclass
class CacheEntry:
    value: Any
    expires_at: float | None


class MemoryCache:
    def __init__(self) -> None:
        self._entries: dict[str, CacheEntry] = {}
        self.hits = 0
        self.misses = 0
        self.writes = 0
        self.evictions = 0

    def get(self, key: str) -> Any | None:
        entry = self._entries.get(key)
        if entry is None:
            self.misses += 1
            return None
        if entry.expires_at is not None and entry.expires_at <= time.monotonic():
            del self._entries[key]
            self.evictions += 1
            self.misses += 1
            return None
        self.hits += 1
        return entry.value

    def set(self, key: str, value: Any, ttl_seconds: int | None = None) -> None:
        if ttl_seconds is not None and ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        expires_at = time.monotonic() + ttl_seconds if ttl_seconds is not None else None
        self._entries[key] = CacheEntry(value=value, expires_at=expires_at)
        self.writes += 1

    def snapshot(self) -> dict[str, int | float]:
        requests = self.hits + self.misses
        return {
            "entries": len(self._entries),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.hits / requests if requests else 0.0,
            "writes": self.writes,
            "evictions": self.evictions,
        }
