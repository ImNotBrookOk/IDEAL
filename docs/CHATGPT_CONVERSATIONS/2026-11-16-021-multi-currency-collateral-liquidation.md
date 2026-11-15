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

## Addendum — verbatim transcript completion

The final assistant partial message in this conversation is reproduced below verbatim to preserve the append-only audit requirement:

> 81 / 81 passed on both architectures
>
> The corrected test now passes:
>
> | CI verification | Result |
> |---|---:|
> | x86_64 | 81 passed |
> | ARM64 | 81 passed |
> | Deterministic replay | Passed |
> | Engine version check | Passed |
> | SQLite benchmark step | Passed |
>
> Verified in [CI run 43761762953](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43761762953).
>
> This establishes a concrete simulator limitation: **the tested liquidation model does not pool BTC collateral to protect a USDT-settled position.** It evaluates maintenance equity in the position's settlement currency.

## Continuation — reporting-currency FX freshness

This work continues the same user request recorded above; no new user message was issued between the two research gates.

### Verbatim user-visible assistant update

> ## Next research gate — reporting-currency conversion
>
> We have also completed the next test rather than stopping at liquidation.
>
> 84 / 84 passed on both architectures
>
> [CI run 43762099188](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43762099188)
>
> The tests establish three behaviours:
>
> 1. Native BTC and USDT equity remains separated in a multi-currency account.
> 2. Explicit USDT-to-USD PnL conversion uses the latest available FX midpoint.
> 3. If the FX instrument disappears, an explicit USD valuation fails closed, even when an older conversion rate was cached.
>
> The key distinction is that NautilusTrader can convert PnL, but its native equity output still does not provide a consolidated reporting-currency account total for this no-base-currency configuration.

### 8. Reporting-currency POC test

- Added `research/nautilus_poc/test_reporting_currency_fx_freshness.py` on branch `research/reporting-currency-fx-freshness`.
- Fixture: no-base-currency margin account with 2 BTC and 1,000 USDT; open 0.1 BTCUSDT long from 60,000 to a 61,000 bid; USDT/USD mid updates from 1.00000 to 0.90000.
- Verified `Portfolio.equity()` returns a native map containing 2 BTC and 1,100 USDT, without a USD total.
- Verified `Portfolio.unrealized_pnls(target_currency=USD)` converts +100 USDT PnL using the latest 0.90000 mid and returns 90.00 USD.
- Verified explicit USD queries fail closed after the USDT/USD instrument is purged despite a previously cached rate, and also fail when no FX rate ever existed.
- Inspected exact v2.0.0rc9 source: `Portfolio.equity()` has no target-currency argument; explicit PnL conversion uses a current mark xrate when configured, otherwise/fallback to current MID; the explicit target-currency path disables stale-xrate fallback.

### 9. CI and merge

- Final PR-head CI [run 43762099188](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43762099188):
  - x86_64: **84 passed in 0.40s**.
  - ARM64: **84 passed in 0.61s**.
  - Exact engine version check and SQLite benchmark step passed on both.
- Five-axis review:
  1. Correctness: native equity, latest FX midpoint, missing-rate and purged/stale-rate assertions; both architectures green.
  2. Scope: one isolated research test file only.
  3. Security: no secrets, credentials, exchange accounts, or network exchange calls.
  4. Maintainability: self-contained fixture, no new dependencies.
  5. Cost: public GitHub Actions runners only.
