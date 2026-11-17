# IDEAL Phase 02 Owner Decision Register — Draft for Final Review

**Status:** Draft; not yet presented for approval  
**Checkpoint:** 093 — 17 November 2026  
**Purpose:** Consolidate all material owner decisions deferred during Phase 02 research  
**Authority:** D-001, D-006–D-008, D-010, D-014–D-023  
**Boundary:** Decision preparation only. Nothing in this register changes accepted decisions, activates domains, authorises implementation or unlocks Phase 03.

## 1. How to use this register

This is a decision pack index, not an approval request at this checkpoint. The owner is busy; do not interrupt with individual questions. Present the complete pack only after:
- all Phase 02 architecture deliverables are reconciled;
- independent architecture/security/operations review is completed or explicitly marked unavailable;
- findings are resolved or presented with residual risk;
- every decision has evidence, options, consequences and a recommended default;
- all changed GitHub files have been read back and verified.

Status labels:
- **Accepted:** existing owner decision; do not reopen without evidence and explicit owner request.
- **Open:** decision required before the dependent future capability.
- **Deferred:** not needed to complete current research-only Phase 02 work.
- **Gate:** owner acceptance required before Phase 02 closure or Phase 03 consideration.

## 2. Existing accepted decisions — preserved

| Decision | Accepted position | Constraint |
|---|---|---|
| D-001 | Crypto perpetual futures only as initial active market scope | Spot/equities/commodities/hedging/personal finance/tax remain proposals |
| D-006 | Initial 0.5% per-trade risk target | Equity denominator unresolved; applies only to initial perp policy |
| D-007 | 1:3 net reward/risk research objective | Not guaranteed; applies to initial perp research |
| D-008 | 10% UTC day-start equity hard daily loss boundary, realised + unrealised, 24-hour cooldown | Value accepted; baseline/cashflow/multicurrency semantics unresolved |
| D-010 | $0 recurring cost target; no spend without approval | No paid service or billing activation |
| D-013 | Decision-quality-first execution research | No execution policy selected |
| D-015 | Phase 01 closed; Phase 02 architecture/contracts authorised | No runtime/venue/account/credentials/paper/live execution |
| D-018 | Tax reserves informational; no software capital lock or forced payment | Applies across personal finance/investment domains |
| D-019 | Data integrity and independent system health foundational | Design only |
| D-020 | Integrated bounded-engine system with mutually reinforcing foundations | No scope expansion or implementation |
| D-021 | Security is fourth foundational pillar | No implementation/external testing |
| D-022 | Architecture-first research/design before stack proposal | Separate approval required for implementation/dependencies |
| D-023 | Future bounded owner-authorised autonomy | No execution capability approved or active |

## 3. Grouped open owner decisions

### ODR-01 — Final domain scope and activation rules

**Question:** Which proposed domains remain in the long-term architecture, and what evidence/approval is required before each becomes active?

- Current: crypto perpetual futures research only (D-001).
- Proposed: crypto spot, equities/ETFs, commodity-linked exposure, cross-asset hedging, personal finance, tax intelligence, archive/learning and local AI.
- Recommendation: retain all as logical future domains, but activate one domain at a time only after a separate owner decision and domain-specific risk/data/legal gates.
- Consequence of expansion: new legal, tax, data, security, risk and operational assumptions; no inherited permissions.
- Evidence: integrated domain map, risk/capital architecture, requirements traceability.
- Status: OPEN, but no action needed for current Phase 02.

### ODR-02 — D-006 equity denominator

**Question:** What equity measure defines the accepted 0.5% initial per-trade risk target?

- Candidate A: venue margin equity — simple but venue-specific and may misrepresent economic capital.
- Candidate B: economic account equity — intuitive but may ignore conservative haircuts, liabilities and uncertainty.
- Candidate C: risk-adjusted equity — deducts explicit liabilities, collateral haircuts and uncertainty; separates risk budget from available margin.
- Recommendation: C, with a fully specified formula, source timestamps, asset haircuts, currency conversion, liabilities and conservative handling of unknown values.
- Exclude: available margin as the denominator.
- Consequence: affects all sizing, risk budgets, drawdown and backtest comparability.
- Evidence: Risk Management Architecture §§6/22 and Domain Risk and Capital Architecture.
- Status: OPEN; required before any future execution proposal.

### ODR-03 — D-008 daily loss boundary semantics

**Question:** How should the accepted 10% UTC day-start equity boundary handle capital flows, multi-currency assets and valuation uncertainty?

Required sub-decisions:
- exact UTC day-start snapshot and source;
- realised/unrealised P&L and fees/funding inclusion;
- deposits/withdrawals/transfers after day start;
- internal transfers versus external capital flows;
- FX source/side/time and stale-rate handling;
- open positions, pending orders and account-level exposure;
- exchange outages and unknown position state;
- 24-hour cooldown start/end and owner recovery process.

