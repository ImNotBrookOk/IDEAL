# IDEAL Conversation Audit 023 — Decision-Quality Execution Priority

**Date:** 16 November 2026  
**Project:** IDEAL  
**Phase:** 01 — Open-source and infrastructure research (IN PROGRESS)  
**Transcript status:** Complete for the user-visible messages in this conversation.  
**Approval status:** The owner authorised continuation of the existing Phase 01 research scope and explicitly set execution-quality priorities. No Phase 02 or implementation approval was given.

## 1. User-visible transcript

**User:**
> To be honest we arent here to be the fastest to place an order. We are here to build a platform that is the smartest in placing an order regardless of the ms we miss. In the long scheme of things a few ms missed is nothing compared to having a correctly functioning profitable system. So keep going

**Assistant:**
> Agreed. We should optimise for **decision quality, execution correctness and durable profitability**, not minimum order-placement latency.
>
> That changes how we evaluate the engine. We do not need to win a race to the exchange. We need to understand the market correctly, identify when an order is justified, choose the right order type and price, size it within risk limits, and verify that the resulting execution behaves as expected.
>
> A few milliseconds of additional processing are acceptable when they buy materially better decisions. They are not acceptable if they introduce stale data, hidden look-ahead, uncontrolled risk or unreliable execution.
>
> I’ll treat this as an explicit engineering priority and use it to judge architecture, data requirements, tests and engine candidates. It does **not** mean ignoring latency entirely: we still need bounded processing times and predictable behaviour, but latency is a constraint rather than the primary objective.

**User:**
> Ok it sounds like you have it all figured out. I trust you know what to do. And by this i mean continue all the test until we get the results we are looking for. If multiple test can be done in one test then do so to cut time and save time. If not then do what is best. Do not move on to the next phase until you are satisfied with all the evidence we need to implement the engine and customize to our liking.

**Assistant:**
> I’ve widened the data-source investigation rather than repeatedly retrying the same blocked download route.
>
> **A stronger candidate has emerged: OKX’s official historical-market-data service.** Its public API documentation describes a batch historical-data endpoint covering order-book data at 50, 400 and 5,000 levels, with daily and monthly aggregation. OKX also advertises historical L2 from March 2023. This is more promising than relying on an ambiguously identified community dataset, but I have not yet verified the actual download permissions, file schema or successful retrieval.
>
> There is an important distinction: OKX’s 10 ms incremental live channels have VIP-tier restrictions, while its standard `books` channel is 100 ms. Historical download availability must be evaluated separately from live-channel entitlements.

## 2. Owner decisions recorded

1. Decision quality, execution correctness and risk-adjusted net outcome take priority over minimum order-placement latency.
2. Latency remains a measured and bounded operational constraint; it is not the primary optimisation target.
3. Continue Phase 01 research and tests. Do not progress to Phase 02 or implementation until the required evidence is complete and the owner approves the next phase.
4. Batch compatible tests where doing so preserves diagnostic value; otherwise keep tests isolated enough to identify failure causes.
5. No order execution, account connection, paid infrastructure or risk-control changes are authorised.

Decision register update: **D-013 accepted** in `DECISIONS.md`.

## 3. Research performed

### 3.1 Execution quality objective

Created `docs/EXECUTION_QUALITY_RESEARCH.md`. It defines a decision-quality-first objective based on expected gross strategy value captured minus fees, spread, market impact, adverse selection, opportunity cost and inventory/operational risk, subject to deterministic risk and data-quality constraints.

The document separates:
- trade intent;
- market-quality gating;
- pre-trade economics;
- scheduling (when/how much);
- placement (where/how);
- deterministic OMS and risk validation;
- reconciliation and transaction-cost analysis;
- bounded learning from measured outcomes.

It identifies immediate IOC, passive/post-only, TWAP, VWAP, POV, adaptive catch-up and Almgren–Chriss scheduling as candidate baselines/research methods. GLFT/Avellaneda–Stoikov are retained as specialist placement/market-making references, not presumed default entry/exit strategies.

### 3.2 Open-source repository screening

- `eshaan2418/sorx` (MIT): reviewed README, OMS design, microstructure notes, Go module and CI workflow. Useful property/fuzz-tested OMS invariants, fixed-point accounting, deterministic replay, latency-at-arrival simulation and parent-level paired TCA. Its capture is spot BTC-USD/ETH-USD, not perpetuals; 40 minutes and 154 parent orders; reported consolidated best bid/ask crossed in all 2,374 one-second samples; fees and latency are assumptions; no passive queue or full market-impact model. Reference only.
- `moussoulijane/execution-cost-analytics` (MIT): reviewed README, licence and initial commit dated 16 October 2026. Useful causal VWAP/POV/adaptive comparisons, path-level paired inference, bootstrap uncertainty and explicit negative/inconclusive results. It acknowledges that OHLCV/trade data do not identify causal market impact; not a calibrated perps model.
- `AshJha0/electronic-trading` (MIT): reviewed README, licence and release 2.0.1 commit dated 31 October 2026. Useful Almgren–Chriss, Avellaneda–Stoikov/GLFT, impact/markout and cross-language golden-test ideas. Equity examples and illustrative parameters are not directly transferable to crypto perpetuals.
- Existing NautilusTrader and HftBacktest candidate boundaries remain unchanged. No new engine or dependency was selected.

### 3.3 Methodological conclusions

