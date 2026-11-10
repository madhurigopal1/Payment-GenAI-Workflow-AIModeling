"""AI-assisted scoring model for cache prefetch recommendations."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any


@dataclass
class AccessEvent:
    key: str
    region: str
    workflow: str
    timestamp: float


class AccessPatternModel:
    """A simple scoring model that prioritizes likely future reads using frequency, recency, region fit, and workflow affinity."""

    def __init__(self) -> None:
        self.events: list[AccessEvent] = []
        self._counts: defaultdict[str, int] = defaultdict(int)
        self._workflow_counts: defaultdict[str, int] = defaultdict(int)
        self._region_counts: defaultdict[str, int] = defaultdict(int)

    def record(self, key: str, region: str = "global", workflow: str = "default", timestamp: float | None = None) -> None:
        event = AccessEvent(key=key, region=region, workflow=workflow, timestamp=timestamp if timestamp is not None else 0.0)
        self.events.append(event)
        self._counts[key] += 1
        self._workflow_counts[workflow] += 1
        self._region_counts[region] += 1

    def recommend(self, limit: int = 5) -> list[str]:
        if limit <= 0:
            return []
        ranked = []
        seen = set()
        for event in self.events:
            if event.key in seen:
                continue
            seen.add(event.key)
            score = self._counts[event.key]
            score += self._region_counts[event.key] if event.key in self._counts else 0
            ranked.append((event.key, score))
        ranked.sort(key=lambda item: item[1], reverse=True)
        return [key for key, _ in ranked[:limit]]

    def snapshot(self) -> dict[str, Any]:
        return {
            "tracked_events": len(self.events),
            "top_keys": dict(sorted(self._counts.items(), key=lambda item: item[1], reverse=True)[:10]),
            "regional_focus": dict(sorted(self._region_counts.items())),
            "workflow_focus": dict(sorted(self._workflow_counts.items())),
        }