Recommendation: keep the accepted 10% boundary unchanged, define a flow-adjusted risk-equity comparison so deposits do not mask loss and withdrawals do not create artificial loss, and fail closed on unknown material valuation. The exact formula must be backtested and approved before use.

Status: OPEN; no value change proposed.

### ODR-04 — Domain risk hierarchy, portfolio limits and hedge credit

**Question:** Should future domains share any portfolio-level risk budget, netting or hedge credit?

- Recommendation: initially no unified risk budget; maintain domain-specific policies and a read-only portfolio risk view.
- No implicit netting across accounts, venues, legal entities, instruments or collateral pools.
- Hedge credit only after enforceable netting-set evidence, stressed basis/correlation/liquidity/counterparty analysis and owner-approved policy.
- Consequence: conservative capital usage and less apparent diversification, but fewer false offsets.
- Status: DEFERRED until any additional domain is activated.

### ODR-05 — Portfolio/capital view scope and valuation policy

**Question:** Which assets, liabilities and accounts should appear in consolidated views, and how should valuation/FX be selected?

Required choices:
- include only explicitly connected/approved accounts or manually entered assets too;
- household/personal assets versus IDEAL-connected investment accounts;
- valuation hierarchy and stale-value rules;
- native currency and consolidated reporting currency;
- FX source, side, timestamp, spread/haircut and rounding;
- legal ownership and beneficial ownership distinctions;
- pending/encumbered/collateral/derivative treatment.

Recommendation: native-currency records remain authoritative; consolidated view is read-only and partial when data is stale/missing; no implicit legal netting or collateral transferability.

Status: OPEN for future portfolio domain.

### ODR-06 — Personal-finance ingestion path

**Question:** Manual/file import only, or a private one-user Akahu Personal App later?

- Manual import: lowest provider dependency and easiest audit/privacy path, but more user effort and slower updates.
- Akahu Personal App: free one-user account-information path, no payments/webhooks, daily scheduled refresh and one-hour manual-refresh rest period; suitable only for non-real-time visibility.
- Full enduring app: separate accreditation and materially greater privacy/security/review burden; likely unnecessary for private single-user use unless a future product requirement changes.
- Recommendation: manual/file import first; consider Personal App only if user value exceeds privacy/provider dependency and current terms are reviewed.
- Status: DEFERRED; D-017 remains proposed and no connection is authorised.

### ODR-07 — NZ tax interpretation and automation boundary

**Question:** What tax treatment applies to crypto perpetual/futures contracts and later asset classes?

- IRD spot cryptoasset guidance does not conclusively determine the tax treatment of perpetual derivatives.
- Contract terms, taxpayer facts, financial-arrangement rules and current law may matter.
- Recommendation: obtain qualified NZ tax advice before hard-coding derivative classification or tax calculations; keep outputs informational and versioned.
- D-018 remains non-negotiable: no automatic capital lock, forced reserve, filing or payment.
- Status: OPEN before tax domain activation; no filing/payment integration.

### ODR-08 — Data source licensing, archive retention and training rights

**Question:** Which feeds may be stored, retained, derived, shared or used for model training?

- Every source requires exact licence, permitted purpose, retention, derivative and training-rights review.
- Raw data and derived data may have different restrictions.
- IRD cryptoasset record retention (at least seven years where applicable) is separate from RCASP CARF provider record retention.
- Recommendation: source-by-source rights register; no data collection or training without explicit rights and owner approval.
- Status: OPEN; no data subscriptions or provider selected.

### ODR-09 — Host trust topology and availability tier

**Question:** What threat tier must the first deployed system survive?

- Current: undeployed; phone is presentation/owner-control device.
- Existing Windows PC may be inspected later as a research worker only.
- WSL2 is not a security sandbox; Hyper-V remains host-dependent; KVM/Firecracker requires full host hardening; separate physical action gateway is stronger against worker-host compromise.
- Recommendation: no deployment until required; if future execution is approved, require a separate action-gateway trust domain if host-root compromise is outside accepted risk.
- Status: DEFERRED; no device inspection, hardware purchase or hosting.

### ODR-10 — Owner authenticator, root key and recovery

**Question:** Which device/key ceremony and recovery path protects owner authority?

Required choices:
- passkey/platform authenticator versus dedicated hardware key;
- offline owner root and separate recovery root;
- key backup/escrow and loss/compromise distinction;
- owner device loss and replacement ceremony;
- independent revocation anchor and rollback prevention;
- emergency manual recovery.

Recommendation: separate owner approval, policy signing, workload identity, encryption, audit and recovery key purposes; use phishing-resistant hardware-backed protection where feasible, with a tested independent recovery path. Do not select a vendor before platform review.

Status: OPEN before any owner envelope activation.

### ODR-11 — Revocation objective, health supervisor and audit witness

**Question:** What maximum revocation propagation, supervisor independence and audit retention/witness are acceptable?

