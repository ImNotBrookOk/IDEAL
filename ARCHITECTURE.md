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