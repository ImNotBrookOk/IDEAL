# IDEAL Phase 02 Architecture Document Map

**Status:** Canonical documentation ownership and navigation index; design-only  
**Checkpoint:** 088 — 17 November 2026  
**Authority:** D-015, D-018–D-023  
**Boundary:** This index does not approve implementation, dependency adoption, runtime integration, account/provider access, paper/live execution, hosting, paid infrastructure or phase advancement.

## 1. Purpose

This document establishes one navigation and ownership map for the Phase 02 architecture pack. It formalises the documentation-ownership proposal in [the complexity and maintainability review](IDEAL_ARCHITECTURE_COMPLEXITY_AND_MAINTAINABILITY_REVIEW.md), including architecture artefacts added after checkpoint 084.

It does not replace detailed evidence, rewrite historical checkpoints or consolidate/delete source documents. New substantive requirements belong in the canonical source for that concern; other documents should link to it and keep only a concise summary.

## 2. Authority and conflict precedence

When statements conflict, use this order:

1. **Accepted owner decisions:** `DECISIONS.md` (append-only; a proposal or assistant recommendation is not an accepted decision).
2. **Current phase/status and task order:** the authoritative current-state section of `ROADMAP.md`.
3. **Normative requirements and operating constraints:** `REQUIREMENTS.md` and `RULES.md`, interpreted consistently with accepted decisions.
4. **Canonical architecture/contract source:** the single primary document named in the map below.
5. **Supporting research, diagrams, matrices and summaries:** useful evidence, but not independent authority to change policy.
6. **Conversation audit records:** chronological evidence of work and decisions; never supersede the decision register.

Historical dated status statements remain historical. Do not silently rewrite them to mimic current status.

## 3. Canonical document ownership

