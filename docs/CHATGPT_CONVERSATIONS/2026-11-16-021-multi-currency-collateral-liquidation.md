# IDEAL Conversation Record 021 — Multi-Currency Collateral and Liquidation Boundary

**Date:** 16 November 2026  
**Scope:** Continue Phase 01 engine research; inspect the exact NautilusTrader 2.0.0rc9 multi-currency account, portfolio equity and simulated liquidation paths; add a deterministic POC test; verify x86_64 and ARM64 CI; merge the research PR; synchronize roadmap and audits.  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Branch:** `main`  
**Status:** Research gate completed for the tested simulator boundary. Phase 01 remains IN PROGRESS; Phase 02 remains LOCKED; no runtime integration or engine adoption authorized.

## Available user-visible transcript

### User
> Yes lets keep building

### Assistant
We'll continue with the existing IDEAL project and preserve the roadmap, decision register and audit requirements.

**One important boundary:** We have approval to continue Phase 01 research, but not yet to integrate NautilusTrader into the actual IDEAL runtime. We can continue building and testing the isolated engine proof of concept without crossing that boundary.

The next target is multi-currency collateral and liquidation. This is one of the remaining gaps that could materially affect the engine-selection decision.

### Assistant
## New collateral test — first result

The first CI run has already exposed an important limitation.

80 passed · 1 assertion failed.

The simulated account held 2 BTC plus 1,000 USDT. It opened a 0.1 BTCUSDT long, then experienced an adverse price move.

Despite the substantial BTC balance, NautilusTrader triggered liquidation against the USDT-settled position.

The actual settlement was:

- Entry: 60,000 USDT
- Liquidation fill: 49,999.5 USDT
- Realised loss: 1,000.05 USDT
- Remaining BTC: 2 BTC
- Remaining USDT: -0.05 USDT

The test's expected USDT balance was incorrectly set to zero. The engine's actual result is more informative: it permits a small negative residual after the synthetic liquidation close.

### Assistant
81 / 81 passed on both architectures.

The corrected test now passes:

| CI verification | Result |
|---|---:|
| x86_64 | 81 passed |
| ARM64 | 81 passed |
| Deterministic replay | Passed |
| Engine version check | Passed |
| SQLite benchmark step | Passed |

Verified in [CI run 43761762953](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43761762953).

This establishes a concrete simulator limitation: the tested liquidation model does not pool BTC collateral to protect a USDT-settled position. It evaluates maintenance equity in the position's settlement currency.

## Operational audit log

### 1. Governance and repository inspection

- Read the installed test-driven-development skill and followed its test-first / evidence-driven workflow.
- Re-read `ROADMAP.md`, `DECISIONS.md`, `RULES.md`, `research/nautilus_poc/README.md`, `research/nautilus_poc/execution_realism_matrix.md`, `docs/INFRASTRUCTURE_RESEARCH.md` and the conversation audit index.
- Confirmed D-012 authorizes Phase 01 research PRs with green CI, five-axis review, scope verification and unchanged-head confirmation. It does not authorize runtime integration, account access, paper/live orders, risk changes or paid services.
- Confirmed Phase 01 is IN PROGRESS and Phase 02 is LOCKED. No production implementation was started.
- A local clone attempt could not resolve `github.com` in the container environment; remote GitHub Actions CI was therefore used for executable test verification.

### 2. Exact upstream source inspection

Inspected the exact upstream tag `v2.0.0rc9`, not a moving development branch:

- `crates/backtest/src/exchange.rs`, lines 2020–2088: the simulated liquidation path buckets positions by `settlement_currency`; for each account currency it adds only unrealized PnL for positions in that same currency to that currency's balance, compares against maintenance margin in that currency, then performs currency-scoped liquidation.
- `crates/portfolio/src/portfolio.rs`, lines 851–900: portfolio equity starts with account balances and accumulates margin equity into a per-currency map.
- `crates/portfolio/src/portfolio.rs`, lines 1347–1405: margin equity is accumulated per position/currency; the no-base-currency account does not receive a single converted reporting-currency total.
- `crates/model/src/accounts/margin.rs`, lines 455–500: margin locking and balance recalculation are performed within the requested currency.
- `docs/concepts/accounting.md`, lines 257–271: the model can represent account-wide margin entries keyed by collateral currency. This is a venue-reported margin representation, not evidence that the simulated liquidation path applies cross-currency collateral conversion or haircuts.

