# IDEAL Conversation Record 007 — L2/L3 Queue Behaviour and Impact Calibration

**Date:** 15 November 2026  
**Scope:** Phase 01 execution-realism research — L2 snapshot rebasing, L3 MBO queue tracking, cancellation/amendment priority, and market-impact calibration methodology  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** PR #13 merged; 49 tests pass on the final PR head. Empirical impact calibration remains blocked pending venue selection and representative historical data.

## Available user-visible transcript

### User
> Yes

### Assistant
L2 depth and competing-order research is complete and merged.

Two new tests reproduce multi-level L2 depth walking with a partially unfilled residual and competing market orders sharing finite displayed liquidity. The POC suite reported 35 passing tests. PR #11 was merged and the execution realism report, POC README, roadmap and conversation audit record 006 were updated.

### User
> Complete them all then return with the outcome. Make sure to correctly save the information along the way as you have been

### Assistant
I’m treating this as the remaining execution-realism research gate, not as permission to move into implementation or trading.

The work is being split into independently testable parts:

- L2 snapshot rebasing.
- L3 order-by-order queue tracking.
- Queue changes caused by cancellations, size amendments and partial fills.
- Slippage and market-impact calibration.

One important constraint: genuine empirical market-impact calibration requires historical order-book and trade data from a defined venue. IDEAL has not selected an exchange, and synthetic fixtures cannot establish real-world slippage. I’ll build and validate the calibration methodology, but I will not present synthetic results as empirical.

### User
> Did you document that last conversation. And update everything before I had to start a new conversation here in chatgpt? Lets continue

### Assistant
Yes. The previous conversation was documented and its changes were saved to GitHub before you moved to this chat. I independently checked the repository.

Verified on main:

- Conversation audit record 006 exists.
- The conversation index lists record 006.
- The execution realism report contains the L2 findings.
- The POC README records the test coverage.
- The roadmap was updated in PR #11.

PR #11 was confirmed merged at `3d6a49ac7adb629b9bf7bcc5d7fe2b7f233e9b87`; its final CI run reported 35 passing tests. The audit record also preserves failed test attempts and corrections.

### Assistant
Current technical findings from the pinned NautilusTrader `v2.0.0rc9` source:

- L2 snapshot rebasing waits for a multi-delta snapshot to finish before recalculating queue-ahead estimates.
- L3 MBO tracks individual order IDs ahead of a simulated order.
- L3 cancellations can advance queue by the cancelled order's remaining displayed size.
- Simulated-order amendments use a configurable priority-reset policy.
- Partial fills must account for remaining order quantity and pending fill events.

These are simulator behaviours, not proof of how an unselected exchange prioritises orders.

## Operational audit log

### 1. Repository and governance verification

- Re-read `docs/CHATGPT_CONVERSATIONS/2026-11-15-006-l2-depth-competing-orders.md`, the conversation index, `ROADMAP.md`, `research/nautilus_poc/README.md` and `research/nautilus_poc/execution_realism_matrix.md` from the GitHub default branch.
- Confirmed PR #11 was merged and record 006 was indexed.
- Read the installed test-driven-development skill before adding behavioural tests.
- Continued under D-012 standing authorization for Phase 01 research. No production implementation, venue selection, exchange connection or paid service was authorised.

### 2. Pinned upstream source audit

Inspected NautilusTrader tag `v2.0.0rc9`, including:

- `crates/execution/src/matching_engine/mod.rs`: queue snapshot, delta adjustment, L2 rebase, L3 order-ID tracking, per-order deletion/update and trade-driven queue allocation.
- `crates/execution/src/matching_engine/config.rs`: `OrderPriorityResetPolicy` definitions and default.
- `crates/execution/src/matching_engine/tests.rs`: upstream L2 snapshot rebase, L3 snapshot identity, queue cancellation, size changes and simulated-order modification tests.
- `crates/execution/tests/integration/matching_engine.rs`: L3 delete/cancel and size-change cases.
- `python/nautilus_trader/backtest/__init__.pyi`: confirms `BacktestEngine.add_venue` exposes `order_priority_reset_policy`.
- `python/nautilus_trader/trading/__init__.pyi`: confirms the strategy order-modification API.

Findings reproduced in the IDEAL POC:

- L2 snapshot decrease caps an existing queue estimate at the replacement visible size.
- L2 snapshot increase does not push an already-resting order backwards.
- L3 snapshots preserve previously tracked order identities; newly observed IDs are not retroactively inserted ahead of an existing simulated order.
- L3 cancellation/deletion and size decrease advance queue by the tracked amount; size increase adds to the queue ahead under this simulator's FIFO assumption.
- The simulator exposes three priority reset policies: `PRICE_CHANGE`, `PRICE_OR_QUANTITY_INCREASE` and `ANY_MODIFY`.

### 3. Existing research branch discovered and reused

- Discovered the already-developed branch `research/l2-l3-queue-impact`, which contained L2/L3 queue tests and an offline impact-calibration utility.
- Its pre-amendment suite had 46 passing tests in [CI run 43698665865](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43698665865).
- The branch was not yet merged. Its report and roadmap correctly stated that empirical market-impact calibration remained blocked by the absence of a selected venue and representative historical order-book/fill data.
- A separate narrow branch and PR #12 were briefly created while investigating the work. They were closed as duplicates without merging once the broader existing branch was verified. PR #10 was also closed as superseded by merged PR #11.

