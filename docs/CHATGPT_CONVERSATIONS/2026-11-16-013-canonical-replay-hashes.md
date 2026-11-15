# IDEAL Conversation Record 013 — Canonical Replay Hashes and Reset Determinism

**Date:** 16 November 2026  
**Scope:** Phase 01 replay integrity — canonical state projection, fresh replay, same-engine reset/replay and identity normalization  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** PR #19 merged; 61 tests pass on final PR head. Research only.

## Available user-visible transcript

### User
> Ok keep going

### Assistant
Continued to canonical event/account replay hashes and process restart/recovery. The pinned NautilusTrader source includes a Rust canonical result API, but that method is not exposed through the Python binding in this evaluated release. The IDEAL POC therefore uses a separate versioned canonical JSON/SHA-256 projection over observable event and account state.

## Operational audit log

### 1. Pinned upstream source audit

Inspected NautilusTrader `v2.0.0rc9`:

- `crates/backtest/src/engine.rs`: `get_canonical_result()`, `reset()`, data iterator reset, retained data, funding-error reset and run-state cleanup.
- `crates/backtest/src/result.rs`: `CanonicalBacktestResult`, schema `nautilus-backtest-result/v1`, compact JSON, BLAKE3 digest, identity normalization and first-divergence support.
- `crates/backtest/src/python/engine.rs` and `python/nautilus_trader/backtest/__init__.pyi`: Python exposes `get_result()` and `reset()`, but does not expose `get_canonical_result()`.
- `crates/common/src/cache/mod.rs`: cache reset clears orders, positions, accounts, quotes, trades, mark prices, funding rates and other transient state; instruments are retained by the BacktestEngine reset configuration unless purged.

Findings:
- The pinned Rust engine already has a strong canonical result projection with a BLAKE3 digest, but the Python POC cannot invoke it directly.
- `BacktestEngine.reset()` retains loaded data and resets data iterator cursors to the beginning.
- The generated client order ID counter does not reset: same-engine replay produced raw order ID suffixes `-1/-2` on the first run and `-3/-4` on the second.
- Raw generated IDs therefore cannot be included directly in a replay hash if same-engine reset replay is expected to compare equal. They must be mapped to canonical local aliases while preserving identity relationships and event ordering.

### 2. IDEAL research utility

Added:
- `research/nautilus_poc/replay_audit.py`
- `research/nautilus_poc/test_replay_integrity.py`

The independent `ideal-replay-audit/v1` helper:
- Produces compact UTF-8 JSON with sorted object keys.
- Rejects floating-point values; exact decimal quantities and prices are strings.
- Produces SHA-256 digests with a schema/version prefix.
- Is intentionally separate from NautilusTrader's BLAKE3 canonical result format.

Four regression tests:
1. Two fresh engines replaying identical inputs produce identical canonical snapshots and digests.
2. Same-engine `BacktestEngine.reset()` and replay produce the same canonical digest after mapping generated client order IDs to sequence aliases.
3. Changing a fill price or account balance changes the digest.
4. Object insertion order does not change canonical bytes; floats are rejected.

Snapshot includes deterministic run counts, engine summary/account state, fills and open/closed position counts.

### 3. Test debugging and corrections

- First same-engine reset hash comparison failed because raw client order IDs advanced across reset. Corrected the projection to normalize IDs to sequence aliases while retaining fill ordering, prices, quantities and timestamps.
- An exploratory attempt to test same-engine recovery from a funding FX failure after deliberately purging the BTC/USD instrument from cache failed. The second run denied the order because the purged FX instrument/quote feed was not restored by the reset fixture. The attempt was removed from the merged PR rather than claiming unsupported recovery.
- Fresh-engine replay with corrected FX data remains verified by PR #18.
- Generic same-engine reset/replay hash determinism is verified by PR #19.
- Same-engine reset recovery from the specific purged-FX funding failure remains unverified.

### 4. CI and merge

- Initial test-only branch suite: 61 tests, one failure due to raw order ID differences.
- Corrected test-only branch [CI run 43755658769](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43755658769): **61 passed in 0.23s**.
- Documentation updates were made to roadmap, POC README and execution realism report.
- Final PR-head CI [run 43755742479](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43755742479): **61 passed in 0.22s**, exact `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 x86_64 / Python 3.14.
- Five-axis review:
  - Correctness: fresh replay, reset replay, fill/account tamper sensitivity and float rejection are asserted.
  - Security: standard-library serialization and hashing only; no network, credentials or dynamic code execution.
  - Cost: no dependencies or paid services.
  - Maintainability: versioned schema and explicit decimal/identity normalization rules.
  - Scope: research helper, tests and documentation only.
- Final PR head `7feb21d450dedeee01565d9bb04ce7d7bb723870` matched branch ref before merge.
- [PR #19](https://github.com/ImNotBrookOk/IDEAL/pull/19) squash-merged under D-012.
- Merge commit: `e2cc9e5e5d0961cb03e2bf7b74dfb2eb67793cf6`.

## Documentation updated

- [Roadmap](https://github.com/ImNotBrookOk/IDEAL/blob/main/ROADMAP.md): canonical replay hashes now tested; durable process restart/checkpoint restore remains open.
- [POC README](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/README.md): adds canonical replay coverage and latest test count.
- [Execution realism report](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/execution_realism_matrix.md): upstream canonical API, Python binding limitation, ID normalization, tests and boundaries.

## Remaining replay/recovery work

- Durable process restart checkpoint/restore is not implemented or tested.
- Cross-process replay hash equivalence is untested.
- Same-engine reset/replay for a normal deterministic workload is tested.
- Same-engine recovery after funding failure with a purged FX instrument is not established.
- Canonical projection currently covers selected observable run, fills, account summary and position counts; full IDEAL domain event coverage and schema migration are future work.

## Current state

- Phase 01: IN PROGRESS.
- Phase 02: LOCKED.
- Implementation phases: LOCKED.
- Isolated POC suite: 61 passing tests.
- No runtime code, dependencies, exchange adapter, credentials, account, testnet, paper/live trading or paid service introduced.