| Concern | Canonical source | Supporting sources / role |
|---|---|---|
| Owner decisions and accepted policy | `DECISIONS.md` | Append-only decision register; proposals remain proposals |
| Current phase, task order and gates | `ROADMAP.md` | `RULES.md`, `README.md` summaries |
| Normative product/system requirements | `REQUIREMENTS.md` | Requirement traceability matrix |
| Contributor and agent constraints | `RULES.md` | `TESTING.md` for future verification discipline |
| Public project identity and navigation | `README.md` | This document map |
| Overall system and bounded contexts | [Integrated System and Bounded-Context Architecture](IDEAL_INTEGRATED_SYSTEM_AND_DOMAIN_ARCHITECTURE.md) | `ARCHITECTURE.md`, [System Architecture Diagrams](IDEAL_SYSTEM_ARCHITECTURE_DIAGRAMS.md) |
| Four foundational pillars and their integration | [Core Protection Architecture](IDEAL_CORE_PROTECTION_ARCHITECTURE.md) | [Foundation Traceability Matrix](IDEAL_FOUNDATION_TRACEABILITY_MATRIX.md) |
| Derivatives risk and initial crypto-perpetual policy | [Risk Management Architecture](IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md) | [Domain Risk and Capital Architecture](IDEAL_DOMAIN_RISK_AND_CAPITAL_ARCHITECTURE.md), [Risk Architecture Reconciliation](RISK_ARCHITECTURE_RECONCILIATION.md) |
| Domain risk/capital separation and aggregation | [Domain Risk and Capital Architecture](IDEAL_DOMAIN_RISK_AND_CAPITAL_ARCHITECTURE.md) | [Cross-Domain Accounting Examples](IDEAL_CROSS_DOMAIN_ACCOUNTING_AND_VALUATION_EXAMPLES.md) |
| Data provenance, temporal semantics and point-in-time evidence | [Data Trust and Point-in-Time Architecture](IDEAL_DATA_TRUST_TEMPORAL_AND_POINT_IN_TIME_ARCHITECTURE.md) | `DATA_INTEGRITY_AND_HEALTH.md`, historical data validation report |
| Operational health model | `DATA_INTEGRITY_AND_HEALTH.md` | [Core Protection Architecture](IDEAL_CORE_PROTECTION_ARCHITECTURE.md), risk and security architecture |
| Security requirements, trust boundaries and incident authority | [Security Architecture](IDEAL_SECURITY_ARCHITECTURE.md) | [Security Control and Threat Traceability Matrix](IDEAL_SECURITY_CONTROL_AND_THREAT_TRACEABILITY_MATRIX.md) |
| Security asset/control/threat/test mapping | [Security Control and Threat Traceability Matrix](IDEAL_SECURITY_CONTROL_AND_THREAT_TRACEABILITY_MATRIX.md) | Security Architecture; this matrix does not certify security |
| Data classification, privacy, retention and deletion | [Data Classification, Retention and Audit Policy](IDEAL_DATA_CLASSIFICATION_RETENTION_AND_AUDIT_POLICY.md) | Security Architecture |
| Owner authority, policy and bounded autonomy | [Autonomy Authority and Permission Architecture](IDEAL_AUTONOMY_AUTHORITY_AND_PERMISSION_ARCHITECTURE.md) | [Autonomy Authority Closure Assessment](IDEAL_AUTONOMY_AUTHORITY_CLOSURE_ASSESSMENT.md) |
| Cross-authority state machines and admission | [Integrated State-Machine and Contract Architecture](IDEAL_INTEGRATED_STATE_MACHINE_AND_CONTRACT_ARCHITECTURE.md) | Autonomy, risk, security and reconciliation sources |
| Cross-domain interface semantics | [Canonical Contract Catalogue](IDEAL_CANONICAL_CONTRACT_CATALOGUE.md) | Bounded-context and state-machine architecture; checkpoint 089 adds canonical fiat/crypto AssetId semantics |
| Reconciliation, incident containment and recovery | [Reconciliation and Verified Recovery Architecture](IDEAL_RECONCILIATION_AND_VERIFIED_RECOVERY_ARCHITECTURE.md) | Data Integrity and Health, Security, Risk |
| Host trust, topology and recovery options | [Host Trust Topology and Recovery Options](IDEAL_HOST_TRUST_TOPOLOGY_AND_RECOVERY_OPTIONS.md) | `INFRASTRUCTURE_RESEARCH.md`; no host is selected |
| Worked accounting and valuation examples | [Cross-Domain Accounting and Valuation Examples](IDEAL_CROSS_DOMAIN_ACCOUNTING_AND_VALUATION_EXAMPLES.md) | Personal Finance Research; examples are design fixtures, not advice or executed tests |
| Requirements to owners, controls and future tests | [Requirement Component Control Test Traceability](IDEAL_REQUIREMENT_COMPONENT_CONTROL_TEST_TRACEABILITY.md) | [Foundation Traceability Matrix](IDEAL_FOUNDATION_TRACEABILITY_MATRIX.md), security control matrix |
| Whole-system internal desk review | [Phase 02 Integrated Architecture Review](IDEAL_PHASE_02_INTEGRATED_ARCHITECTURE_REVIEW.md) | [Integrated Adversarial Review](IDEAL_INTEGRATED_ADVERSARIAL_REVIEW.md) |
| Architecture-first sequence and exit criteria | [Architecture-First Research Plan](IDEAL_ARCHITECTURE_FIRST_RESEARCH_PLAN.md) | Roadmap and this map |
| Complexity, simplicity and maintainability constraints | [Architecture Complexity and Maintainability Review](IDEAL_ARCHITECTURE_COMPLEXITY_AND_MAINTAINABILITY_REVIEW.md) | This map formalises its proposed document ownership |
| Execution-quality research and simulator evidence | `EXECUTION_QUALITY_RESEARCH.md` and `research/nautilus_poc/` | Research only; not venue calibration or engine adoption |
| Venue and market-data research | `EXCHANGE_AND_DATA_SHORTLIST.md`, `HISTORICAL_L2_SAMPLE_VALIDATION.md` | Conditional research evidence; no venue/account selected |
| Personal finance and tax research | `PERSONAL_FINANCE_RESEARCH.md` | Proposed future domain; no bank/tax provider connection or filing/payment |
| Conversation/audit chronology | `docs/CHATGPT_CONVERSATIONS/README.md` | Individual dated checkpoint records; append-only evidence |

## 4. Phase 02 architecture pack contents

The architecture pack is logically complete enough for a final integrated challenge, but not accepted or implementation-ready. Its evidence layers are:

