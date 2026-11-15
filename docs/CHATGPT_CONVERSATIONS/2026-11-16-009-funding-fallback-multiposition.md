# IDEAL Conversation Record 009 — Funding Fallback, Multi-Position Settlement and Idempotency

**Date:** 16 November 2026  
**Scope:** Phase 01 funding settlement research — mark-price fallback, multi-position settlement and repeated funding update handling  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** PR #15 merged; 54 tests pass on final PR head. Research only.

## Available user-visible transcript

### User
> Ok keep going

### Assistant
The next Phase 01 gate is funding settlement edge cases. The source audit identifies three separate failure paths:

1. Missing mark price: the simulator falls back to the midpoint of the best bid and ask. If neither is available, settlement fails and the pending funding rate is retained.
2. Missing conversion rate: a single-currency account may require conversion from the position's settlement currency into its account base currency. Without an exchange rate, settlement is deferred.
3. Multiple positions: funding is calculated per open position and aggregated by settlement currency before the account adjustment is applied.

Regression tests were started using two independently opened positions, no mark-price update and a repeated funding update to check settlement idempotency.

## Operational audit log

### 1. Pinned source audit

Inspected NautilusTrader `v2.0.0rc9`:

- `crates/backtest/src/exchange.rs`: `process_funding_rate`, `queue_funding_rate`, `process_funding_settlement`, `settle_funding_boundary`, `settle_funding_rate`, `funding_settlement_price`, `funding_boundary`.
- `crates/backtest/src/engine.rs`: `settle_funding_rates` and `fail_funding`.

Findings:

- Funding settlement price uses cached mark price when present. Otherwise, both best bid and best ask are required and their midpoint is used.
- If neither a mark nor complete top-of-book exists, settlement fails and the pending funding rate is reinserted into the exchange's pending map.
- A single-currency account whose base currency differs from position settlement currency needs a cached mid FX rate. Missing or invalid conversion fails settlement.
- Funding is calculated per open position, then aggregated by currency before account balance adjustments. Mixed settlement currencies for positions in the same instrument are rejected by this path.
- Settlement idempotency uses `(boundary timestamp, instrument ID)`; a settled key is not applied again.
- Important recovery nuance: although the exchange retains a failed pending funding rate internally, the backtest engine's `settle_funding_rates` turns the failed boundary into a fatal `Funding settlement failed` error. It does not simply continue to later market data and retry in the same run. Recovery requires explicit reset/replay or corrected input; no automatic in-run retry is established.

### 2. IDEAL-side regression tests

Added `research/nautilus_poc/test_funding_edge_cases.py`:

1. **Missing mark fallback:** two independent 0.100 BTC long positions are opened under HEDGING OMS. No mark update is supplied. Funding uses the 60,000.25 top-of-book midpoint and settles both positions. Expected account balance: 9,992.79994600 USDT.
2. **Duplicate post-settlement update:** the same rate and boundary are submitted again after settlement. Fill count, open-position count and account balance are identical to the single-update replay; the funding debit is not applied twice.

### 3. Fixture debugging history

- First run: two failures because the test instrument was on venue BINANCE while the simulated venue was configured as SIM. Corrected the venue to BINANCE.
- Second run: one failure because the test quote prices had precision 2 while the provider instrument requires precision 1. Corrected prices to 60,000.0 / 60,000.5.
- Third run: one failure from a 0.000001 USDT expectation difference. Actual balance was 9,992.79994600 USDT, reflecting per-position Money quantization; updated the independent expected value.
- Final test suite passed. These were test fixture/expectation corrections, not simulator defects.

### 4. CI, review and merge

- Test branch CI [run 43753618622](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43753618622): **54 passed in 0.18s**.
- Documentation updates were made to `ROADMAP.md`, `research/nautilus_poc/README.md` and `research/nautilus_poc/execution_realism_matrix.md`.
- Final PR-head CI [run 43753694223](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43753694223): **54 passed in 0.20s**, exact `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 x86_64 / Python 3.14.
- Five-axis review:
  - Correctness: independent positions, expected midpoint-based debit and repeated-boundary idempotency are asserted from observable account/position state.
  - Security: synthetic inputs only; no secrets, network calls or arbitrary execution in the new test.
  - Cost: no dependency or paid service added.
  - Maintainability: focused standalone tests and explicit source/limitation notes.
  - Scope: tests and documentation only; no runtime code, venue selection or exchange integration.
- Final PR head `89b7c8be11e21b76561098990ec4845b28d400b3` matched the branch ref before merge.
- [PR #15](https://github.com/ImNotBrookOk/IDEAL/pull/15) squash-merged under D-012.
- Merge commit: `5479d15d97046324995460390afb4b1c00b98c49`.

## Documentation updated

- [Roadmap](https://github.com/ImNotBrookOk/IDEAL/blob/main/ROADMAP.md): funding fallback, multi-position/idempotency coverage and outstanding no-price/FX recovery tests.
- [POC README](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/README.md): test count and funding gaps.
- [Execution realism matrix](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/execution_realism_matrix.md): funding source audit, test evidence, quantization correction and retry/recovery caveat.

## Remaining funding research

- Missing both mark and top-of-book at the boundary: no IDEAL end-to-end test yet. Source indicates fatal backtest funding failure.
- Missing FX conversion from position settlement currency to account base currency: source-audited, not yet reproduced end-to-end.
- Explicit replay recovery after correcting missing market/FX data: untested.
- Mixed settlement currencies and multi-currency accounts: untested.
- Multi-position test currently covers two same-instrument positions with the same settlement currency under HEDGING OMS.

## Current state

- Phase 01: IN PROGRESS.
- Phase 02: LOCKED.
- Implementation phases: LOCKED.
- POC suite: 54 passing tests.
- Empirical impact calibration remains blocked pending venue selection and representative historical data.
- Funding no-price failure, FX conversion and replay recovery remain open.
- No exchange adapter, account, testnet, paper or live trading was introduced.
