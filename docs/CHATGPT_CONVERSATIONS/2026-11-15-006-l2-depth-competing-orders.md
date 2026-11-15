# IDEAL Conversation Record 006 — L2 Depth Walking and Competing Liquidity

**Date:** 15 November 2026  
**Scope:** Phase 01 research — L2 multi-level depth, partial market fills and competing orders consuming finite displayed liquidity  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** PR #11 merged; L2 depth/consumption scenarios verified. L2 queue rebasing and L3 MBO queue tracking remain open.

## Available user-visible transcript

### User
> Yes

### Assistant
Continued the next Phase 01 execution-realism gate: reproduce L2 multi-level depth walking and finite displayed-liquidity consumption in the IDEAL Python POC, then update the research report, POC README and roadmap with test and CI evidence. No production runtime or exchange integration was in scope.

## Operational audit log

### 1. Governance and method

- Continued under D-012 standing Phase 01 research authorization. No new approval was requested for this bounded research task.
- Read the installed test-driven-development skill before changing test behavior.
- Inspected the current IDEAL POC, execution realism matrix, README and roadmap on `main`.
- Confirmed exact engine pin remains `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 x86_64, Python 3.14.
- Inspected the pinned upstream v2.0.0rc9 Python acceptance fixture for `BookType.L2_MBP`, `OrderBookDelta`, `OrderBookDeltas`, `BookOrder` and `RecordFlag`, and the pinned order-book delta documentation.
- The test plan was to create explicit two-sided L2 MBP depth, submit market orders only after the book had been processed, and assert fill quantities/prices against a finite liquidity budget.

### 2. IDEAL tests added

File: `research/nautilus_poc/test_execution.py`.

Two new tests were added:

1. **L2 multi-level depth walking and partial market fill**
   - Synthetic asks: 0.400 at 40,001.0 and 0.600 at 40,002.0.
   - Synthetic bid: 2.000 at 39,999.0.
   - Submit a 1.500-unit BUY market order after the L2 book is loaded.
   - Assert fills of 0.400 at 40,001.0 and 0.600 at 40,002.0.
   - The remaining 0.500 is unfilled because no further displayed ask liquidity exists.

2. **Competing L2 market orders cannot reuse consumed depth**
   - Same 1.000 total displayed ask depth.
   - Submit two sequential 0.750-unit BUY market orders.
   - Enable `liquidity_consumption=True`.
   - Assert aggregate fills are exactly 1.000, not 1.500.

The L2 test strategy subscribes to quotes and submits orders on a quote event after the L2 snapshot. This ordering ensures the matching engine has an initialized book before the orders are submitted.

### 3. Test and CI chronology

All failed attempts were retained in GitHub Actions history and corrected:

- Initial test commit `affd81347a503cc3a9ff04043d0f99308f86fd30`; CI [run 43697297555](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43697297555) failed with two fixture errors because `RecordFlag.F_LAST` was passed as an enum object where the Python binding expected an integer.
- Correction used `RecordFlag.F_LAST.value`. CI [run 43697348897](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43697348897) then showed that market orders were submitted before the L2 book was processed; no fills were produced.
- Strategy was changed to subscribe to quotes and submit only after the L2 snapshot event. A missing `submitted` guard initialization was then corrected.
- Corrected L2 test head `0f2195f89118de0fc28fae56aae6c59280844bd2`; CI [run 43697425596](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43697425596): **35 passed in 0.22s**.
- Final documentation and fixture cleanup were committed; final PR head `dbcd74446d2c8c288e0b5fb342e142dca11eaf7d`.
- Final-head CI [run 43697786352](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43697786352): **35 passed in 0.14s**.
- Exact dependency version assertion passed for `nautilus_trader==2.0.0rc9`; runner was Ubuntu 24.04 x86_64 / Python 3.14.
- These failures were test-fixture construction/order issues, not defects in NautilusTrader's matching engine.

### 4. Findings

- The pinned L2 MBP matching engine walks available ask levels for a BUY market order.
- With 0.400 available at the first ask and 0.600 at the second, a 1.500 order receives two fills totalling 1.000; the remaining 0.500 has no displayed liquidity to execute against.
- With liquidity consumption enabled, two competing 0.750 market orders cannot each reuse the same historical displayed depth. Aggregate fills are capped by the 1.000 units available in the book.
- This is a simulator-level finite-depth result using a synthetic fixture. It does not establish venue-specific matching priority, hidden liquidity, latency behavior, or actual market impact.
- The POC still does not reproduce L2 snapshot queue rebasing or L3 MBO order-ID queue tracking. Those remain source-audited only.

### 5. Documentation updated in PR #11

Exactly four files changed:
- `research/nautilus_poc/test_execution.py`
- `research/nautilus_poc/execution_realism_matrix.md`
- `research/nautilus_poc/README.md`
- `ROADMAP.md`

The report records source semantics, both L2 scenarios, exact test results, failed attempts and limitations. The README and roadmap now reflect L1 plus L2 coverage and retain the L2 snapshot/L3 MBO work as open.

### 6. Five-axis review and merge

PR #11: [Verify L2 depth walking and competing liquidity consumption](https://github.com/ImNotBrookOk/IDEAL/pull/11)

- Final PR head: `dbcd74446d2c8c288e0b5fb342e142dca11eaf7d`.
- Changed files: 4; additions: 144; deletions: 16.
- **Correctness:** exact pinned simulator behavior is asserted through fill quantities and prices; final full suite passed.
- **Readability:** scenario names and fixtures describe the intended market mechanics; no blocking readability issue.
- **Architecture:** test-only additions remain isolated under `research/nautilus_poc/`; no production imports or runtime integration.
- **Security:** synthetic in-memory data only; no credentials, account access, external market-data calls or exchange connectivity.
- **Performance:** full suite completed in 0.14s on the final-head CI run.
- **Scope:** only the POC test module and its three supporting research/roadmap documents changed. No dependency or production behavior changed.
- Final-head check `research-poc` was completed with success. The head SHA was checked immediately before merge and matched the reviewed SHA.
- Automatically squash-merged under D-012.
- Merge commit: `3d6a49ac7adb629b9bf7bcc5d7fe2b7f233e9b87`.
- PR #11 verified closed with `merged=true`.
- Main-branch readback verified the updated report, README, roadmap and test file.

## Current project state

- Phase 01 remains **IN PROGRESS**.
- IDEAL POC verifies selected L1 queue depletion, trade-driven partial fills, competing limit-order trade consumption, one-tick L1 slippage, L2 multi-level depth walking and finite displayed-depth consumption across competing market orders.
- L2 snapshot rebasing and L3 MBO order-ID queue tracking remain open.
- Queue cancellation/amendment priority, venue-specific queue rules and empirical slippage/market-impact calibration remain open.
- Phase 02 remains LOCKED. No exchange is selected; no exchange account, testnet, paper or live trading is connected or authorised. No production runtime integration or new dependency was added.

## Next proposed step

Reproduce L2 snapshot rebasing and L3 MBO order-ID queue tracking in the IDEAL Python POC, then test queue behaviour through partial fills, cancellation and order amendments. Keep empirical market-impact calibration as a separate later gate.

**Owner approval:** Not required for this bounded Phase 01 research under D-012. Explicit owner approval remains required before Phase 02 or any separately restricted activity.
