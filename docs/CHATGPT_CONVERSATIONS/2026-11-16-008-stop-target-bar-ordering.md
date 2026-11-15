# IDEAL Conversation Record 008 — Stop/Target OHLC Ordering and Gap-Through

**Date:** 16 November 2026  
**Scope:** Phase 01 execution-realism research — stop-loss/take-profit OCO ordering within OHLC bars and stop-loss gap-through  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** PR #14 merged; 52 tests pass on final PR head. Research only.

## Available user-visible transcript

### User
> Ok keep going

### Assistant
The next Phase 01 gate is stop-loss / take-profit execution realism. The pinned NautilusTrader source confirms that OHLC bar execution synthesises an intrabar path. Its default path is Open → High → Low → Close. An optional adaptive setting changes high/low order according to which extreme is closer to the open. A candle touching both stop and target can therefore produce different outcomes depending on configuration. This is a simulator path assumption, not evidence of actual market chronology.

## Operational audit log

### 1. Scope and TDD

- Continued Phase 01 under standing D-012 authorization.
- Read the installed test-driven-development skill before writing behavioural tests.
- Inspected the current main branch, POC tests, README, execution realism report, roadmap and CI workflow.
- Work was restricted to isolated research tests and documentation. No runtime code, dependency, venue, exchange access, account, paper/live trading or paid service was changed.

### 2. Pinned upstream source audit

Inspected NautilusTrader tag `v2.0.0rc9`, especially:

- `crates/execution/src/matching_engine/mod.rs`: `process_bar`, `process_trade_ticks_from_bar`, `process_bar_high`, `process_bar_low`, `bar_high_first`, and synthetic tick processing.
- `crates/execution/src/matching_engine/config.rs`: default matching-engine config.
- `crates/backtest/src/python/engine.rs`: `BacktestEngine.add_venue` Python API.
- `crates/common/src/python/order_factory.rs`: OCO bracket factory parameters.
- `python/nautilus_trader/trading/__init__.pyi`: strategy `submit_order_list` API.

Source findings:

- L1 bar execution uses externally aggregated time bars and synthesises market ticks from OHLC legs. Mark-price bars are not processed as executable bars.
- Default path: Open → High → Low → Close.
- `bar_adaptive_high_low_ordering` defaults to false.
- When adaptive ordering is true, high-first is chosen only if `high - open < open - low`; otherwise low-first. A tie therefore selects low-first.
- This is a deterministic simulator convention. OHLC data alone does not identify the true chronological order of the high and low.
- Stop-market order fills in this setup use the simulator's synthetic L1 state; they are not exchange-level order-book replay.

### 3. IDEAL-side regression tests

Added `research/nautilus_poc/test_stop_target_bar.py` with three end-to-end cases using a market-entry OCO bracket:

1. **Default path:** one OHLC bar touches both a 40,010 take-profit and 39,990 stop. Default O-H-L-C reaches the take-profit first; the TP limit fills at 40,010 and the OCO stop is cancelled.
2. **Adaptive path:** same OHLC range and bracket, but adaptive ordering is enabled. The high and low are equidistant from the open, so the tie resolves low-first; the stop-market exit fills at 39,990 and the OCO TP is cancelled.
3. **Gap-through:** bar opens at 39,980, below the 39,990 stop. The simulator fills the stop-market order at the synthetic bar-open price 39,980.

The first two tests intentionally use the same OHLC values; only the matching-engine path configuration changes. They demonstrate that the same candle can select opposite OCO exits under different deterministic path assumptions.

### 4. Test failure and correction

- Initial test run: 50 passed, 1 failed. The stop-market intrabar-touch fill was exactly 39,990, not strictly below the trigger as the first assertion expected.
- Corrected the assertion to the observed exact trigger price. This was a test expectation error, not an engine defect.
- Added the separate gap-through case to test the distinct open-beyond-stop condition.
- Test-only branch CI [run 43753234096](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43753234096): **52 passed in 0.19s**.
- Updated documentation and re-ran final PR-head CI [run 43753312313](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43753312313): **52 passed** on exact `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 x86_64 / Python 3.14.

### 5. Five-axis review and merge

- **Correctness:** assertions identify the exact OCO child order filled, verify fill price, and verify the position closes. The gap-through case is separate from an intrabar touch.
- **Security:** tests use synthetic fixtures; no credentials, external network calls or filesystem access beyond the test runner.
- **Cost:** no dependencies or paid services added.
- **Maintainability:** isolated regression file, documented source behaviour, clear simulator-vs-venue boundary.
- **Scope:** 4 files changed: `ROADMAP.md`, `research/nautilus_poc/README.md`, `research/nautilus_poc/execution_realism_matrix.md`, `research/nautilus_poc/test_stop_target_bar.py`. Research/tests/docs only.
- Final PR head `9c9aa0f437238377312c29f1bf4fb3d97d3dc995) was read back and matched the branch ref before merge.
- [PR #14](https://github.com/ImNotBrookOk/IDEAL/pull/14) squash-merged under D-012.
- Merge commit: `2e77e43bd9acce5ef155588cafaa83606cfb112c`.
- PR closed/merged state and main commit were read back and verified.

## Documentation updated

- [Roadmap](https://github.com/ImNotBrookOk/IDEAL/blob/main/ROADMAP.md): records stop/target dual-touch path dependence, gap-through behavior and 52-test evidence.
- [POC README](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/README.md): adds test coverage and states that ambiguous bars need explicit conservative or higher-resolution handling.
- [Execution realism matrix](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/execution_realism_matrix.md): source audit, test cases, CI evidence and limitations.

## Interpretation and remaining limitations

- OHLC bars cannot prove whether high or low occurred first. A backtest that always chooses the favourable path can overstate strategy expectancy.
- The simulator's synthetic L1 gap-through fill does not establish real bid/ask spread, depth, market impact, latency, exchange trigger reference or venue-specific stop execution.
- Before strategy validation, IDEAL needs an explicit bar ambiguity policy. Candidate options include conservative adverse-first handling, lower-timeframe reconstruction, or tick/order-book replay where data supports it. This policy must be deterministic, documented and tested; AI must not choose the favourable path opportunistically.
- This task does not establish exchange execution parity or profitability.

## Current state

- Phase 01: IN PROGRESS.
- Phase 02: LOCKED.
- Implementation phases: LOCKED.
- Execution realism POC suite: 52 passing tests.
- Empirical market-impact calibration remains blocked pending venue selection and representative historical L2/trade/fill data.
- Funding missing-data/retry/multi-position cases, canonical replay/restart hashes, free-worker capacity proof, stable dependency pins/licence review, adapter assessment and final component selection remain open.
- No exchange account, adapter, testnet, paper or live trading has been introduced.