- **Governance:** decisions, requirements, roadmap, rules and explicit non-authorisations.
- **System definition:** domain/context ownership, active versus deferred scope, system diagrams and complexity constraints.
- **Four foundations:** risk, data integrity, health and security with independent authority and bounded interlocks.
- **Cross-pillar control:** owner authority, identity, policy, revocation, state-machine composition, canonical contracts and action/transaction boundaries.
- **Financial integrity:** domain-specific risk/capital semantics, accounting examples, reconciliation and recovery.
- **Operational trust:** host threat assumptions, backup/recovery, audit, privacy, retention and data rights.
- **Assurance:** requirement/control/test traceability, security threat traceability, internal adversarial review and future deterministic test catalogue.
- **Evidence history:** dated checkpoint records and source research.

## 5. Consolidated unresolved-decision inventory

This is an inventory for eventual grouped owner review, not a request for decisions now. No default or assistant recommendation in this list is an owner-approved choice.

### A. Scope, authority and domain activation
- Confirm final active/deferred domain map and exact owner-reserved actions.
- Confirm the exact authority/envelope semantics and activation/recovery boundaries.
- Preserve D-001 crypto-perpetual-only active market scope unless the owner changes it through a new decision.

### B. Derivatives risk policy
- D-006 equity denominator and exact risk-sizing basis.
- D-008 UTC day-start snapshot, deposits/withdrawals, multi-currency valuation, funding/fees and reset semantics.
- Any additional warning/suspension thresholds, portfolio/concentration/leverage caps, and approved netting/hedge-credit rules.
- No numerical risk parameter is changed by this inventory.

### C. Capital, accounting and personal finance
- Included assets, liabilities, accounts and ownership boundaries in any future consolidated view.
- FX source/side/freshness, valuation basis and treatment of incomplete values.
- Whether to use manual imports only or later assess a private Personal App data path; provider terms, freshness and legal role must be verified first.
- Budget categories remain owner-controlled; D-018 prohibits tax-estimate-driven capital locks or forced payments.

### D. Tax and legal interpretation
- Whether to commission specialist New Zealand advice for crypto perpetual contract classification and any future asset classes.
- Provider/processor roles, cross-border processing, retention and legal obligations before any external connection.
- No tax classification, filing, payment or legal conclusion is selected here.

### E. Data, archive and learning
- Source-specific point-in-time availability, sequence continuity, corrections, freshness thresholds and permitted-use/licence constraints.
- Archive retention/deletion classes and whether any data may be used for model training; private financial data remains excluded by default.
- Cross-vendor comparison and representative fill/impact calibration remain unproven.

### F. Security, host trust and recovery
- Host-root/kernel compromise threat tier and whether a separate gateway/watchdog/recovery trust domain is required from day one.
- Owner authenticator, root/recovery key custody, loss/replacement and manual recovery procedure.
- Independent revocation anchor and measured revocation propagation objective.
- Workload identity, sandbox and egress enforcement depend on actual host/runtime capabilities.

### G. Storage, contracts and audit
- Transactional store, single-writer topology, WAL/fsync/durability and restore semantics.
- Exact contract canonicalisation, schema/serialization, monetary/quantity/time types and error-code mapping.
- Audit retention classes/durations, legal holds, deletion interactions and optional independent witness.
- Worker inventory completeness and proof that all dispatch boundaries are fenced.

### H. Assurance and phase acceptance
- Independent architecture, security/operations and maintainability/testability reviews.
- Disposition of each finding with evidence, severity, owner and residual-risk treatment.
- Owner acceptance of the complete Phase 02 architecture baseline.
- Separate explicit owner decision before any Phase 03 consideration; no automatic phase transition.

## 6. Evidence and verification status

- Core local document targets in this map were checked against the current GitHub `main` tree; the canonical sources were fetched back for read-back inspection during checkpoint 088.
- The conversation audit index and checkpoint records through 087 are present in the repository.
- This was a scoped manual cross-reference/read-back check, not a full automated link crawler across every Markdown file.
- External source URLs remain recorded in their owning research/architecture documents. This checkpoint does not claim that every external URL, current legal interpretation or provider term was revalidated live.
- No runtime tests, security scans, penetration tests, recovery drills or implementation verification were performed.

