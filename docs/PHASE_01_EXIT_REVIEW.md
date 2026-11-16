# IDEAL — Phase 01 Exit Review

**Last updated:** 16 November 2026  
**Current phase:** Phase 01 — Open-source and infrastructure research  
**Phase state:** IN PROGRESS  
**Next phase:** Phase 02 — Architecture/contracts (**LOCKED**)

## Executive position

Phase 01 has produced enough evidence to retain several research candidates and reject unsuitable alternatives. It is not ready to close. The remaining blockers are now concentrated in two areas:

1. **Persistent $0 core compute:** no reliable free cloud worker is proven. An existing Windows PC/laptop is available as a fallback, but phone-data bandwidth/caps/tethering, stable uptime, power and safe remote administration are unverified; the owner prefers phone-first operation, so host selection is explicitly deferred unless a concrete requirement forces it.
2. **Owner approval:** the component matrix and explicit accepted/rejected/deferred choices still require final review and approval.

The scoped research dependency/security gates now pass: both locked Python environments have zero known vulnerabilities, hash-pinned locks and CycloneDX SBOMs are retained, and online zizmor auditor-persona analysis reports no findings after a concurrency-control fix. These controls cover the two current research environments and nine workflows, not a future product dependency graph. orjson 3.11.6 MPL obligations remain relevant before distribution.

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
| $0 persistent worker | OPEN — deferred | Oracle A1 remains an unreliable sole host; GCP e2-micro too small/US-only; Render Free unsuitable; Cloudflare DO is supporting edge/relay only. Existing Windows PC/laptop is a fallback, but mobile-data limits, uptime/power and remote-access safety are unverified; phone-first preferred. |
| Engine POC | RESEARCH CANDIDATE ONLY | NautilusTrader 2.0.0rc9, LGPL-3.0-only, pre-release; 84 tests pass on x86_64 and ARM64 using pytest 9.2.0. Known liquidation/accounting/queue and worker gaps remain. |
| Direct dependency licences | REVIEWED WITH LIMITS | NautilusTrader LGPL-3.0-only; pytest 9.2.0 MIT; orjson 3.11.6 MPL-2.0 AND (Apache-2.0 OR MIT), selected to fix CVE-2025-67221 affecting 3.11.3. Review MPL file-level obligations before distribution. |
| IDEAL-specific security / SBOM | PASS WITH LIMITS | Scoped parser and Nautilus POC scans each report zero known vulnerabilities; universal hash locks and CycloneDX SBOMs retained. Online zizmor auditor-persona scan reports no findings across nine workflows after fixing a concurrency-limits issue. Future product dependency graph is not covered. |
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

- [x] Scoped pip-audit review: parser and Nautilus POC locked environments report zero known vulnerabilities; orjson 3.11.6 replaces vulnerable 3.11.3 (CVE-2025-67221). Current product/runtime dependency graph does not yet exist and must be scanned when introduced.
- [x] Online zizmor auditor-persona scan completed; one low-severity concurrency-limits finding in Nautilus POC workflow was fixed with workflow/ref concurrency cancellation. Final run #43825684618 reports no findings across nine workflows.
- [x] Hash-pinned universal locks and CycloneDX SBOMs generated, installed/compared and retained for parser and Nautilus POC environments on the research branch. Review checkpoint 041; repeat for every future runtime/product dependency set.
- [ ] Keep host selection deferred unless a concrete requirement forces it. If the Windows PC becomes necessary, measure mobile-data allowance/tethering and representative bandwidth first; then assess sleep/power, uptime, backup and outbound-only secure remote access. No provisioning or paid service without approval.
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
- [Checkpoint 041 — scoped security, locks and SBOM review](CHATGPT_CONVERSATIONS/2026-11-16-041-scoped-security-locks-and-sbom-review.md)


## Owner decision — seven-day dataset (16 November 2026)

The owner has explicitly accepted the seven-day OKX dataset as conditional historical market-structure research and directed that the project move on without another run of the same test. Workflow #43803546192 completed all daily calculations and unconditional cleanup; its original strict result remains 5/7 days passed, with 7 and 8 November conditional-quality exceptions. The classification gate is therefore **closed by owner decision**, not by a retroactive strict-test pass. The limits in checkpoint 039 are binding.

This decision does not approve the remaining Phase 01 gates, close Phase 01, unlock Phase 02, authorise venue selection/connectivity, runtime integration, paper/live trading or paid infrastructure.


## Hosting constraint update — phone-first (16 November 2026)

The owner prefers phone-only operation and has an existing Windows PC/laptop available only as a fallback if materially necessary. Internet access is via mobile phone data, so data caps, tethering policy, variable connectivity and bandwidth cost must be treated as constraints. The PC is not selected or provisioned. Do not assume it is an always-on host or expose it directly to the internet. Prefer phone as control/monitoring client, GitHub Actions for offline research/CI, compressed/incremental transfers and low-bandwidth summaries. Host selection remains OPEN and deferred; revisit PC feasibility only after a concrete requirement and measured bandwidth case. See [checkpoint 040](CHATGPT_CONVERSATIONS/2026-11-16-040-phone-first-hosting-constraints.md).


## Scoped dependency/security audit update — 16 November 2026

The latest completed online auditor-persona security audit [#43825684618](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43825684618) regenerated and compared universal hash-pinned locks, installed the exact locked environments, generated CycloneDX SBOMs, and ran pip-audit and online zizmor. The parser environment (orjson 3.11.6) and Nautilus POC environment (six resolved packages) each reported **zero known vulnerabilities**. Zizmor reported **no findings across nine workflow files**.

The stricter auditor-persona run first surfaced one low-severity `concurrency-limits` finding in `.github/workflows/nautilus-poc.yml`; it was fixed by adding workflow/ref concurrency cancellation. The final scan then passed. The POC workflow was rerun on x86_64 and ARM64: 84 tests passed on each architecture in [#43825684604](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43825684604).

The hash locks and two SBOMs are retained on the research branch under `research/requirements.lock`, `research/nautilus_poc/requirements.lock`, and `research/sbom/`. This closes the scoped reproducible-lock, vulnerability-scan and workflow-lint gates for the current research environments. It does not constitute a complete future-product SBOM or security clearance for dependencies not yet selected.

The final parser pin is orjson 3.11.6. It fixes the uncontrolled-recursion issue affecting 3.11.3 (CVE-2025-67221), but introduces MPL-2.0-covered source files alongside Apache-2.0 OR MIT. Retain 3.11.6 for internal research; review MPL file-level obligations before distribution/product integration. See [checkpoint 041](CHATGPT_CONVERSATIONS/2026-11-16-041-scoped-security-locks-and-sbom-review.md).
