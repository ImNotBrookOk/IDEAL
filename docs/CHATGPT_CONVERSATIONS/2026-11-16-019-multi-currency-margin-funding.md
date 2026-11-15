# IDEAL Conversation Record 019 — Multi-Currency Margin Funding

**Date:** 16 November 2026  
**Scope:** Phase 01 account and funding research — native-currency funding in a multi-currency margin account  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** [PR #25](https://github.com/ImNotBrookOk/IDEAL/pull/25) merged; 79 tests pass on x86_64 and ARM64. Research only.

## Available user-visible transcript

### User
> Ok keep going. Remember we have a lot to do.

### Assistant
> **PR #25 is merged.** The multi-currency funding test now verifies two settlement currencies in one margin account.
>
> | Balance | Funding debit |
> |---|---:|
> | BTC — inverse BTCJPY | 0.00016667 BTC |
> | USDT — linear BTCUSDT | 0.60000000 USDT |
> | USD | Unchanged |
>
> The account uses `base_currency=None` and starts with USD, BTC and USDT balances. Both positions open, both funding debits settle in their native currencies, and no FX conversion instrument is loaded.
>
> - Final PR-head CI: [run 43760817077](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43760817077).
> - x86_64: 79 passed; ARM64: 79 passed.
> - Merge commit: `b1b20de7e0826bb4dbd34741508fea89fea8b298`.
>
> One architectural constraint is now explicit: NautilusTrader reports multi-currency equity as a per-currency map, not a single USD-equity value. IDEAL must preserve native balances and calculate a separate, deterministic reporting-currency risk view. This is a research recommendation, not an approved design decision.

## Operational audit log

### 1. Upstream source research

Inspected NautilusTrader `v2.0.0rc9` source:
- `crates/backtest/src/exchange.rs#L225-L237`: `SimulatedExchange::new` accepts multiple starting currencies when `base_currency=None`; it rejects multiple starting currencies when a base currency is set.
- `crates/backtest/src/exchange.rs#L1626-L1664`: funding adjustments are converted to the account base currency only when one exists. With `base_currency=None`, settlement adjustments remain in their native currency.
- `crates/model/src/accounts/margin.rs#L1757-L1823`: Rust tests document multi-currency margin accounts with no base currency. Margin locking only affects currencies already reported in account balances; the POC pre-seeds BTC and USDT.
- `crates/portfolio/src/portfolio.rs#L836-L894`: `Portfolio::equity` returns a per-currency map.
- `crates/portfolio/src/portfolio.rs#L1003-L1015`: snapshot `base_currency_equity` is only populated when the account has a base currency.

### 2. POC test

Added `research/nautilus_poc/test_multi_currency_funding.py`.

Configuration:
- Simulated Binance venue.
- `AccountType.MARGIN`, `OmsType.HEDGING`, `base_currency=None`.
- Starting balances: 100,000 USD, 2 BTC and 100,000 USDT.
- Inverse BTCJPY perpetual settles in BTC.
- Linear BTCUSDT perpetual settles in USDT.
- Both positions are long and use a positive funding rate of 0.0001.
- A funded run is compared with an otherwise identical no-funding baseline.
- No BTC/USD, USDT/USD or other FX conversion instrument is loaded.
- Fees are zero to isolate funding effects.

Assertions:
- Both baseline and funded runs open two positions and record two fills.
- BTC balance difference is exactly **0.00016667 BTC**.
- USDT balance difference is exactly **0.60000000 USDT**.
- USD balance is exactly unchanged at **100,000 USD**.
- The account has no base currency.

### 3. Interpretation and architectural implication

This confirms native-currency funding settlement in the pinned simulator's multi-currency margin mode. It does not prove exchange-specific unified margin parity.

For IDEAL, retain native-currency account balances, funding and fees in the canonical ledger. Portfolio-level risk controls still require a deterministic reporting-currency view based on timestamped, side-aware FX marks, with explicit freshness, missing-rate and conversion-failure handling. Never add unlike currency amounts directly or assume a multi-currency account has a single USD equity value.

This is a research recommendation only. It does not change project decisions or authorize implementation.

Not tested by this PR:
- Cross-currency collateral offsets or haircuts.
- Venue-specific margin tiers, liquidation and ADL.
- Portfolio risk aggregation under stale or missing FX marks.
- Exchange parity for Bybit UTA, Binance Portfolio Margin or OKX account modes.

### 4. Final verification

Final PR-head CI [run 43760817077](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43760817077):
- Exact `nautilus_trader==2.0.0rc9`.
- Ubuntu 24.04 / Python 3.14.10.
- x86_64: **79 passed in 0.36s**.
- ARM64: **79 passed in 0.53s**.

### 5. Five-axis review

- **Correctness:** funded vs no-funding baseline; exact BTC and USDT deltas; unchanged USD; two fills and two open positions.
- **Security:** no credentials, exchange connectivity or external data.
- **Cost:** no dependencies or paid services; GitHub-hosted CI only.
- **Maintainability:** one isolated research test file; deterministic fixtures; no production abstractions added.
- **Scope:** test plus roadmap and research documentation. No runtime, risk, execution or permission changes.

### 6. Merge and read-back

- PR: [#25 — Test multi-currency margin funding settlement](https://github.com/ImNotBrookOk/IDEAL/pull/25).
- Final PR head: `62b6678533e1dc7b4008743a9d45b1e633064660`.
- Final PR-head CI: [43760817077](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43760817077), both architectures green.
- Squash merge succeeded under D-012.
- Merge commit: `b1b20de7e0826bb4dbd34741508fea89fea8b298`.
- PR closed/merged and main ref read back at the merge commit.
- Read back and verified `ROADMAP.md`, `research/nautilus_poc/README.md`, `research/nautilus_poc/execution_realism_matrix.md` and `research/nautilus_poc/test_multi_currency_funding.py`.

## Current state and remaining work

- Phase 01: IN PROGRESS.
- Phase 02 and implementation phases: LOCKED.
- Isolated POC: **79 passing tests on x86_64 and ARM64**.
- Native-currency funding in a multi-currency margin account is verified in the simulator.
- Same-engine reset after cache-purged FX instrument remains unsupported by the current Python POC; fresh-engine reconstruction with restored definitions/data is the verified workaround.
- Multi-currency equity aggregation, reporting-currency FX freshness, cross-currency collateral, margin and liquidation remain open.
- Empirical market-impact calibration remains blocked on venue selection and representative historical L2/trade/fill data.
- Venue-specific queue priority, cancel/amend behavior and liquidation parity remain blocked on venue selection.
- SQLite journal runtime integration, external signed hash anchoring, encrypted backup/restore, retention/compaction, and worker capacity remain open; runtime integration and paid provisioning are not authorised.
- No exchange, account, credentials, testnet, paper/live trading or paid service introduced.
- Next research task: test how multi-currency portfolio equity and margin reporting behave under missing/stale FX rates, and define the deterministic reporting-currency valuation boundary without implementing runtime code.
