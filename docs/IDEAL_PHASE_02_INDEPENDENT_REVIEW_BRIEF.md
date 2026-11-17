# IDEAL Phase 02 — Independent Architecture Review Brief

**Status:** Prepared for independent read-only review; no reviewer has been engaged  
**Checkpoint:** 091 — 17 November 2026  
**Authority:** D-022; Phase 02 research/design only  
**Review type:** Independent architecture, security/operations, and maintainability/testability challenge

## 1. Purpose

This brief defines the independent review required before the Phase 02 architecture baseline can be presented for owner acceptance. The current internal challenge is not independent assurance. A reviewer must be materially independent of the authoring/reviewing agent and must assess the source documents directly rather than merely endorse checkpoint conclusions.

No reviewer is appointed by this document. No external reviewer is contacted, no project data is disclosed externally, and no review result is presumed.

## 2. Review boundaries

The reviewer must:
- perform read-only analysis of the specified repository documents;
- make no code, configuration, dependency, infrastructure or documentation changes;
- execute no application code, tests, scans, penetration tests or external probes;
- use no credentials, accounts, private financial records or external services;
- treat all proposals and assistant recommendations as non-authoritative unless recorded as accepted in `DECISIONS.md`;
- make no owner policy, risk-limit, domain-activation or phase-advancement decisions;
- identify evidence gaps and uncertainty rather than infer that a control works because it is documented.

This is an architecture/design review, not legal, tax, accounting, penetration-testing or certification work.

## 3. Independence protocol

To reduce confirmation bias:

1. **First pass — blind challenge:** provide the canonical source set in §4, but do not provide checkpoint 089's finding dispositions or any suggested conclusions. The reviewer independently identifies strengths, contradictions, omissions, failure paths and residual risks.
2. **Structured output:** every finding must cite a file and section/heading, map to a requirement/control/contract where possible, and state why the current design is insufficient or adequate.
3. **Second pass — reconciliation:** only after the first-pass report is frozen should the reviewer receive the internal integrated challenge and source-revalidation report. They then mark each internal finding as agree, disagree, partially agree or new, with evidence.
4. **No forced consensus:** disagreement is preserved with evidence and owner decision impact. Findings are not closed by wording changes alone.

A reviewer should disclose prior involvement, tool/model used, scope limitations, conflicts of interest and whether any automated assistance was used. If a second AI model is used, record model/version/date and avoid claiming that model diversity alone proves independence.

## 4. Canonical evidence pack

Read these sources first:

### Governance and requirements
- `DECISIONS.md`
- `REQUIREMENTS.md`
- `ROADMAP.md`
- `RULES.md`
- `ARCHITECTURE.md`

### System and four foundations
- `docs/IDEAL_INTEGRATED_SYSTEM_AND_DOMAIN_ARCHITECTURE.md`
- `docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md`
- `docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md`
- `docs/IDEAL_DATA_TRUST_TEMPORAL_AND_POINT_IN_TIME_ARCHITECTURE.md`
- `DATA_INTEGRITY_AND_HEALTH.md`
- `docs/IDEAL_SECURITY_ARCHITECTURE.md`
- `docs/IDEAL_DOMAIN_RISK_AND_CAPITAL_ARCHITECTURE.md`

### Authority, contracts and recovery
- `docs/IDEAL_AUTONOMY_AUTHORITY_AND_PERMISSION_ARCHITECTURE.md`
- `docs/IDEAL_INTEGRATED_STATE_MACHINE_AND_CONTRACT_ARCHITECTURE.md`
- `docs/IDEAL_CANONICAL_CONTRACT_CATALOGUE.md`
- `docs/IDEAL_RECONCILIATION_AND_VERIFIED_RECOVERY_ARCHITECTURE.md`
- `docs/IDEAL_DATA_CLASSIFICATION_RETENTION_AND_AUDIT_POLICY.md`
- `docs/IDEAL_HOST_TRUST_TOPOLOGY_AND_RECOVERY_OPTIONS.md`

### Assurance and examples
- `docs/IDEAL_SYSTEM_ARCHITECTURE_DIAGRAMS.md`
- `docs/IDEAL_SECURITY_CONTROL_AND_THREAT_TRACEABILITY_MATRIX.md`
- `docs/IDEAL_FOUNDATION_TRACEABILITY_MATRIX.md`
- `docs/IDEAL_REQUIREMENT_COMPONENT_CONTROL_TEST_TRACEABILITY.md`
- `docs/IDEAL_CROSS_DOMAIN_ACCOUNTING_AND_VALUATION_EXAMPLES.md`
- `docs/IDEAL_ARCHITECTURE_COMPLEXITY_AND_MAINTAINABILITY_REVIEW.md`

The [canonical architecture document map](IDEAL_PHASE_02_ARCHITECTURE_DOCUMENT_MAP.md) is the navigation and ownership index. Supporting research may be consulted where a claim depends on a specific source, but historical checkpoint summaries must not replace canonical documents.

