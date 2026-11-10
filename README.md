# Payment GenAI Workflow & AI Modeling

An MVP starter for exploring faster B2B payment operations through three complementary capabilities:

1. **Near-user caching** for frequently requested reference data.
2. **AI-assisted prefetching** that learns from access patterns (the starter uses a transparent frequency baseline, not a trained model).
3. **Automated payment workflow** with a pluggable smart-contract adapter (the included adapter is a simulation only).

The repository includes a small FastAPI service, an in-memory cache, a prediction baseline, a payment state machine, a live metrics dashboard, MVP KPI guidance, and a 25-slide pitch-deck outline.

> **Prototype only:** This project does not move money, connect to a blockchain, provide payment authorization, or meet production security/compliance requirements. Keep sensitive payment and personal data out of the demo. Production use requires security, legal, compliance, reliability, and payment-provider reviews.

## Quick start

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) for the dashboard and [http://localhost:8000/docs](http://localhost:8000/docs) for the API docs.

Run tests:

```bash
pytest
```

## MVP modules

- `app/cache.py` — TTL-aware in-memory cache with hit/miss/eviction counters. Replace with a regional cache backend for a real deployment.
- `app/predictor.py` — access-frequency baseline and prefetch recommendations. Evaluate against a non-prefetching baseline before enabling automated warming.
- `app/contracts.py` — explicit simulated contract adapter. A production chain integration should be isolated behind this interface and carefully reviewed; do not put sensitive payment data or secrets on-chain.
- `app/payments.py` — minimal idempotent payment lifecycle and approval checks. It is not a payment processor or a ledger.
- `app/metrics.py` — process-local operational and product KPI counters.
- `dashboard/index.html` — lightweight dashboard polling the local API.

## Demo API

- `GET /health` — service status.
- `GET /metrics` — cache, prefetch, payment, and latency metrics.
- `GET /cache/{key}` — read a cached value.
- `PUT /cache/{key}` — write a JSON value; optional `ttl_seconds` query parameter.
- `POST /prefetch` — apply predicted keys from recent accesses to the local cache.
- `POST /payments` — create a demo payment (`idempotency_key`, `amount`, `currency`, `beneficiary_ref`).
- `POST /payments/{payment_id}/approve` — approve a created payment and emit a simulated contract event.
- `GET /payments/{payment_id}` — inspect the demo payment status.

Example:

```bash
curl -X PUT 'http://localhost:8000/cache/vendor:acme?ttl_seconds=60' \\
  -H 'content-type: application/json' -d '{"country":"US","tier":"standard"}'
curl -X POST http://localhost:8000/prefetch
```

The sample payment endpoints intentionally omit settlement and external provider calls. Payment records and metrics are in-memory and are lost when the process restarts.

## Customer-viable MVP path

Start with one design partner, one region, one low-risk read-heavy workflow, and read-only/reference data. Establish a measured baseline before caching or prefetching. Keep payment execution behind an existing licensed payment provider, use human approval for the initial workflow, and treat blockchain as an optional audit/automation integration rather than a prerequisite. See [`docs/mvp-kpis.md`](docs/mvp-kpis.md) for KPI definitions, target-setting guidance, and an initial revenue model, and [`docs/investor-deck-outline.md`](docs/investor-deck-outline.md) for the 25-slide deck outline.

## Next engineering steps

1. Add persistent, tenant-isolated storage and a real regional cache with explicit invalidation.
2. Add authentication, authorization, tenant boundaries, audit logging, rate limits, and secrets management.
3. Add provider sandbox integration, webhook verification, reconciliation, and robust idempotency.
4. Add a feature store / offline evaluation pipeline before graduating the frequency baseline to a learned model.
5. Add distributed tracing, alerting, load tests, failure-mode tests, and an SLO-driven rollout plan.
6. Validate buyer pain, willingness to pay, implementation effort, and compliance scope with design partners.

## License

No license has been selected yet. All rights reserved by default until the repository owner adds a license.
