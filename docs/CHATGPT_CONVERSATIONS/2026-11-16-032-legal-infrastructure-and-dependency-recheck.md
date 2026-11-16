# 032 — Legal, zero-cost infrastructure and engine-version recheck

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Phase state:** IN PROGRESS; Phase 02 remains LOCKED  
**Research branch:** `research/okx-l2-sample-2026-11-16`

## Scope

Rechecked New Zealand derivatives issuer guidance, the Financial Markets Conduct Act territorial-scope issue, Oracle Always Free compute limits, and the current NautilusTrader release state. No accounts, cloud resources, exchange credentials, API keys, billing or paid services were created or activated.

## New Zealand derivatives eligibility

The FMA's current derivatives issuer guidance (page last updated 1 July 2026) states:
- The FMC Act derivative definition includes recurrently entered financial-market transactions, regardless of duration, commonly referred to as futures, forwards, swaps, CFDs, margin contracts or rolling spot contracts.
- The FMA's view is that recurrently entered means regularly traded, and a product cannot avoid the definition merely by being renamed.
- A derivatives issuer making a regulated offer must be FMA-licensed. A regulated offer includes an offer to one or more investors where at least one investor requires disclosure, for example because the investor is retail.
- FMA consumer crypto guidance says providers offering crypto CFDs in New Zealand require a derivatives issuer licence.

The FMC Act territorial-scope text (section 47, in the 2025-03-30 consolidated version returned by search) states Part 3 applies to offers of financial products in New Zealand regardless of where the issue occurs or where the issuer/offeror is resident, incorporated or carries on business; an offer is treated as in New Zealand if received by a person in New Zealand unless the offeror demonstrates reasonable steps to prevent NZ persons accepting it.

Official sources:
- FMA Derivatives issuers: https://www.fma.govt.nz/business/services/derivatives-issuers/
- FMA consumer cryptocurrency guidance: https://www.fma.govt.nz/consumer/investing/types-of-investments/cryptocurrencies/
- FMC Act section 47: https://www.legislation.govt.nz/act/public/2013/69/en/2025-03-30.pdf
- FMA consumer derivatives guidance: https://www.fma.govt.nz/consumer/investing/types-of-investments/derivatives/

**Scope interpretation and limit:** This is not a legal determination that every crypto perpetual offered by every offshore venue is covered in precisely the same way, nor that a New Zealand resident merely operating personal trading software is required to hold a derivatives issuer licence. The cited guidance clearly places the licensing obligation on the derivatives issuer making a regulated offer. Exact instrument terms, contracting entity, customer classification, territorial facts and any exemptions require product-specific independent New Zealand legal advice. No venue has been verified as eligible.

**Phase 01 disposition:** Explicitly exclude venue selection, exchange account creation, API credentials and exchange connectivity from Phase 01. No venue is selected. The platform may continue venue-neutral research and simulation. Reopen the venue gate only after product/entity-specific legal confirmation. This is a containment decision, not a finding that any candidate venue is compliant.

## Oracle Cloud Always Free — $0 worker feasibility

Current Oracle documentation confirms:
- Ampere A1 Always Free allowance: 1,500 OCPU-hours and 9,000 GB-hours per month, equivalent to 2 OCPUs and 12 GB RAM for an Always Free tenancy.
- Compute must be provisioned in the tenancy home region.
- A1 capacity can be unavailable; Oracle documents `out of host capacity` as a temporary regional capacity limitation.
- 200 GB total Always Free block volume, including boot volumes.
- Oracle may reclaim idle Always Free compute when, over a seven-day period, CPU p95 is below 20%, network utilization is below 20%, and (for A1) memory utilization is below 20%.
- Oracle's free tier requires payment-card identity verification for most users; Oracle states it does not charge unless the account is upgraded, although temporary authorization holds can occur.
- Free Tier has no service-level agreement (SLA), per Oracle's FAQ.

Official sources:
- Always Free resource limits and idle reclamation: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- Free Tier and post-trial behaviour: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm
- Oracle Free Tier FAQ, including card verification and no-SLA terms: https://www.oracle.com/cloud/free/faq/

