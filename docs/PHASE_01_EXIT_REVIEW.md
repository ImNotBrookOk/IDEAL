# IDEAL — Phase 01 Exit Review

**Last updated:** 16 November 2026  
**Current phase:** Phase 01 — Open-source and infrastructure research  
**Phase state:** IN PROGRESS  
**Next phase:** Phase 02 — Architecture/contracts (**LOCKED**)

## Executive position

Phase 01 has produced enough evidence to retain several research candidates and reject unsuitable alternatives. It is not ready to close. The remaining blockers are now concentrated in three areas:

1. **Persistent $0 core compute:** no reliable free cloud worker is proven; a self-hosted always-on host is possible but the user's hardware/power/network availability is unconfirmed.
2. **IDEAL-specific dependency and workflow security:** direct licences are reviewed and a first vulnerability/SBOM/workflow audit is running, but the audit has found four known vulnerabilities in two packages in its first run; the exact packages and fixes must be examined before acceptance.
3. **Owner approval:** the component matrix and explicit accepted/rejected/deferred choices still require final review and approval.

The seven-day OKX dataset is conditionally accepted for historical market-structure research, and the Tardis multi-day comparison is complete with a secondary-reference-only disposition. These are evidence classifications, not execution-readiness claims. Tardis use is limited to internal research under the published terms; external product use requires separate written rights.

## Evidence and gate register

| Gate | Status | Evidence / disposition |
|---|---|---|
| Open-source component research | PASS — research complete | Component matrix covers engine, replay, data, risk, orchestration, UI, edge services and execution methods. No engine/runtime dependency adopted. |
| OKX historical L2 structural reconstruction | PASS | Three consecutive archive reconstructions and 400-level seven-day reconstruction; book validity checks passed. Historical archive still lacks live seqId/prevSeqId continuity proof. |
| Seven-day trade/BBO alignment | CONDITIONAL — research acceptance | 19,918,682 aligned trades; original strict screen 5/7 days. 7 Nov one unmatched trade is 2 ms before first snapshot; 8 Nov side/BBO diagnostic 96.453%. Research use accepted with per-day age/source flags; not execution-grade calibration. |
| Independent Tardis comparison | PASS WITH LIMITS | 1 Sep, 1 Oct, 1 Nov strict-preceding exact BBO match >99.3%; inclusive 100%. Tardis is materially sparser and has multi-second gaps; secondary sampled BBO only. |
| Live feed entitlement | DOCUMENTED | OKX 10 ms books-l2-tbt VIP4+; standard books 100 ms; RPI channel separate and permissioned. Historical archives do not prove live entitlement. |
| NZ legal / venue eligibility | CONTAINED BY EXCLUSION | No venue selected; venue selection, exchange accounts and connectivity explicitly excluded pending independent product/entity-specific NZ legal review. |
| $0 persistent worker | OPEN | Oracle A1 is highest-capacity free VM but no SLA, home-region capacity and idle reclamation. GCP e2-micro too small/US-only; Render Free unsuitable; Cloudflare DO useful only as supporting edge/relay. Self-hosted host unconfirmed. |
| Engine POC | RESEARCH CANDIDATE ONLY | NautilusTrader 2.0.0rc9, LGPL-3.0-only, pre-release; 84 tests pass on x86_64 and ARM64 using pytest 9.2.0. Known liquidation/accounting/queue and worker gaps remain. |
| Direct dependency licences | REVIEWED | NautilusTrader LGPL-3.0-only; pytest MIT; orjson 3.11.3 Apache-2.0 OR MIT. Newer orjson 3.13.0 has MPL-2.0-covered files; not adopted. |
| IDEAL-specific security / SBOM | OPEN | First audit found 4 known vulnerabilities in 2 packages; exact findings and remediation pending. Zizmor workflow analysis and CycloneDX SBOM generated, but report must be inspected. Transitive dependency hash lock and complete licence/SBOM review remain open. |
| Documentation / audit trail | VERIFIED | Checkpoint audits 031–036, historical data validation, component matrix, roadmap, shortlist and research docs saved to main and fetched back for verification. |
| Owner approval | OPEN | Final component selections/rejections and residual risk acceptance require explicit owner review. |

