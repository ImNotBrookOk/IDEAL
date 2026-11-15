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