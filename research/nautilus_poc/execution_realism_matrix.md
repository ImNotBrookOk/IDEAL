# Execution Realism Research — Partial Fills, Queue Position, Liquidity Consumption and Slippage

**Research date:** 15 November 2026  
**Phase:** 01 — open-source and infrastructure research  
**Status:** L1/L2 depth, L2 snapshot rebasing and L3 MBO queue scenarios reproduced in the isolated POC. A provenance-aware impact-calibration utility is implemented and tested; empirical calibration remains blocked pending a selected venue and representative historical order-book/fill data.  
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

### 2.6 IDEAL L2 snapshot and L3 MBO queue reproduction

The POC now tests queue rebasing and order-level queue events through observable fills, not only source inspection.

**L2 MBP snapshot rebasing**
- Start with 10.000 units displayed at the simulated SELL order's price; the order joins behind that quantity.
- A replacement snapshot reducing visible quantity to 8.000 caps the existing queue estimate at 8.000. A subsequent 9.000-unit BUY trade fills exactly 1.000.
- A replacement snapshot increasing visible quantity to 15.000 does not push the existing order back. Its queue estimate remains capped at the prior 10.000; an 11.000-unit BUY trade fills exactly 1.000.
- The clear/start and final-delta snapshot sequence is processed as a batch, so the queue estimate is not discarded on the intermediate clear.

**L3 MBO identity-aware queue tracking**
- Two displayed ask orders (IDs 101 and 102, 5.000 units each) establish 10.000 units ahead of a simulated SELL limit.
- A completed snapshot retaining IDs 101 and 102 while introducing a new 50.000-unit ID 103 preserves only the previously tracked IDs. New IDs in the replacement snapshot are not retroactively inserted ahead of the resting simulated order.
- Deleting ID 101 advances the queue by its 5.000 units only. A 6.000-unit BUY trade then fills exactly 1.000.
- Updating ID 101 from 5.000 to 3.000 advances the queue by the 2.000-unit decrement. A 9.000-unit BUY trade fills exactly 1.000.
- Updating ID 101 from 5.000 to 7.000 adds 2.000 units ahead under this simulator's retained-FIFO-slot rule. An 11.000-unit BUY trade cannot reach the simulated order.
- With 10.000 units ahead, a 12.000-unit BUY trade partially fills a 5.000-unit resting order by 2.000; the next 3.000-unit BUY trade fills the remaining 3.000.

**Simulated order amendments:** the pinned documentation and Rust tests define `OrderPriorityResetPolicy`. Default `PRICE_CHANGE` preserves progress for quantity-only decreases/increases but resets at a changed price. `PRICE_OR_QUANTITY_INCREASE` also resets on quantity increases. `ANY_MODIFY` resets on every successful modify command, including no-op changes. The Python POC now tests all three policies for a quantity increase after queue progress and an L2 depth increase: `PRICE_CHANGE` preserves the original order's priority, while `PRICE_OR_QUANTITY_INCREASE` and `ANY_MODIFY` move it behind the unmodified peer. Price changes, quantity decreases and no-op modifications remain untested end-to-end. Venue-specific amendment priority remains unknown until a venue is selected.

