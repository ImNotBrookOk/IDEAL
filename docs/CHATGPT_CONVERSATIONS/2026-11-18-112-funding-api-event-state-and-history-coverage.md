# Checkpoint 112 — funding API event-state and historical coverage refinement

**Date:** 18 November 2026  
**Phase:** 02 — Architecture and contracts  
**Status:** Research only; no runtime or venue integration

## Findings

Official exchange documentation reveals that a single generic `funding_rate` field is not sufficient for deterministic reconstruction:

- OKX V5 funding history distinguishes predicted `fundingRate` from actual `realizedRate`, includes `fundingTime`, `formulaType` and `method`, and states that interval changes may be inferred from `fundingTime` versus `nextFundingTime`. The API guide says the history endpoint returns up to three months.
- OKX V5 funding WebSocket distinguishes `processing` from `settled`, and includes rate bounds, premium, formula/method identifiers, settlement timestamps and source update time. It documents a deprecated `next_period` method. Consumers must preserve API/schema revision and reject unknown enums rather than assume current semantics.
- OKX mark-price guidance describes mark as index plus a moving-average basis and provides distinct linear USDT/USDC and inverse crypto-margined PnL formulae. Contract face value, multiplier and settlement asset are necessary to interpret quantities.
- Binance funding guidance describes interval changes and identifies an API endpoint for current funding information; it also states that funding deductions can reduce available balance and then position margin. This is venue/account-mode-specific and cannot be universalised.
- Bybit exposes a distinct historical mark-price kline endpoint; this is not interchangeable with trade-price candles and does not by itself prove complete historical mark-method inputs.

## Changes

- Added §7 to [Perpetual Funding and Mark-Price Semantics Source Refresh](../IDEAL_PHASE_02_PERPETUAL_FUNDING_AND_MARK_PRICE_SEMANTICS_REFRESH.md).
- Added FundingObservation, FundingHistoryCoverage and MarkSeriesEvidence logical records in Critical Contract Field Schemas §20.
- Added R-FUND-004–006 and T-FUND-04–06 to requirement traceability.
- Required explicit coverage/gap/retention/licence metadata. Missing historical data is UNKNOWN, not zero.
- Required distinct predicted, assessed, realised and settled funding values; immutable realised settlement remains the only ledger posting source.
- Preserved linear/inverse denomination-specific accounting and exact signed decimal semantics.

## Sources

- OKX V5 API: https://app.okx.com/docs-v5/en/ (funding history and funding-rate channel, reviewed 18 November 2026)
- OKX mark price and Last price: https://www.okx.com/en-gb/help/ii-mark-price-and-last-price (updated 5 August 2026)
- Binance Introduction to Futures Funding Rates: https://www.binance.com/en-AU/support/faq/detail/360033525031
- Bybit Get Mark Price Kline: https://bybit-exchange.github.io/docs/v5/market/mark-kline

## Verification and disposition

- No code or tests were run; all T-FUND IDs are future test specifications.
- No venue, product, account mode, formula, API client, dependency or runtime selected.
- ODR-02/03 remain OPEN; ODR-12 remains the Phase 02 owner gate; TST-105-01 remains open.
- Phase 02 ACTIVE / NOT COMPLETE; Phases 03–19 LOCKED.
- No exchange account, credential, paper/live execution, paid service or external action authorised.