**Assessment:** Oracle A1 is a credible $0 compute experiment candidate, but not a proven reliable persistent trading worker. Regional capacity, no SLA, idle reclamation and payment-card verification are material constraints. An automated trading process may be low-activity for days and could satisfy the provider's idle criteria; deliberately burning CPU/network/memory to avoid reclamation is unacceptable. Do not rely on A1 as the only safety-critical execution host.

GitHub Actions is proven for ephemeral research CI but is not a persistent WebSocket runtime. Cloudflare Workers remains a supporting edge/API/notification candidate, not a substitute for a continuously running Python/Rust trading process.

**Disposition:** No cloud provisioning. $0 persistent production-worker feasibility remains OPEN. Keep runtime deployment portable and do not make architecture depend on Oracle availability. A self-hosted always-on machine is a possible no-new-subscription alternative, but hardware, power, internet and backup availability have not been confirmed.

## NautilusTrader version and maturity recheck

As of 16 November 2026:
- Latest 2.x release is `2.0.0rc9`, published 10 November 2026 and explicitly marked pre-release.
- PyPI continues to show stable 1.x `1.231.0` (2 August 2026); the 2.x API is materially different and requires pre-release installation.
- Upstream installation guidance explicitly says not to use 2.x release candidates in production environments controlling real capital.
- Existing IDEAL isolated POC remains pinned to `nautilus_trader==2.0.0rc9`; 84 deterministic tests passed on x86_64 and ARM64, but important liquidation, partial-fill, queue, funding-recovery and free-worker benchmarks remain open.

Sources:
- https://github.com/nautechsystems/nautilus_trader/releases
- https://pypi.org/project/nautilus-trader/
- https://nautilustrader.io/docs/latest/getting_started/installation/

**Disposition:** retain NautilusTrader as the leading engine research candidate, not an adopted dependency. The pre-release status is a material reason to keep the engine decision open. Do not pin it into runtime until stable-release status, POC gaps, exact licences, security posture and worker benchmarks are closed.

## Tardis multi-day comparison work

A new research-only workflow was added:
- Commit: `e24781a06c0530254573bf282d4431ef646f3a2f`
- Workflow: [#43804760777](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43804760777)
- It downloads public Tardis OKX Swap incremental L2 and official OKX module-4 400-level archives for 1 September and 1 October 2026.
- It reconstructs both sources, emits BBO series, stable-sorts by exchange timestamp, compares strict-preceding/no-lookahead BBO matches, then deletes raw archives and BBO rows before retaining only summary artifacts.
- The complete research unit suite runs first.
- 1 November 2026 remains the existing baseline comparison (workflow #43778824863).

At the time of this record, retrieval had completed and reconstruction/comparison was in progress. No September/October result or multi-day acceptance is claimed yet. The workflow does not prove raw channel provenance: the normalized Tardis CSV lacks the source WebSocket channel ID. Tardis coverage documentation lists OKX `books-l2-tbt` through 21 May 2026 and `books` from that date onward, but exact raw message channel identity is not available in the normalized sample. Treat any channel interpretation as documentation-based, not packet-level provenance.

## Current gate disposition

| Gate | Current disposition |
|---|---|
| NZ legal / venue | Venue selection explicitly excluded pending independent legal review; no venue/account/API selected |
| $0 persistent worker | OPEN; Oracle A1 is conditional experiment candidate, not dependable production host |
| NautilusTrader | Leading research candidate; 2.0.0rc9 remains pre-release, not adopted |
| Tardis multi-day | Workflow #43804760777 in progress; no result claimed |
| Seven-day OKX trade/BBO | Original result remains 5/7 per-day strict screens passed; 7 Nov and 8 Nov failures preserved; timestamp-boundary revalidation #43803546192 in progress |
| Phase 01 | IN PROGRESS |
| Phase 02 | LOCKED |

No scope expansion, runtime integration, account access, paper/live execution, spend or billing is authorised.