Source links:
- [Pinned simulated exchange liquidation path](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/backtest/src/exchange.rs#L2020-L2088)
- [Pinned portfolio equity](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/portfolio/src/portfolio.rs#L851-L900)
- [Pinned margin equity accumulation](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/portfolio/src/portfolio.rs#L1347-L1405)
- [Pinned margin-account currency locking](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/model/src/accounts/margin.rs#L455-L500)
- [Pinned account-wide margin representation](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/docs/concepts/accounting.md#L257-L271)

### 3. POC test and initial failure

- Created branch `research/multi-currency-collateral-liquidation` from the current `main`.
- Added `research/nautilus_poc/test_multi_currency_collateral_liquidation.py`.
- Fixture: `base_currency=None`, starting balances 2 BTC and 1,000 USDT, one 0.1 BTCUSDT long entered at the 60,000 ask, followed by a 49,999.5 bid.
- Initial PR-head CI [run 43761714468](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43761714468) completed both x86_64 and ARM64 test jobs with 80 passed and one assertion failure. The test incorrectly expected zero USDT.
- Inspected the actual job log. It recorded a liquidation trigger with USDT equity -0.05 versus 15.00 USDT maintenance, a synthetic close at 49,999.5, realised PnL -1,000.05 USDT and final USDT balance -0.05. BTC remained 2.
- Corrected the test to assert the observed exact -0.05 USDT residual and documented the half-tick bid difference. No engine implementation or runtime code was modified.

### 4. Final CI verification

- Final PR-head CI [run 43761762953](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43761762953):
  - x86_64: **81 passed in 0.43s**.
  - ARM64: **81 passed in 0.68s**.
  - Exact `nautilus_trader==2.0.0rc9` version check passed on both.
  - SQLite event-journal benchmark step passed on both.
- Both jobs completed successfully.
- This is synthetic POC verification. It does not establish live exchange collateral eligibility, haircuts, account-wide margin offsets, venue liquidation priority, bankruptcy-price takeover, insurance-fund or ADL behavior.

### 5. Review and merge

Five-axis review of PR #26:
1. **Correctness:** exact test outcome and replay are asserted; both architectures pass.
2. **Scope:** one isolated research test file only; no runtime integration or dependency changes.
3. **Security:** no secrets, credentials, accounts, external exchange connections or live orders.
4. **Maintainability:** self-contained fixture and descriptive assertions; no new dependencies.
5. **Cost:** public-repository GitHub Actions research CI only; no paid service or infrastructure provisioned.

- PR [#26](https://github.com/ImNotBrookOk/IDEAL/pull/26) changed only `research/nautilus_poc/test_multi_currency_collateral_liquidation.py`.
- Verified the PR head remained `c5d0cc222f84d2bfb2d15c737d74f1beb8bd058b`, matching the successful CI run; `main` had not advanced from the PR base before merge.
- Squash-merged under D-012.
- Merge commit: [b440d3815b296ee62ce21dd7f55d929b8600e011](https://github.com/ImNotBrookOk/IDEAL/commit/b440d3815b296ee62ce21dd7f55d929b8600e011).

### 6. Documentation and roadmap synchronization

Updated and committed:
- `ROADMAP.md`: records the collateral/liquidation result and keeps Phase 01 open for actual venue rules, FX aggregation and haircuts. Commit [44c8544](https://github.com/ImNotBrookOk/IDEAL/commit/44c8544108e4b3bde490a59a0d51ed1363899a02).
- `research/nautilus_poc/README.md`: latest suite now 81 tests; records the cross-currency collateral/liquidation test and its limits. Commit [47af285](https://github.com/ImNotBrookOk/IDEAL/commit/47af28537cd51fbca2ac4bbd04255c1ed01c9052).
- `docs/INFRASTRUCTURE_RESEARCH.md`: synchronized the latest 81-test x86_64/ARM64 verification. Commit [2978d13](https://github.com/ImNotBrookOk/IDEAL/commit/2978d132e37ddad9f0258f27d687e3e331c0a2a6).
- `research/nautilus_poc/execution_realism_matrix.md`: added exact pinned-source analysis, test evidence and IDEAL implications. Commit [bee25f5](https://github.com/ImNotBrookOk/IDEAL/commit/bee25f5d578f650590e0b1d26b8acaa1fee930a4).

Historical conversation records 019 and 020 remain unchanged under the append-only audit policy.

### 7. Finding and approval boundary

**Verified finding:** this pinned NautilusTrader simulated liquidation path checks each position's settlement currency independently. In the tested account, BTC collateral did not offset USDT-settled maintenance equity. The engine closed the position and left a -0.05 USDT residual after synthetic execution.

**Not established:** how any live venue treats multi-asset collateral, conversion rates, haircuts, concentration limits, cross-margin maintenance, liquidation ordering, bankruptcy price, insurance fund or ADL. The account-wide margin data model can represent per-collateral-currency reported margin; it is not the same as proving simulated cross-collateral liquidation.

**IDEAL implication (proposal, not a new owner decision):** preserve native currency balances and build deterministic reporting-currency valuation plus venue-specific collateral/risk rules if the selected venue uses unified multi-asset margin. Require current, side-aware conversion data and fail closed on missing/stale inputs.

**Current state:** Phase 01 remains IN PROGRESS; Phase 02 remains LOCKED; NautilusTrader remains an unapproved engine candidate; no runtime integration, exchange account, paper order, live order, risk change, cloud resource or paid service was created.

**Single next task:** continue the Phase 01 multi-currency account research with a deterministic POC for reporting-currency equity conversion, FX freshness and missing-rate failure handling. Then continue the remaining Phase 01 blockers in roadmap order.

**Owner approval:** still required before Phase 02 and runtime implementation under D-012.
