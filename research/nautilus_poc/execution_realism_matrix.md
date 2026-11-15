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

**Simulated order amendments:** the pinned Rust implementation defines `OrderPriorityResetPolicy` in `crates/execution/src/matching_engine/mod.rs#L3793-L3889`. The POC now tests all three policies end-to-end. A quantity increase after queue progress preserves priority under `PRICE_CHANGE`, but resets under `PRICE_OR_QUANTITY_INCREASE` and `ANY_MODIFY`. A quantity decrease preserves priority under `PRICE_CHANGE` and `PRICE_OR_QUANTITY_INCREASE`, but resets under `ANY_MODIFY`. A price change snapshots queue position at the new price level under all three policies. An identical/no-op modification is rejected by the Python strategy command factory before a `ModifyOrder` reaches the matching engine; consequently even `ANY_MODIFY` does not reset priority for a rejected no-op. These are simulator/API semantics only. Venue-specific amendment priority remains unknown until a venue is selected.

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
2. The POC reproduces external L3 MBO order deletion and size updates, and tests all three simulated-client amendment reset policies for quantity increases, quantity decreases and price changes. No-op requests are rejected before reaching the matching engine. Venue-specific order amendment/cancellation priority remains unverified.
3. No test here covers spread widening, latency races, stale book updates, hidden liquidity or adverse selection.
4. The tests use zero fees to isolate execution mechanics. Fee, funding and empirically calibrated market impact must be combined in later strategy validation.
5. Simulator queue estimates rely on visible feed data and documented FIFO assumptions; they cannot reconstruct hidden queue, feed gaps or priority rules absent from the source venue.

## 5. Current decision

- Keep NautilusTrader as an isolated research candidate only. Do not add it to the IDEAL runtime or adopt a synthetic fill model.
- Any future execution simulation must explicitly configure and record book type, trade execution, liquidity consumption, queue tracking, fill model, price protection, fee model, timestamps and random seeds.
- Unknown aggressor side, missing depth, stale data, or a synthetic liquidity fallback must be labelled as uncertainty and must not silently improve backtest fills.
- The IDEAL POC now reproduces L2 snapshot rebasing, L3 MBO order identity, queue partial fills, external order deletion and size amendments, plus all three configured simulated-order priority policies for quantity increases, quantity decreases and price changes. No-op requests are rejected at the Python command boundary. Keep empirical calibration blocked until venue-specific historical data is available; do not substitute synthetic fixtures.
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

This first-run test establishes the fatal conversion-failure behaviour. The same-engine reset boundary and its false-success replay case are evaluated separately in section 10.


## 10. Corrected-data replay and same-engine reset boundary

### Fresh-engine corrected-data replay

Extended [`test_funding_fx_conversion.py`](test_funding_fx_conversion.py) with a deterministic corrected-data run:

- The failure scenario removes BTC/USD after the inverse BTCJPY position is opened and raises a fatal funding settlement error.
- The corrected replay creates a fresh engine and retains the valid BTC/USD quote through the funding boundary.
- The same inverse BTCJPY position opens, the mark price remains available, the funding boundary is crossed, and settlement completes.
- The test asserts one fill, one open position and a USD account balance below the initial 100,000 USD, proving that the funding debit was applied.

This demonstrates a **fresh replay using corrected FX data**, not an in-place recovery of the failed engine.

### Same-engine reset after cache-purged FX instrument

A new regression test exercises the failed engine itself:

- First run: entry succeeds using a temporary BTC/USD quote; the strategy purges the BTC/USD instrument after the fill; the funding boundary fails closed with `Funding settlement failed`.
- `BacktestEngine.reset()` clears the latched funding error and rewinds the loaded data stream. The strategy's `on_reset()` restores its local submission/fill state.
- After reset, `engine.cache.instrument(BTCUSD_INSTRUMENT.id)` and `engine.cache.load_instrument(...)` both return `None`.
- Calling `engine.add_instrument(BTCUSD_INSTRUMENT)` does not restore the cache entry: the exchange still considers that instrument registered, so `BacktestEngine.add_instrument()` returns early.
- A second `engine.run()` returns normally, but the BTCJPY entry is denied because BTC/USD conversion is missing. The run has zero fills and zero open positions. A green `run()` return is therefore not sufficient evidence of replay recovery.

