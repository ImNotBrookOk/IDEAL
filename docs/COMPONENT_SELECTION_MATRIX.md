# IDEAL Component Selection Matrix

**Status:** Draft research matrix — no runtime dependencies selected or adopted.  
**Last reviewed:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Scope:** Initial crypto perpetual-futures system. Spot accumulation and equities remain deferred.

This matrix consolidates the repository landscape review, proof-of-concept evidence, historical-data tests, licensing and deployment constraints. It is a decision aid, not an architecture approval. Adoption requires a pinned version/commit, source and test review, licence/dependency review, bounded integration plan, resource benchmark and explicit owner approval.

## Decision labels

- **Preferred POC candidate:** strongest current candidate for further isolated testing; not production-approved.
- **Research/reference only:** useful ideas or code patterns, but not selected as a dependency.
- **Hold:** potentially useful, but a material legal, data-quality, maintenance or cost gate is unresolved.
- **Rejected for current scope:** does not meet the initial perpetual-futures requirement or has an unacceptable constraint.

## Candidate matrix

| Capability | Candidate | Licence / stack | Evidence and strengths | Blocking gaps / risks | Current disposition |
|---|---|---|---|---|---|
| Event-driven engine / simulator | NautilusTrader 2.0.0rc9 | LGPL-3.0; Rust/Python; pre-release | Isolated POC expanded to 84 deterministic tests, passing on x86_64 and ARM64. Covers linear/inverse PnL, fees, funding, order lifecycle, margin and FX freshness. | Pre-release API; -0.05 USDT simulator liquidation residual in BTC collateral / USDT settlement case; no proof of exchange-equivalent liquidation, ADL, cross-collateral, collateral haircuts or consolidated reporting equity; actual free-worker performance untested. | **Preferred POC candidate**, not adopted. |
| L2 execution backtesting | HftBacktest 2.2.0 | MIT; Python | Event-based market-data replay and L2-oriented execution modelling. | L2 cannot establish true FIFO queue position; fill model requires venue-specific calibration, latency, queue and adverse-selection sensitivity; no validated IDEAL integration. | **Research/reference only**; benchmark against NautilusTrader/custom oracle. |
| Exchange REST adapter | CCXT | MIT; JS/Python/PHP | Broad unified market metadata and REST API coverage. | CCXT Pro WebSocket is separately licensed/paid; endpoint coverage, rate limits, precision and derivatives semantics vary by venue. | **Candidate for REST only**; no Pro assumption. |
| Exchange WebSocket / execution connector | Native venue adapter; Hummingbot as reference | Hummingbot Apache-2.0; Python/Cython | Hummingbot provides connector and order-lifecycle patterns; native adapters preserve venue-specific depth, sequence, checksum and order semantics. | Venue not selected; NZ derivatives eligibility unresolved; OKX live 400-level 10 ms feed is VIP4+, standard depth is 100 ms. | **Build behind IDEAL-owned contracts after venue approval**; Hummingbot reference only. |
| Historical L2 source | OKX module-4 400-level archive | Public downloadable archive; exchange data terms to verify | 11–13 Nov 2026 all structurally reconstructed (19.63m records, zero invalid states, all 288 snapshots 400 levels/side); 10–12 Nov? The validated alignment sample includes 11–13 Nov: 10.37m trades aligned with zero missing/invalid matches; 11–12 Nov passed the 98% side screen, 13 Nov failed at 97.8348%; strict-preceding 97.8877%, same-timestamp 97.3518%, <=10ms age 97.7814%, older age buckets >99.5%; cause remains unresolved. | No sequence IDs/checksums, no L3, unresolved archive tuple schema, stale tail up to ~509 ms, same-timestamp event order ambiguous; live 10 ms full depth VIP4+. | **Leading research-data candidate**, not execution-grade or venue-selected. |
| Independent normalized L2 source | Tardis first-of-month public CSV | Public sample no API key; data-use rights separate | Binance Futures 1 Nov 2026 sample: 79.44m L2 rows / 3.24m message groups, all reconstructed states valid; 1.19m trades passed schema/value/time checks. Parser has six focused tests. | One day/one venue per sample; no event-level trade/BBO alignment yet; normalized feed omits sequence IDs and L3; paid API costs and public sample commercial rights not established. Same-day OKX normalized sample had 6.90x fewer messages and max 3.804s gap versus official archive, so it is not proven 10ms-equivalent. | **Validated sample/reference**, not selected vendor. |
| Historical data replay / cache server | Tardis Machine 18.9.0 | MPL-2.0; TypeScript/Node 24.22.1+ | 313 stars, 60 forks, 0 open issues; latest push/release 10 Nov 2026; supports historical replay, normalized/native APIs, local cache and live streaming. | Uses Tardis.dev HTTP API under the hood; broader data access may be paid; MPL file-level obligations; adds Node runtime; cannot create missing sequence/L3 data. | **Research/reference only**, not adopted. |
| Alternative data vendor | CryptoHFTData | Terms restrict redistribution/downstream use | Multi-venue hourly L2 downloads and explicit correction notices provide a potential data source. | October 2026 correction release was not deployed at inspection; known stale/crossed books, reconnect gaps and other defects; licensing restrictions. | **Hold** pending corrected release and independent validation. |
| Public LOB dataset | MaximumLeverage/crypto_lob_stream | MIT; Hugging Face dataset | Large dataset (251m rows / 1.72 GB) and collector code. | Confirmed Binance spot, not perpetual futures; early initial snapshot anchor not demonstrated and a 43-minute gap documented. | **Rejected for initial perp calibration**; generic parser fixture only if needed. |
| L2 collector | Goodie-Goody/crypto_lob_stream_pypi | MIT; alpha collector | Multi-venue Binance USDⓈ-M, OKX swaps and Bybit linear adapters; useful sequence/resync design reference. | Binance sequence IDs absent before 2026-06-03 14:38:49; no checksum verification; reconnect and pre-0.9.2 file-flush issues. | **Research/reference only**; not adopted. |
| Indicators | TA-Lib Python | BSD-2-Clause; C/Python | Mature, widely used indicator baseline. | Formula parity, warm-up, NaN and numerical semantics must be tested; C build/packaging on ARM. | **Preferred indicator baseline for comparison**, not yet selected. |
| Indicator alternative | Pandas TA Classic | MIT; Python | Broad indicator and candlestick-pattern coverage. | Correlated features and implementation differences; formula parity required. | **Alternative/reference**. |
| Regime models | hmmlearn + IDEAL-owned causal filter | Verify exact licence/version at pin time | Mature HMM library can support regime research. | Smoothed state estimates leak future data; only forward-filtered probabilities allowed; explicit UNKNOWN state and calibration required. | **Library candidate**, regime logic owned by IDEAL. |
| Optimisation | Optuna | MIT; Python | Mature hyperparameter/experiment optimisation. | Multiple testing, data snooping, search-budget and holdout contamination risk. | **Candidate** after immutable evaluator and search governance. |
| Performance reporting | QuantStats | Apache-2.0; Python | Useful reporting and cross-check calculations. | Metric definitions, annualisation and risk-free assumptions must be independently verified. | **Candidate reporting utility**. |
| Portfolio analytics | Riskfolio-Lib | BSD-3-Clause; Python | Broad portfolio optimisation/risk analytics. | Not a substitute for deterministic order-level risk controls; crypto/perp assumptions need validation. | **Research/reference only**. |
| Strategy research agents | RD-Agent; LLM Trading Auto-Research | MIT; Python | RD-Agent provides agentic R&D patterns; Auto-Research has a useful invariant that AI proposes candidates while evaluator stays fixed. | Examples and data are largely equity-oriented; sandbox and validator security not proven; AI must never alter evaluator or risk policy. | **Research workflow reference**; evaluator remains IDEAL-owned. |
| Strategy platform | Forven | AGPL-3.0; Python/FastAPI/SvelteKit/SQLite/ChromaDB | End-to-end autonomous research, backtest, robustness and paper-trading patterns. | AGPL legal review; large risk/policy modules; risk defaults differ from IDEAL. | **Reference only**; do not copy defaults. |
| Event journal | SQLite | Public-domain core; Python stdlib | Low-cost durable append-only event journal candidate; no separate server. | Must design idempotency, migrations, integrity checks, hash anchoring, encrypted backups, retention/compaction and recovery tests. | **Preferred storage POC candidate**, no runtime implementation yet. |
| Research CI | GitHub Actions | Hosted free quota/limits; YAML | Reproducible research workflows and x86_64/ARM64 CI without exchange credentials or paid runner. | Not a persistent low-latency runtime; public artifact retention and raw-data cleanup must be controlled. | **Selected for research CI only**, not trading runtime. |
| Persistent worker | Oracle Cloud Always Free A1 | Free tier subject to region/capacity/account terms | ARM64 candidate with potential 4 OCPU / 24 GB RAM limits under Always Free allocation. | Requires payment card; regional capacity, idle reclamation, persistent volume and actual performance not verified; owner approval required before provisioning. | **Hold** pending region/resource proof and owner approval. |
| Edge/serverless | Cloudflare Workers | Free/paid usage tiers | Useful for lightweight API, notifications or dashboard edge. | Not a persistent WebSocket trading engine or durable high-throughput event processor. | **Supporting service only**, not core runtime. |
| Android dashboard | PWA / Android-first control plane | Open web stack; exact framework TBD | Keeps mobile UI separate from compute and allows low-cost deployment. | Authentication, signed actions, audit, secrets, connectivity and operator safeguards not yet implemented. | **Architecture direction only**, Phase 17 locked. |

