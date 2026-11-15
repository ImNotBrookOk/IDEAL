# IDEAL Decision Register

Append decisions; do not silently rewrite history. Superseding decisions must reference the prior ID and explain the change.

| ID | Decision | Status |
|---|---|---|
| D-001 | Initial market scope is crypto perpetual futures only. | Accepted |
| D-002 | Timeframes: 1W/1D macro, 4H/1H structure, 30M intermediate, 15M entry, optional 5M refinement. | Accepted |
| D-003 | Strategy discovery and generation are autonomous; AI proposes candidates, deterministic validation controls eligibility. | Accepted |
| D-004 | Strategies are classified by market regime; unknown regime or no eligible strategy means no trade. | Accepted |
| D-005 | After absolute quality gates, retain the strongest 50% of a sufficiently large comparable passing cohort; never force a selection. | Accepted |
| D-006 | Initial per-trade risk target is 0.5% of equity. | Accepted |
| D-007 | 1:3 reward/risk is a research objective measured net of costs, not a guaranteed result. | Accepted |
| D-008 | Hard daily loss boundary is 10% of UTC day-start equity, realised plus unrealised, followed by 24-hour cooldown. Earlier warnings and portfolio controls remain unresolved. | Accepted |
| D-009 | Progression gates are predefined and deterministic; AI cannot alter thresholds or permissions. Demotion preserves knowledge/history. | Accepted |
| D-010 | Target $0 recurring cost; no paid plan or billing activation without explicit approval. | Accepted |
| D-011 | Maintain a dated, append-only GitHub record for every IDEAL work conversation, including the available verbatim user-visible transcript and operational evidence. At conversation close, present the record and one proposed next step, then wait for explicit owner approval before proceeding. | Accepted |

## Open decisions
Exchange and data sources; deployment and storage; market universe/liquidity filters; fee/slippage/funding model; absolute statistical gates; minimum comparable cohort size; leverage and portfolio limits; early loss warnings; gate thresholds; AI provider and token budget; backup/retention policy.

## Approval boundary
Accepted decisions define planning constraints. They do not authorise implementation, paper trading or live trading. Pending decisions are not active until explicitly approved by the owner.
