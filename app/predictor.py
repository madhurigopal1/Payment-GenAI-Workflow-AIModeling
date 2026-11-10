"""Transparent frequency baseline for suggesting cache prefetches."""

from __future__ import annotations

from collections import Counter


class FrequencyPredictor:
    """Recommend the most frequently observed keys; not a trained AI model."""

    def __init__(self) -> None:
        self._counts: Counter[str] = Counter()

    def record(self, key: str) -> None:
        self._counts[key] += 1

    def recommend(self, limit: int = 5) -> list[str]:
        if limit < 1:
            return []
        return [key for key, _ in self._counts.most_common(limit)]

    def snapshot(self) -> dict[str, int]:
        return dict(self._counts)