## Cross-cutting hard gates

1. **New Zealand derivatives eligibility:** FMA guidance requires a derivatives issuer licence for retail derivative offers; the exact classification of a crypto perpetual swap and exact contracting entity/product require product-specific legal confirmation. No venue is verified as eligible. No account or API key.
2. **Live data entitlement:** OKX 400-level 10 ms books-l2-tbt requires VIP4+; standard 400-level books is 100 ms. Historical access does not imply live entitlement.
3. **Sequence continuity:** OKX archive schema lacks sequence IDs/checksums; Tardis normalized CSV omits exchange sequence IDs. Reconstructed valid books do not prove no lost updates.
4. **Passive fills:** L2 market-by-price is not L3; no true FIFO queue position. Do not claim passive-fill accuracy.
5. **Execution-quality gate:** 11–12 Nov OKX aggregate side-consistency passed; 13 Nov missed the original 98% threshold at 97.835%. Diagnose timestamp ties and age buckets without relaxing the gate.
6. **Independent source comparison:** Tardis Binance and OKX normalized samples reconstructed; same-day OKX comparison showed materially lower message volume/longer gaps than official archive; direct BBO matching and channel provenance remain pending.
7. **$0 runtime feasibility:** GitHub Actions is CI only; Oracle A1 capacity, region and resource performance remain unverified. No paid infrastructure.
8. **Licensing and version pins:** exact commits, transitive dependency licences, stable releases, vulnerability posture and commercial data rights must be rechecked before adoption.

## Phase 01 exit criteria

- [ ] Third-day OKX side-consistency failure explained; original failed result retained.
- [ ] Third consecutive OKX archive structural reconstruction passed.
- [ ] Direct timestamp-aligned Tardis OKX vs official OKX BBO comparison and channel provenance completed.
- [ ] Historical and live feed entitlement documented separately.
- [ ] New Zealand product/entity/legal eligibility confirmed or venue explicitly excluded.
- [ ] $0 persistent worker feasibility proven on a permitted region/resource plan, or a viable alternative identified.
- [ ] Final dependency pins and licence/security review completed.
- [ ] Component matrix reviewed with owner and explicit selections/rejections approved.
- [ ] All evidence, decisions, risks and audit records saved and read-back verified.

**Current phase state:** Phase 01 IN PROGRESS. Phase 02 and implementation phases remain LOCKED. This matrix does not approve runtime integration, exchange access, paper/live execution or spend.
