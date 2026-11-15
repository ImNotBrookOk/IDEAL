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

- **22 tests passed** on the liquidation research branch in GitHub Actions run [43691805092](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43691805092); the tested change was subsequently squash-merged to `main`.
- Merged commit: [`9a5ee8488bedf762999ca03c4969771c1e803157`](https://github.com/ImNotBrookOk/IDEAL/commit/9a5ee8488bedf762999ca03c4969771c1e803157).
- Test command: `python -m pytest -q`.

Coverage:

1. Independent Decimal oracles: linear and inverse long/short PnL, execution fee arithmetic, funding sign convention and invalid-input rejection.
2. Native models: pinned version, linear and inverse `CryptoPerpetual` construction, `FundingRateUpdate` construction and simulated margin venue registration.
3. Order lifecycle: `OrderSubmitted → OrderAccepted → OrderFilled` when simulated market-order acknowledgements are explicitly enabled; one open position; market buy executes at the synthetic best ask.
4. Replay: repeated identical order and funding fixtures produce identical asserted outcomes.
5. Margin: a resting limit order reserves exactly `299.99500000 USDT` initial margin under `StandardMarginModel`; a filled position has exactly `150.00125000 USDT` maintenance margin under the same fixed-percentage model.
6. Funding: positive funding of `0.0001` on `6000.05 USDT` mark notional debits `0.60000500 USDT` at the specified funding boundary. The taker fee is `3.00002500 USDT`; final balance is `9996.39997000 USDT`.
7. Missing boundary: a funding update without `next_funding_ns` and not aligned to its interval does not create a funding payment.
8. Liquidation: a quote-driven inverse BTCUSD maintenance-margin breach closes the position; replay is deterministic. The 40,000 → 20,000 gap fixture leaves a negative account balance, and bar/trade liquidation remains a known engine limitation.

## Liquidation POC findings (2.0.0rc9)

- A synthetic inverse BTCUSD position opened from quote ticks is closed when the next quote creates a maintenance-margin breach with `liquidation_enabled=True` and `liquidation_trigger_ratio=1.0`.
- The deterministic fixture closes one position and leaves the account at **-249.56250000 BTC** after a 40,000 → 20,000 quote gap. This is a critical limitation: the simulated close occurs at the observed quote and can produce a deeply negative balance. It does not model a guaranteed bankruptcy-price cap, insurance-fund recovery or ADL protection in this scenario.
- Liquidation tests must currently be quote-driven. NautilusTrader issue [#5453](https://github.com/nautechsystems/nautilus_trader/issues/5453) documents that the liquidation check in the evaluated code path calculates unrealised PnL from cached quotes; bar-only, trade-only and bar-plus-mark-price inputs can leave a breached position open. This limitation must be retested against any later engine pin before considering adoption.
- The synthetic liquidation fill is not a realistic exchange liquidation model. Exchange-specific liquidation fees, partial liquidation, bankruptcy price, insurance fund, ADL and recovery remain unverified.

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

## Still unverified

- Exchange-specific liquidation thresholds, liquidation price, bankruptcy price, insurance fund, ADL and account recovery.
- Partial fills, queue position, conservative liquidity consumption under multiple competing orders.
- Slippage, spread widening, adverse selection and stop/target same-bar ordering/gap-through.
- Funding with missing mark prices, missing exchange rates, multiple positions and multiple currencies.
- Full canonical event/account replay hashes and restart/recovery semantics.
- Resource benchmarks on the intended free worker.
- Exchange-specific linear/inverse contract multipliers, fees, margin tiers and liquidation rules.

No claim of production suitability, profitability or live-execution parity is made.