Sources: [pinned queue implementation and rebase logic](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L625-L1088), [pinned queue lifecycle and amendment policies](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/docs/concepts/backtesting/trade-execution.md#L116-L258), [upstream L2/L3 queue tests](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/tests.rs#L3983-L4297).

### 2.7 Empirical market-impact calibration utility

Added `impact_calibration.py`, a standard-library-only offline analysis utility. It accepts one row per parent order and requires a single venue, instrument and data source, unique order IDs, event timestamps, side, requested/filled quantity, fill VWAP, decision-time midpoint, spread, volatility, visible depth within 10 bps and execution latency.

It calculates side-aware realized implementation shortfall:
- BUY: `(fill_vwap / decision_mid - 1) × 10,000` bps.
- SELL: `-(fill_vwap / decision_mid - 1) × 10,000` bps.
- Residual impact is measured as realized slippage less half the quoted spread; this is a diagnostic decomposition, not a causal impact estimate.
- It reports fill ratio, volume-weighted mean slippage, p50/p90/p95, and training buckets by order-size participation versus displayed depth, spread, volatility and latency.
- It sorts chronologically, uses the first 70% for descriptive calibration and the final 30% as an untouched temporal check, reports observed coverage against the training p90, hashes the source CSV and rejects mixed provenance, duplicate IDs and invalid fill records.
- Provisional diagnostic review minimums are 200 parent orders, at least 30 filled OOS orders and 30 observations per bucket. These are not owner-approved strategy gates.

**Empirical status: BLOCKED.** No venue has been selected and no representative historical L2 snapshots/trades paired with IDEAL-style parent-order execution outcomes have been supplied. Synthetic unit fixtures verify arithmetic, data validation, provenance handling and chronological splitting only. They do not calibrate real-world slippage, adverse selection or market impact. Do not use the generated synthetic test data as a trading cost model.

Run with:
```bash
python impact_calibration.py path/to/parent_order_fills.csv --output impact_calibration_report.json
```

## 3. IDEAL POC tests

New file: [`test_execution.py`](test_execution.py)

All tests use synthetic BTCUSDT perpetual fixtures, zero fees to isolate the tested execution mechanism, and the exact pinned NautilusTrader package.

| Test | Fixture | Expected result |
|---|---|---|
| Queue-ahead depletion | 10 units displayed ahead; a 12-unit SELL trade then a 3-unit SELL trade | First print clears 10 ahead and fills 2; next print fills remaining 3 |
| Competing-order trade budget | Two 2-unit resting BUY limits; one 3-unit SELL trade; consumption enabled; queue tracking disabled to isolate consumption | Aggregate fills cannot exceed the 3-unit trade size |
| L1 probabilistic slippage | BUY market order at ask 40,001.0; tick size 0.1; `prob_slippage=1.0` | Fill at 40,001.1 |
| L2 depth walking | 1.500-unit BUY; asks 0.400 @ 40,001.0 and 0.600 @ 40,002.0 | Two fills of 0.400 and 0.600 at their respective levels; residual 0.500 unfilled |
| Competing L2 market orders | Two 0.750-unit BUYs against 1.000 total ask depth; consumption enabled | Aggregate fill quantity exactly 1.000; no reuse of consumed depth |
| L2 snapshot queue decrease | Queue 10.000; replacement snapshot 8.000; BUY trade 9.000 | Queue caps at 8.000; 1.000 fills |
| L2 snapshot queue increase | Queue 10.000; replacement snapshot 15.000; BUY trade 11.000 | Existing queue remains 10.000; 1.000 fills |
| L3 MBO snapshot identity | Retain IDs 101/102; add new ID 103; then delete ID 101 | Only previously tracked IDs remain ahead; 1.000 fills on 6.000 trade |
| L3 MBO cancel/delete | Delete 5.000-unit order ID 101 from 10.000 ahead | Queue advances by exactly 5.000; 1.000 fills on 6.000 trade |
| L3 MBO size decrease | ID 101 decreases 5.000 → 3.000 | Queue advances 2.000; 1.000 fills on 9.000 trade |
| L3 MBO size increase | ID 101 increases 5.000 → 7.000 | Queue ahead increases to 12.000; 11.000 trade does not fill |
| L3 partial fills | 10.000 ahead; 5.000-unit simulated order; trades 12.000 then 3.000 | Partial fills 2.000 then 3.000 |
| Impact calibration arithmetic | BUY and SELL parent-order examples; 2 bps spread | Both directions report 10 bps adverse slippage and 9 bps residual after half-spread; unfilled order is retained in fill-ratio counts |

### Verification

- Command: `python -m pytest -q`
- Exact dependency assertion: `nautilus_trader==2.0.0rc9`
- Runner: Ubuntu 24.04 x86_64 / Python 3.14
- Final queue/impact research branch verification: **49 passed in 0.18s** in [final PR-head CI run 43699506563](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43699506563), exact pinned wheel / Ubuntu 24.04 / Python 3.14.
- CI: [run 43696169232](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43696169232) and [PR-triggered run 43696163846](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43696163846), both successful.
- Test-harness correction: the first attempt passed constructor arguments to the NautilusTrader `Strategy` wrapper and failed with `Strategy.__new__()`. The fixture was corrected to instantiate with no arguments and set test parameters afterwards. The corrected head passed both CI runs. This was a test-harness API error, not a simulator defect.
- The prior main baseline had 35 tests; this branch adds 7 queue-reproduction tests, 3 simulated-client amendment-priority tests and 4 impact-utility tests. Final suite: 49 passed. No production code or dependency changed.
- L2 fixture debugging history: first run failed because the Python binding required integer record flags (`RecordFlag.F_LAST.value`); second run constructed the book but submitted market orders before the book had been processed, resulting in no fills. The strategy was changed to submit on a subsequent quote event after the L2 book snapshot. The final run passed. These were test-fixture issues, not engine defects.

Upstream source tests also cover L1 partial queue depletion and shared trade budgets ([Rust tests around lines 4704–4915](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/tests.rs#L4704-L4915)), plus L2 snapshot/depth queue rebasing ([tests around lines 3983–4140](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/tests.rs#L3983-L4140)). Those upstream tests are source evidence, not IDEAL POC integration tests.

## 4. Gaps and risks still open

1. Empirical calibration remains blocked until a venue is selected and representative historical L2 snapshots/trades and execution outcomes are available. The new utility is validated on synthetic fixtures only.
2. The POC reproduces external L3 MBO order deletion and size updates, and tests all three simulated-client amendment reset policies for quantity increases. Price changes, quantity decreases and no-op amendments remain untested end-to-end. Venue-specific order amendment/cancellation priority remains unverified.
3. No test here covers spread widening, latency races, stale book updates, hidden liquidity or adverse selection.
4. The tests use zero fees to isolate execution mechanics. Fee, funding and empirically calibrated market impact must be combined in later strategy validation.
5. Simulator queue estimates rely on visible feed data and documented FIFO assumptions; they cannot reconstruct hidden queue, feed gaps or priority rules absent from the source venue.

## 5. Current decision

- Keep NautilusTrader as an isolated research candidate only. Do not add it to the IDEAL runtime or adopt a synthetic fill model.
- Any future execution simulation must explicitly configure and record book type, trade execution, liquidity consumption, queue tracking, fill model, price protection, fee model, timestamps and random seeds.
- Unknown aggressor side, missing depth, stale data, or a synthetic liquidity fallback must be labelled as uncertainty and must not silently improve backtest fills.
- The IDEAL POC now reproduces L2 snapshot rebasing, L3 MBO order identity, queue partial fills, external order deletion and size amendments, plus all three configured simulated-order priority policies for quantity increases. Keep empirical calibration blocked until venue-specific historical data is available; do not substitute synthetic fixtures.
- No exchange, adapter, account, testnet, paper or live trading authorization is implied.


## 6. Stop-loss / take-profit bar ordering and gap-through

Pinned source: NautilusTrader `v2.0.0rc9`, `crates/execution/src/matching_engine/mod.rs`:

- `process_bar` accepts external time-aggregated Last/Mid bars for L1 bar execution and synthesises trade ticks from OHLC legs.
- The default path is Open → High → Low → Close.
- With `bar_adaptive_high_low_ordering=True`, `bar_high_first` selects high-first only when `high - open < open - low`; otherwise low-first. A tie therefore resolves low-first.
- The default config is `bar_adaptive_high_low_ordering=False`.
- Stop-market orders triggered by the synthetic bar path are executed by the simulator's synthetic L1 execution state. This is not a venue order-book replay.

New IDEAL POC file: [`test_stop_target_bar.py`](test_stop_target_bar.py)

| Test | OHLC path | Expected observed exit |
|---|---|---|
| Ambiguous dual-touch, default | O-H-L-C | Take-profit limit fills at 40,010; OCO stop is cancelled |
| Ambiguous dual-touch, adaptive | O-L-H-C (high/low distances tie) | Stop-market fills at 39,990; OCO take-profit is cancelled |
| Stop-loss gap-through | Opens at 39,980 below 39,990 stop | Stop-market fills at synthetic bar open 39,980 |

The first two tests use the same OHLC range and bracket; only the bar-ordering configuration changes. They produce different exits. The candle itself cannot establish which extreme occurred first. A backtest that silently chooses the favourable path can materially overstate performance. IDEAL must label dual-touch OHLC bars as path-ambiguous and must not assume the profitable exit. A conservative policy, lower-timeframe reconstruction or tick/order-book replay must be selected and documented before strategy validation.

The gap-through test proves only the pinned simulator's synthetic L1 behavior: a stop-market exit is priced at the bar open when the open is already beyond the stop. It does not establish real executable bid/ask, spread, market impact, latency or exchange stop-trigger reference semantics.

### Verification

- Exact pin: `nautilus_trader==2.0.0rc9`
- Ubuntu 24.04 x86_64 / Python 3.14
- Final branch CI: [run 43753234096](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43753234096), **52 passed in 0.19s**.
- One initial assertion expected the synthetic stop-market fill to be strictly worse than the stop trigger. The engine filled exactly at the stop trigger in the intrabar-touch fixture; the assertion was corrected to the observed exact trigger price. The separate gap-through test expects and verifies the open price. The final 52-test suite passed.
- Research/test/documentation changes only. No runtime logic, dependency or venue selection changed.


## 7. Funding settlement fallback and multi-position behaviour

Pinned source: NautilusTrader `v2.0.0rc9`, `crates/backtest/src/exchange.rs`:

- `funding_settlement_price` prefers a cached mark price. If no mark exists, it requires both best bid and best ask and uses their midpoint.
- If neither mark nor a complete top-of-book is available, settlement returns false and the pending funding rate is retained in the exchange's pending map.
- A single-currency account whose base currency differs from the position settlement currency requires a cached mid FX conversion rate. Missing/invalid conversion returns false.
- Funding is calculated per open position and aggregated by currency before account balance adjustments. Positions for the instrument with different settlement currencies are rejected.
- The backtest engine's `settle_funding_rates` converts a failed settlement into a fatal `Funding settlement failed` error. The pending item remains internally, but the current run does not simply continue and retry when later market data arrives. Recovery must be handled explicitly by reset/replay or corrected data; no automatic in-run retry is established.
- Settlement idempotency is keyed by `(boundary timestamp, instrument ID)`; a previously settled key is not applied again.

New IDEAL POC file: [`test_funding_edge_cases.py`](test_funding_edge_cases.py)

- Missing mark-price fallback: two independent 0.100 BTC long positions are opened under HEDGING OMS. No mark update is supplied. The funding calculation uses the 60,000.25 top-of-book midpoint, settles both positions, and verifies the aggregate account balance of 9,992.79994600 USDT. Per-position Money quantization is reflected in the expected result.
- Duplicate update: the same funding rate/boundary is submitted again after settlement. The result (fills, open positions and account balance) is identical to the single-update replay; no second funding debit is applied.

### Verification

- Exact pin: `nautilus_trader==2.0.0rc9`
- Ubuntu 24.04 x86_64 / Python 3.14
- [CI run 43753618622](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43753618622): **54 passed in 0.18s**.
- Fixture corrections recorded during development: first, the instrument venue (BINANCE) did not match the configured SIM venue; second, the quote prices used precision 2 while the instrument requires precision 1; third, the exact account balance differed by 0.000001 due to per-position Money rounding. Each fixture/expectation was corrected from observed engine behavior and the final suite passed.
- No runtime code or dependencies changed.

### Remaining funding risks

- No test yet forces both mark and top-of-book to be absent at the funding boundary and verifies the fatal run error/pending state.
- No end-to-end test yet constructs a position whose settlement currency differs from a single-currency account base and proves missing FX conversion failure, followed by explicit replay recovery.
- Multi-position testing covers two same-instrument, same-settlement-currency long positions under HEDGING OMS. Mixed settlement currencies and multi-currency accounts remain untested.


## 8. Missing mark and missing top-of-book: fatal funding path

New IDEAL POC file: [`test_funding_failure_modes.py`](test_funding_failure_modes.py).

The test opens a long position against an L2 book, queues a funding rate with a future boundary, clears both bid and ask sides before that boundary, and deliberately supplies a later quote after the boundary. No mark update is supplied. At settlement, neither a mark nor a complete top-of-book exists.

Observed result: `BacktestEngine.run()` raises `RuntimeError` matching `Funding settlement failed`. The strategy has one filled entry and the position remains open. The later quote does not recover the same run because the engine aborts at the failed boundary.

This confirms the distinction between exchange-level pending-rate retention and backtest-engine recovery: the exchange retains the failed pending item internally, but the engine surfaces a fatal error and does not continue replaying later data. Recovery must be explicit (e.g. reset and replay with corrected market data); that recovery procedure is not yet end-to-end tested.

Final test-only branch verification before documentation update: [CI run 43753816852](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43753816852), **55 passed in 0.20s**, exact pinned release / Ubuntu 24.04 / Python 3.14.


## 9. Missing FX conversion at funding settlement

New IDEAL POC file: [`test_funding_fx_conversion.py`](test_funding_fx_conversion.py).

Fixture design:
- Open an inverse BTCJPY perpetual position settled in BTC, with account base currency USD.
- A temporary BTC/USD spot quote is present at entry so the risk engine can validate the position. The order is a marketable limit order against the L2 ask because market-order risk validation requires an available market price.
- After the BTCJPY position fills, the strategy purges the temporary BTC/USD instrument from cache. The position remains open.
- A mark price for BTCJPY is supplied before funding settlement, so funding valuation itself has a valid price.
- The remaining ETH/USD trigger quote does not provide a conversion path from BTC to USD.
- The funding boundary is advanced by a later event.

Observed result: the funding boundary raises a fatal `RuntimeError: Funding settlement failed`. The test asserts one entry fill and the position remains open. This isolates the FX-conversion failure from missing settlement valuation price.

Earlier attempts and corrections:
- A BTCUSD inverse instrument inadvertently provided its own BTC/USD conversion rate, so it did not reproduce missing FX.
- Removing the quote before entry caused the risk engine to deny the order with `Account currency conversion failed: No exchange rate from BTC to USD`; a position could not be opened.
- A first replay ended before the funding boundary, so it never attempted settlement. A later event was added to advance beyond the boundary.
- Final fixture uses BTCJPY plus a temporary BTC/USD quote purged after entry, a valid mark price, and a later event after the boundary.

Verification: [CI run 43754511937](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43754511937), **56 passed in 0.20s**, exact `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 / Python 3.14.

Explicit reset/replay recovery after the fatal conversion failure remains untested. This test establishes failure behaviour only; it does not implement recovery.