### 4. Additional end-to-end amendment tests

Added three tests to `research/nautilus_poc/test_queue_rebase.py`:

1. Under `PRICE_CHANGE`, a quantity increase preserves the resting order's prior queue priority.
2. Under `PRICE_OR_QUANTITY_INCREASE`, a quantity increase resets priority; the unmodified peer receives the next fill.
3. Under `ANY_MODIFY`, the successful quantity increase also resets priority; the unmodified peer receives the next fill.

The test sequence first advances queue position with a trade, then increases visible L2 depth, then modifies one of two same-price resting orders. A subsequent trade distinguishes preservation from reset by asserting which client order ID receives the fill.

These are synthetic simulator tests. They do not establish venue-specific exchange priority.

### 5. Offline impact-calibration utility

The branch includes:

- `research/nautilus_poc/impact_calibration.py`
- `research/nautilus_poc/impact_calibration_template.csv`
- `research/nautilus_poc/test_impact_calibration.py`

The standard-library utility accepts one row per parent order and validates required fields, unique order IDs, a single venue/instrument/data-source provenance universe, timestamps, fill quantities, fill VWAP and decision-time midpoint. It computes side-aware implementation shortfall, a half-spread residual diagnostic, fill ratios, volume-weighted slippage, percentiles and participation/spread/volatility/latency buckets. It sorts chronologically, uses a 70/30 temporal split, reports OOS coverage against the training p90 and hashes the input CSV.

The four utility tests use synthetic data and validate arithmetic, provenance, duplicate IDs and invalid fill records. Provisional review sample minimums are explicitly labelled as research diagnostics, not owner-approved trading gates.

**Empirical calibration is not complete.** No venue is selected and no representative historical L2 snapshots, trades and parent-order execution outcomes are available. Synthetic data does not calibrate real market impact, adverse selection or live slippage.

### 6. CI, review and merge

- Added three queue-priority amendment tests; the suite increased from 46 to 49 tests.
- Push CI [run 43699493469](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43699493469): 49 passed in 0.27s.
- PR-head CI [run 43699506563](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43699506563): 49 passed in 0.18s.
- Updated `ROADMAP.md`, `research/nautilus_poc/README.md`, `research/nautilus_poc/execution_realism_matrix.md` and the PR description to reflect the new amendment tests and remaining gaps.
- Final-head CI [run 43699637760](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43699637760): **49 passed in 0.26s**, exact `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 x86_64 / Python 3.14.
- Five-axis review:
  - Correctness: queue outcomes are asserted through observable fills; policy tests distinguish which order gets the next fill.
  - Security: utility reads CSV and writes JSON only; no network, shell execution, credentials or secrets.
  - Cost: standard library only; no new dependency or paid service.
  - Maintainability: isolated research tests and a standalone CLI; limitations and sample minimums documented.
  - Scope: research/tests/docs only; no production runtime or exchange integration.
- Verified final PR head `5d954c22ce5befa75d555bd16bedad4956e78424) was unchanged before merge.
- [PR #13](https://github.com/ImNotBrookOk/IDEAL/pull/13) was squash-merged under D-012.
- Merge commit: `b25fc5415e9aec6620fe5a4cc22f4a52fabb03e3`.
- PR #13 closed/merged state and the repository's `main` commit were read back and verified.

### 7. Documentation updated by PR #13

- `ROADMAP.md`: records L2/L3 queue results, all three quantity-increase amendment policies, 49-test CI evidence and remaining empirical/venue-specific gaps.
- `research/nautilus_poc/README.md`: updates coverage, command, environment, test count and remaining limitations.
- `research/nautilus_poc/execution_realism_matrix.md`: updates source findings, test evidence, policy behaviour and unresolved gaps.
- `research/nautilus_poc/test_queue_rebase.py`: L2/L3 queue and amendment regression tests.
- `research/nautilus_poc/impact_calibration.py`, `impact_calibration_template.csv`, `test_impact_calibration.py`: offline calibration methodology and synthetic validation.

## Current state

- L2 depth walking and finite liquidity consumption: reproduced in prior PR #11.
- L2 snapshot rebasing: reproduced.
- L3 MBO order identity, snapshot retention, cancellation/deletion, size decrease/increase and partial fills: reproduced.
- Simulated-order quantity-increase amendment behaviour: tested for all three configured priority-reset policies.
- Price-change, quantity-decrease and no-op simulated-order amendments: not yet tested end-to-end.
- Venue-specific queue cancel/amend priority: unresolved until a venue is selected.
- Empirical market-impact calibration: BLOCKED pending venue selection and representative historical L2/trade/parent-order-fill data. Do not use synthetic fixture outputs as a live trading cost model.
- Phase 01: IN PROGRESS.
- Phase 02: LOCKED.
- Implementation phases: LOCKED.
- No exchange account, adapter, testnet, paper trading, live trading or paid infrastructure was introduced.

## Next proposed step

Continue Phase 01 in roadmap order. Extend amendment-policy edge-case tests where useful, then proceed to stop/target same-bar ordering, funding missing-data/retry/multi-position cases, canonical replay/restart hashes, free-worker resource/capacity proof, licence and stable-pin review, and final component selection. Empirical calibration must remain blocked until a venue and valid historical dataset are available.

Owner approval: not required for the bounded Phase 01 research completed here under D-012. Explicit owner approval remains required before Phase 02, implementation, exchange connection, account use, paper/live orders, risk changes or cost.
