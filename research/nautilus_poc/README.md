# NautilusTrader isolated proof-of-concept

**Status:** native synthetic test suite passes; research only; engine adoption is not approved.

## Scope and safety

- Exact engine pin: `nautilus_trader==2.0.0rc9`.
- Python 3.14; Ubuntu 24.04 x86_64 GitHub Actions runner.
- Synthetic fixtures only. No exchange adapter, credentials, network market data, paper/live orders or persistent service.
- The release is a pre-release candidate. It is not approved for production or real-money trading.
- This directory is not imported by the IDEAL application and must not become a runtime dependency without a separate architecture decision.

## Verified test coverage

The exact pinned package installed in CI, its version assertion passed, and the complete suite passed:

- **24 tests passed** in GitHub Actions run [43692019956](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43692019956); the change is covered by [PR #4](https://github.com/ImNotBrookOk/IDEAL/pull/4).
- Test command: `python -m pytest -q`.
- The preceding 22-test baseline and source-audit documentation are on [main commit e4c5f1c](https://github.com/ImNotBrookOk/IDEAL/commit/e4c5f1cde0df6bb75625d24f94b0618fd02560f5).

Coverage:

1. Independent Decimal oracles: linear and inverse long/short PnL, execution fee arithmetic, funding sign convention and invalid-input rejection.
2. Native models: pinned version, linear and inverse `CryptoPerpetual` construction, `FundingRateUpdate` construction and simulated margin venue registration.
3. Order lifecycle: `OrderSubmitted → OrderAccepted → OrderFilled` when simulated market-order acknowledgements are explicitly enabled; one open position; market buy executes at the synthetic best ask.
4. Replay: repeated identical order and funding fixtures produce identical asserted outcomes.
5. Margin: a resting limit order reserves exactly `299.99500000 USDT` initial margin under `StandardMarginModel`; a filled position has exactly `150.00125000 USDT` maintenance margin under the same fixed-percentage model.
6. Funding: positive funding of `0.0001` on `6000.05 USDT` mark notional debits `0.60000500 USDT` at the specified funding boundary. The taker fee is `3.00002500 USDT`; final balance is `9996.39997000 USDT`.
7. Missing boundary: a funding update without `next_funding_ns` and not aligned to its interval does not create a funding payment.
8. Quote-driven liquidation: an inverse BTCUSD maintenance-margin breach closes the position; replay is deterministic. The 40,000 → 20,000 gap fixture leaves a negative account balance.
9. Mark precedence: a 20,000 mark triggers liquidation while the cached matching-engine quote remains 40,000; the synthetic close executes at the 40,000 bid and the exact final balance is `0.62500000 BTC`. Replaying this conflict fixture is deterministic.
10. Bar-only and trade-only liquidation: an external LAST bar with L1 bar execution triggers and closes a liquidation using the bar-generated synthetic book; a separate L2 case opens a position from an ask, clears the L2 book, then moves LAST to 20,000 with a TradeTick. The independent inverse-PnL oracle gives -250 BTC against 0.8125 BTC account balance and 0.0875 BTC maintenance margin. The liquidation trigger is therefore breached, but the close is skipped because the L2 book has no executable best bid. Both cases replay deterministically.
11. Long/short quote-side selection under a non-zero spread: from a 40,000 entry, a later 39,800 bid / 40,200 ask makes the long adverse only at bid and the short adverse only at ask. Separate engine runs assert both positions liquidate and the close fills at the expected executable side. Replays are deterministic.
12. Execution realism L1: queue-ahead depletion, partial trade-driven fills, shared trade-volume consumption across competing L1 limit orders, and deterministic one-tick L1 slippage.
13. Execution realism L2: multi-level ask depth walking with a partially unfilled residual, plus competing market orders sharing finite displayed depth.
14. Queue rebasing and MBO: L2 snapshot size decrease/increase; L3 order-ID snapshot retention; L3 delete/cancel, size decrease/increase and sequential partial fills. Ten queue scenarios pass, including three end-to-end quantity-increase amendment tests across all three configured reset policies.
15. Impact calibration utility: provenance-checked parent-order CSV input, side-aware slippage, half-spread residual, fill ratios, size/depth participation, spread/volatility/latency buckets, chronological 70/30 split, OOS p90 coverage, dataset SHA-256 and input validation. Four synthetic-fixture tests pass; empirical market impact remains blocked pending venue selection and historical depth/fill data.

## Liquidation source audit (2.0.0rc9)

The source audit corrects an earlier interpretation of NautilusTrader issue [#5453](https://github.com/nautechsystems/nautilus_trader/issues/5453).

- The issue reported quote-only liquidation valuation on an earlier development build and was closed on 5 November 2026.
- In the exact evaluated `v2.0.0rc9` source, `SimulatedExchange::process_liquidations` calls a dedicated `liquidation_unrealized_pnl` helper. Its valuation precedence is **mark price → position-side quote → last trade → latest valid bar close**. For a long, the quote side is bid; for a short, it is ask. This means the issue's quote-only finding must not be repeated as a confirmed defect in this pin.
- The execution-path limitation is now reproduced directly. `OrderMatchingEngine::liquidate_open_positions` checks for a best bid (long close) or best ask (short close) in the matching engine before creating the synthetic market close. The L2 test opens a position from an ask, clears the book, and supplies only an adverse TradeTick. The last-trade fallback values the breach, but the empty book has no best bid, so the engine skips the close and leaves the position open.
- Bar-only behaviour depends on execution configuration. With `bar_execution=True` and `BookType.L1_MBP`, the matching engine converts the external LAST bar into synthetic L1 market updates. The bar-close fallback triggers liquidation and the bar-generated synthetic bid executes the close. This is model-generated liquidity, not evidence that a real exchange supplied an executable quote.
- Do not equate a trade-only feed with an empty order book in every configuration. An initial L1 `trade_execution=True` experiment showed trade ticks can populate synthetic L1 bid/ask state and allow a close. The no-book test therefore uses L2, an explicit book clear, and `trade_execution=False` for the adverse trade.
- The mark-precedence test confirms that the 20,000 mark triggers liquidation despite a stale 40,000 quote. The synthetic close then fills against the available 40,000 bid. This separates *trigger valuation* from *close execution price*; the two prices are not interchangeable.
- The spread tests exercise the quote fallback with no mark price: long valuation must use bid, while short valuation must use ask. The deliberately asymmetric 39,800/40,200 quote makes the opposite side favourable, so an incorrect side selection would not trigger liquidation. The synthetic close then executes at the same position-closing side (bid for a long, ask for a short).
- The current inverse quote-gap fixture closes one position and leaves the account at **-249.56250000 BTC**. The synthetic close uses the observed quote and can produce a negative balance; no guaranteed bankruptcy-price cap, insurance-fund recovery or ADL protection is demonstrated.
- The synthetic liquidation fill is not a realistic exchange liquidation model. Exchange-specific liquidation fees, partial liquidation, bankruptcy price, insurance fund, ADL and account recovery remain unverified.

Source references pinned to the evaluated release:

- [Liquidation trigger/account evaluation](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/backtest/src/exchange.rs#L1995-L2060).
- [Mark/quote/trade/bar liquidation valuation precedence](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/backtest/src/exchange.rs#L2381-L2458).
- [Bar and trade matching paths](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L1922-L2070) and [trade tick processing](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L2403-L2495).
- [Best-bid accessor](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L1356-L1365) and [synthetic close executable-side pre-check](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L2939-L3025).
- [NautilusTrader liquidation issue #5453](https://github.com/nautechsystems/nautilus_trader/issues/5453).

## Important engine semantics observed

- A simulated market order does not emit `OrderAccepted` by default. The test enables `use_market_order_acks=True` to explicitly exercise the acknowledgement stage. Do not assume this is identical to every live adapter's event sequence.
- Funding updates are not payments by themselves. The exchange schedules settlement at `next_funding_ns` (or a valid interval boundary), then adjusts the position and account.
- Fees are configured on the simulated venue with `MakerTakerFeeModel`, not on the `CryptoPerpetual` instrument constructor.
- The venue requires an explicit fee model, including when zero fees are intended.
- The default margin model is leverage-adjusted. `StandardMarginModel` is used here only to test exact fixed-percentage collateral arithmetic; this is not a final exchange-specific margin choice.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

CI runs the same command on GitHub-hosted Linux runners. No paid service or secret is used.

Latest verification: **71 tests passed in 0.50s** in [final PR-head CI run 43756560957](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43756560957), exact `nautilus_trader==2.0.0rc9` pin on Ubuntu 24.04 / Python 3.14. The suite includes L1/L2 depth, L2 snapshot rebasing, L3 MBO queue/cancel/amend/partial-fill scenarios, impact-calibration utility tests and stop/target OHLC path/gap-through cases. Full findings and the empirical-data blocker are in [execution_realism_matrix.md](execution_realism_matrix.md).

## Execution realism research

The POC reproduces selected L1 queue depletion, partial trade-driven fills, shared trade-volume consumption and one-tick L1 slippage; L2 multi-level depth and finite displayed-depth consumption; L2 snapshot rebasing; and L3 MBO order-ID snapshot retention, delete/cancel, size updates and partial fills. All three simulated-client priority reset policies are end-to-end tested for quantity-increase amendments. A separate standard-library calibration utility is tested on synthetic fixtures. Real empirical calibration is blocked pending venue selection and representative historical depth/fill data. No production code or dependency was added.

## Exchange-specific liquidation and recovery gap

A source comparison of Binance Futures, Bybit UTA derivatives and OKX derivatives is recorded in [exchange_liquidation_gap_matrix.md](exchange_liquidation_gap_matrix.md). The venues differ in staged liquidation, bankruptcy-price takeover, insurance-pool allocation, ADL triggers/ranking and telemetry. The pinned NautilusTrader simulator's current liquidation path submits one full-position reduce-only IOC after an executable-side check; it does not implement these venue-specific workflows. No venue is selected and no testnet/account access was used. Refresh official contract specifications, API changelogs and jurisdiction eligibility immediately before any future adapter implementation.

## Still unverified

- Empirical slippage/market-impact calibration using representative venue-specific historical L2, trade and execution data. The analysis utility is implemented and tested on synthetic fixtures only; it cannot generate empirical results without that dataset.
- Amendment tests currently cover quantity increases under `PRICE_CHANGE`, `PRICE_OR_QUANTITY_INCREASE` and `ANY_MODIFY`. Price changes, quantity decreases and no-op modifications remain untested end-to-end; venue-specific amendment/cancel priority is unknown until a venue is selected.
- Spread widening, latency races, stale book updates, hidden liquidity and adverse selection.
- Stop/target same-bar ordering and stop-loss gap-through are now reproduced in `test_stop_target_bar.py`. Default O-H-L-C selects TP when both OCO exits are inside one bar; adaptive low-first ordering selects SL on an equidistant high/low bar. A stop-market gap-through fills at the synthetic bar-open price. OHLC does not reveal actual intrabar chronology or executable spread/depth, so ambiguous dual-touch bars must remain uncertainty-labelled.
- Funding with missing mark price fallback, two hedged positions and duplicate post-settlement updates are covered in `test_funding_edge_cases.py`. Missing both mark and top-of-book is now tested: an L2 book is cleared before the funding boundary and the run raises a fatal funding error even though a later quote is queued. The pending rate is retained internally, but the engine does not automatically retry later data in the same run. Missing account FX conversion is now tested with an inverse BTCJPY position: a temporary BTC/USD quote permits entry, then the conversion instrument is purged after the fill while a mark price remains available for settlement valuation. The funding boundary fails closed because BTC/USD conversion is absent. A fresh deterministic replay with the BTC/USD conversion quote restored through the funding boundary is now tested and completes settlement with an account-balance debit. Same-engine reset/replay recovery remains unverified.
- Full canonical event/account replay hashes and restart/recovery semantics.
- Resource benchmarks on the intended free worker.
- Exchange-specific linear/inverse contract multipliers, fees, margin tiers and liquidation rules.

## Impact calibration utility

Use the standard-library-only `impact_calibration.py` utility with one row per parent order. Start from [the CSV template](impact_calibration_template.csv), populate it only with provenance-labelled observations from one venue, instrument and source, then run:

```bash
python impact_calibration.py path/to/parent_order_fills.csv --output impact_calibration_report.json
```

The utility reports side-aware implementation shortfall, half-spread residual, fill ratios, p50/p90/p95, size/depth participation and spread/volatility/latency buckets, dataset SHA-256, and a chronological 70/30 train/OOS diagnostic. It rejects duplicate IDs, mixed provenance and invalid fills. Its provisional sample minimums are diagnostic only, not approved trading gates. No actual market data is bundled or inferred.


No claim of production suitability, profitability or live-execution parity is made.


16. Canonical replay audit: `replay_audit.py` produces versioned compact JSON and SHA-256 digests; `test_replay_integrity.py` compares independent fresh-engine replays and same-engine `reset()` replays, verifies tamper sensitivity and rejects floats in favor of exact decimal strings. Raw client order IDs advance across same-engine reset, so the test maps them to deterministic sequence aliases before hashing. Four replay-integrity tests pass. Durable process restart checkpoint/restore remains open.


17. Durable replay prototype: `event_journal.py` is a standard-library SQLite WAL append-only event journal with FULL synchronous commits, schema versioning, event-ID idempotency/conflict detection, SHA-256 hash chaining, canonical decimal-string payloads, checkpoint state hashes and post-checkpoint replay. `test_event_journal.py` covers close/reopen durability, abrupt writer-process exit recovery, tamper detection, duplicate handling, checkpoint/tail restore, float rejection and schema version rejection. This is isolated research code, not runtime integration. Requires persistent local storage and a backup/restore policy before production use. The in-database hash chain detects accidental/partial corruption, not a malicious writer able to rewrite the whole database; an external signed checkpoint or HMAC anchor is required for stronger tamper evidence.


18. SQLite event-journal benchmark: the CI runner executes 5,000 committed events for 256B and 1,024B payloads using WAL + synchronous FULL. Latest measured baseline: approximately 10.8k events/s, p50 write latency 0.074–0.076ms, p95 0.174–0.198ms, p99 0.298–0.338ms, 36.1 MiB peak process RSS. This is GitHub-hosted runner data, not a target-worker guarantee.