Required choices:
- registered dispatch-worker inventory and propagation SLO;
- separate process/VM/host/watchdog tier;
- failure response when supervisor or authority store is unavailable;
- local audit retention classes/durations;
- external checkpoint/witness or no external witness;
- privacy/deletion and legal-hold handling.

Recommendation: do not set a numerical SLO until topology/worker inventory is known; local pre-dispatch audit remains mandatory; external witness is optional only if it adds genuine independent trust and acceptable privacy/cost.

Status: OPEN before any execution-capable architecture is accepted.

### ODR-12 — Final architecture baseline and Phase 03 consideration

**Question:** Does the owner accept the complete architecture baseline, including residual risks and all required constraints?

Required evidence:
- final logical/physical architecture and state ownership;
- four foundations and cross-pillar contracts;
- data, temporal, freshness and privacy policies;
- domain risk/capital semantics and worked examples;
- autonomy authority, state machines and recovery;
- threat/control matrix and independent review findings;
- requirement/component/control/test traceability;
- cost, deployment, licensing and portability evidence;
- unresolved decisions and accepted residual risks.

Recommendation: accept or amend the architecture as a whole; then consider Phase 03 separately. Architecture acceptance does not itself approve implementation, runtime integration, dependency adoption, accounts, credentials, paper/live execution, paid infrastructure or external actions.

Status: GATE; not ready until independent review and all Phase 02 exit criteria pass.

## 4. Decision dependencies

| Decision | Must precede | Can remain deferred while |
|---|---|---|
| ODR-01 | Activation of any future domain | Current perp research and architecture documentation continue |
| ODR-02 | Any future perp risk sizing/execution proposal | Architecture can document alternatives |
| ODR-03 | Any future perp loss-control runtime | Architecture can document semantics/options |
| ODR-04 | Cross-domain risk offsets or portfolio risk budget | Read-only portfolio design continues |
| ODR-05 | Complete consolidated capital view | Domain-local ledgers/research continue |
| ODR-06 | Bank provider integration | Manual import architecture can be designed |
| ODR-07 | Tax automation/classification | Tax architecture can remain informational |
| ODR-08 | Raw data retention/training/provider ingestion | Public research with permitted source evidence continues |
| ODR-09 | Persistent worker/deployment | Repository research and documentation continue |
| ODR-10 | Owner envelope activation | D-023 remains design only |
| ODR-11 | Any execution-capable runtime | Architecture can specify required behaviour |
| ODR-12 | Phase 03 consideration | Phase 02 research can continue until complete |

## 5. Items that are not owner decisions

The following are engineering requirements, not preferences to be casually waived:
- no untrusted AI/strategy credentials or generic venue egress;
- no self-authorisation or self-modifying hard policy;
- exact action digest and final dispatch-time recheck;
- risk reservation before external side effect;
- UNKNOWN state and authoritative reconciliation;
- no implicit cross-domain netting or collateral portability;
- no tax-reserve capital lock under D-018;
- provenance, point-in-time data and explicit quality/freshness;
- independent security status and scoped health interlocks;
- restore quarantine and no resurrection of revoked authority;
- durable audit before consequential external action;
- no paper/live execution without separate explicit approval.

## 6. Readiness assessment

The register is sufficiently complete for internal preparation but **not ready to present as a final approval pack**. Remaining prerequisites:
- complete cross-document consistency/read-back pass;
- independent architecture/security/operations review or explicit documentation that it cannot be obtained;
- resolve or clearly bound all review findings;
- confirm no missing accepted decision or deferred owner constraint;
- publish one final architecture baseline and review summary.

No decision in this draft is accepted by silence. No new authority or phase transition is created.


### ODR-13 — Authorization policy engine and publication protocol

**Question:** Which policy engine, runtime binding and policy publication/activation protocol should implement the future authorization decision point?

Research candidates: Cedar Rust 4.15.0 and OPA 1.22.4 (as observed 18 November 2026). Cedar offers an authorization-specific model and schema validation but skips individual policy evaluation errors; OPA supports embedded Go evaluation and signed bundles but has application-defined decision semantics, undefined-result behaviour and eventually consistent bundle rollout. Both require an IDEAL-owned fail-closed wrapper and exact policy/schema/bundle digest binding. CedarJava is a separate binding with its own security advisories.

Required evidence before decision:
- final trusted-core language/runtime and host topology;
- tested wrapper semantics for missing, undefined, malformed and diagnostic/error responses;
- signed immutable policy publication, monotonic generation, revocation and rollback rules;
- policy/schema digest binding to action admission and dispatch;
- negative tests, resource limits, deterministic replay and audit integration;
- binding-specific licence, maintenance, vulnerability and compatibility review.

Status: DEFERRED until the architecture baseline and runtime/topology evidence are ready. This research entry creates no engine selection or execution permission. See [Policy Engine Evaluation](IDEAL_POLICY_ENGINE_EVALUATION.md).
