# Conversation 058 — Risk management research, Stage 5: drawdown and loss containment

**Date:** 17 November 2026  
**Phase:** 02 — Architecture and contracts  
**Status:** Research/documentation only; findings provisional

## Work completed

Expanded `docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md` with:
- layered capital, portfolio, strategy, instrument, order and runtime risk controls;
- separation of realised/unrealised P&L, daily loss, rolling-period loss, peak-to-trough drawdown, capital impairment and stress loss;
- explicit capital-flow and high-water-mark accounting requirements;
- proposed deterministic caution/restricted/risk-off/emergency/recovery-pending states;
- separate semantics for block-new-risk, cancel-risk-increasing-orders, cancel-all, risk-reducing orders, flattening and credential isolation;
- anti-reset protections for restarts, UTC boundaries, account changes, partial fills and manual/external activity;
- capital preservation, strategy de-risking and no loss-chasing requirements;
- fault-injection, replay, boundary and independent assurance tests.

## Key sources

- FIA Best Practices for Automated Trading Risk Controls and System Safeguards (July 2024): https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf
- SEC market-access risk-control FAQ (scope-limited securities broker-dealer reference): https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions/divisionsmarketregfaq-0
- SEC Rule 15c3-5 final rule overview: https://www.sec.gov/rules-regulations/2011/06/risk-management-controls-brokers-or-dealers-market-access
- FIA exchange risk controls overview: https://www.fia.org/sites/default/files/2025-01/Exchange%20Risk%20Controls%20%E2%80%93%20Overview%20of%20CME%20and%20ICE%20risk%20controls.pdf

## Important conclusions

1. Daily loss and peak-to-trough drawdown are different; rolling loss and stress loss are different again. Preserve all as separate measures.
2. Deposits, withdrawals and internal transfers must not distort trading performance or silently reset risk state.
3. The D-008 10% UTC day-start boundary remains an outer hard limit, not a normal target or complete risk system.
4. Kill switch is not one action: blocking new risk, cancelling orders, allowing reductions, flattening and disabling compromised components have different consequences.
5. Risk-state escalation should be deterministic and conservative; recovery must require reconciliation and evidence, not merely a restart or temporary P&L improvement.
6. No loss-chasing, automatic size increases to recover losses, or AI/strategy modification of hard limits.
7. External/manual trades and unknown exposure can invalidate risk calculations; state must be reconciled or restricted.

## Decisions and boundaries

- No new accepted decision added.
- D-006 remains 0.5% per trade; equity denominator unresolved.
- D-008 remains 10% of UTC day-start equity including realised and unrealised P&L, followed by 24-hour cooldown.
- No new daily/rolling/drawdown threshold, kill-switch scope, flattening authority or recovery rule approved.
- Phase 02 remains active; Phases 03–19 remain locked.
- No implementation, runtime changes, exchange credentials, paper/live execution, external services or phase advancement authorised.

## Verification

The risk architecture and roadmap were committed. This audit record and the conversation index were created. All paths must be fetched back from the default branch and checked before closeout.