## Current component dispositions

| Component | Phase 01 disposition |
|---|---|
| Official OKX module-4 400-level history | Primary historical research source, with archive sequence limitations documented |
| Tardis OKX normalized L2 | Secondary sampled BBO/reference for internal research only; no raw/sub-10-minute redistribution or external product embedding without separate written licence |
| NautilusTrader 2.0.0rc9 | Preferred engine POC candidate; pre-release and not adopted |
| HftBacktest | Execution-model research/reference only; no FIFO claim |
| Cloudflare Workers / Durable Objects | Supporting edge, API, notification or low-volume relay only |
| Oracle A1 | Bounded $0 compute experiment candidate only; not sole production host |
| Render Free / GCP e2-micro | Rejected for core trading engine |
| Venue/exchange connectivity | Explicitly excluded pending NZ legal review |
| Runtime, paper or live trading | Not authorised |

## Work required before Phase 01 can close

- [ ] Inspect exact pip-audit findings, distinguish direct vs transitive and runtime vs dev exposure, upgrade/mitigate or document bounded exceptions; rerun until no unresolved high/critical findings.
- [ ] Inspect Zizmor output, fix actionable workflow security findings, and rerun.
- [ ] Produce and review a reproducible transitive dependency lock (hash-pinned) for the research POC/parser; preserve the generated CycloneDX SBOM and complete licence inventory.
- [ ] Decide the $0 core-compute route: confirm availability of an always-on self-hosted machine with stable power/network/backup, or accept that a reliable $0 cloud host is not currently available and explicitly defer deployment choice. No paid service without approval.
- [ ] Final pass over every row in `docs/COMPONENT_SELECTION_MATRIX.md`; approve preferred candidates, reject alternatives, and record deferred items.
- [ ] Confirm all final Phase 01 evidence and decisions are documented, indexed and fetched back from `main`.
- [ ] Obtain explicit owner approval to close Phase 01 and unlock Phase 02.

## Non-negotiable boundary

Phase 01 closure does not itself authorise exchange credentials, account access, runtime integration, paper trading, live trading, risk-policy changes or paid infrastructure. Phase 02 remains locked until the owner explicitly approves the Phase 01 exit review.

## Key audit records

- [Checkpoint 031 — risk-weighted acceptance and alignment diagnostics](CHATGPT_CONVERSATIONS/2026-11-16-031-risk-weighted-acceptance-and-boundary-diagnostics.md)
- [Checkpoint 032 — legal and zero-cost infrastructure recheck](CHATGPT_CONVERSATIONS/2026-11-16-032-legal-infrastructure-and-dependency-recheck.md)
- [Checkpoint 033 — dependency licence and supply-chain review](CHATGPT_CONVERSATIONS/2026-11-16-033-dependency-licence-and-supply-chain-review.md)
- [Checkpoint 034 — OKX seven-day boundary and risk classification](CHATGPT_CONVERSATIONS/2026-11-16-034-okx-seven-day-boundary-and-risk-classification.md)
- [Checkpoint 035 — free-tier hosting alternatives](CHATGPT_CONVERSATIONS/2026-11-16-035-free-tier-hosting-alternatives.md)
- [Checkpoint 036 — Tardis multi-day BBO validation](CHATGPT_CONVERSATIONS/2026-11-16-036-tardis-multiday-bbo-validation.md)


## Owner decision — seven-day dataset (16 November 2026)

The owner has explicitly accepted the seven-day OKX dataset as conditional historical market-structure research and directed that the project move on without another run of the same test. Workflow #43803546192 completed all daily calculations and unconditional cleanup; its original strict result remains 5/7 days passed, with 7 and 8 November conditional-quality exceptions. The classification gate is therefore **closed by owner decision**, not by a retroactive strict-test pass. The limits in checkpoint 039 are binding.

This decision does not approve the remaining Phase 01 gates, close Phase 01, unlock Phase 02, authorise venue selection/connectivity, runtime integration, paper/live trading or paid infrastructure.
