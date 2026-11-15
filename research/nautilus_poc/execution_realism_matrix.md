# Execution Realism Research — Partial Fills, Queue Position, Liquidity Consumption and Slippage

**Research date:** 15 November 2026  
**Phase:** 01 — open-source and infrastructure research  
**Status:** IN PROGRESS — selected L1 and L2 execution scenarios reproduced; L2 snapshot rebasing and L3 order-level queue scenarios remain source-audited but not yet reproduced in IDEAL's Python POC.  
**Engine under evaluation:** `nautilus_trader==2.0.0rc9` (pre-release; not approved for production)  
**Environment:** Ubuntu 24.04 x86_64, Python 3.14, GitHub Actions  
**Adoption decision:** None. This is isolated research only.

## 1. Scope and method

The purpose is to establish what the pinned simulator actually models when multiple simulated orders compete for finite liquidity, how resting limit orders estimate queue priority, and what slippage assumptions are available. In the exact pinned matching-engine configuration, `trade_execution` defaults to enabled, while `liquidity_consumption` and `queue_position` default to disabled; IDEAL must set the latter two explicitly when required.

The work uses three evidence layers:

1. Exact-tag source inspection at NautilusTrader `v2.0.0rc9`, not the moving default branch.
2. Inspection of upstream Rust matching-engine tests for L1, L2 and L3 queue/consumption cases.
3. IDEAL Python POC tests against the exact pinned wheel. Synthetic fixtures only; no exchange connection or market-data download.

The source files and test evidence are linked below. The simulator's behavior must not be treated as exchange-specific matching parity.

## 2. Findings

### 2.1 Partial fills and depth walking

- With L2/L3 books, market-style orders walk the crossed price levels. If displayed crossed quantity is smaller than the remaining order quantity, the order can partially fill.
- The book determines price impact across depth levels. The engine does not apply `prob_slippage` to L2/L3 fills.
- With L1, only the best bid/ask is visible. Eligible market-style orders have a separate deterministic residual rule: after displayed top-of-book size is exhausted, residual quantity can fill one tick worse, subject to price-protection and instrument-price bounds.
- That L1 residual rule is not the same mechanism as probabilistic fill-model slippage.

**Implication:** L1-only tests can materially understate or distort impact. L2 depth is required for a credible market-impact model, and the one-tick L1 residual fallback must not be mistaken for a calibrated impact curve.

