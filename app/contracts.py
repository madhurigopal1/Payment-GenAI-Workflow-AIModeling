"""Replace this simulator only after a security and legal design review."""

from __future__ import annotations

from typing import Any


class SimulatedContractAdapter:
    """A local event stub; it does not connect to a blockchain or execute funds."""

    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def record_approval(self, payment_id: str, approved_at: str) -> dict[str, Any]:
        event = {
            "event": "PaymentApproved",
            "payment_id": payment_id,
            "approved_at": approved_at,
            "mode": "simulation",
        }
        self.events.append(event)
        return event

    def snapshot(self) -> dict[str, int | str]:
        return {"mode": "simulation", "approval_events": len(self.events)}
