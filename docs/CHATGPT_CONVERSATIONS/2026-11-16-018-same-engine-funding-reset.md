# IDEAL Conversation Record 018 — Same-Engine Funding Reset Boundary

**Date:** 16 November 2026  
**Scope:** Phase 01 recovery research — same-engine reset/replay after missing FX conversion  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** [PR #24](https://github.com/ImNotBrookOk/IDEAL/pull/24) merged; 78 tests pass on x86_64 and ARM64. Research only.

## Available user-visible transcript

### User
> Ok keep going. Remember we have a lot to do.

### Assistant
> I’m moving to the next independent recovery question: whether the *same* backtest engine can recover after a funding FX-conversion failure, rather than rebuilding a fresh engine with corrected data. That distinction matters because a production recovery mechanism cannot assume a clean restart will reproduce the original state automatically.

### Assistant
> The first same-engine recovery test exposed a second failure mode. After the first run purges the BTC/USD conversion instrument, `engine.reset()` rewinds the data stream and clears the fatal funding error, but the replay does not automatically restore that purged instrument definition. The next entry is denied for missing BTC-to-USD conversion, so it can appear that the replay succeeded when it actually opened no position.
>
> I’m tightening the test to explicitly restore the instrument after reset and verify that the replay either reproduces the funding failure or completes settlement with a valid conversion quote.

### Assistant
> **PR #24 is merged.** This closes the same-engine reset investigation with a verified limitation rather than an unsupported recovery claim.
>
> - x86_64: 78 passed; ARM64: 78 passed.
> - Final PR-head CI: [run 43760184590](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43760184590).
> - Merge commit: `58f157804aa1183e3858243bc94a16a223cec9de`.
> - The test confirms that `reset()` can clear the funding error yet replay with zero fills and zero positions because the purged FX instrument is missing. A normal return from `run()` is not proof of recovery.
> - The roadmap, POC README and execution report were updated and read back.
>
> **Operational implication:** until a supported cache-restoration path is established, recovery from this condition must rebuild a fresh engine with the required instrument definitions and market data.

## Operational audit log

### 1. Scope and initial hypothesis

The task was to test whether the same Python `BacktestEngine` could be reset and replayed after the inverse BTCJPY funding-settlement failure caused by purging the BTC/USD conversion instrument after entry.

The existing fresh-engine corrected-data test already passed. This task did not assume that fresh-engine success implied same-engine recovery.

### 2. Test iterations and findings

Added `test_same_engine_reset_does_not_restore_purged_fx_instrument` to `research/nautilus_poc/test_funding_fx_conversion.py`.

The test:
1. Opens an inverse BTCJPY position with a temporary BTC/USD quote available for entry risk validation.
2. Purges BTC/USD from cache after the fill.
3. Supplies a valid BTCJPY mark price and advances past the funding boundary.
4. Confirms the first run raises `Funding settlement failed`, with one fill and one open position.
5. Calls `engine.reset()`.
6. Confirms `engine.cache.instrument(BTCUSD_INSTRUMENT.id)` and `engine.cache.load_instrument(...)` both return `None`.
7. Calls `engine.add_instrument(BTCUSD_INSTRUMENT)`; the instrument remains absent from the Python cache.
8. Replays the loaded data. The second `engine.run()` returns normally, but the entry is denied because BTC/USD conversion is missing. There are zero fills and zero open positions.

An attempted direct `engine.cache.add_instrument(...)` restoration failed because the Python cache wrapper does not expose that method. The test was revised to assert the actual exposed API and the false-success replay outcome.

### 3. Pinned source audit

NautilusTrader `v2.0.0rc9` source inspected:
- `crates/backtest/src/engine.rs`:
  - `BacktestEngine::run` checks the latched funding error and aborts the failed run.
  - `BacktestEngine::reset` clears `funding_error`, resets components and resets data iterator cursors.
  - `BacktestEngine::add_instrument` returns early when the exchange already reports the instrument registered.
- `crates/common/src/cache/mod.rs`:
  - `Cache::load_instrument` returns `None` when the instrument is not cached and no cache database is configured.
- `crates/common/src/python/cache.rs`:
  - The Python cache wrapper exposes `load_instrument` and `purge_instrument`; it does not expose a callable `add_instrument` method on the `BacktestEngine.cache` wrapper in this pin.
- `crates/backtest/src/exchange.rs`:
  - Exchange reset reinitializes registered matching engines and initial instrument state. The end-to-end test remains the authority for the observed Python wrapper/cache outcome.

### 4. Interpretation

This is a deterministic replay from the beginning, not an in-place continuation. The reset clears the fatal funding error and rewinds data, but does not make a cache-purged FX instrument available to the subsequent Python replay.

A second `run()` can return normally while the risk engine denies the strategy entry. Therefore:
- A successful method return is not a successful trading replay.
- Recovery checks must assert expected fills, positions, account balances and canonical state.
- For this failure mode, the verified workaround is to reconstruct a fresh engine with the required instrument definitions and valid FX market data.
- No same-engine recovery claim is made.

### 5. Final verification

Final PR-head CI [run 43760184590](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43760184590):
- Exact `nautilus_trader==2.0.0rc9`.
- Ubuntu 24.04 / Python 3.14.10.
- x86_64: **78 passed in 0.37s**.
- ARM64: **78 passed in 0.49s**.

### 6. Five-axis review

- **Correctness:** test asserts the initial fatal failure, post-reset cache absence, inability to repopulate through `BacktestEngine.add_instrument`, and the second run's zero fills/positions.
- **Readability:** descriptive test name and comments explain why a green `run()` can be misleading.
- **Architecture:** test-only POC coverage; no production recovery code or new abstraction.
- **Security:** no secrets, credentials, exchange connections or external services.
- **Performance:** negligible fixture runtime; no production hot path changed.

### 7. Merge and read-back

- PR: [#24 — Test same-engine reset after funding FX failure](https://github.com/ImNotBrookOk/IDEAL/pull/24).
- Final PR head: `75c39f91fc3424b2048646b446b8d73f0a22f894`.
- Final PR-head CI: [43760184590](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43760184590), both architectures green.
- Squash merge succeeded under D-012.
- Merge commit: `58f157804aa1183e3858243bc94a16a223cec9de`.
- PR closed/merged and main ref read back at the merge commit.
- Read back and verified `ROADMAP.md`, `research/nautilus_poc/README.md`, `research/nautilus_poc/execution_realism_matrix.md` and the test file.

## Current state and remaining work

- Phase 01: IN PROGRESS.
- Phase 02 and implementation phases: LOCKED.
- Isolated POC: **78 passing tests on x86_64 and ARM64**.
- Same-engine reset after a cache-purged FX instrument is not a valid recovery path in this Python POC.
- Fresh-engine replay with restored FX instrument/data is verified.
- A supported cache restoration path or documented fresh-engine rebuild procedure remains to be designed and tested.
- Multi-currency account cases remain open.
- Empirical market-impact calibration remains blocked on venue selection and representative historical L2/trade/fill data.
- Venue-specific queue priority and exchange execution parity remain blocked on venue selection.
- SQLite journal runtime integration, signed external hash anchoring, encrypted backup/restore, retention/compaction, and worker capacity remain open; runtime integration and paid provisioning are not authorised.
- No exchange, account, credentials, testnet, paper/live trading or paid service introduced.
- Next research task: investigate multi-currency account and settlement behaviour, including how the simulator models balances, collateral and conversion across more than one currency.
