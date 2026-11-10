"""Small process-local KPI collector for the demo API."""

from __future__ import annotations

from collections import defaultdict


class Metrics:
    def __init__(self) -> None:
        self.request_count = 0
        self.total_latency_ms = 0.0
        self.latency_samples = 0
        self.prefetch_recommendations = 0
        self.prefetch_writes = 0
        self.payment_creates = 0
        self.payment_approvals = 0
        self.payment_errors = 0
        self.status_counts: dict[str, int] = defaultdict(int)

    def observe_request(self, latency_ms: float) -> None:
        self.request_count += 1
        self.latency_samples += 1
        self.total_latency_ms += latency_ms

    def snapshot(self, cache: dict, payments: dict, contract: dict) -> dict:
        average_latency = self.total_latency_ms / self.latency_samples if self.latency_samples else 0.0
        return {
            "cache": cache,
            "prefetch": {
                "recommendations": self.prefetch_recommendations,
                "cache_writes": self.prefetch_writes,
            },
            "payments": {
                "created": self.payment_creates,
                "approved": self.payment_approvals,
                "errors": self.payment_errors,
                "by_status": payments,
            },
            "service": {
                "requests": self.request_count,
                "average_latency_ms": round(average_latency, 2),
            },
            "contract_adapter": contract,
        }