## 7. Next gate

The next task is a final integrated architecture challenge against this map, the current requirements, canonical contracts, four foundations, threat matrix, failure/recovery paths and unresolved-decision inventory. The challenge must identify contradictions, unowned responsibilities, ambiguous authority, missing negative tests and residual risks. It must not silently close open decisions.

Only after that challenge and independent review are complete should the grouped owner decision pack be presented. Phase 02 remains active; Phases 03–19 remain locked.


## 8. Final integrated challenge — checkpoint 089

[Final Integrated Architecture Challenge](IDEAL_PHASE_02_FINAL_INTEGRATED_ARCHITECTURE_CHALLENGE.md) records the cross-pillar challenge and the corrected asset-denomination gap. It distinguishes design consistency from runtime proof and lists remaining blockers. Independent review and owner acceptance remain outstanding.


## 9. Official source register — checkpoint 090

The dated [Official Source Reference Revalidation](IDEAL_PHASE_02_SOURCE_REFERENCE_REVALIDATION.md) records current primary-source positions for NZ Privacy Act sections 11/27 and IPP 12, IRD cryptoasset records/CARF/tax-bill status, NIST key-management/crypto-agility guidance and Firecracker host hardening. External URLs and legal/provider facts must be rechecked before implementation or provider selection.


## 10. Current architecture pack refresh — checkpoint 093

Additional canonical sources added after the original checkpoint 088 map:

| Concern | Canonical source | Supporting sources / role |
|---|---|---|
| Data freshness and clock quality | [Data Freshness, Clock Quality and Decision-Validity Requirements](IDEAL_DATA_FRESHNESS_AND_CLOCK_REQUIREMENTS.md) | Data Trust architecture; source-specific consumer fitness |
| Critical field-level logical schemas | [Critical Contract Field Schemas](IDEAL_CRITICAL_CONTRACT_FIELD_SCHEMAS.md) | Canonical Contract Catalogue; no wire format selected |
| Consolidated owner decisions | [Phase 02 Owner Decision Register](IDEAL_PHASE_02_OWNER_DECISION_REGISTER.md) | Draft only; not presented for approval |
| Official primary-source revalidation | [Phase 02 Source Reference Revalidation](IDEAL_PHASE_02_SOURCE_REFERENCE_REVALIDATION.md) | NZ Privacy/IRD, NIST and Firecracker source status |
| Final integrated architecture challenge | [Final Integrated Architecture Challenge](IDEAL_PHASE_02_FINAL_INTEGRATED_ARCHITECTURE_CHALLENGE.md) | Internal challenge; independent review remains open |

The canonical contract and critical field schemas now consistently require AssetId for all fiat/crypto-denominated amounts. Fiat may map to ISO 4217; crypto-native assets and tokens require canonical identities including network/contract where applicable and effective-dated provider/venue symbol mappings. Stablecoins are distinct assets; no par assumption is permitted. The final challenge's T-ASSET-01–06 remain future tests, not executed evidence.

The audit index now contains checkpoints through 093. The checkpoint 088 and 089 entries remain historical and retain their original meaning; later work is numbered 090–093. Older duplicate audit paths from the numbering correction are retained with explicit supersession notes for continuity.

The architecture pack remains design-level. Independent architecture/security/operations and maintainability/testability reviews, finding disposition, owner acceptance and separate implementation approval remain outstanding. Phase 02 active; Phases 03–19 locked.


## 11. Infrastructure revalidation — checkpoint 094

The infrastructure evidence pack now includes a dated revalidation of SQLite WAL durability, NautilusTrader persistence boundaries, Firecracker production host controls and OCI Always Free quota/capacity caveats:

- [Infrastructure Research](INFRASTRUCTURE_RESEARCH.md) owns the component/hosting evidence and POC caveats.
- [Component Selection Matrix](COMPONENT_SELECTION_MATRIX.md) owns candidate dispositions and adoption gates.
- [Host Trust Topology and Recovery Options](IDEAL_HOST_TRUST_TOPOLOGY_AND_RECOVERY_OPTIONS.md) owns host and trust-domain trade-offs.
- [Core Protection Architecture](IDEAL_CORE_PROTECTION_ARCHITECTURE.md) owns cross-foundation implications.

