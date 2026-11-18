# Checkpoint 114 — risk-tier completeness and portfolio margin semantics

**Date:** 19 November 2026  
**Phase:** 02 — Architecture and contracts  
**Status:** Research only; no venue or runtime selected

## Findings

- Bybit V5 `GET /v5/market/risk-limit` returns symbol-specific risk tier IDs, position limits, initial and maintenance margin rates, maximum leverage and maintenance deduction. Linear results are paginated (15 symbols per response) and may experience increased latency or temporary delivery delays during extreme volatility. A partially retrieved or delayed table cannot be treated as current and complete.
- OKX tiered maintenance-margin rules (updated 11 August 2026) describe different tier aggregation by account mode. Cross-margin futures may aggregate positions in both directions of a contract and across expiries for the same underlying; isolated treatment is position/direction scoped. Portfolio margin maintenance is based on losses under extreme stress scenarios, not simply a sum of position tier requirements.
- OKX tier schedules can be changed; dated exchange notices confirm tier revisions. A change can alter risk without any market price movement.

## Changes

- Margin/liquidation architecture §18: added complete-pagination and freshness requirements, raw-vs-normalised tier preservation, aggregation scope, portfolio stress provenance and tier-revision interlock.
- Critical Contract Field Schemas §22: added RiskTierSnapshot, RiskTierRow, PortfolioStressPolicy and PortfolioStressResult.
- Traceability: added R-MARGIN-011–014 / T-MARGIN-11–14.
- Partial cursor results, API delay, stale tier state, unknown aggregation semantics and incomplete stress inputs are explicit fail-closed conditions.
- Portfolio margin must not silently fall back to a generic position-level MMR sum.

## Sources

- Bybit V5 Get Risk Limit: https://bybit-exchange.github.io/docs/v5/market/risk-limit
- OKX Tiered maintenance margin ratio rules, updated 11 August 2026: https://www.okx.com/help/v-tiered-maintenance-margin-ratio-rules
- OKX API V5: https://www.okx.com/docs-v5/en/
- Binance USDⓈ-M margin-tier update, 12 September 2026: https://www.binance.com/en/support/announcement/detail/2adc4f459022496db814a96b93215a1e

## Verification and disposition

- Source and design documentation only; no tests or runtime code were executed.
- Fetch-back verification is complete. The margin architecture, critical schemas, traceability matrix, document map, readiness assessment, audit index, roadmap and this audit were fetched back from GitHub main. The current map contains 46 unique local Markdown targets; all 46 were fetched successfully in bounded batches, with no missing targets.
- No venue, account mode, tier schedule, API client, dependency or runtime selected.
- ODR-02/03 remain OPEN; ODR-12 remains owner gate; TST-105-01 remains open.
- Phase 02 ACTIVE / NOT COMPLETE; Phases 03–19 LOCKED. No credentials, paper/live trading or external action authorised.
