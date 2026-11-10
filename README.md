# payment-genai-workflow

This repository is a starter MVP for a distributed caching and workflow automation concept designed for B2B payment operations.

## What it demonstrates

- regional and edge-style cache semantics
- AI-assisted prefetch recommendations based on observed access patterns
- a workflow engine for payment lifecycle states
- simulated smart-contract event tracking
- KPI dashboard for customer-facing metrics

## Key files

- `app/main.py` — FastAPI application and API routes
- `app/predictor.py` — frequency-based prefetch logic
- `app/ai_model.py` — higher-level pattern scoring model
- `app/payments.py` — payment lifecycle simulation
- `app/contracts.py` — smart-contract adapter stub
- `dashboard/index.html` — KPI dashboard
- `docs/system-architecture.md` — architecture overview
- `docs/commercial-viability.md` — revenue model and market framing
- `docs/mvp-kpis.md` — KPI definitions
- `docs/investor-deck-outline.md` — 25-slide pitch outline

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

- http://localhost:8000
- http://localhost:8000/docs
- http://localhost:8000/dashboard

## Run with Docker

```bash
docker compose up --build
```

## License

No license has been selected yet.