Checkpoint 094 changes no owner-approved component disposition. SQLite, NautilusTrader, Firecracker and OCI A1 remain candidates with explicit gates; no host or runtime is selected. Phase 02 remains active.


## 11. Infrastructure revalidation — checkpoint 094

The infrastructure evidence pack now includes dated revalidation of SQLite WAL durability, NautilusTrader persistence boundaries, Firecracker production host controls and OCI Always Free quota/capacity caveats:

- [Infrastructure Research](INFRASTRUCTURE_RESEARCH.md) owns component/hosting evidence and POC caveats.
- [Component Selection Matrix](COMPONENT_SELECTION_MATRIX.md) owns candidate dispositions and adoption gates.
- [Host Trust Topology and Recovery Options](IDEAL_HOST_TRUST_TOPOLOGY_AND_RECOVERY_OPTIONS.md) owns host and trust-domain trade-offs.
- [Core Protection Architecture](IDEAL_CORE_PROTECTION_ARCHITECTURE.md) owns cross-foundation implications.

Checkpoint 094 changes no owner-approved component disposition. SQLite, NautilusTrader, Firecracker and OCI A1 remain candidates with explicit gates; no host or runtime is selected. Phase 02 remains active.


## 12. Workload isolation comparison — checkpoint 095

[Host Trust Topology and Recovery Options](IDEAL_HOST_TRUST_TOPOLOGY_AND_RECOVERY_OPTIONS.md) and [Infrastructure Research](INFRASTRUCTURE_RESEARCH.md) now compare gVisor, Kata Containers and Firecracker from their official security/architecture documentation. No runtime is selected; the decision remains dependent on the actual threat model, host platform, workload compatibility and ability to operate the controls.


## 13. Authorization policy engine evidence — checkpoint 096

[Policy Engine Evaluation](IDEAL_POLICY_ENGINE_EVALUATION.md) owns the Cedar vs OPA comparison, current release/advisory revalidation, fail-closed wrapper requirements, signed policy publication and future acceptance tests. No engine or binding is selected; the decision is deferred under ODR-13 until the trusted-core runtime and deployment topology are known.


## 14. Owner authenticator and recovery evidence — checkpoint 097

[Owner Authenticator and Recovery Options](IDEAL_OWNER_AUTHENTICATOR_AND_RECOVERY_OPTIONS.md) owns the WebAuthn BE/BS and origin-binding model, Android Keystore/StrongBox constraints, device-bound versus synced credential trade-offs, action-digest-bound approval ceremony, key-role separation and recovery lifecycle. ODR-10 remains open; no authenticator or vendor selected.


## 15. Audit integrity and external witness evidence — checkpoint 098

[Audit Integrity and External Witness Options](IDEAL_AUDIT_INTEGRITY_AND_EXTERNAL_WITNESS_OPTIONS.md) owns the local hash/Merkle versus independent checkpoint distinction, Rekor/Tessera/Trillian/immudb comparison, privacy implications, witness trust boundary and recovery verification requirements. ODR-11 remains open; no database, log or witness selected.


## 16. Margin, collateral and liquidation — checkpoint 099

[Margin, Collateral and Liquidation Architecture](IDEAL_MARGIN_COLLATERAL_AND_LIQUIDATION_ARCHITECTURE.md) owns the canonical margin/collateral model, tiered IM/MM, mark/index/last separation, collateral eligibility/haircuts, multi-currency valuation, portfolio stress/hedge-credit boundaries, order reservations, liquidation lifecycle, failure behaviour and verification plan. It extends [Risk Management Architecture](IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md) §27. ODR-02/03 remain open; ODR-04 remains deferred; no venue or margin mode selected.


## 17. Integrated challenge refresh — checkpoint 100

[Final Integrated Architecture Challenge](IDEAL_PHASE_02_FINAL_INTEGRATED_ARCHITECTURE_CHALLENGE.md) was reopened after checkpoints 096–099. Checkpoint 100 corrected a section-numbering defect and integrated margin/collateral logical schemas, liquidation/reservation state composition and requirement-to-test traceability. Eight findings are recorded. Independent review remains outstanding; this is not Phase 02 closure.
