# IDEAL Architecture (Provisional)

## Principles
Deterministic-first, modular, auditable, fail-closed and cost-constrained. AI is an untrusted bounded reasoning component, never the authority for risk or execution permissions.

## Logical components
1. **Market data** — exchange adapters, historical loader, live stream, normaliser, candle completeness and freshness checks.
2. **Knowledge registry** — versioned SKILLS.md knowledge, rules and indicator metadata.
3. **Market state** — multi-timeframe structure, regime classifier and explicit UNKNOWN state.
4. **Indicator library** — pure calculations with warm-up, missing-data and numerical-stability contracts.
5. **Intelligence/context** — evidence aggregation, source lineage and correlated-feature controls.
6. **Strategy lab** — bounded candidate generation, versioning and deterministic parameter schemas.
7. **Research engine** — event-driven backtester, cost/fill models, walk-forward and out-of-sample validation.
8. **Strategy registry/selector** — eligibility, regime scope, cohort ranking and selection history.
9. **Risk engine** — sizing, exposure, stop/exit validation, daily loss and cooldown state machine.
10. **Paper broker** — simulated order lifecycle, fills, fees, funding, positions and reconciliation.
11. **Learning store** — trade records, lessons, retrieval metadata and immutable history.
12. **Gate controller** — deterministic promotion/demotion and permission state.
13. **Orchestrator** — startup, scheduling, health checks, recovery and safe shutdown.
14. **Mobile dashboard** — Android-first status, controls, audit trail and alerts.

## Data flow
Market feeds → validation/normalisation → market state and indicators → contextual evidence → strategy eligibility → risk approval → paper order simulator → reconciliation → trade journal/learning. Gate controller consumes verified performance evidence and independently updates allowed strategy permissions. Every stage emits versioned events and traceable decisions.

## Trust boundaries
- Exchange/API responses, external text, historical datasets and model outputs are untrusted.
- Secrets remain server-side.
- Strategy code runs in a constrained environment with resource/time limits.
- Risk and order validation are separate from strategy generation.
- A paper order is rejected if required inputs or state are absent or inconsistent.

## Contracts to define in Phase 02
Instrument and candle schema; timestamp/timezone convention; market-state schema; indicator metadata; strategy manifest; backtest result; order/fill/position ledger; risk decision; gate state; trade lesson; event envelope; error taxonomy.

## Deployment
Deployment remains intentionally undecided. The owner has approved phone-first control/monitoring, with an existing Windows PC/laptop only as a fallback if a concrete requirement forces it. No cloud provider or host is selected; no PC/cloud provisioning, inbound ports, continuous feed or paid infrastructure is authorised. GitHub Actions remains research CI, not a persistent trading worker. The pinned NautilusTrader POC passes on x86_64 and ARM64 but remains a pre-release research candidate, not an adopted engine. See [Infrastructure Research](docs/INFRASTRUCTURE_RESEARCH.md). SQLite event journal remains an isolated research prototype and requires target-environment durability, external hash anchoring and backup/restore validation before any future runtime consideration.

## Cross-domain scope and user authority (Phase 02 design requirements)

IDEAL is intended to become one coherent personal system with independently governed domains, not one monolithic trading strategy. The initial active trading scope remains crypto perpetual futures under D-001. Future research scope includes long-term crypto spot accumulation, stock/ETF investing, commodity exposure and cross-asset hedging (D-014/D-016), plus Personal Finance and Tax Intelligence proposals (D-017/F-004 and F-005). These future domains must not be mistaken for active implementation approval.

**User authority is a system invariant.** IDEAL provides information, analysis, recommendations, alerts and explicitly authorised actions. It does not own the user's capital or silently impose financial choices. In particular, tax estimates and recommended tax reserves are informational/accounting views only: no mandatory segregation, escrow, lock, deduction, forced payment, trade block or investment block. The user may choose to deploy funds shown as a recommended reserve. IDEAL must explain and record the resulting estimated exposure and relevant due dates, without restricting access. Legal obligations remain distinct from software permissions.

## Shared data trust and system-health plane (proposed Phase 02 architecture)

All domains depend on a shared, deterministic data trust plane. It is more foundational than any individual strategy or execution engine. It must track source identity and permissions, raw observations, normalisation, provenance, event time and ingest time, sequence continuity, freshness, completeness, quality state, corrections, reconciliation and downstream consumption. Each datum used in a decision must be traceable to its source, retrieval time, transformation/version, validation outcome and applicable instrument/venue.

Data must never be labelled live merely because it was recently retrieved. Each feed has an explicit freshness contract appropriate to its market/session and use. A missing, delayed, stale, contradictory, malformed, out-of-order or incomplete critical input becomes a visible degraded/unknown state. No fabricated values, silent forward-fill, guessed timestamps or stale-as-live substitution are permitted. Critical risk/execution decisions fail closed when mandatory data contracts are not satisfied; non-critical reporting may show last-known values only when visibly marked with age and quality.

A separate deterministic health and audit supervisor should monitor the data plane and the rest of the system: source connectivity and rate limits, feed lag and gaps, clock drift, schema/contract violations, event backlog, scheduler/worker liveness, storage capacity and write failures, reconciliation mismatches, backup age/restore evidence, dependency and configuration drift, audit-chain integrity and component heartbeats. The supervisor must not rely on the component it is checking as its sole source of truth. Health state, incidents, acknowledgements, recovery and overrides are append-only and auditable. It must distinguish healthy, degraded, stale, unavailable and unknown; recovery requires verified conditions, not merely a successful reconnect.

Prefer deterministic scripts, rules, tests and scheduled jobs for ingestion, validation, monitoring, reconciliation, alerting, housekeeping and routine reporting. AI is optional and bounded to tasks where it adds material value (for example, summarising an already verified incident); it is not the data validator, source of truth, risk authority or continuous monitor. This is a token-cost and reproducibility requirement.

## Deployment portability

Phone-first is the current interaction preference, not a permanent compute constraint. Architecture must separate user interface/control plane from data ingestion, scheduled work, storage and compute. A mobile client must not need to stay awake or connected for reliable ingestion/monitoring. Keep deployment portable across a future Windows/Linux PC and a later private server, with explicit adapters/configuration rather than phone-specific business logic. No PC/server/cloud provisioning, paid service, always-on worker or hosting choice is authorised by this requirement.

See `docs/DATA_INTEGRITY_AND_HEALTH.md` for the proposed data contracts, health model, failure behaviour and research questions.
