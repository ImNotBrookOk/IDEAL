# IDEAL Roadmap

## Governance
Implementation begins only after the planning baseline is reviewed and approved. Execute one task at a time. Each task moves through LOCKED → READY → IN PROGRESS → TESTING → AUDITING → VERIFIED. A task cannot unlock its successor until isolated tests, integration tests, regression tests, audit findings and documentation evidence are recorded.

## Phases and exit criteria
| Phase | Scope | Exit criteria |
|---|---|---|
| 00 | Governance and scope freeze | Requirements, decisions, non-goals and change control approved |
| 01 | Open-source and infrastructure research | Candidate components assessed for licence, maintenance, security, limits and cost |
| 02 | Architecture and contracts | Interfaces, schemas, trust boundaries and failure behaviour documented |
| 03 | Engineering foundation | Reproducible project, config, logging, tests and CI verified |
| 04 | Market data | Historical/live ingestion, normalisation, gap detection and provenance verified |
| 05 | Trading knowledge | Versioned foundational knowledge and rule catalogue established |
| 06 | Regime and market structure | Multi-timeframe regime labels and confidence/unknown handling validated |
| 07 | Indicator research library | Indicators implemented, categorised and tested for correctness/redundancy |
| 08 | Market intelligence | Context/confluence scoring with dependency and correlation controls validated |
| 09 | Autonomous strategy discovery | Candidate generation is bounded, reproducible and regime-aware |
| 10 | Backtesting and validation | Costs, execution assumptions, walk-forward and out-of-sample tests pass |
| 11 | Strategy classification/selection | Only eligible, statistically qualified strategies selected; no forced selection |
| 12 | Risk and portfolio engine | Deterministic sizing, exposure, stops, exits and hard limits verified |
| 13 | Paper execution | Orders, fills, positions, funding, fees and reconciliation verified |
| 14 | Learning and retention | Trade lessons stored, indexed and retained across demotions |
| 15 | Progression gates and rollback | Predefined gates, bounded unlocks, demotion and cooldown logic verified |
| 16 | Orchestration | Safe startup, scheduling, recovery and AI-unavailable behaviour verified |
| 17 | Android dashboard | Mobile control/monitoring interface with safe operational controls |
| 18 | End-to-end verification | Full data-to-decision-to-paper-fill lifecycle and failure injection pass |
| 19 | Operational readiness | Security, observability, backup/restore, runbooks and paper soak test pass |

## Task protocol
1. Inspect repository and existing implementation before changing anything.
2. Confirm the task is the next READY item and has no existing implementation.
3. Define acceptance criteria and tests before code.
4. Implement only that task.
5. Run isolated tests.
6. Run integration tests against every previously VERIFIED dependency.
7. Run regression tests.
8. Audit security, correctness, cost and scope.
9. Update this roadmap and relevant documents with commands, results and commit references.
10. Mark VERIFIED only with reproducible evidence.

## Change control
Any new component, changed requirement, altered risk parameter or reordered dependency is a change request. Document rationale, impact, cost, risk and tests; obtain owner approval before implementation.

## Current state
All implementation phases remain LOCKED pending completion and approval of the planning baseline and Phase 01 research.