- Execution cost alone is not the objective: alpha decay and opportunity cost can make a more aggressive order rational.
- Fastest order entry is not evidence of better execution; compare policies using matched parent intents and market paths.
- Scheduling and placement must be evaluated separately and together.
- No passive fill/queue model should claim exact queue position from L2 market-by-price alone.
- Adaptive/learned policies must beat deterministic baselines out of sample, with uncertainty bounds and regime coverage.
- No order is valid when data quality, expected net value or risk state is inadequate.

## 4. Repository changes

Commits made sequentially on `main`:

| File | Commit |
|---|---|
| `docs/EXECUTION_QUALITY_RESEARCH.md` | `7c6117f45803cec8f906da2684300ec24e7ee5b7` |
| `DECISIONS.md` (D-013) | `a22889d4066dfef6ff96ab416c1aab2fc50ca94b` |
| `REQUIREMENTS.md` (execution quality objective) | `aeefd71170a48138c5635f20a5bd1c771d8ef332` |
| `ROADMAP.md` (Phase 01 research state) | `e9f3d5ccdbcebf409ea683fdccc576630fa43665` |
| `docs/EXCHANGE_AND_DATA_SHORTLIST.md` | `8e25b7ee5c87490c10bd18dc48fae0a6d3c413cb` |
| `docs/CHATGPT_CONVERSATIONS/README.md` (this record indexed) | `833045eb406eed1a3ae1475a6f138a5e0ee6982b` |

A malformed literal newline escape in the existing ROADMAP remaining-work entry was corrected as part of the roadmap update.

## 5. Test and audit status

- No source code, executable logic or dependency changed.
- No unit, integration, regression or CI tests were run in this documentation/research update; no code-test pass is claimed.
- Repository read-back verification is required after the audit record is committed.
- The historical L2 sample acceptance gate remains BLOCKED because actual perpetual L2 and paired trade bytes have not been retrieved and independently validated.
- No venue or execution policy has been selected.

## 6. Current state and next step

Phase 01 remains IN PROGRESS. Phase 02 remains LOCKED. The next technical gate is still actual-file historical perpetual L2/trade retrieval and independent reconstruction. Only after that gate passes should the replay harness and matched-parent execution-policy comparisons proceed. Continue in roadmap order; do not weaken acceptance criteria to force progress.

No owner approval is pending for continued Phase 01 research under D-012. Explicit owner approval is still required before Phase 02, runtime implementation/integration, account access, paper/live execution, risk changes or paid infrastructure.


## 7. Publication and read-back verification

The audit record was committed as `ba85d3caf072a94dbd851d11b01229c8442c8462`. All seven project files were fetched again from `main`; content checks passed for the research report, D-013, REQUIREMENTS execution objective, ROADMAP Phase 01/Phase 02 gate, shortlist, audit record and index entry. Read-back blob SHAs:
- `docs/EXECUTION_QUALITY_RESEARCH.md`: `a1c9a3a583d650e3f071f58f670b4a1e9d68f23b`.
- `DECISIONS.md`: `f0e260e04bccd2b6a26b962a691bf93c45223afb`.
- `REQUIREMENTS.md`: `aa3f53bba7b50945653df7f687477e6c83954462`.
- `ROADMAP.md`: `301b24ad651d84ece8acf104c48824eb4527f044`.
- `docs/EXCHANGE_AND_DATA_SHORTLIST.md`: `faf39ccc03e10d871086ac031ee120b8e009b753`.
- This audit record: `c7e9d75a9775bcb9398c97ebca52bb358bb1f5df`.
- `docs/CHATGPT_CONVERSATIONS/README.md`: `54f2706255534ab98227178ef2f3c75a3b25a1ee`.

No code tests were run because this change is documentation and research only. No phase transition occurred.


## 8. Follow-up: Hugging Face dataset market identity and API preview

After publishing the execution-quality decision, the Hugging Face dataset was inspected through its public metadata and datasets-server row-preview API:
- Metadata: public, ungated, MIT; 251,388,868 rows / 1,723,754,188 bytes. Configurations: depth 220,581,733 rows / 1,491,633,558 bytes; snapshots 224,000 rows / 1,659,329 bytes; trades 30,583,135 rows / 230,461,301 bytes.
- Bounded previews exposed depth/snapshot/trade schemas. Published schemas omit a separate `exchange_ts` field.
- Market identity resolved to **Binance spot**. Dataset records use `exchange=binance`; collector `BinanceExchange` uses `stream.binance.com` and `api.binance.com/api/v3/depth`. The separate `BinanceFuturesExchange` uses `binance_futures`, `fstream.binance.com` and `fapi.binance.com/fapi/v1/depth`. The dataset is not perpetual market data.
- First returned snapshot row is 2026-06-05 06:29:48.543 UTC; first depth/trade rows are 2026-06-04 00:54:40.378 / 00:54:34.149 UTC. An anchor for the first ~29.6 hours is not demonstrated by the exposed row preview. Dataset card records a separate ~43-minute outage on 2026-07-05 requiring a hard reset.
- The public API returned metadata and sample rows, but no Parquet bytes were downloaded or locally parsed. One depth row-preview request returned HTTP 502. No sequence-completeness, reconstruction or data-quality pass is claimed.

Updated `docs/HISTORICAL_L2_SAMPLE_VALIDATION.md` section 9, `docs/EXCHANGE_AND_DATA_SHORTLIST.md` section 11 and ROADMAP Phase 01 status. The earlier “spot/perpetual unclear” statement is superseded. Historical perpetual L2 gate remains BLOCKED.
