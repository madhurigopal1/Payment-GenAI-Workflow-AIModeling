"""Run with: uvicorn app.main:app --reload"""

from __future__ import annotations

import time
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.cache import MemoryCache
from app.contracts import SimulatedContractAdapter
from app.metrics import Metrics
from app.payments import PaymentService
from app.predictor import FrequencyPredictor

app = FastAPI(title="Payment Workflow MVP Demo", version="0.1.0")
cache = MemoryCache()
predictor = FrequencyPredictor()
payments = PaymentService()
contract_adapter = SimulatedContractAdapter()
metrics = Metrics()
app.mount("/dashboard", StaticFiles(directory="dashboard"), name="dashboard")


@app.middleware("http")
async def record_latency(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    metrics.observe_request((time.perf_counter() - start) * 1000)
    return response


class CacheWrite(BaseModel):
    value: Any


class PrefetchRequest(BaseModel):
    values: dict[str, Any] = Field(default_factory=dict)
    limit: int = Field(default=5, ge=1, le=100)


class PaymentCreate(BaseModel):
    idempotency_key: str = Field(min_length=1, max_length=128)
    amount: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    beneficiary_ref: str = Field(min_length=1, max_length=128)


@app.get("/")
def dashboard() -> FileResponse:
    return FileResponse("dashboard/index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "demo"}


@app.get("/metrics")
def get_metrics() -> dict:
    return metrics.snapshot(cache.snapshot(), payments.snapshot(), contract_adapter.snapshot())


@app.get("/cache/{key}")
def read_cache(key: str) -> dict[str, Any]:
    predictor.record(key)
    value = cache.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="cache key not found")
    return {"key": key, "value": value}


@app.put("/cache/{key}")
def write_cache(key: str, body: CacheWrite, ttl_seconds: int | None = None) -> dict[str, Any]:
    if ttl_seconds is not None and ttl_seconds <= 0:
        raise HTTPException(status_code=422, detail="ttl_seconds must be positive")
    cache.set(key, body.value, ttl_seconds)
    return {"key": key, "stored": True, "ttl_seconds": ttl_seconds}


@app.post("/prefetch")
def prefetch(body: PrefetchRequest) -> dict[str, Any]:
    keys = predictor.recommend(body.limit)
    written = []
    for key in keys:
        if key in body.values:
            cache.set(key, body.values[key])
            written.append(key)
    metrics.prefetch_recommendations += len(keys)
    metrics.prefetch_writes += len(written)
    return {"recommended_keys": keys, "prefetched_keys": written}


@app.post("/payments", status_code=201)
def create_payment(body: PaymentCreate) -> dict[str, Any]:
    try:
        payment = payments.create(body.idempotency_key, body.amount, body.currency, body.beneficiary_ref)
    except ValueError as exc:
        metrics.payment_errors += 1
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    metrics.payment_creates += 1
    return payment.as_dict()


@app.post("/payments/{payment_id}/approve")
def approve_payment(payment_id: str) -> dict[str, Any]:
    try:
        payment = payments.approve(payment_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="payment not found") from exc
    except ValueError as exc:
        metrics.payment_errors += 1
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    metrics.payment_approvals += 1
    event = contract_adapter.record_approval(payment.payment_id, payment.approved_at or "")
    return {"payment": payment.as_dict(), "contract_event": event}


@app.get("/payments/{payment_id}")
def get_payment(payment_id: str) -> dict[str, Any]:
    try:
        return payments.get(payment_id).as_dict()
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="payment not found") from exc
