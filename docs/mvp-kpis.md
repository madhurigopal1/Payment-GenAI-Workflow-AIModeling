# MVP KPI framework and commercial validation

This document proposes what to measure for a customer-viable MVP. Targets below are **hypotheses for design-partner validation, not guarantees or measured product results**. Agree on a baseline, data definitions, and acceptance thresholds with each pilot customer before launch.

## North-star outcome

**Successful eligible B2B payment workflows completed within the customer's target time, with no increase in payment errors, duplicate submissions, or control exceptions.** Report volume and denominators alongside rates. Separate product impact from customer/provider/network changes.

## KPI dashboard definitions

| Area | KPI | Definition / instrumentation | Pilot target hypothesis |
|---|---|---|---|
| Performance | p50 / p95 / p99 read latency | Client-observed latency for eligible reference-data reads, segmented by region and cache hit/miss | Demonstrate a material improvement vs. the agreed baseline; initial hypothesis: >=30% lower p95 for cacheable reads |
| Performance | Cache hit ratio | Valid cache hits / all eligible cache reads; exclude bypassed or ineligible requests | >=70% after a warm-up period, only if freshness and correctness remain within policy |
| Performance | Stale-data rate | Requests served with data beyond the source's allowed freshness window / eligible reads | 0 policy-violating stale responses |
| Prefetch | Prefetch precision | Predicted keys used within the defined horizon / all prefetched keys | Establish baseline; seek >=60% before expanding prefetch traffic |
| Prefetch | Useful-prefetch coverage | Accesses served from prefetched entries / eligible accesses | Improve over frequency baseline without excess origin load |
| Prefetch | Origin-read reduction | Change in eligible origin reads per workflow vs. baseline | Initial hypothesis: >=20% reduction |
| Payment ops | Approval cycle time | Time from workflow-ready to authorized decision; split automated and human wait | Initial hypothesis: >=20% faster for eligible workflows |
| Payment ops | Straight-through processing | Eligible workflows completing without manual rework / eligible workflows | Increase vs. customer baseline, with explicit controls and exclusions |
| Reliability | Workflow success rate | Valid workflows reaching the customer-defined terminal state / submitted workflows | >=99.9% in production-like pilot, subject to agreed scope and volume |
| Reliability | Duplicate/incorrect execution | Confirmed duplicate or unauthorized payment actions | Zero; stop rollout and investigate any occurrence |
| Security/control | Approval-policy exceptions | Workflow actions violating configured approval rules | Zero |
| Business | Cost per eligible workflow | Infrastructure + provider + support costs / completed eligible workflows | Demonstrate a credible, repeatable reduction or justified value premium |
| Commercial | Pilot conversion / willingness to pay | Signed paid pilots, conversion, and validated pricing feedback | At least 2-3 paid design partners before scaling go-to-market spend |

## Measurement plan

1. **Baseline (2-4 weeks):** capture region-tagged latency, origin reads, workflow timings, exceptions, and volume from existing systems. Use consistent eligibility criteria.
2. **Shadow mode:** produce cache/prefetch recommendations without serving cached values or influencing payment decisions. Compare predictions and freshness against actual access patterns.
3. **Canary:** enable cache only for explicitly approved, read-only reference data, with bypass and rollback. Verify source-of-truth parity and invalidation behavior.
4. **Workflow pilot:** integrate through the customer's existing payment provider. Keep human approvals and existing policy controls; measure cycle time and rework.
5. **Review:** report confidence intervals and segment results by region, customer, workflow, and provider. Do not infer causation from a before/after comparison without accounting for changes in mix and traffic.

## Revenue model hypotheses

A practical starting point is **B2B SaaS platform fee + usage tier**, rather than a fee that depends on payment amount or implying custody/processing. Example packaging to validate (illustrative, not a price quote):

- **Pilot:** fixed 8-12 week fee, scoped integration, measured success criteria, and support cap.
- **Growth:** annual platform subscription by tenant/region, including a defined monthly workflow/cache volume.
- **Scale:** enterprise annual commitment with volume bands, premium support, observability, and deployment options.
- Optional implementation services should be priced separately and tracked for gross margin.

Validate pricing through paid pilots and procurement conversations. Estimate gross margin after cloud/edge infrastructure, observability, support, provider fees (if applicable), security/compliance work, and customer-specific integration. Do not charge a share of transaction value until legal, regulatory, partner, and customer requirements are assessed.

## MVP readiness gates

- One buyer persona and one high-cost, read-heavy B2B workflow are validated.
- At least two design partners share baseline data and agree on pilot outcomes.
- Cacheable fields, freshness budgets, data residency, retention, and invalidation are approved by customers.
- No sensitive payment credentials, full bank details, or personal data are cached in the initial scope.
- Payment authorization/execution stays with a licensed existing provider; system has tested idempotency and reconciliation boundaries.
- Security threat model, tenant isolation, access controls, audit trail, incident response, and vendor review are complete before production data.
- Deployment has SLOs, alerting, tested rollback, load/failure testing, and documented ownership.
- Smart-contract use case demonstrates a concrete advantage; otherwise retain an auditable conventional workflow.
