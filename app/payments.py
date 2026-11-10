"""Demo payment lifecycle and idempotency handling (not a payment processor)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass
class Payment:
    payment_id: str
    idempotency_key: str
    amount: float
    currency: str
    beneficiary_ref: str
    status: str
    created_at: str
    approved_at: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class PaymentService:
    def __init__(self) -> None:
        self._payments: dict[str, Payment] = {}
        self._by_idempotency_key: dict[str, str] = {}

    def create(self, idempotency_key: str, amount: float, currency: str, beneficiary_ref: str) -> Payment:
        if not idempotency_key.strip():
            raise ValueError("idempotency_key is required")
        if amount <= 0:
            raise ValueError("amount must be positive")
        if len(currency) != 3 or not currency.isalpha():
            raise ValueError("currency must be a three-letter code")
        existing_id = self._by_idempotency_key.get(idempotency_key)
        if existing_id:
            existing = self._payments[existing_id]
            if (existing.amount, existing.currency, existing.beneficiary_ref) != (amount, currency.upper(), beneficiary_ref):
                raise ValueError("idempotency_key was already used with different payment details")
            return existing
        payment = Payment(
            payment_id=str(uuid4()), idempotency_key=idempotency_key, amount=amount,
            currency=currency.upper(), beneficiary_ref=beneficiary_ref, status="created",
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._payments[payment.payment_id] = payment
        self._by_idempotency_key[idempotency_key] = payment.payment_id
        return payment

    def approve(self, payment_id: str) -> Payment:
        payment = self.get(payment_id)
        if payment.status != "created":
            raise ValueError(f"cannot approve payment in '{payment.status}' status")
        payment.status = "approved"
        payment.approved_at = datetime.now(timezone.utc).isoformat()
        return payment

    def get(self, payment_id: str) -> Payment:
        payment = self._payments.get(payment_id)
        if payment is None:
            raise KeyError(payment_id)
        return payment

    def snapshot(self) -> dict[str, int]:
        counts: dict[str, int] = {"created": 0, "approved": 0}
        for payment in self._payments.values():
            counts[payment.status] = counts.get(payment.status, 0) + 1
        return counts
