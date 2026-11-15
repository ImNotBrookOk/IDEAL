# IDEAL Conversation Record 012 — Corrected FX Replay Recovery

**Date:** 16 November 2026  
**Scope:** Phase 01 funding research — fresh deterministic replay after missing-FX settlement failure  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** PR #18 merged; 57 tests pass on final PR head. Research only.

## Available user-visible transcript

### User
> Ok keep going

### Assistant
The missing-FX funding failure is now reproduced separately from missing settlement valuation. The next test checks whether a fresh deterministic replay with the required BTC/USD conversion data restored can complete the funding boundary. This is distinct from automatic recovery within the failed run.

## Operational audit log

### 1. Test extension

Extended `research/nautilus_poc/test_funding_fx_conversion.py`:

- Existing failure path purges the temporary BTC/USD conversion instrument after the BTCJPY position fills. The mark price remains available, but funding settlement fails because the USD account cannot convert the BTC settlement amount.
- Added a fresh-engine replay path that retains the BTC/USD quote through the funding boundary.
- Both paths use the same inverse BTCJPY instrument, BTC settlement currency, USD account base, mark price, funding update and boundary.
- Corrected replay asserts one filled position remains open and the USD account balance falls below the initial 100,000 USD, proving the funding debit was applied.

The first corrected-replay assertion showed no visible USD balance change because the order was constrained by the available L2 ask depth to 5,000 contracts. The funding adjustment was 0.00000008 BTC, which converted to less than one cent and rounded to zero at the USD account precision. The fixture's ask depth was increased to match the 10,000,000-contract order size; the resulting funding debit became observable.

### 2. Strategy API correction

The first replay-test attempt passed a constructor argument into a NautilusTrader Python Strategy subclass. The extension's `Strategy.__new__` rejected the argument. Corrected by constructing the strategy without arguments and setting the test-only boolean attribute after construction, consistent with the existing POC fixture pattern.

### 3. Final verification

- Test-only branch suite [CI run 43754898908](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43754898908): 57 passed in 0.31s.
- Clean PR branch created from current main so PR #18 contained only the replay-test extension and related documentation changes, not the already-merged PR #17 diff.
- Final PR-head CI [run 43754987779](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43754987779): **57 passed in 0.28s**, exact `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 x86_64 / Python 3.14.

### 4. Five-axis review and merge

- **Correctness:** failure path and corrected replay are distinct fresh-engine runs; corrected path verifies observable account debit and open position.
- **Security:** synthetic fixtures only; no secrets or external network operations.
- **Cost:** no dependencies or paid services.
- **Maintainability:** one focused test extension, parameterized purge behavior and explicit replay distinction.
- **Scope:** roadmap, POC README, execution realism report and funding FX test only.
- Final PR head `a21706318e0deeb067e45e9dc41967084b9db0a8` matched the branch ref before merge.
- [PR #18](https://github.com/ImNotBrookOk/IDEAL/pull/18) squash-merged under D-012.
- Merge commit: `52f31f6c7a8164d2dfd374412ac37d6ebd75d639`.

## Documentation updated

- [Roadmap](https://github.com/ImNotBrookOk/IDEAL/blob/main/ROADMAP.md): records successful fresh replay with corrected FX and leaves same-engine reset/replay open.
- [POC README](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/README.md): test count and corrected replay coverage.
- [Execution realism report](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/execution_realism_matrix.md): separate missing-FX failure and corrected replay recovery evidence.

## Interpretation and remaining work

- The failed funding boundary remains fatal; it is not automatically recovered within the same engine run.
- A fresh deterministic replay with corrected FX data successfully settles funding.
- Same-engine `BacktestEngine.reset()` recovery has not been tested.
- Multi-currency account behavior and mixed settlement currencies remain open.
- No runtime recovery mechanism was implemented.

## Current state

- Phase 01: IN PROGRESS.
- Phase 02: LOCKED.
- Implementation phases: LOCKED.
- POC suite: 57 passing tests.
- No runtime code, dependency, exchange adapter, credentials, account, testnet, paper/live trading or paid service introduced.
