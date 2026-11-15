# IDEAL Rules

These rules are mandatory for every contributor and agent.

## Scope and delivery
- Follow ROADMAP.md in order. Do not skip, bundle, reorder or silently expand tasks.
- Inspect existing code before adding a module; do not duplicate completed work.
- No implementation before the planning baseline and next task are approved.
- A task is not complete without isolated, integration, regression and audit evidence.
- Record deviations and failures; never claim an unrun test passed.
- No paid service, subscription or billing activation without explicit owner approval.

## Trading safety
- Paper trading only. No live orders or real-money credentials until separate explicit approval.
- Initial risk target is 0.5% of equity per trade; 1:3 is a research objective, not a guaranteed outcome.
- Daily hard loss boundary is 10% of UTC day-start equity, including realised and unrealised PnL; breach triggers a 24-hour trading cooldown.
- The 10% boundary is an emergency ceiling, not a normal risk budget. Earlier warning/suspension thresholds and portfolio limits must be researched, documented and approved before paper trading.
- Unknown regime, stale/incomplete data, failed reconciliation, unavailable risk service or ambiguous state means no new trade.
- Risk, permissions, progression gates and execution invariants are deterministic and independently enforced.
- AI cannot edit its own limits, gate thresholds, permissions, kill switches or execution rules.

## Research integrity
- Include fees, spread, slippage, funding, partial fills and realistic latency assumptions.
- Prevent look-ahead, survivorship and selection bias; separate training, validation and untouched out-of-sample data.
- Use walk-forward validation and report sample size, uncertainty, drawdown and regime coverage.
- Win rate alone is not evidence of edge. If absolute quality gates fail, reject the candidate.
- Apply relative cohort ranking only after absolute gates and only to sufficiently large, comparable cohorts. Retain the strongest 50% of that eligible cohort; select none if none qualify.
- Correlated indicators are not independent confirmations.
- Preserve strategy versions, datasets, parameters, code/config hashes and reproducible run metadata.

## AI boundaries
- Treat model output, market text, exchange payloads and external data as untrusted.
- AI may research, propose, explain and write bounded lessons; deterministic validators decide eligibility and enforce safety.
- AI unavailability must fail safely; routine ingestion, calculations, risk checks and state transitions must not depend on AI.