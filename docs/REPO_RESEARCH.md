# IDEAL Open-Source Repository Research

**Research snapshot:** 15 November 2026  
**Status:** Preliminary shortlist; no dependency or code has been adopted.  
**Scope:** Crypto perpetual-futures research, market data, strategy discovery, backtesting, execution, risk, learning and mobile operations.

This register preserves the initial GitHub landscape review. Star counts are approximate snapshots, not quality scores. Repository activity, licences and APIs can change; re-check the upstream repository, exact commit, licence text, dependencies and tests before any reuse.

## Decision rule

A repository is a source of ideas until it passes technical due diligence. Stars are a discovery signal only. Adoption requires:
- Source and test inspection, not README-only review.
- Active maintenance appropriate to the component, known unresolved issues and security posture.
- Licence compatibility and any attribution, network-copyleft or commercial-use obligations.
- A bounded integration plan, resource footprint and $0 deployment feasibility.
- Reproducible tests against IDEAL contracts and failure cases.
- Explicit approval before adding a dependency or changing architecture.

No source code has been copied into IDEAL as a result of this research.

## Priority 1 — deep technical due diligence

| Candidate | Licence / stack | Relevant capability | Preliminary assessment |
|---|---|---|---|
| [NautilusTrader](https://github.com/nautechsystems/nautilus_trader) | LGPL-3.0; Rust/Python; ~31k stars | Event-driven trading engine, multi-venue adapters, order/position lifecycle, backtesting and live architecture | Strongest engine architecture candidate. Heavy integration/runtime footprint; compare stable APIs and licence obligations before selection. |
| [Hummingbot](https://github.com/hummingbot/hummingbot) | Apache-2.0; Python/Cython; ~21k stars | Exchange connectors, WebSocket handling, order lifecycle, paper trading and position executors | Strong connector/execution reference. Its candle-based position simulator is not sufficient as IDEAL's final intrabar validation engine. |
| [CCXT](https://github.com/ccxt/ccxt) | MIT; JavaScript/Python/PHP; ~45k stars | Unified exchange REST API, markets, OHLCV and supported derivatives endpoints | Likely useful adapter layer. Verify endpoint coverage, rate limits, precision and the separate terms/pricing of CCXT Pro; do not assume Pro/WebSocket features are free. |
| [crypto-data-warehouse](https://github.com/holarchic/crypto-data-warehouse) | MIT; Python/TimescaleDB | OHLCV, funding, open interest, liquidations and premium-index collection | Useful ingestion/schema reference: idempotency, gap detection, feed health and UTC candle semantics. TimescaleDB and historical endpoint limits affect $0 feasibility. |
| [Forven](https://github.com/judder659/Forven) | AGPL-3.0; Python/FastAPI/SvelteKit/SQLite/ChromaDB | Autonomous research workflow, strategy generation, backtest, robustness checks and paper trading | Valuable end-to-end architecture reference. AGPL review required; large risk/policy modules merit maintainability review. Its risk defaults differ from IDEAL and must not be copied. |
| [Microsoft RD-Agent](https://github.com/microsoft/RD-Agent) | MIT; Python | Agentic R&D and iterative factor/model research | Good hypothesis-generation and experiment-evolution reference; finance examples are primarily equity-oriented, not a perp execution engine. |
| [LLM Trading Auto-Research](https://github.com/nhocconan/AutoResearch-based-Trading-Strategy-Generation-and-Testing) | MIT; Python; small community | Autonomous crypto-futures strategy generation with fixed evaluator, validation and backtest workflow | Strong design principle: AI proposes candidates but cannot edit the evaluator. Low adoption; validator is not a secure sandbox and backtester does not fully model margin/liquidation. |
| [TA-Lib Python](https://github.com/TA-Lib/ta-lib-python) | BSD-2-Clause; C/Python; ~12k stars | Established technical indicator implementations | Candidate primary indicator baseline; verify formula parity, packaging and warm-up semantics. |
| [Pandas TA Classic](https://github.com/xgboosted/pandas-ta-classic) | MIT; Python | Broad indicator and candlestick-pattern library with tests | Candidate alternative; compare outputs against TA-Lib and independently specified formulas. Avoid treating correlated indicators as independent evidence. |
| [Optuna](https://github.com/optuna/optuna) | MIT; Python; ~15k stars | Hyperparameter and experiment optimisation | Useful bounded search engine. Must control multiple testing, search budgets and untouched holdout contamination. |
| [QuantStats](https://github.com/ranaroussi/quantstats) | Apache-2.0; Python; ~8k stars | Performance and risk reporting | Useful independent reporting/cross-check layer. Independently verify metric definitions before using any metric for promotion gates. |

## Priority 2 — compare and borrow selectively

| Candidate | Licence / stack | Relevant capability | Preliminary assessment |
|---|---|---|---|
| [Freqtrade](https://github.com/freqtrade/freqtrade) | GPL-3.0; Python; ~57k stars | Crypto trading, futures/shorting, backtesting, dry-run and FreqAI | Useful research baseline. GPL obligations require review. Historical funding coverage and defaults need careful audit; missing funding treated as zero can bias results. |
| [Jesse](https://github.com/jesse-ai/jesse) | MIT; Python; ~9k stars | Crypto strategy research, multi-timeframe backtesting and indicators | Good strategy API and research workflow reference. |
| [Barter](https://github.com/barter-rs/barter-rs) | MIT; Rust; ~2.4k stars | Modular event-driven live, paper and backtest components | Useful typed-interface and modular Rust reference; smaller ecosystem and maintenance maturity need review. |
| [Cryptofeed](https://github.com/bmoscon/cryptofeed) | AGPL with additional attribution condition; Python | Normalised exchange WebSocket market feeds | Useful streaming reference; licence terms need explicit review. |
| [QuantConnect LEAN](https://github.com/QuantConnect/Lean) | Apache-2.0; C#/Python; ~22k stars | Large multi-asset event-driven research and execution engine | Alternative to NautilusTrader; substantial complexity and runtime footprint. |
| [FinRL-X](https://github.com/AI4Finance-Foundation/FinRL-Trading) | Apache-2.0; Python; ~4k stars | Data, model, backtest and trading pipeline with risk overlays | Architecture reference, but examples are primarily equities and Alpaca-oriented. |
| [Qlib](https://github.com/microsoft/qlib) | MIT; Python; ~50k stars | Quant research, factors, models and portfolio backtesting | Strong research platform; not a crypto-perpetual execution solution. |
| [Riskfolio-Lib](https://github.com/dcajasn/Riskfolio-Lib) | BSD-3-Clause; Python; ~4.6k stars | Portfolio optimisation and risk measures | Useful analytics research, not a substitute for deterministic per-order risk enforcement. |
| [TradingAgents](https://github.com/TauricResearch/TradingAgents) | Apache-2.0; Python | Multi-agent financial analysis | Agent collaboration patterns only; largely equity/fundamental analysis. |
| [FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) | Apache-2.0; Python; ~8k stars | Financial AI agents and research workflows | Potential bounded research-agent patterns; not a trading runtime. |
| [backtesting.py](https://github.com/kernc/backtesting.py) | Licence to re-check | Bar-based strategy backtesting | Secondary comparison only; not derivatives-specific. Re-check licence before any reuse. |

## Research-only / not core-adoption candidates

| Candidate | Licence / status | Reason |
|---|---|---|
| [vectorbt](https://github.com/polakowo/vectorbt) Community | Apache-2.0 plus Commons Clause | Community licence has restrictions relevant to commercial use; advanced futures, leverage and execution features are associated with PRO. Do not make it the core engine without a licence determination. |
| [qtfinance](https://github.com/lymnal/qtfinance) | MIT; small project | HMM/Markov/change-point ideas are interesting, but documented packaging/export issues and limited maturity make it research-only. |
| [Hidden Regime](https://github.com/hidden-regime/hidden-regime) | MIT; last observed commit Nov 2025 | Stale; educational reference only. |
| [hmmlearn](https://github.com/hmmlearn/hmmlearn) | Licence/version to verify | A modelling library, not a ready-made trading regime system. Causal forward-filtered probabilities are required; smoothed labels using future observations would leak information. |
| FinRL legacy | Superseded by FinRL-X | Avoid starting from the older project without a specific reason. |

## Component mapping — hypotheses, not decisions

| IDEAL capability | Repositories to study | Likely build/reuse boundary |
|---|---|---|
| Strategy research agents | Forven, RD-Agent, LLM Trading Auto-Research | Reuse bounded workflow ideas; IDEAL owns candidate schema, evaluator, validation and permission boundary. |
| Backtest and simulation | NautilusTrader, LEAN, Jesse, Hummingbot | Select one engine only after event/fill/funding/margin semantics and resource costs are tested. |
| Exchange connectivity | CCXT, Hummingbot, Cryptofeed | Use adapters behind IDEAL-owned contracts; never allow adapter responses to directly authorise risk. |
| Market-data pipeline | crypto-data-warehouse, Cryptofeed | Own canonical schema, provenance, freshness, gap recovery and idempotency. |
| Indicators | TA-Lib, Pandas TA Classic | Choose after formula parity, numerical and packaging tests. |
| Regime classification | hmmlearn plus independently researched change-point methods | IDEAL-owned causal classifier with explicit UNKNOWN state. |
| Optimisation | Optuna | Bounded experiments with immutable evaluator and untouched holdout. |
| Risk and portfolio controls | Forven, Riskfolio-Lib, Hummingbot | Build IDEAL-owned deterministic risk state machine; never import another project's risk defaults as policy. |
| Learning and memory | Forven and RD-Agent workflow patterns | Immutable structured trade/experiment records; vector search only as a secondary index. |
| Reporting | QuantStats | Cross-check calculations against independent fixtures and hand-computed cases. |
| Android dashboard | Forven/Freqtrade/Hummingbot dashboard patterns | Android-first PWA as control plane; compute stays on a separately assessed worker. |

## Critical technical findings and cautions

1. **Backtest realism:** close-to-close candle simulation is not sufficient for stop/target ordering, intrabar ambiguity, partial fills, funding, fees, spread, slippage, latency, liquidation and margin constraints. Final validation needs an event-driven model with documented assumptions and conservative ambiguity handling.
2. **Research leakage:** AI must not alter the evaluator or access untouched out-of-sample labels during candidate generation. Keep data splits, strategy versions, parameters and run hashes immutable.
3. **Regime leakage:** use only information available at decision time. HMM smoothed state estimates can use future observations; use causal filtering for live-equivalent regime classification.
4. **Funding bias:** missing historical funding must not silently become zero. Missing or uncertain funding should be flagged, bounded or cause the affected sample to be rejected.
5. **Risk separation:** external projects' risk defaults are not IDEAL policy. IDEAL's 0.5% per-trade target, daily hard boundary and progression rules remain governed by its own decision register.
6. **Licences:** MIT/BSD/Apache are generally simpler, but still require notice compliance. GPL/LGPL/AGPL, attribution clauses and Commons Clause require project-specific legal review before copying, linking or network deployment.
7. **Deployment:** most engines require Linux/macOS/Windows and meaningful CPU/RAM/storage. Android is the control plane, not the target compute host. A free-tier worker may sleep, have limited CPU/networking or ephemeral storage; no always-on $0 assumption is approved.
8. **Security:** strategy code and AI-generated code must run in a constrained process/container with resource, filesystem, network and time limits. A schema validator alone is not a sandbox.

## Outstanding Phase 01 work

- [ ] Re-open upstream repositories and pin exact commits/releases for the leading candidates.
- [ ] Inspect source trees, tests, dependency graphs, open critical issues and recent release history for the top candidates.
- [ ] Compare NautilusTrader vs LEAN vs a smaller custom event-driven engine against IDEAL's required order, funding, margin and replay semantics.
- [ ] Compare Hummingbot vs CCXT plus dedicated WebSocket adapters for target exchange coverage and actual free-feature availability.
- [ ] Audit Forven and RD-Agent/AutoResearch execution boundaries, sandboxing, reproducibility and maintainability.
- [ ] Verify current licence texts and obligations for every candidate considered for reuse.
- [ ] Benchmark minimum viable worker/database/PWA deployment on free tiers, including sleep, quotas, persistent storage, secrets and networking.
- [ ] Produce a component selection matrix with evidence, rejected alternatives, costs and migration risks.
- [ ] Obtain owner approval of the Phase 01 findings before Phase 02 architecture/contracts are unlocked.

## Current decision

**No repository is selected for adoption. No dependency has been added. No implementation phase is unlocked by this research record.** The shortlist is a research backlog, not an architecture decision.

## Source-level due-diligence addendum (15 November 2026)

This addendum records findings from direct source/documentation inspection, not just repository landing pages. Upstream paths are linked so the review can be repeated against a pinned commit.

### NautilusTrader — execution realism requires explicit configuration

Inspected:
- [Fill-model documentation](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/backtesting/fill-models.md)
- [Backtest crate overview](https://github.com/nautechsystems/nautilus_trader/blob/develop/crates/backtest/README.md)
- [Trade execution documentation](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/backtesting/trade-execution.md)

Findings:
- The engine supports event-driven replay, configurable latency/fill models, simulated exchanges and multi-venue/multi-asset tests.
- Documented default fill settings are permissive for limit touches (`prob_fill_on_limit=1.0`) and have no probabilistic L1 slippage (`prob_slippage=0.0`). These defaults are not suitable as an unexamined realism baseline.
- Historical book liquidity is immutable after a fill. The docs warn that, with `liquidity_consumption=False`, multiple simulated orders may reuse the same displayed size. IDEAL must explicitly evaluate `liquidity_consumption=True`, queue-position assumptions and whether input data is L1, L2 or L3.
- Synthetic order books have separate consumption caveats. A custom fill model must own its synthetic liquidity-consumption behavior.
- A reproducible random seed is available for probabilistic fill/slippage models.

Assessment: **keep as leading engine candidate, not selected**. A proof-of-concept must test limit queue/touch rules, partial fills, market impact, gap-through stops, stop/target same-bar ambiguity, liquidity consumption, funding, fees, margin/liquidation and deterministic replay. Compare its actual futures/account model against the target exchange before adoption.

### Forven — strong execution-kernel pattern, but parity claim has a boundary

Inspected:
- [Shared execution kernel](https://github.com/judder659/Forven/blob/main/forven/strategies/execution_kernel.py)
- [Kernel replay parity tests](https://github.com/judder659/Forven/blob/main/tests/test_execution_parity.py)
- [Pending-action tests](https://github.com/judder659/Forven/blob/main/tests/test_kernel_pending_actions.py)
- [Funding completeness policy search result/source](https://github.com/judder659/Forven/blob/main/forven/policy.py)

Positive findings:
- One kernel is designed to serve both batch backtesting and the paper/live scanner.
- Signals on bar i are modelled as entries at bar i+1 open; stop/target checks use intrabar high/low; trailing stops are based on the prior bar's extreme; fees and slippage are explicitly charged.
- A replay-parity test compares closed trades from full-history execution with repeated growing-prefix kernel execution across sizing and exit profiles.
- Funding completeness is treated as a promotion concern: the policy source includes a block for incomplete funding history rather than silently approving it.

Important limitation:
- The parity harness proves the kernel's growing-prefix replay property; it does not by itself prove end-to-end equivalence of the actual paper scanner, exchange fills and backtest. The kernel documentation says the scanner emits pending actions when the signal bar closes for the next forming bar's open. The pending-action tests cover projected entry timestamps, reconciliation and duplicate suppression, and describe this mechanism as removing a previous one-bar scan lag. This is a useful design, but these tests do not by themselves prove exchange acknowledgement/fill-price parity or full scanner-to-backtest event equivalence.
- The kernel is OHLCV-driven. Its intrabar model cannot infer the true ordering of stop and target touches within a candle; conservative ambiguity rules and higher-resolution/order-book evidence are still needed.
- Funding is an opt-in aligned series in the kernel, with a completeness flag. The downstream policy needs to be tested to ensure incomplete funding blocks eligibility across every path.

Assessment: **retain as a high-value reference for shared-kernel design and replay tests**. Do not adopt its kernel replay suite as proof of exchange-level paper/backtest parity. Build an IDEAL contract test that compares signal time, submitted order time, exchange/simulator acknowledgement, actual fill price, fees and position state against the backtest event stream.

### CCXT — useful REST adapter primitives, not a complete feed/execution stack

Inspected:
- [Python exchange base](https://github.com/ccxt/ccxt/blob/master/python/ccxt/base/exchange.py)

Findings:
- The Python base exchange class enables rate limiting by default and includes configurable request pacing, timeout, exception mapping and exchange metadata.
- The library contains precision conversion helpers and unified market/position/funding-related fields, but endpoint support is exchange-specific.
- CCXT's own class metadata distinguishes the Pro integration for WebSocket support; the free core must not be assumed to include the paid Pro streaming product.

Assessment: **candidate for REST market/account adapter only**, subject to a per-exchange capability matrix. Keep WebSocket streaming, sequence recovery, stale-feed detection and canonical data contracts independently owned by IDEAL unless a separately verified free adapter is chosen.

### RD-Agent — experiment abstraction is useful; execution isolation is not automatic

Inspected:
- [Experiment/workspace abstractions](https://github.com/microsoft/RD-Agent/blob/main/rdagent/core/experiment.py)
- [Hypothesis and experiment trace](https://github.com/microsoft/RD-Agent/blob/main/rdagent/core/proposal.py)

Findings:
- The framework models tasks, workspaces, experiment feedback, checkpoints and a trace of accepted/rejected experiments.
- Its hypothesis/feedback/trace abstraction is a useful pattern for retaining why a candidate was proposed, what changed and how it was evaluated.
- The generic workspace abstraction does not itself establish a secure sandbox. Scenario-specific execution environments and their isolation controls must be audited separately before generated code is run.

Assessment: **research workflow reference only**. IDEAL should retain immutable candidate/experiment lineage and deterministic evaluation separately from agent orchestration. Do not import an agent framework as the strategy evaluator or trust boundary.

### Optuna — persistent and seeded search is feasible, but parallel search is not strictly reproducible

Inspected:
- [Optuna FAQ](https://github.com/optuna/optuna/blob/master/docs/source/faq.rst)
- [TPE sampler implementation](https://github.com/optuna/optuna/blob/master/optuna/samplers/_tpe/sampler.py)

Findings:
- Optuna supports in-memory studies and SQLite-backed study persistence/resumption.
- A fixed sampler seed improves reproducibility for sequential studies.
- Its documentation explicitly warns that distributed/parallel optimisation introduces inherent nondeterminism and that objective functions must themselves be deterministic.
- Trial records persist suggested parameters and objective values; external artifacts need a separate artifact store.

Assessment: **candidate optimiser, not an evaluator**. Begin with sequential seeded studies and immutable data/evaluator versions. Persist all trial metadata and cap search budgets. Parallelism is a later optimisation only if reproducibility controls are demonstrated.

## Updated technical direction

These inspections strengthen the following provisional boundaries:
- Evaluate NautilusTrader first as an event-driven engine candidate, with strict custom fill/liquidity settings and exchange-specific futures validation.
- Keep Forven's shared-kernel and replay-test ideas, but explicitly test scanner-to-fill parity rather than relying on its kernel parity suite.
- Use CCXT only where the exact exchange endpoint and free feature set are verified; do not conflate REST and Pro WebSocket capabilities.
- Use RD-Agent-like hypothesis/experiment lineage without delegating evaluation or permissions to an agent.
- Use Optuna sequentially with fixed seeds for controlled parameter exploration; protect untouched holdout data and account for multiple testing.


### Additional candidate comparison: crypto-perpetual support and control surfaces

- NautilusTrader documents a dedicated `CryptoPerpetual` instrument with linear/inverse settlement, precision, contract multiplier, min/max quantity/notional and initial/maintenance margin fields. Its documented adapters include Binance, Bybit, dYdX, Hyperliquid, Kraken and OKX. Funding is delivered as timestamped data updates rather than stored as a static instrument field. This is a material advantage for IDEAL's target market, but each adapter's exact order types, funding history, mark/index feed and account-margin semantics still require exchange-specific tests. See the [crypto perpetual instrument contract](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/instruments/crypto_perpetual.md).
- Barter's README describes separable MarketStream and ExecutionClient interfaces, mock execution for paper/backtesting, pluggable Strategy/RiskManager components, a central order-management system and an Engine AuditStream suitable for an external monitoring process. This is a useful smaller Rust architecture comparison, especially for clean control-plane boundaries. It does not establish that the exchange integrations or derivatives semantics meet IDEAL's needs. See the [Barter README](https://github.com/barter-rs/barter-rs/blob/main/README.md).
- Forven's current policy defaults are materially different from IDEAL's preliminary screen: the inspected quick-screen config uses a 20-trade minimum and disables a minimum win-rate floor by default, with profit-factor and other gates. IDEAL's user-defined initial screen is over 100 trades and over 30% win rate, while also requiring net expectancy, PF, drawdown, costs and out-of-sample robustness. These thresholds must not be copied or treated as interchangeable. See [Forven policy](https://github.com/judder659/Forven/blob/main/forven/policy.py).



## Engine and zero-cost deployment comparison — 15 November 2026

### Engine comparison

| Requirement | NautilusTrader | QuantConnect LEAN | Barter |
|---|---|---|---|
| Crypto perpetuals | Dedicated CryptoPerpetual model; linear/inverse contract metadata | Crypto-future margin models exist; exact perp funding semantics need validation | Modular execution interfaces; exact funding/margin coverage unproven |
| Exchange adapters | Current docs cover Binance, Bybit, OKX and Hyperliquid perpetuals | Broad brokerage ecosystem; exact target venue and data availability need validation | Smaller exchange ecosystem |
| Funding backtest | Explicit FundingRateUpdate and boundary-driven settlement | Not established by this review | Not established by this review |
| Margin | Simulated margin accounts and configurable models; live venue-reported margin has distinct reconciliation semantics | Crypto-future buying-power/margin models | Pluggable risk manager; exact engine needs audit |
| Fill realism | Event-driven matching and configurable fills, but permissive defaults/liquidity reuse need correction | Mature fill abstractions; custom perp funding/liquidation semantics need validation | Smaller OHLCV-driven implementation cannot infer true intrabar order |
| Current position | **First engine to prototype; not selected** | Alternative benchmark | Smaller architectural alternative |

Evidence:
- [Nautilus crypto perpetual model](https://nautilustrader.io/docs/latest/concepts/instruments/) and [instrument details](https://nautilustrader.io/docs/nightly/concepts/instruments/crypto_perpetual/).
- [Nautilus backtest funding/margin](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/backtesting/accounts-and-margin.md), [accounting](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/accounting.md), and [backtesting guide](https://nautilustrader.io/docs/latest/concepts/backtesting/).
- Exchange guides: [Binance](https://nautilustrader.io/docs/latest/integrations/binance/), [Bybit](https://nautilustrader.io/docs/latest/integrations/bybit/), [OKX](https://nautilustrader.io/docs/latest/integrations/okx/), [Hyperliquid](https://nautilustrader.io/docs/latest/integrations/hyperliquid/).
- [LEAN crypto-futures margin model](https://github.com/QuantConnect/Lean/blob/master/Common/Brokerages/DefaultBrokerageModel.cs); [Barter architecture](https://github.com/barter-rs/barter-rs).

Nautilus is the strongest current match found for a first proof-of-concept: it models perpetual instruments, funding settlement and margin, and documents data/execution adapters for the four exchanges above. This is not proof of production correctness. Hyperliquid's guide, for example, documents mark/index/funding updates, L2 data, conditional/reduce-only orders and reconciliation, but historical trades are only available as a recent snapshot rather than arbitrary historical depth. Every venue's funding history, fee tiers, margin modes, order types, testnet and recovery semantics still require independent testing.

### Free-tier deployment feasibility

| Provider/service | Current documented free limits | IDEAL suitability |
|---|---|---|
| GitHub Actions | Standard hosted runners are free for public repositories; GitHub Free private repos include 2,000 minutes/month and 500 MB artifact storage | CI and tests only; not a persistent runtime |
| Cloudflare Workers Free | 100,000 requests/day, 10 ms CPU per HTTP request, 128 MB memory, 50 subrequests/request; limited Cron CPU | Static/control plane, lightweight API and alerts; not strategy/backtest worker |
| Supabase Free | 2 free projects, 500 MB database size/project, 5 GB egress; low-activity projects can pause after 7 days; no automatic backups | Prototype metadata/dashboard projection; not sole authoritative audit store |
| Render Free | Sleeps after 15 minutes idle; cold start; ephemeral local filesystem; free Postgres expires after 30 days | Demo/preview only; reject as trading worker or primary persistence |
| Oracle Cloud Always Free A1 | Up to 1,500 OCPU-hours and 9,000 GB-hours/month (equivalent to 2 OCPUs and 12 GB RAM when fully allocated); home-region capacity can be unavailable | Only credible always-on $0 VM candidate identified, subject to eligibility, capacity, ARM compatibility and no-billing safeguards |

Official sources: [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions), [Cloudflare limits](https://developers.cloudflare.com/workers/platform/limits/), [Supabase pricing](https://supabase.com/pricing), [Supabase pausing](https://supabase.com/docs/guides/platform/free-project-pausing), [Render free limits](https://render.com/docs/free), [Oracle Always Free resources](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm).

Oracle is not approved or activated. Its free allocation does not guarantee capacity in the user's home region. Before considering it, verify account eligibility, sign-up/payment-card requirements, A1 availability, ARM64 dependency compatibility, persistent storage, outbound exchange connectivity and hard zero-spend controls. Do not upgrade to a paid account or create resources if there is uncertain billing exposure.

### Provisional $0 deployment shape (not approved)

- Android runs the PWA dashboard only.
- Cloudflare Pages serves static frontend assets; Workers handle lightweight control-plane requests only.
- GitHub Actions runs deterministic CI on the public repo; never expose secrets to untrusted pull-request workflows.
- A verified always-free Linux worker runs the research/paper engine. If no such worker is available, IDEAL remains intermittent/manual-trigger research mode and must not claim continuous operation.
- Authoritative event history uses durable local SQLite/Postgres on the worker with encrypted off-host exports where free capacity allows. Supabase can be a projection, not the only copy.
- Watchdog, heartbeat, stale-feed guard, restart recovery, durable order/position reconciliation and fail-closed behavior are mandatory.

### Phase 01 recommendation and proof-of-concept gates

1. Prototype NautilusTrader first, pinned to a stable release/commit (not nightly docs); do not add it as a dependency yet.
2. Compare its native adapter with CCXT REST plus a separately verified free WebSocket feed for one exchange.
3. Select the first exchange based on testability and the user's lawful account access. Do not create credentials or connect an account without explicit approval.
4. Test exact linear/inverse PnL, multipliers, precision, mark/index/last prices, funding timestamps/signs/missing-history rejection, maker/taker fees, spread/slippage, partial fills, liquidity consumption, stop/target ambiguity, gap-through stops, initial/maintenance margin, leverage brackets, liquidation, cancel/replace races, duplicate events, reconnect/restart recovery and deterministic replay hashes.
5. Benchmark CPU/RAM/disk/egress on the candidate free worker. Testnet/paper adapter parity only; no mainnet order submission.

**Phase 01 remains IN PROGRESS.** This review narrows the first experiment but does not authorise Phase 02, real-money trading, account linking, paid services or dependency adoption.


### Exchange-selection constraint carried forward

The earlier project plan specified that public market-data research and simulated paper execution should begin without requiring an exchange account. Exchange/API access must remain free. Therefore the first engine proof-of-concept should be exchange-neutral and use deterministic fixtures or public unauthenticated market data with a simulated execution venue. Do not create credentials, request API keys or connect an account as a prerequisite.

Binance and Kraken were previously discussed as initial exchange candidates, with OKX as an additional candidate, but that discussion did not select a venue for this perpetual-futures implementation. Their regional product availability, derivatives endpoints, test environments and free access must be re-verified before any adapter is selected. The first proof-of-concept must not silently turn an earlier candidate list into an exchange decision.


## NautilusTrader proof-of-concept execution record — 15 November 2026

An isolated experiment has been added under `research/nautilus_poc/`; it is not imported by IDEAL and is not an adopted runtime dependency.

- Exact package pin: `nautilus_trader==2.0.0rc9` (pre-release only).
- CI target: Ubuntu 24.04 x86_64, Python 3.14, GitHub-hosted runner.
- Data: synthetic, deterministic fixtures only.
- No exchange adapters, API credentials, external market data, paid services, paper orders or live orders.
- The test harness contains independent Decimal oracles for linear PnL, inverse PnL, fees and funding cashflow, plus native smoke tests for package identity, CryptoPerpetual construction, FundingRateUpdate construction and margin-venue/instrument registration.
- Native GitHub Actions CI installed the exact `2.0.0rc9` wheel on Ubuntu 24.04/Python 3.14 and passed the full repository suite on merged `main`: **20 passed in 0.13s**, run [43691402915](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43691402915), commit `fb13425c7318f9426c78a230231aa6f0a372b1a6`.
- Verified synthetic cases include linear/inverse long/short Decimal PnL oracles; linear and inverse `CryptoPerpetual` construction; funding event construction; venue fee configuration; submit/ack/fill/position lifecycle; best-ask market execution; deterministic replay of order and funding fixtures; fixed initial and maintenance margin calculations under `StandardMarginModel`; positive funding settlement at a specified boundary; and rejection of implicit funding settlement when no valid boundary is available.
- Exact funding case: 0.1 BTC long, mark price 60,000.50 USDT, funding rate +0.0001, boundary at the scheduled timestamp. The simulated venue debited 0.60000500 USDT funding and 3.00002500 USDT taker fee, leaving 9,996.39997000 USDT. A separate missing-boundary case applied no funding debit.
- Exact margin cases: resting buy limit 0.1 at 59,999 USDT reserves 299.99500000 USDT initial margin at 5%; filled 0.1 long at 60,000.50 USDT carries 150.00125000 USDT maintenance margin at 2.5%. These are fixture parameters for testing the model, not selected IDEAL or exchange risk settings.
- An initial CI run exposed incorrect assumptions: maker/taker fees are venue-level, a venue requires an explicit fee model, and market-order acknowledgement events are disabled by default unless `use_market_order_acks=True`. These were corrected and covered by passing tests.

Important version distinction: the upstream installation guide states that plain PyPI stable installs resolve to the 1.x API, while the 2.x docs require pre-release installation. The 2.0.0rc9 package is explicitly a pre-release and must not be treated as production-ready. Python 3.14/Linux x86_64 is selected because it is within the documented wheel support matrix. See [release 2.0.0rc9](https://github.com/nautechsystems/nautilus_trader/releases), [installation/version guidance](https://nautilustrader.io/docs/latest/getting_started/installation/), and [2.x funding/margin model](https://nautilustrader.io/docs/latest/concepts/backtesting/accounts-and-margin/).

### POC gates still open

1. Test liquidation triggers, liquidation price, partial close/ADL behaviour and account recovery against independent expected values.
2. Verify partial fills, queue position, conservative liquidity consumption under multiple competing orders, spread/slippage and adverse selection.
3. Test stop/target same-bar ordering, gap-through, and the ambiguity of OHLCV-only data.
4. Test funding with missing mark prices, missing FX rates, multiple positions, multiple currencies, repeated updates and settlement retry/recovery.
5. Expand deterministic replay to canonical event/order/position/account hashes and process restart/recovery.
6. Benchmark CPU, RAM, disk and egress on the candidate free worker; verify the exact worker can run the engine within the $0 budget.
7. Complete licence review and the component selection matrix before proposing any engine adoption.

**Current result: 20-test synthetic POC suite passes; engine adoption not decided.** Phase 01 remains IN PROGRESS. No Phase 02 unlock, runtime dependency adoption, exchange connection or trading permission follows from this experiment.
