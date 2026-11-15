# IDEAL Conversation Record 010 — Missing Funding Settlement Price and Fatal Backtest Failure

**Date:** 16 November 2026  
**Scope:** Phase 01 funding research — no-mark/no-top-of-book settlement failure and same-run recovery semantics  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** PR #16 merged; 55 tests pass on final PR head. Research only.

## Available user-visible transcript

### User
> Ok keep going

### Assistant
Funding settlement source audit and regression testing found that:
- The exchange prefers a cached mark price; otherwise it uses the midpoint of a complete best bid/ask.
- Missing both sources makes settlement fail.
- The exchange retains the pending rate internally, but the backtest engine converts a failed settlement into a fatal funding error. It does not automatically continue to later market data and retry in the same run.

### User
> Ok keep going

### Assistant
The next tests cover the missing-price path by opening a position against L2 depth, clearing both sides of the book before the funding boundary, omitting a mark update, and queuing a later quote. The expected outcome is a fatal funding error with the position still open, not a silent retry.

## Operational audit log

### 1. Source inspection

Inspected NautilusTrader tag `v2.0.0rc9`:

- `crates/backtest/src/exchange.rs`: `funding_settlement_price`, `settle_funding_rate`, pending-rate retention on failure.
- `crates/backtest/src/engine.rs`: `settle_funding_rates` and `fail_funding`.

Source behavior:
- Settlement price is mark price first, else complete top-of-book midpoint.
- Missing both prices makes the exchange settlement function return false and retain the pending rate.
- The engine then raises a fatal `Funding settlement failed` error. The run does not proceed to later replay data, so the retained pending rate does not imply automatic same-run retry.

### 2. IDEAL-side test

Added `research/nautilus_poc/test_funding_failure_modes.py`:

1. Build an L2 MBP book with bid and ask depth.
2. Open a 0.100 BTC long position.
3. Queue a funding rate with a future settlement boundary.
4. Clear both L2 sides before the boundary.
5. Supply no mark price.
6. Queue a later quote after the boundary.
7. Assert `BacktestEngine.run()` raises `RuntimeError` matching `Funding settlement failed`; assert one entry fill and one still-open position.

The later quote does not recover the same run. This is an explicit regression for the distinction between internal pending-rate retention and engine-level fatal failure.

### 3. Test quality corrections

- Initial test file included unused imports; removed them.
- Narrowed the assertion from broad `Exception` to `RuntimeError`, matching the Python-facing failure type.
- Final test passed; no simulator code was modified.

### 4. CI and merge

- Earlier test-only branch run [43753816852](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43753816852): 55 passed in 0.20s.
- Final PR-head CI [43753902519](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43753902519): **55 passed in 0.24s**, exact `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 x86_64 / Python 3.14.
- Five-axis review:
  - Correctness: test asserts the precise fatal exception and confirms position remains open after one entry fill.
  - Security: synthetic data, no secrets or network operations in test.
  - Cost: no dependency or paid service added.
  - Maintainability: one focused failure-mode test with explicit setup and assertions.
  - Scope: test and documentation only.
- PR #16 final head `f361fd611107f1266261f73cf070250cd29a6904` matched the branch ref before merge.
- [PR #16](https://github.com/ImNotBrookOk/IDEAL/pull/16) squash-merged under D-012.
- Merge commit: `38d659fcaea170ac67a3be33312461ca8dc8a5b1`.

## Documentation updated

- [Roadmap](https://github.com/ImNotBrookOk/IDEAL/blob/main/ROADMAP.md): records missing mark/top-of-book fatal funding path and 55-test evidence.
- [POC README](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/README.md): records test and remaining FX/replay gaps.
- [Execution realism report](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/execution_realism_matrix.md): source semantics and observed fatal failure.

## Remaining funding work

- Missing FX conversion from settlement currency to account base currency remains source-audited but not end-to-end reproduced.
- Explicit reset/replay recovery with corrected market/FX data remains untested.
- Mixed settlement currencies and multi-currency accounts remain untested.
- Two same-currency positions and repeated-update idempotency are already covered by PR #15.

## Current state

- Phase 01: IN PROGRESS.
- Phase 02: LOCKED.
- Implementation phases: LOCKED.
- Isolated NautilusTrader POC: 55 passing tests.
- No production runtime code, dependency, venue, exchange adapter, account, testnet, paper/live trading or paid infrastructure introduced.
