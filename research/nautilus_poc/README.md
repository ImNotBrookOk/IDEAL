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

## Liquidation source audit (2.0.0rc9)

The source audit corrects an earlier interpretation of NautilusTrader issue [#5453](https://github.com/nautechsystems/nautilus_trader/issues/5453).

- The issue reported quote-only liquidation valuation on an earlier development build and was closed on 5 November 2026.
- In the exact evaluated `v2.0.0rc9` source, `SimulatedExchange::process_liquidations` calls a dedicated `liquidation_unrealized_pnl` helper. Its valuation precedence is **mark price → position-side quote → last trade → latest valid bar close**. For a long, the quote side is bid; for a short, it is ask. This means the issue's quote-only finding must not be repeated as a confirmed defect in this pin.
- The execution-path limitation is now reproduced directly. `OrderMatchingEngine::liquidate_open_positions` checks for a best bid (long close) or best ask (short close) in the matching engine before creating the synthetic market close. The L2 test opens a position from an ask, clears the book, and supplies only an adverse TradeTick. The last-trade fallback values the breach, but the empty book has no best bid, so the engine skips the close and leaves the position open.
- Bar-only behaviour depends on execution configuration. With `bar_execution=True` and `BookType.L1_MBP`, the matching engine converts the external LAST bar into synthetic L1 market updates. The bar-close fallback triggers liquidation and the bar-generated synthetic bid executes the close. This is model-generated liquidity, not evidence that a real exchange supplied an executable quote.
- Do not equate a trade-only feed with an empty order book in every configuration. An initial L1 `trade_execution=True` experiment showed trade ticks can populate synthetic L1 bid/ask state and allow a close. The no-book test therefore uses L2, an explicit book clear, and `trade_execution=False` for the adverse trade.
- The mark-precedence test confirms that the 20,000 mark triggers liquidation despite a stale 40,000 quote. The synthetic close then fills against the available 40,000 bid. This separates *trigger valuation* from *close execution price*; the two prices are not interchangeable.
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

Latest branch verification: **27 tests passed** in [GitHub Actions run 43693369153](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43693369153) on the pre-documentation test revision. The final documentation/test assertion revision is rerunning CI before the pull request is opened.

## Still unverified

- Long/short position-side quote selection under a non-zero spread.
- Exchange-specific liquidation thresholds, liquidation price, bankruptcy price, insurance fund, ADL and account recovery.
- Partial fills, queue position, conservative liquidity consumption under multiple competing orders.
- Slippage, spread widening, adverse selection and stop/target same-bar ordering/gap-through.
- Funding with missing mark prices, missing exchange rates, multiple positions and multiple currencies.
- Full canonical event/account replay hashes and restart/recovery semantics.
- Resource benchmarks on the intended free worker.
- Exchange-specific linear/inverse contract multipliers, fees, margin tiers and liquidation rules.

No claim of production suitability, profitability or live-execution parity is made.