Sources: [fill-price rules, L2/L3 and L1](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/docs/concepts/backtesting/fill-prices-and-matching.md#L18-L64).

### 2.2 Liquidity consumption

- Historical order-book data is immutable: simulated fills do not decrement the recorded market-data book.
- `liquidity_consumption=True` tracks consumed quantity by price level, so subsequent simulated orders cannot reuse already-consumed displayed size until fresh book data resets the relevant consumption state.
- Trade-driven fills also share a per-trade consumption budget when enabled. With the flag disabled, the same trade size may support more than one simulated order during one matching iteration.
- For L2/L3, the engine seeds consumption from the triggering trade when the depth book has not yet reflected that trade; it avoids double counting when the book update is newer than the trade.
- Synthetic books supplied by a fill model do not automatically use the matching engine's per-level consumption tracker. A custom model must represent its own liquidity depletion.

**Implication:** Enable consumption for conservative competing-order simulation. A synthetic fill model that supplies unlimited or fixed synthetic depth can bypass the normal consumption assumptions and needs its own explicit budget model.

Source for defaults: [matching-engine configuration](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/config.rs#L25-L56).

Sources: [matching-engine consumption implementation](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L353-L455), [trade-consumption seeding](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L535-L625), [book immutability and consumption rules](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/docs/concepts/backtesting/fill-prices-and-matching.md#L137-L198).

### 2.3 Queue position

- Queue tracking is an explicit opt-in: `queue_position=True`, used together with `trade_execution=True`.
- It applies to resting `LIMIT` orders. On acceptance, the engine snapshots visible same-side quantity at the order's price as quantity ahead.
- Correct-side aggressor trades at that price reduce the quantity ahead. Only trade volume beyond the cleared queue can fill the simulated order.
- The queue allocator shares one trade-volume budget across competing simulated orders at the same price.
- L2/aggregate L3 book updates and snapshots rebase the queue estimate. A snapshot caps the old estimate at the new visible quantity; newly added size does not push an existing simulated order further back.
- L3 MBO can track individual displayed order IDs ahead. L2 MBP and L1 are aggregate/TOB estimates rather than full venue order-level priority.
- L1 quote moves and displayed-size changes also alter the estimate. Orders behind the BBO can remain pending until the BBO reaches their price or a trade crosses it.
- Queue-priority reset behavior on order modifications is configurable. The default policy is `PRICE_CHANGE`; other policies can reset priority on quantity increases or any successful modification.

**Important optimistic case:** `NO_AGGRESSOR` trades can reduce queues on both sides. Upstream documentation explicitly warns that this can clear a queue and fill earlier than reality. Historical data cannot reveal hidden orders or all venue-specific priority rules.

**Implication:** Queue tracking is a useful conservative approximation only when aggressor side and book updates are reliable. It is not an exact exchange queue simulator. Missing aggressor-side data must be treated as an optimistic execution assumption, not neutral evidence.

Sources: [queue tracking contract and limitations](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/docs/concepts/backtesting/trade-execution.md#L116-L258), [queue snapshot and trade depletion code](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L625-L910), [L1 quote queue adjustment](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L1139-L1215).

### 2.4 Slippage and fill models

- `DefaultFillModel` uses the recorded book. Its documented defaults are `prob_fill_on_limit=1.0` and `prob_slippage=0.0`.
- For L1, `prob_slippage` can move each fill one tick against the order. A fixed `random_seed` makes the fill-model draws repeatable.
- For L2/L3, `prob_slippage` does not apply; the recorded depth is the impact model.
- Built-in synthetic models include tiered books and `CompetitionAwareFillModel`. The latter exposes a configurable fraction of a synthetic 1,000-unit best level (default factor 0.3, clamped to at least one quantity increment).
- Tier quantities are model constants expressed in instrument units. They are not calibrated to IDEAL's target instrument, venue, volatility, depth or trade-size distribution.
- Fill-model randomness is not a global determinism guarantee for every engine ordering decision.

**Implication:** Use empirical L2/L3 depth and trade data as the primary impact evidence. Synthetic models are controlled stress fixtures, not substitutes for measured liquidity. The single-tick L1 model is a deliberately crude sensitivity parameter.

Sources: [fill model behavior and catalogue](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/docs/concepts/backtesting/fill-models.md#L7-L69), [probabilistic slippage semantics](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/docs/concepts/backtesting/fill-models.md#L173-L196).

### 2.5 IDEAL L2 reproduction results

The IDEAL POC now exercises the pinned L2 MBP matching path using explicit `OrderBookDelta` data. The fixture creates two ask levels (0.400 at 40,001.0 and 0.600 at 40,002.0) and a bid to establish a valid two-sided book. A quote event is delivered only after the L2 book snapshot so the strategy submits its market orders against initialized depth.

- A 1.500-unit BUY market order fills 0.400 at 40,001.0 and 0.600 at 40,002.0. The remaining 0.500 is not filled because no more displayed ask depth exists. This reproduces multi-level depth walking and a partial market-order fill.
- Two sequential 0.750-unit BUY market orders share the same 1.000 units of displayed ask depth. With liquidity consumption enabled, aggregate fills equal 1.000, not 1.500. The second simulated order cannot reuse depth already consumed by the first.

**Interpretation:** This demonstrates finite displayed L2 depth consumption in the pinned simulator. It does not model hidden liquidity, latency races, exchange matching priority or the impact of other real participants beyond what is present in the supplied book/trade feed.

## 3. IDEAL POC tests

New file: [`test_execution.py`](test_execution.py)

All tests use synthetic BTCUSDT perpetual fixtures, zero fees to isolate the tested execution mechanism, and the exact pinned NautilusTrader package.

| Test | Fixture | Expected result |
|---|---|---|
| Queue-ahead depletion | 10 units displayed ahead; a 12-unit SELL trade then a 3-unit SELL trade | First print clears 10 ahead and fills 2; next print fills remaining 3 |
| Competing-order trade budget | Two 2-unit resting BUY limits; one 3-unit SELL trade; consumption enabled; queue tracking disabled to isolate consumption | Aggregate fills cannot exceed the 3-unit trade size |
| L1 probabilistic slippage | BUY market order at ask 40,001.0; tick size 0.1; `prob_slippage=1.0` | Fill at 40,001.1 |\n| L2 depth walking | 1.500-unit BUY; asks 0.400 @ 40,001.0 and 0.600 @ 40,002.0 | Two fills of 0.400 and 0.600 at their respective levels; residual 0.500 unfilled |\n| Competing L2 market orders | Two 0.750-unit BUYs against 1.000 total ask depth; consumption enabled | Aggregate fill quantity exactly 1.000; no reuse of consumed depth |

### Verification

- Command: `python -m pytest -q`
- Exact dependency assertion: `nautilus_trader==2.0.0rc9`
- Runner: Ubuntu 24.04 x86_64 / Python 3.14
- Final L2 research branch verification: **35 passed in 0.22s** in [CI run 43697425596](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43697425596), exact pinned wheel / Ubuntu 24.04 / Python 3.14.
- CI: [run 43696169232](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43696169232) and [PR-triggered run 43696163846](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43696163846), both successful.
- Test-harness correction: the first attempt passed constructor arguments to the NautilusTrader `Strategy` wrapper and failed with `Strategy.__new__()`. The fixture was corrected to instantiate with no arguments and set test parameters afterwards. The corrected head passed both CI runs. This was a test-harness API error, not a simulator defect.
- The prior main baseline had 33 tests; this branch adds 2 L2 tests. Final suite: 35 passed. No production code or dependency changed.

Upstream source tests also cover L1 partial queue depletion and shared trade budgets ([Rust tests around lines 4704–4915](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/tests.rs#L4704-L4915)), plus L2 snapshot/depth queue rebasing ([tests around lines 3983–4140](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/tests.rs#L3983-L4140)). Those upstream tests are source evidence, not IDEAL POC integration tests.

## 4. Gaps and risks still open

1. IDEAL has not yet reproduced L2 snapshot rebasing or L3 MBO order-ID queue tracking in its own Python POC.
2. Queue behavior under partial fills, cancellations, amendments and the selected exchange's exact priority rules needs additional tests. No venue is selected.
3. One-tick L1 slippage is not a market-impact curve. No empirical calibration has been performed for order size, volatility, spread, depth, latency or adverse selection.
4. No test here covers spread widening, latency races, stale book updates, hidden liquidity, or venue-specific matching priority.
5. The tests use zero fees to isolate execution mechanics. Fee, funding and market-impact costs must be combined in later strategy validation.

## 5. Current decision

- Keep NautilusTrader as an isolated research candidate only. Do not add it to the IDEAL runtime or adopt a synthetic fill model.
- Any future execution simulation must explicitly configure and record book type, trade execution, liquidity consumption, queue tracking, fill model, price protection, fee model, timestamps and random seeds.
- Unknown aggressor side, missing depth, stale data, or a synthetic liquidity fallback must be labelled as uncertainty and must not silently improve backtest fills.
- Continue Phase 01 with L2 snapshot rebasing, L3 MBO order-ID queue reproduction, queue cancellation/amendment cases and empirical impact calibration before closing this execution-realism gate.
- No exchange, adapter, account, testnet, paper or live trading authorization is implied.