Source boundaries in the pinned `v2.0.0rc9` implementation:
- [`BacktestEngine.run`](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/backtest/src/engine.rs#L695-L751) aborts on the latched funding error.
- [`BacktestEngine.reset`](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/backtest/src/engine.rs#L1213-L1299) clears the funding error and resets iterator cursors.
- [`BacktestEngine.add_instrument`](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/backtest/src/engine.rs#L359-L390) returns early when the exchange already has the instrument registered.
- [`Cache.load_instrument`](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/common/src/cache/mod.rs#L1002-L1019) returns `None` when the instrument is absent and no cache database is configured.
- The Python `BacktestEngine.cache` wrapper exposes `load_instrument` and `purge_instrument`, but not a callable `add_instrument` method in this pin; the test verifies the runtime surface.

**Conclusion:** same-engine reset/replay is not a recovery path after a strategy purges a required FX instrument from cache in this Python POC. Reconstruct a fresh engine with the instrument definition and valid data, or design and verify an explicit persistence/cache-restoration mechanism. Do not count a reset run as recovered unless the expected position, fill and account effects are present.

Verification: [CI run 43760008008](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43760008008), **78 passed on x86_64 and ARM64**, exact `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 / Python 3.14.10.


## 11. Canonical replay hashes and reset/replay determinism

### Pinned source audit

NautilusTrader `v2.0.0rc9` includes a Rust-side canonical result API:

- `BacktestEngine::get_canonical_result()` projects observable result, orders, fills, positions, position snapshots, accounts, portfolio snapshots, statistics, component state and diagnostics.
- `CanonicalBacktestResult` uses schema `nautilus-backtest-result/v1`, canonical compact JSON and a BLAKE3 digest.
- Its identity canonicalization is designed to remove generated identity noise while retaining event relationships.
- `BacktestEngine::reset()` resets exchanges, data/execution/risk engines, trader, portfolio, funding error, accumulators and iterator cursors. Loaded data persists and iterator cursors are reset to the beginning. The engine forces `drop_instruments_on_reset=false` so registered instruments can be reused.
- The engine's order ID generator does not reset to the original counter: same-engine replay emits different raw client order IDs.
- The Rust `get_canonical_result` method is not exposed by the Python `BacktestEngine` binding or Python stub in this pin. IDEAL's Python POC therefore cannot call the upstream canonical projection directly.

### IDEAL research utility

Added:
- [`replay_audit.py`](replay_audit.py): standard-library versioned canonical JSON and SHA-256 helper (`ideal-replay-audit/v1`). It sorts mapping keys, uses compact UTF-8 JSON, rejects floats (exact decimal values must be strings), and hashes the canonical bytes.
- [`test_replay_integrity.py`](test_replay_integrity.py): four tests:
  1. Two fresh engines with identical data produce identical event/account snapshots and digests.
  2. Same-engine `BacktestEngine.reset()` and replay produce the same canonical digest.
  3. Changing a fill price or account balance changes the digest.
  4. Mapping insertion order does not change bytes; floating-point values are rejected.

The replay snapshot includes deterministic run counts, summary/account state, fills, open/closed position counts. Generated raw client order IDs are mapped to sequence aliases (`order-0001`, etc.) before hashing. The reset test explicitly verifies raw IDs differ across runs while the canonical projection remains identical.

### Verification

- Exact pin: `nautilus_trader==2.0.0rc9`
- Ubuntu 24.04 x86_64 / Python 3.14
- [Final branch CI run 43755658769](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43755658769): **61 passed in 0.23s**.
- One initial reset-hash test failed because raw client order IDs advanced from suffixes `-1/-2` to `-3/-4` across engine reset. This is expected identity-generator behavior; the canonical test now normalizes those generated IDs while preserving event order and all economic fields.
- An exploratory attempt to recover a funding failure in the same engine after purging the FX instrument from cache did not recover: the reset/replay run denied the entry because the FX quote/instrument was not restored by that fixture. This was not merged as a recovery claim. Fresh-engine corrected-data replay is already covered by the funding tests; same-engine funding-failure recovery after a cache purge remains unverified.

### Boundary

This is a POC audit hash, not the upstream NautilusTrader BLAKE3 canonical result and not a production event-sourcing/checkpoint design. It covers deterministic backtest replay and reset within one process. Durable process restart, persisted checkpoints, crash recovery, cross-process hash equivalence, schema migration and canonical hashing of every IDEAL domain event remain open.


## 12. Durable process recovery: Nautilus cache adapters and SQLite journal prototype

### NautilusTrader v2.0.0rc9 persistence architecture

Source audit:
- [`CacheConfig`](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/common/src/cache/config.rs): `persist_account_events=true`, `save_market_data=false`, `flush_on_start=false`, tick/bar capacities default to 10,000, `drop_instruments_on_reset=true`.
- [Cache database adapter contract](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/common/src/cache/database.rs): persists currencies, instruments, accounts, orders, positions, order/position snapshots, actor/strategy state, account events and supported market data.
- [Python cache wrapper](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/common/src/python/cache.rs): `PyCache.__new__` calls `Cache::try_new(config, None)`; no Python `set_database` method is exposed.
- [Python BacktestEngine wrapper](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/backtest/src/python/engine.rs): constructs `BacktestEngine::new(config)`; no cache database factory injection is exposed.
- [LiveNode builder](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/live/src/node/builder.rs) supports `with_cache_database_factory`; [Python LiveNode builder](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/live/src/python/node.rs) exposes this through the registered cache factory.
- [LiveNodeConfig](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/live/src/node/config.rs) has `load_state` and `save_state`, both false by default. These load/save actor and strategy state; they do not constitute a full process checkpoint of all engine scheduling/data-cursor state. LiveNode rejects the Backtest environment.
- [Redis adapter](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/infrastructure/src/redis/cache.rs): Redis 6.2+ required. It persists cache entities and state, but its `add_quote`, `add_trade`, `add_funding_rate`, `add_bar` and `add_order_book` methods explicitly return unsupported errors. Its `flush()` invokes `FLUSHDB`, clearing the entire logical Redis database, including other traders and user keys.
- [PostgreSQL adapter](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/infrastructure/src/sql/cache.rs): supports quote, trade, funding-rate and bar persistence, but explicitly does not support order-book persistence. Its `flush()` deletes only rows for the configured trader. PostgreSQL schema migrations are required; integration tests require a running PostgreSQL service and are Linux-only.
- No SQLite cache adapter exists in the pinned repository tree.

**Conclusion:** Nautilus cache persistence is not a complete replay/checkpoint system. Redis is unsuitable as the only historical market-data store in this release and its flush semantics are unsafe for a shared logical database. PostgreSQL stores more market data but not L2 order books. Neither is injectable into the Python `BacktestEngine` wrapper in this pin. LiveNode supports cache DB injection and component state load/save, but it is not a BacktestEngine checkpoint mechanism.

### IDEAL SQLite event journal POC

Added:
- [`event_journal.py`](event_journal.py)
- [`test_event_journal.py`](test_event_journal.py)

Implementation:
- SQLite file-backed database, WAL mode, `synchronous=FULL`, foreign keys and configurable busy timeout.
- Schema version stored in `PRAGMA user_version`; newer unsupported schemas fail closed.
- Append-only event table with monotonically assigned sequence, unique event ID, event type, event timestamp, canonical payload, previous hash and SHA-256 event hash.
- Hash chain starts from a fixed genesis hash; every event commits in `BEGIN IMMEDIATE` transaction.
- Duplicate event ID with identical content is idempotent; conflicting content raises an error.
- Checkpoints store canonical state JSON, state hash, event sequence and chain hash at that point.
- Restore verifies the full event chain, checkpoint state hash and chain anchor, then returns the checkpoint plus events after its sequence.
- Floating-point payloads are rejected; exact financial values must be decimal strings.
- No external dependency or database server is required.

Ten tests cover:
1. Close/reopen durability.
2. Abrupt writer-process exit after a committed event, then WAL recovery from a new process/connection.
3. Event-ID idempotency and conflicting duplicate rejection.
4. Event payload tamper detection.
5. Snapshot/checkpoint restore and post-checkpoint event replay.
6. Snapshot chain-anchor tamper detection.
7. Float rejection.
8. Newer schema version rejection.
9. Event metadata-column tampering (event ID/type/timestamp columns must agree with canonical payload).
10. Snapshot-state tampering (stored state must match its snapshot hash).

Verification: [final PR-head CI run 43756560957](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43756560957), **71 passed in 0.50s**, exact NautilusTrader pin / Ubuntu 24.04 / Python 3.14.

### Production boundaries and open risks

- The SQLite journal is an isolated research prototype, not integrated into IDEAL runtime, NautilusTrader Cache or trading execution.
- SQLite is single-writer; IDEAL should serialize writes through one journal writer/queue.
- WAL and `synchronous=FULL` improve local durability but do not replace filesystem persistence, backups or off-host recovery.
- The database file must reside on persistent local storage, not an ephemeral worker filesystem or unsupported network filesystem.
- Encryption at rest, key management, backup verification, retention/compaction, schema migration tests, disk-full handling, corruption recovery and write-latency/capacity benchmarks remain open.
- The hash chain is stored in the same database it protects. It detects accidental or partial edits, but a malicious writer with full database access can recompute the entire chain. An off-host signed checkpoint, HMAC key kept outside the database, or immutable external hash anchor is required for stronger tamper evidence.
- The current snapshot stores generic state JSON and an event-chain anchor. It does not yet encode the full Nautilus/IDEAL engine state or safely restore live exchange connections and outstanding orders.
- A fresh deterministic replay with corrected market/FX data remains the verified fallback for backtests; live recovery requires exchange reconciliation and explicit owner-approved architecture.


## 13. SQLite event-journal performance baseline

Added [`benchmark_event_journal.py`](benchmark_event_journal.py) and a non-gating CI benchmark step. Each case appends 5,000 events in individual transactions using WAL and `synchronous=FULL`, creates a midpoint checkpoint, appends the remaining events, verifies the full hash chain, loads the checkpoint and replays the tail.

[CI run 43756858418](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43756858418) measured:

| Metric | 256-byte payload | 1,024-byte payload |
|---|---:|---:|
| Events | 5,000 | 5,000 |
| Throughput | 10,779 events/s | 10,813 events/s |
| p50 append latency | 0.0736 ms | 0.0756 ms |
| p95 append latency | 0.1976 ms | 0.1744 ms |
| p99 append latency | 0.3382 ms | 0.2982 ms |
| Max append latency | 1.4036 ms | 1.3900 ms |
| DB size after close | 4.04 MB | 10.85 MB |
| WAL size before close | 4.14 MB | 4.14 MB |
| Full chain verification | 0.0527 s | 0.0659 s |
| Snapshot + tail restore | 0.0658 s | 0.0791 s |

Environment: GitHub-hosted Ubuntu 24.04 x86_64, 4 vCPU, Python 3.14.10, SQLite 3.45.1; peak process RSS 36,964 KiB (~36.1 MiB). Benchmark step is informational and asserts no throughput threshold.

**Interpretation:** the standard-library prototype is inexpensive in this small synthetic workload. These figures are not a production SLO, not a measurement of an Oracle Always Free VM, and not evidence of durable storage on an ephemeral runner. The test writes one event per transaction; payload shape, disk class, WAL checkpoint frequency, concurrency, backup traffic and long-run growth will materially affect results. The next capacity gate must run on the actual candidate worker with persistent storage and realistic IDEAL event distributions.


## 14. ARM64 compatibility and infrastructure candidate

### POC compatibility

Changed `.github/workflows/nautilus-poc.yml` to a two-runner matrix:
- `ubuntu-24.04` x86_64
- `ubuntu-24.04-arm` ARM64

[final PR-head CI run 43757428845](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43757428845) completed both jobs successfully:
- x86_64: **71 passed in 0.40s**
- ARM64: **71 passed in 0.49s**
- Exact `nautilus_trader==2.0.0rc9`, Python 3.14.10, Ubuntu 24.04 / glibc 2.39.
- The pinned PyPI release includes a `cp314 manylinux_2_34_aarch64` wheel; Ubuntu 24.04 glibc 2.39 satisfies the wheel's glibc floor.

### SQLite benchmark cross-architecture comparison

Same CI run, 5,000 events per payload size, WAL + synchronous FULL:

| Architecture | Payload | Throughput | p50 | p95 | p99 | Peak RSS |
|---|---:|---:|---:|---:|---:|---:|
| x86_64 | 256B | 2,863/s | 0.158 ms | 0.390 ms | 0.896 ms | 35.6 MiB |
| x86_64 | 1,024B | 4,075/s | 0.161 ms | 0.372 ms | 0.694 ms | 35.6 MiB |
| ARM64 | 256B | 2,659/s | 0.320 ms | 0.791 ms | 1.294 ms | 34.4 MiB |
| ARM64 | 1,024B | 2,735/s | 0.326 ms | 0.555 ms | 1.019 ms | 34.4 MiB |

x86_64 maximum append latency outliers reached ~101–111 ms; ARM64 maxima were ~3.2–4.4 ms in this run. These are noisy GitHub-hosted runner measurements and should not be interpreted as a stable architecture ranking. Both jobs use 4 reported CPUs; Oracle A1 is limited to 2 OCPU in the Always Free allocation.

### Oracle Cloud Always Free candidate

Official Oracle documentation currently lists an Always Free Ampere A1 allocation of **2 OCPU and 12 GB RAM**, plus up to **200 GB block storage** and **10 TB outbound data transfer/month** within Always Free quotas. A1 is ARM64, and the pinned NautilusTrader wheel/POC has now passed on ARM64.

Constraints:
- Oracle public region list shows Sydney and Melbourne as the nearest public OCI regions; no New Zealand public OCI region is listed.
- Home region is selected at signup and cannot be changed later; Always Free capacity is region/availability-domain dependent.
- A1 capacity errors can block instance creation; do not upgrade to paid capacity. Wait or use a different eligible availability domain/region only if it remains free.
- Oracle can reclaim idle A1 instances after sustained low utilisation (CPU, memory and network metrics below documented thresholds over a seven-day window).
- Signup requires a supported credit/debit card for verification and may place a temporary authorisation hold; Oracle states it is not a service charge. No account was created and no card details were entered.
- Always Free resources are not an uptime SLA. Persistent boot/block storage must remain within free quotas and the account must not be upgraded to PAYG or create paid resources.

### Other free-tier options

- Google Cloud's free Compute Engine e2-micro allowance is restricted to selected US regions and is too small/remote for the full IDEAL worker.
- AWS's current new-account free plan is time-limited rather than a permanent free VM allocation.
- Cloudflare Workers Free is suitable for a lightweight API/control-plane edge function, not a continuously running Python/Nautilus engine (request CPU limits and serverless lifecycle).

### Current infrastructure decision

Oracle A1 is the **leading candidate, not an approved deployment**. Do not create an account or provision a VM without owner approval. First verify the exact home-region choice, available A1 capacity, persistent-volume quotas and idle-reclamation risk. If free capacity is unavailable, remain in GitHub Actions/manual research mode; do not upgrade or incur cost.


## 15. Multi-currency margin account and native-currency funding

New POC file: [`test_multi_currency_funding.py`](test_multi_currency_funding.py).

Fixture:
- One simulated Binance venue with `AccountType.MARGIN`, `OmsType.HEDGING` and `base_currency=None`.
- Starting balances: 100,000 USD, 2 BTC and 100,000 USDT.
- One inverse BTCJPY perpetual settled in BTC and one linear BTCUSDT perpetual settled in USDT.
- Both long positions are opened with no BTC/USD, USDT/USD or other FX conversion instrument in the engine.
- A positive 0.0001 funding rate is applied to both positions at the same settlement boundary.
- A no-funding baseline run is compared with the funded run.

Observed exact native-currency deltas:
- BTC balance decreases by **0.00016667 BTC** from inverse BTCJPY funding.
- USDT balance decreases by **0.60000000 USDT** from linear BTCUSDT funding.
- USD balance is unchanged.
- Both runs have two fills and two open positions.

This confirms the pinned simulator supports a multi-currency margin account when `base_currency=None`, and applies funding adjustments in each instrument's settlement currency rather than converting all adjustments to one base currency.

Pinned source boundaries:
- [`SimulatedExchange::new`](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/backtest/src/exchange.rs#L225-L237) rejects multiple starting currencies only when a base currency is specified.
- [Funding settlement conversion](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/backtest/src/exchange.rs#L1626-L1664) converts adjustments only when the account has a base currency; otherwise native-currency adjustments remain native.
- [`MarginAccount` multi-currency tests](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/model/src/accounts/margin.rs#L1757-L1823) document no-base-currency margin accounts and show that margin locks only currencies already reported in account balances. The POC therefore pre-seeds both BTC and USDT balances.
- [`Portfolio::equity`](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/portfolio/src/portfolio.rs#L836-L894) returns a per-currency map. [Snapshot base-currency equity](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/portfolio/src/portfolio.rs#L1003-L1015) is absent when the account has no base currency.

**IDEAL design implication (proposal, not an approved decision):** preserve native-currency balances and funding/fee events in the canonical ledger. For portfolio-level risk limits, compute a deterministic reporting-currency equity view from timestamped, side-aware FX marks with explicit freshness and missing-rate handling. Do not sum unlike currency amounts or treat a multi-currency account as having a single USD equity value. This test does not establish venue-specific collateral haircuts, cross-currency margin offsets, liquidation rules or exchange parity.

Verification: [CI run 43760637330](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43760637330), **79 passed on x86_64 and ARM64**, exact `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 / Python 3.14.10.


## 16. Multi-currency collateral and liquidation boundary

Added `test_multi_currency_collateral_liquidation.py` to test whether the pinned simulated exchange pools BTC collateral into the maintenance-equity calculation for a USDT-settled linear perpetual.

### Deterministic fixture and observed result

- Margin account uses `base_currency=None` with starting balances of **2 BTC** and **1,000 USDT**.
- Opens a **0.1 BTCUSDT long** at the 60,000 USDT ask.
- The next quote has a 49,999.5 USDT bid; the close-side move realises **-1,000.05 USDT**.
- The simulator triggers liquidation against the USDT settlement-currency balance and maintenance margin.
- The 2 BTC balance remains unchanged; it is not converted or applied to the USDT maintenance-equity check.
- The synthetic liquidation close leaves the USDT balance at **-0.05 USDT**. This is the observed half-tick residual, not a guaranteed bankruptcy-price cap or insurance-fund recovery.
- The replay test confirms deterministic outcomes.

Verification: [CI run 43761762953](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43761762953), **81 passed on x86_64 and ARM64**, exact `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 / Python 3.14.10. Research PR [#26](https://github.com/ImNotBrookOk/IDEAL/pull/26) was squash-merged as [b440d3815b296ee62ce21dd7f55d929b8600e011](https://github.com/ImNotBrookOk/IDEAL/commit/b440d3815b296ee62ce21dd7f55d929b8600e011).

### Exact pinned source behaviour

- [Simulated exchange liquidation path, `exchange.rs`](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/backtest/src/exchange.rs#L2020-L2088) buckets open positions by `settlement_currency`. It loops through the account's currencies, reads the balance for that currency, sums unrealized PnL only for positions in that same settlement-currency bucket, and compares the result with maintenance margin in that currency. The subsequent liquidation call is also currency-scoped.
- [Portfolio equity, `portfolio.rs`](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/portfolio/src/portfolio.rs#L851-L900) starts from account balances and accumulates margin equity into a per-currency map. With no account base currency, it does not produce a single reporting-currency total.
- [Margin-account balance locking, `margin.rs`](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/model/src/accounts/margin.rs#L455-L500) totals margin entries within the requested currency and recalculates that currency's balance. It does not convert a different collateral currency in this path.
- The account model can represent [account-wide margin entries keyed by collateral currency](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/docs/concepts/accounting.md#L257-L271). That is a representation of venue-reported per-currency margin, not proof that the backtest liquidation path applies collateral conversion, cross-asset haircuts or a unified portfolio maintenance test.

### IDEAL implication and remaining evidence

The tested NautilusTrader simulated liquidation path is **not a unified multi-collateral liquidation model**. It cannot be treated as exchange-equivalent for an account where BTC, USDT or other assets are pooled with conversion rates and haircuts. If the selected venue supports that account mode, IDEAL will need a deterministic venue-specific collateral/risk model (or a verified engine extension) that explicitly handles collateral eligibility, conversion side/mark, haircuts, concentration limits, stale/missing FX, per-coin maintenance, liquidation ordering and bankruptcy/insurance/ADL outcomes. Preserve native-currency ledger balances and never sum unlike currencies without an explicit conversion.

This test establishes only the pinned simulator behaviour. It does not select a venue, validate a live adapter, or prove how Binance, Bybit, OKX or any other venue handles the user's account mode. Official venue/product/account-mode specifications and representative collateral/liquidation data remain required before the engine-selection gate can close.
