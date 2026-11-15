# NautilusTrader isolated proof-of-concept

**Status:** research experiment only; not an adopted IDEAL dependency.

## Scope and safety

- Exact engine pin: `nautilus_trader==2.0.0rc9`.
- Python: 3.14; Linux x86_64 GitHub Actions runner.
- Synthetic fixtures only. No exchange adapter, credentials, network market data, paper/live orders or persistent service.
- The release is a pre-release candidate. It is not approved for production or real-money trading.
- This directory is not imported by the IDEAL application and must not become a runtime dependency without a separate architecture decision.

## First experiment

The initial test set independently checks linear/inverse contract PnL, fees and funding arithmetic, then smoke-tests the pinned NautilusTrader package, crypto-perpetual instrument model, funding event model and backtest venue construction.

The engine's own backtest funding settlement, margin/liquidation, order lifecycle, fill realism and replay determinism are separate acceptance tests. A constructor smoke test is not proof of those behaviours.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

CI runs the same test command on GitHub-hosted Linux runners. No paid service or secret is used.

## Known limitations

- Synthetic calculations validate our expected-value fixtures, not exchange-specific contract rules.
- Linear and inverse formulas must be matched to the eventual venue's contract multiplier, settlement currency and quantity convention.
- Funding sign convention in the independent oracle: positive rate means longs pay shorts.
- Fee calculation assumes notional times rate; maker/taker classification and fee currency are not inferred.
- No claim of production suitability, profitability or live-execution parity is made.
