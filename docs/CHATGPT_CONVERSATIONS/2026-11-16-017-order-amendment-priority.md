# IDEAL Conversation Record 017 — Order Amendment Priority Edge Cases

**Date:** 16 November 2026  
**Scope:** Phase 01 execution-realism research — price amendments, quantity decreases and no-op modifications  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** [PR #23](https://github.com/ImNotBrookOk/IDEAL/pull/23) merged; 77 tests pass on x86_64 and ARM64. Research only.

## Available user-visible transcript

### User
> Ok keep going. Remember we have a lot to do.

### Assistant
> Continuing Phase 01. The persistence investigation has uncovered an important distinction: **NautilusTrader v2.0.0rc9 does contain Redis/PostgreSQL cache persistence, and its live-node builder has a cache-database factory hook.** My earlier suspicion that persistence was Rust-only was too broad.
>
> That does not yet establish that the Python API exposes the complete configuration path, or that restart recovery restores every state component IDEAL needs. I’m checking those boundaries before designing or claiming a recovery solution.

### Assistant
> The first cross-architecture CI run exposed a useful edge case: **the Python strategy API rejects a modification when every supplied field is unchanged.** That means an identical-quantity “no-op” never reaches the matching engine’s `ANY_MODIFY` priority-reset policy. I’m correcting the test to verify the actual API behaviour rather than attributing a queue reset to an operation the engine never receives.
>
> The other new amendment scenarios passed in that run; I’m rerunning both architectures after the correction.

### Assistant
> **PR #23 is merged.** The amendment tests now cover the three simulator priority policies across price changes and quantity decreases, plus the Python API’s rejection of no-op modifications.
>
> - x86_64: 77 passed; ARM64: 77 passed.
> - Final PR-head CI: [run 43759447826](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43759447826).
> - Merge commit: `c2f3670c74a2e720d56f1a6957f57f737b942d23`.
> - Updated and read back `ROADMAP.md`, the POC README and the execution realism report.
> - No runtime code, dependencies, exchange connections or trading permissions changed.
>
> The remaining uncertainty is venue-specific: these are NautilusTrader simulator behaviours, not proof of Binance, Bybit or OKX matching priority.

## Operational audit log

### 1. Repository and upstream source inspection

Confirmed the actual repository state after PRs #20–#22 had already merged. The working baseline was main commit `955cb34e8e413e4943441498663c87a8943a0efe`, with 71 POC tests and amendment tests for quantity increases already present.

Inspected pinned NautilusTrader `v2.0.0rc9` source:
- `crates/execution/src/matching_engine/mod.rs`, especially `process_modify` and `update_order` around lines 3793–3889.
- `crates/live/src/node/builder.rs` and `crates/live/src/python/node.rs`.
- `crates/common/src/python/cache.rs`, `crates/infrastructure/src/python/redis/cache.rs`, and `crates/common/src/cache/config.rs`.

Additional persistence clarification discovered while resuming the prior investigation:
- Python `LiveNodeBuilder` exposes `with_cache_database_factory`, `with_load_state` and `with_save_state`; Redis cache factory registration is exposed to Python.
- The Python `BacktestEngine` and standalone Python `Cache` limitations documented in record 014 remain distinct. Live-node component state persistence does not imply full engine, scheduler, market-data cursor or exchange-session checkpointing.
- No persistence implementation or runtime code was changed in this task.

### 2. Amendment tests added

Updated `research/nautilus_poc/test_queue_rebase.py`:
- Quantity decreases under all three `OrderPriorityResetPolicy` modes.
- Price changes that move an order to a new L2 price level, proving the new queue snapshot is used.
- No-op modification rejection at the Python strategy command boundary, with an explicit assertion that the rejection occurs before matching-engine processing.

Verified simulator behaviour:
- **Quantity increase:** `PRICE_CHANGE` preserves priority; `PRICE_OR_QUANTITY_INCREASE` and `ANY_MODIFY` reset it.
- **Quantity decrease:** `PRICE_CHANGE` and `PRICE_OR_QUANTITY_INCREASE` preserve priority; `ANY_MODIFY` resets it.
- **Price change:** queue position is rebased at the new price level under all three policies.
- **No-op:** the Python API raises `RuntimeError: Cannot create command ModifyOrder: quantity, price, and trigger were either None or the same as existing values`. The command is rejected before `process_modify`; no priority-reset policy is applied, including `ANY_MODIFY`.

The first CI attempt had one failing no-op expectation. The failure was not a Nautilus matching-engine defect: the test incorrectly expected an unchanged modification to reach the engine. The test was corrected to assert the API rejection and unchanged queue order. The subsequent cross-architecture runs passed.

### 3. Final verification

Final PR-head CI [run 43759447826](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43759447826):
- Ubuntu 24.04, Python 3.14.10, exact `nautilus_trader==2.0.0rc9`.
- x86_64: **77 passed in 0.55s**.
- ARM64: **77 passed in 0.49s**.
- Benchmark steps also completed; they remain informational, not gating.

Earlier successful code-only PR-head run [43759362304](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43759362304) recorded 77 passed on x86_64 and ARM64. The final PR-head run above includes the subsequent documentation commits.

### 4. Five-axis review

- **Correctness:** deterministic L2 fixtures assert which order receives the next fill, exact partial-fill quantity and queue rebasing at the modified price. No-op rejection is asserted.
- **Security:** no credentials, exchange connections, network market data or account access.
- **Cost:** no new dependency or paid service; public GitHub Actions only.
- **Maintainability:** tests reuse the existing priority-policy fixture and document simulator/API boundaries. The suite remains pinned to the exact pre-release.
- **Scope:** one isolated research test file plus roadmap/POC research documentation. No runtime or trading behaviour changed.

### 5. Merge and read-back

- PR: [#23 — Test price changes, quantity decreases and no-op amendment priority](https://github.com/ImNotBrookOk/IDEAL/pull/23).
- Final PR head: `8adfd5f0ae28a9e8539c5b94ba4f6a0bf476954a`.
- Final PR-head CI: [43759447826](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43759447826), both architectures green.
- Final head SHA matched the branch ref before merge.
- Squash merge succeeded under D-012.
- Merge commit: `c2f3670c74a2e720d56f1a6957f57f737b942d23`.
- PR state and main ref were read back; main points to the merge commit.
- Read back and verified `ROADMAP.md`, `research/nautilus_poc/README.md`, `research/nautilus_poc/execution_realism_matrix.md` and `research/nautilus_poc/test_queue_rebase.py`.

## Documentation updated

- `ROADMAP.md`: records the 77-test result and closes the simulator amendment-edge test gap; venue-specific priority remains open.
- `research/nautilus_poc/README.md`: updates current test count and explains price/quantity/no-op semantics.
- `research/nautilus_poc/execution_realism_matrix.md`: adds exact amendment-policy findings and source boundary.

## Remaining work

- Same-engine `BacktestEngine.reset()` recovery after the funding FX failure remains unverified; fresh-engine replay with restored data is verified.
- Multi-currency account and funding recovery edge cases remain open.
- Empirical market-impact calibration remains blocked on venue selection and representative historical L2/trade/fill data.
- Venue-specific queue priority, cancellation/amendment rules and exchange execution parity remain blocked on venue selection.
- SQLite event-journal integration, external hash anchoring, encrypted backups, retention/compaction, disk-full and corruption recovery remain open; runtime integration is not authorised.
- Actual always-free worker capacity and persistent-volume guarantees remain unverified. Oracle signup/card verification and provisioning still require owner approval.
- Stable release pin review, full licence review, adapter assessment and final component selection matrix remain open.

## Current state

- Phase 01: IN PROGRESS.
- Phase 02: LOCKED.
- Implementation phases: LOCKED.
- Isolated NautilusTrader POC: **77 passing tests on x86_64 and ARM64**.
- PR #23 merged; amendment-priority simulator test gap closed.
- No venue selected; no exchange account, credentials, testnet, paper/live trading or paid service introduced.
- Next research task: investigate same-engine reset/replay recovery after the funding FX failure, without claiming it works until a reproducible test passes.
