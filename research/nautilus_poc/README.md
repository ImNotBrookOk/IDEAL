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

- **20 tests passed** on the merged `main` branch in GitHub Actions run [43691402915](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43691402915).
- CI commit: `fb13425c7318f9426c78a230231aa6f0a372b1a6`.
- Test command: `python -m pytest -q`.

Coverage:

1. Independent Decimal oracles: linear and inverse long/short PnL, execution fee arithmetic, funding sign convention and invalid-input rejection.
2. Native models: pinned version, linear and inverse `CryptoPerpetual` construction, `FundingRateUpdate` construction and simulated margin venue registration.
3. Order lifecycle: `OrderSubmitted → OrderAccepted → OrderFilled` when simulated market-order acknowledgements are explicitly enabled; one open position; market buy executes at the synthetic best ask.
4. Replay: repeated identical order and funding fixtures produce identical asserted outcomes.
5. Margin: a resting limit order reserves exactly `299.99500000 USDT` initial margin under `StandardMarginModel`; a filled position has exactly `150.00125000 USDT` maintenance margin under the same fixed-percentage model.
6. Funding: positive funding of `0.0001` on `6000.05 USDT` mark notional debits `0.60000500 USDT` at the specified funding boundary. The taker fee is `3.00002500 USDT`; final balance is `9996.39997000 USDT`.
7. Missing boundary: a funding update without `next_funding_ns` and not aligned to its interval does not create a funding payment.

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

- Liquidation thresholds, liquidation price and account recovery.
- Partial fills, queue position, conservative liquidity consumption under multiple competing orders.
- Slippage, spread widening, adverse selection and stop/target same-bar ordering/gap-through.
- Funding with missing mark prices, missing exchange rates, multiple positions and multiple currencies.
- Full canonical event/account replay hashes and restart/recovery semantics.
- Resource benchmarks on the intended free worker.
- Exchange-specific linear/inverse contract multipliers, fees, margin tiers and liquidation rules.

No claim of production suitability, profitability or live-execution parity is made.
