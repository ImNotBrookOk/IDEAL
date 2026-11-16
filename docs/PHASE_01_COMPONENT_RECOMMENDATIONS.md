# IDEAL — Phase 01 Component Recommendations for Owner Review

**Date:** 16 November 2026  
**Status:** DRAFT RECOMMENDATIONS — NOT APPROVED  
**Phase:** 01 — Open-source and infrastructure research  
**Phase 02:** LOCKED

This document consolidates the current research evidence into a concise decision set for the Phase 01 owner review. "Preferred" means a candidate worth carrying into Phase 02 architecture/contracts, not permission to integrate it or use it in runtime.

## Recommended decisions

| Area | Recommendation | Why | Explicit boundary |
|---|---|---|---|
| Historical perpetual-futures L2 | Retain official OKX module-4 400-level archives as the primary historical research source | Actual BTC-USDT-SWAP archive reconstruction and seven-day alignment evidence; owner accepted conditional research use | No sequence continuity, L3, queue-position or execution-grade fill claim; retain day/age flags |
| Independent historical reference | Retain Tardis normalized OKX L2 as secondary internal sampled-BBO reference only | Multi-day strict-preceding BBO agreement >99.3% against official archives | Sparse feed, multi-second gaps, no raw channel ID; no sub-10-minute redistribution or external product use without separate rights |
| Event-driven engine | Carry NautilusTrader 2.0.0rc9 forward as the preferred isolated POC candidate | 84 tests passed on x86_64 and ARM64; useful event-driven simulation and order lifecycle | Pre-release, LGPL-3.0-only; not adopted as runtime; liquidation, cross-collateral, reporting-equity, venue fidelity and worker gaps remain |
| Execution-model research | Keep HftBacktest as research/reference only | Useful L2 execution and replay modelling concepts | Do not claim true FIFO from L2 market-by-price; no validated fill calibration |
| Exchange REST | Keep CCXT as a possible REST adapter candidate | Broad market metadata and REST coverage | Venue selection and NZ legal eligibility are excluded; CCXT Pro is not assumed |
| Exchange WebSocket / order management | Prefer IDEAL-owned native venue adapters behind IDEAL contracts after venue approval | Preserves venue-specific sequence, checksum, precision and order semantics | No venue selected, no exchange credentials or connectivity authorised |
| Risk, sizing and ledger | Build IDEAL-owned deterministic risk/portfolio/accounting controls; use external libraries only as research references | Hard invariants must remain independently testable and fail-closed | No external risk defaults accepted; exchange-equivalent margin/liquidation still requires venue-specific validation |
| Event journal | Carry SQLite as preferred local event-journal POC candidate | Low operational overhead; initial append/replay benchmark is promising | No storage architecture selected; durability, backup/restore, contention and power-loss recovery still need target testing |
| Research CI | Retain GitHub Actions for research, tests and scheduled offline validation | Existing x86_64/ARM64 and research workflows; no persistent worker assumption | Ephemeral CI only; no trading runtime or high-frequency execution |
| Edge services | Cloudflare Workers / Durable Objects as supporting API, notification or low-volume relay candidates | Low-cost edge use cases | Not the Python/Rust core engine; outgoing exchange WebSocket is not a hibernating persistent process |
| Hosting | Defer host selection; phone-first control/monitoring, Windows PC/laptop fallback only if required | Owner prefers phone-only; mobile data creates bandwidth/cost/uptime constraints | No PC provisioning, inbound ports, continuous feed or paid infrastructure authorised |
| Dashboard | Carry Android-first PWA as a direction, not a framework selection | Mobile control plane can remain separate from compute | Authentication, audit, signed actions and safe controls are Phase 17 concerns |
| Indicators | TA-Lib as a baseline for parity comparisons; no indicator library adopted yet | Mature reference implementation | Verify warm-up, NaN, formula and numerical parity; avoid redundant/correlated features |
| Regime modelling | hmmlearn as a candidate only with IDEAL-owned causal forward filter | HMMs can support regime research | Never use smoothed/future-informed state estimates; explicit UNKNOWN state required |
| Optimisation | Optuna as a later candidate | Mature experiment search tooling | Only after immutable evaluator, search budget and holdout governance exist |
| Performance reporting | QuantStats as a reporting cross-check candidate | Useful analytics and report generation | Independently verify metric definitions and assumptions |
| Portfolio analytics | Riskfolio-Lib research/reference only | Broad optimisation methods | Not a substitute for deterministic order-level risk controls |
| AI research agents | RD-Agent / LLM Auto-Research as workflow references only | Useful bounded hypothesis-generation patterns | AI must not alter evaluator, hard risk rules or acceptance gates |

## Rejections and holds

| Candidate | Recommendation | Reason |
|---|---|---|
| Render Free and GCP e2-micro as core engine hosts | Reject | Spin-down/ephemeral storage or insufficient/remote compute |
| Oracle A1 as sole core host | Hold | Free capacity and idle reclamation make it unsuitable as a proven sole safety-critical host |
| CryptoHFTData | Hold | Known correction defects and downstream licence restrictions; require corrected release and independent revalidation |
| MaximumLeverage/crypto_lob_stream for perp calibration | Reject for current scope | Binance spot rather than perpetual futures; snapshot/gap concerns |
| Goodie-Goody collector as production connector | Research/reference only | Sequence/checksum/resync and flush limitations remain |
| Tardis as an externally embedded/commercial data source | Reject without separate written licence | Published terms impose redistribution and product-use restrictions |
| Any venue or live exchange connection | Defer/exclude | Product/entity-specific New Zealand legal review and owner approval not complete |

## Phase 02 handoff candidates — only after owner approval

If the owner approves closing Phase 01, these are the candidates to examine in Phase 02 contracts and architecture:

1. IDEAL-owned domain contracts for instruments, market events, orders, fills, balances, margin, fees, funding and provenance.
2. NautilusTrader as an isolated engine adapter/POC comparison target, not a hard dependency.
3. SQLite as a journal prototype with independent ledger and recovery invariants.
4. Historical data source abstraction with OKX primary archive and Tardis secondary research reference.
5. Phone-first control plane separated from compute, with host-agnostic deployment interfaces.

No Phase 02 work is started by this recommendation document. No component is adopted or integrated by it.

## Owner approval required

The owner should review the recommendations and either accept them as the Phase 01 research disposition, request changes to named rows, or defer a decision. Explicit approval is still required to close Phase 01 and unlock Phase 02.