## 5. Independent review lanes

### A. Architecture simplicity and pattern fit

Challenge:
- whether logical bounded contexts have been separated without overbuilding physical services;
- whether a modular monolith and one transactional store remain a defensible provisional direction;
- whether each state machine has a distinct owner without creating distributed coordination unnecessarily;
- whether event sourcing/outbox/brokers are applied only at justified boundaries;
- whether dependencies, failure domains and blast radii are explicit;
- whether future domains are represented without implicit activation;
- whether the architecture can be operated by one owner at low recurring cost.

Deliver: unnecessary complexity, missing boundary, simpler viable alternative, trade-offs and evidence.

### B. Security and operations

Challenge:
- owner/root trust, authenticator loss, key-role separation, policy publication and rollback;
- workload identity, least privilege, prompt injection, tool/IPC boundaries and egress control;
- host root/kernel compromise, VM/jailer limitations, physical gateway and watchdog independence;
- dispatch/revocation races, duplicate/uncertain remote outcomes and credential revocation;
- audit integrity, backup/restore, anti-rollback, incident containment and recovery release;
- privacy, processor/subprocessor use, deletion, legal holds and supply-chain risk;
- health supervisor versus security incident authority and common-mode failure.

Deliver: attack path, preconditions, blast radius, existing control, bypass/failure mode, required negative test and residual risk.

### C. Maintainability and testability

Challenge:
- requirement ownership and requirement-to-control-to-test coverage;
- contract completeness, semantic precision, compatibility/versioning and migration;
- deterministic state transitions, idempotency, replay and failure injection;
- financial amount/asset identity, FX, time, rounding and ledger semantics;
- observability, audit evidence, operator runbooks and recovery testability;
- documentation ownership, source traceability and drift prevention;
- whether acceptance criteria can be verified without hidden assumptions.

Deliver: untestable or ambiguous requirement, missing test oracle, coupling, migration hazard, documentation drift risk and proposed acceptance evidence.

## 6. Required challenge scenarios

At minimum, test the architecture on paper against:
1. Revocation and dispatch-start race at every transaction/crash boundary.
2. Local DB/audit failure immediately before or after a network write.
3. Exchange accepts an order but acknowledgement is lost; duplicate retry follows.
4. Partial fill, cancel race, residual reservation and position transfer.
5. Host root compromise while the health supervisor reports healthy.
6. Restoring a backup created before key/policy revocation.
7. Owner device loss while the independent recovery anchor is unavailable.
8. Late/corrected market data leaking into a historical as-known-then backtest.
9. Provider changes a transaction under the same ID; pending/posting/deletion/transfer overlap.
10. BTC, fiat, stablecoin and network-specific token balances in one portfolio view; missing/stale FX and depeg.
11. D-006 and D-008 under deposits, withdrawals, funding, fees and multi-currency equity.
12. Security incident response attempts to cancel, flatten, transfer or otherwise cause financial side effects.
13. AI agent prompt injection attempts secret access, policy change, or direct dispatch.
14. Privacy deletion request conflicts with audit retention, backup and legal hold.
15. A provider uses submitted financial data for its own model training or cross-customer purpose.
16. One failed provider/control causes unnecessary global shutdown or leaves a dependent action unblocked.

## 7. Finding format

Every finding must include:

| Field | Required content |
|---|---|
| Finding ID | Stable reviewer-specific identifier |
| Severity | Critical / High / Medium / Low with rationale |
| Evidence | Exact file and section/heading; quote only what is needed |
| Requirement/control | Requirement, contract, threat or invariant affected |
| Scenario | Concrete misuse/failure and preconditions |
| Current design | Existing control and its claimed boundary |
| Assessment | Why it is adequate, insufficient, contradictory or untestable |
| Recommendation | Minimum change that resolves or bounds the issue |
| Verification | Future deterministic test/evidence required |
| Residual risk | What remains even after the recommendation |
| Confidence | High / Medium / Low and why |
| Owner impact | Whether a reserved owner decision is needed; do not make it |

Classify each item as defect, omission, ambiguity, evidence gap, accepted residual risk candidate, or non-issue. Avoid vague findings such as “needs more security”.

## 8. Acceptance criteria for the review

The review is complete only when:
- all three lanes have a written report and declared scope/limitations;
- every Critical/High finding has an evidence-backed disposition;
- no requirement lacks an owner, control path and future verification method;
- no consequential action has an unowned authority or dispatch boundary;
- residual risks are explicit and grouped for owner acceptance;
- any proposed architecture change is evaluated for cost, complexity, security and maintainability;
- findings are reconciled without weakening accepted controls;
- the owner receives a concise grouped decision pack with evidence and consequences.

The review does not itself approve architecture, implementation, Phase 03 or execution.

## 9. Next step

The project needs a genuinely independent reviewer or reviewers. Until that review is performed and findings are reconciled, IDEAL must not describe Phase 02 as complete or present the grouped owner decision pack as final. Phase 02 remains active; Phases 03–19 remain locked.
