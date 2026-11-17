# Checkpoint 111 — funding/mark-price integration and document-map verification

**Date:** 18 November 2026  
**Phase:** 02 — Architecture and contracts  
**Status:** Research and documentation verification only

## Scope

This checkpoint verifies the checkpoint 110 perpetual funding and mark-price source refresh, confirms the current Phase 02 document-map targets, and closes a traceability/documentation gap. It does not approve a venue, account mode, formula, technology, implementation or phase transition.

## Checkpoint 110 source findings revalidated

Official source material reviewed:

- OKX funding mechanism, updated 31 July 2026: contract funding interval defaults to eight hours but may be one, two or four hours; settlement times and rate caps/floors can change with market conditions. Position eligibility is determined at the assessment boundary, and assessment may take up to a minute. The published rate calculation uses a weighted average premium index and an interval normalisation factor. Source: https://www.okx.com/help/perps-funding-fee-mechanism
- Bybit V5 funding-history API: each symbol has its own funding interval, with the instruments-info endpoint identified as the source for that interval. Funding history exposes rate and settlement timestamp as strings. Source: https://bybit-exchange.github.io/docs/v5/market/history-fund-rate
- Bybit V5 tickers expose last, index and mark prices, funding rate and next funding time as distinct fields. Source: https://bybit-exchange.github.io/docs/v5/market/tickers
- Binance USDⓈ-M liquidation help, updated 31 December 2025, describes cross-margin liquidation in terms of wallet balance, other-contract maintenance margin and unrealised PnL, position direction/size/entry, mark price, maintenance rate and cumulative maintenance amount. It directs users to contract rules and specifications effective 5 January 2026 for legally applicable terms. Source: https://www.binance.com/en/support/faq/detail/b3c689c1f50a44cabb3a84e663b81d93
- Binance mark-price explainer describes a median of three price components and a funding/time component; this is evidence that mark methodology is a calculation, not an interchangeable alias for last or index. Source: https://www.binance.com/en-NG/support/faq/detail/360033525071
- OKX 2026 price-reference explainer distinguishes last (trading), mark (unrealised PnL/liquidation checks) and index (external reference/settlement context). Source: https://www.okx.com/en-us/help/okx-x-perps-eea-mark-last-index-price

These are explanatory/API sources, not a complete review of binding contract terms or authenticated instrument state. The eventual venue/product/entity and account mode must be selected before any venue-specific rule can be treated as authoritative.

## Verification performed

- Fetched the current Phase 02 Architecture Document Map from GitHub main.
- Parsed 41 unique local Markdown targets from the map.
- Fetched all 41 targets successfully from GitHub main.
- Confirmed the funding/mark-price research document exists and is fetchable.
- Confirmed its logical schema integration in Critical Contract Field Schemas §19.
- Confirmed its margin/liquidation integration in Margin, Collateral and Liquidation Architecture §12.
- Identified that the checkpoint 110 audit entry was missing from the conversation audit index and that the map's checkpoint 110 section number duplicated section 21. This checkpoint corrects both.

Path existence verification does not establish semantic consistency, fragment-anchor validity, source freshness beyond the cited review, or independent assurance.

## Traceability refinement

The following requirement groups and future test IDs are now required in the traceability matrix:

- R-FUND-001 / T-FUND-01: effective-dated instrument funding interval, next settlement time, cap/floor and schedule revisions; stale/missing schedule blocks dependent risk calculations.
- R-FUND-002 / T-FUND-02: exact funding amount basis, settlement asset, multiplier, position snapshot and rounding; linear/inverse and long/short oracle coverage.
- R-FUND-003 / T-FUND-03: settlement eligibility at boundary, partial close, duplicate/delayed/corrected event and replay idempotency; forecast never posts to ledger.
- R-MARK-001 / T-MARK-01: mark/index/last/executable price remain distinct and each critical mark decision binds a method/configuration revision.
- R-MARK-002 / T-MARK-02: stale mark, index-source outage, constituent divergence and mark-method revision invalidate risk-increasing admission.
- R-MARGIN-008 / T-MARGIN-08: funding debit/credit and tier changes update venue margin projection without conflating it with IDEAL economic PnL or risk-adjusted equity.
- R-MARGIN-009 / T-MARGIN-09: tier/margin changes at unchanged market price force recomputation and invalidate stale permits.

These are design-level requirements and test specifications. No tests were run.

## Remaining gates

- ODR-02 and ODR-03 remain OPEN.
- ODR-12 remains the Phase 02 owner acceptance gate.
- TST-105-01 remains open until the canonical serialization profile is approved and independent golden vectors are executed.
- No venue, product, account mode, margin formula, funding formula, mark methodology, API, dependency or runtime has been selected.
- Phase 02 remains ACTIVE; Phases 03–19 remain LOCKED.
- No code, exchange connection, account, credential, paper/live execution, paid service or external action is authorised.

## Disposition

Checkpoint 110's findings are confirmed at the source and logical-design level. This checkpoint closes the missing audit-index/map-numbering and traceability documentation issues only. Phase 02 is NOT COMPLETE.