- PR [#27](https://github.com/ImNotBrookOk/IDEAL/pull/27) changed only `research/nautilus_poc/test_reporting_currency_fx_freshness.py`.
- Confirmed PR base remained `35c3d894970afce171b09afe1b58cb2b6b3ff520`, head remained `4c9ea69d76410152755e6f5b86b7c25a40217827`, and both matched the successful CI state before squash merge.
- Squash-merged PR #27 as [66be9a121541a4e740bbfd1d2845a47ce050e5e3](https://github.com/ImNotBrookOk/IDEAL/commit/66be9a121541a4e740bbfd1d2845a47ce050e5e3).

### 10. Documentation synchronization

- `ROADMAP.md`: records the 84-test reporting-currency finding and leaves IDEAL-owned total-equity aggregation open. Commit [285df57](https://github.com/ImNotBrookOk/IDEAL/commit/285df57a75b5241ea16dbbed79a199c2287728e6).
- `research/nautilus_poc/README.md`: latest suite updated to 84 tests; records FX freshness and missing-rate limits. Commit [74a6e77](https://github.com/ImNotBrookOk/IDEAL/commit/74a6e77deaca19d832d2d41749433566d53dd42f).
- `docs/INFRASTRUCTURE_RESEARCH.md`: latest POC verification updated to 84 tests. Commit [7c372bf](https://github.com/ImNotBrookOk/IDEAL/commit/7c372bf685d2b3d4929fb7340538a9acbf8f0877).
- `research/nautilus_poc/execution_realism_matrix.md`: section 17 added with source links, test evidence and IDEAL implications. Commit [b9ad0c9](https://github.com/ImNotBrookOk/IDEAL/commit/b9ad0c9334e3189708c8bcd92c5a71ade5a89888).

### 11. Updated finding and next roadmap gate

**Verified:** the engine's native equity remains a per-currency map for a no-base-currency account. Explicit PnL queries can convert to a requested target currency using current FX data and fail closed when the current conversion is unavailable. They do not convert every native cash balance into a single consolidated equity scalar.

**IDEAL requirement:** build a deterministic reporting-equity aggregator that converts each native balance, liability, PnL and fee into a selected reporting currency; define conservative conversion direction (bid/ask), mark policy, FX path, timestamp freshness, missing/stale-rate failure and collateral haircuts. This is an architectural requirement/proposal, not an approved runtime implementation.

**Current state:** Phase 01 remains IN PROGRESS; Phase 02 remains LOCKED; NautilusTrader remains an unapproved engine candidate; no runtime integration, account access, paper/live orders, risk changes, cloud resources or paid services were created.

**Next task in roadmap order:** begin the venue and historical-data shortlist. Verify official jurisdiction/product/account-mode eligibility and API/data availability; do not select or connect a venue without owner approval. Then obtain representative L2/trade/fill data for empirical market-impact calibration.

## Continuation — venue and historical-data shortlist

This work continues the same user instruction to keep building. The roadmap's next Phase 01 blocker is venue selection plus representative historical L2/trade/fill data. Prior project constraints remain exchange-neutral research, public unauthenticated data only, no credentials, and no venue selected. No account or API key was created.

### 12. Preliminary shortlist document

Created [`docs/EXCHANGE_AND_DATA_SHORTLIST.md`](../EXCHANGE_AND_DATA_SHORTLIST.md) and linked it from `ROADMAP.md`. The document compares Binance USDⓈ-M/COIN-M, Bybit linear/inverse, OKX swaps/futures and Hyperliquid on live public market data, historical L2, trade/funding/OI/liquidation coverage, vendor alternatives, data-quality issues, cost and NZ product eligibility.

### 13. Verified source findings

- [Binance Public Data repository](https://github.com/binance/binance-public-data): public Futures archives document trades, aggregate trades and klines; no general historical L2 archive is documented there.
- [Binance Futures orderbook history endpoint](https://developers.binance.com/docs/derivatives/futures-data/market-data/Get-Future-TickLevel-Orderbook-Historical-Data-Download-Link): `GET /sapi/v1/futures/histDataLink` is a signed USER_DATA path. Current endpoint material indicates VIP gating, request windows shorter than seven days, and no new historical data after 2024-11-01.
- [Bybit V5 orderbook endpoint](https://bybit-exchange.github.io/docs/v5/market/orderbook): public contract snapshots support up to 1,000 levels; response includes update ID `u`, cross sequence `seq` and matching-engine timestamp `cts`; RPI orders are not included.
- [OKX historical data portal](https://www.okx.com/historical-data): advertises tick trades from September 2021, perpetual funding from March 2022 and high-resolution L2 from March 2023.
- [OKX API changelog](https://www.okx.com/docs-v5/log_en/): checksum deprecation from 23 June 2026 means consumers must validate orderbook continuity using `seqId/prevSeqId`; higher-frequency 400-depth `books-l2-tbt` requires VIP5 and 50-depth `books50-l2-tbt` requires VIP4, while standard `books` remains public.
- [Hyperliquid Info API](https://hyperliquid.gitbook.io/Hyperliquid-docs/for-developers/api/info-endpoint): `l2Book` is capped at 20 levels per side; candle snapshots are capped at 5,000; `userFillsByTime` is account-specific and only the 10,000 most recent fills are available.
- [Tardis data types](https://docs.tardis.dev/faq/data): normalized tick-level trades, incremental L2, top-25/top-5 snapshots, quotes, derivative tickers and liquidations; raw API is Pro/Business.
- [Tardis downloadable CSV documentation](https://docs.tardis.dev/downloadable-csv-files): first-day-of-month CSV samples are available without an API key; daily datasets are gzip files ordered by local receive timestamp.
- [Tardis historical data details](https://docs.tardis.dev/historical-data-details): initial snapshots at 00:00 UTC and reconnects; reconnect gaps are documented at approximately 300–3,000 ms depending on venue.
- [FMA derivatives issuer guidance](https://www.fma.govt.nz/business/services/derivatives-issuers/): a derivatives issuer making a regulated offer of derivatives must be licensed; the FMA definition includes futures, swaps, CFDs, margin contracts and rolling spot contracts. Applicability to a specific offshore platform/user arrangement is not decided here.
- [Binance licences and registrations](https://www.binance.com/en/about-legal/licenses): Binance states the NZ local entity's services and explicitly says it is not licensed by a NZ regulator; the listed local services do not establish Futures eligibility.
- [Bybit NZ addendum](https://www.bybit.com/en/help-center/article/Addendum-to-Terms-of-Service-New-Zealand-Users): NZ users may access only the changing NZ Supported Services list; the addendum does not itself confirm perpetual futures availability.

### 14. Preliminary disposition

- No venue selected. OKX is currently the strongest **historical-data access candidate** because its official portal advertises high-resolution L2 downloads from March 2023, but download format, depth, access conditions, price and NZ product eligibility remain unverified.
- Binance remains useful for public live feeds and free historical trades/aggTrades/klines, but its official public archive does not close the L2 gap.
- Bybit exposes useful public live orderbook data, but a native historical L2 archive was not verified and NZ services are product-restricted.
- Hyperliquid's 20-level L2 snapshot limit and lack of a verified public historical delta tape make it a weaker fit for queue-sensitive execution calibration.
- Tardis offers a no-key monthly sample path but no free full-history entitlement was established; full raw replay is a paid tier.
- L2 is not L3. Do not claim true queue-position/fill-probability modelling from market-by-price data alone.

### 15. Sample retrieval limitation

The docs confirm a Tardis first-of-month CSV sample path, including a documented `binance-futures` dataset family. The current execution container could not resolve the external dataset host, so no binary sample was downloaded or parsed. This is an environment/network limitation, not evidence that the vendor endpoint is unavailable. No sample-quality assessment is claimed.

### 16. Roadmap and audit state

- `ROADMAP.md` now records the preliminary venue/data shortlist and changes the next task to validate a free historical L2 sample and produce a data-quality report before venue selection.
- New document: `docs/EXCHANGE_AND_DATA_SHORTLIST.md`.
- No trading venue, account mode, derivatives product, vendor subscription or API key approved.
- No account access, exchange connection, paper/live order, paid data purchase or runtime implementation occurred.
- Phase 01 remains IN PROGRESS; Phase 02 remains LOCKED.

**Next task:** validate a no-cost historical L2 sample end-to-end (Tardis first-of-month CSV and/or OKX historical download) and produce a machine-readable quality report. Only after that should the owner decide whether a venue/product/account-mode shortlist is sufficiently grounded for approval.
