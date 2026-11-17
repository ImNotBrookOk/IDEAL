# IDEAL Phase 02 Integrated Architecture Consistency and Adversarial Review

**Status:** Internal desk review; provisional; independent external review still required  
**Checkpoint:** 077 — 17 November 2026  
**Scope:** Cross-document consistency, adversarial failure paths and Phase 02 architecture completeness  
**Inputs:** Requirements, decisions, roadmap, rules, architecture, four foundations, risk architecture, autonomy authority, domain map, temporal evidence, domain risk/capital, reconciliation/recovery, personal finance/tax research and prior adversarial assessments  
**Boundary:** Read-only design review and documentation. No implementation, runtime tests, external security testing, account access, credentials, paper/live execution or phase advancement.

## 1. Executive assessment

The Phase 02 design has moved beyond an isolated crypto-perpetual test engine. It now defines a private integrated financial-intelligence system with bounded domains, four shared protective foundations, explicit owner authority, evidence provenance, domain-specific capital semantics and verified recovery.

The architecture is materially more coherent than the earlier standalone risk/engine design. The most important invariants are consistent across the current core documents:
- owner authority is explicit and bounded;
- D-023 permits only future in-envelope autonomy and does not activate execution;
- no paper or live execution is authorised;
- risk, data integrity, health and security retain distinct authority;
- each domain owns its canonical state;
- cross-domain portfolio views are read-only by default;
- data time, availability, correction and quality are explicit;
- unknown external state remains conservative;
- restore does not restore authority;
- tax reserves cannot lock capital under D-018;
- Phase 02 remains active and Phases 03–19 remain locked.

**Assessment:** The technology-neutral architecture is substantially specified, but Phase 02 is not complete. The remaining blockers are detailed below. No implementation stack can yet be responsibly frozen, and no execution capability is authorised.

## 2. Review method and limitations

This was a cross-document desk review of current GitHub default-branch files and read-back-verified checkpoints 071–076. It checks semantic consistency, authority separation, failure paths, state ownership and whether important invariants map to future tests.

It is not an independent external architecture review, penetration test, formal verification, runtime test, legal opinion, accounting opinion or venue/bank integration test. No code was executed. Absence of a detected contradiction is not proof of correctness or security.

## 3. Cross-document consistency matrix

| Area | Current disposition | Evidence / remaining work |
|---|---|---|
| Project identity and scope | Consistent | README, REQUIREMENTS, ROADMAP, D-001; crypto perpetual futures remains only active market domain |
| Phase/approval gates | Consistent after checkpoint 075 | RULES, ROADMAP, D-015/D-022; Phase 02 architecture-only, Phases 03–19 locked |
| Paper/live execution wording | Corrected | RULES now prohibits both; REQUIREMENTS and ARCHITECTURE mark paper simulator future/not authorised |
| D-023 autonomy | Consistent at design level | Authority architecture and closure assessment; no envelope active or implementation approved |
| Four pillars | Consistent | Core Protection, Risk, Data/Health, Security; separate authority and scoped interlocks |
| Health vs security | Consistent | Health restrictive only; separate security incident-response authority; common-host compromise remains |
| Domain boundaries | Consistent at logical level | Bounded-context catalogue; canonical state owned by each context; physical boundaries not selected |
| Data temporal semantics | Consistent at conceptual level | Bitemporal and point-in-time contracts; provider-specific availability guarantees remain open |
| Capital semantics | Consistent at conceptual level | Domain risk/capital architecture; D-006 denominator and D-008 flow semantics unresolved |
| Cross-domain aggregation | Consistent | Read-only projection; no implicit netting, collateral portability, hedge credit or capital reallocation |
| Personal finance | Consistent with proposal status | F-004/D-017 remain proposed; Akahu path not selected; no bank connection |
| Tax intelligence | Consistent with D-018 | F-005 proposed; estimates informational; no filing/payment; derivatives tax classification unresolved |
| Reconciliation/recovery | Consistent at design level | Fact-specific source authority, mismatch states, recovery quarantine, pillar attestations |
| Audit and retention | Partially specified | Atomic pre-dispatch audit design exists; cross-domain retention/deletion classes and independent witness unresolved |
| Mobile/PC topology | Consistent as a preference | Phone-first UI, headless future compute; host/runtime and trust topology not selected |
| AI/learning | Consistent at proposal level | Offline research only, no self-promotion, private data excluded by default; framework/model not selected |

## 4. Adversarial scenarios and required outcomes

| ID | Severity if realised | Attack/failure path | Required architecture response | Status |
|---|---|---|---|---|
| SYS-ADV-01 | Critical | Compromised AI/strategy fabricates an action or changes its payload after approval | No credentials/network egress; exact canonical action digest; external permission enforcement; fresh risk gate | Design specified; runtime proof absent |
| SYS-ADV-02 | Critical | Revocation races with dispatch-start | Shared monotonic authority generation and serialised final dispatch boundary; UNKNOWN if already transmitted | Design specified; concurrency/crash tests absent |
| SYS-ADV-03 | Critical | Local audit/DB commit fails but adapter sends an order | Atomic intent/reservation/audit/outbox and dispatch-start transaction before network write | Design specified; durability not tested |
| SYS-ADV-04 | Critical | Lost venue acknowledgement leads to duplicate order or released reservation | Stable client IDs, UNKNOWN state, conservative reservation and authoritative reconciliation | Design specified; venue behaviour untested |
| SYS-ADV-05 | Critical | Host root/kernel compromise defeats process separation and falsifies health | Separate trust domain or dormant fail-closed response for that threat model | Physical topology unresolved |
| SYS-ADV-06 | Critical | Restored backup resurrects revoked credentials/permits or stale owner authority | Restore quarantine; independent current revocation anchor; invalidate old permits and re-attest | Design specified; anchor not selected/tested |
| SYS-ADV-07 | High | Late market-data correction leaks into historical backtest as if known then | Bitemporal history, availability cutoff, immutable dataset manifest and replay | Design specified; source-specific point-in-time fidelity unknown |
| SYS-ADV-08 | High | Provider row changes under same transaction ID and is double-posted | Preserve raw revisions, idempotency plus content/version check, reconciliation case | Design specified; no provider tests |
| SYS-ADV-09 | High | Stale bank snapshot presented as current available cash | Show source refresh/coverage; distinct ledger and provider balance; stale state visible | Design specified; provider-specific guarantees open |
| SYS-ADV-10 | High | Opposite positions across accounts are netted despite separate margin/liquidity/legal risk | Gross and net views; no implicit netting or collateral portability | Design specified; owner netting policy remains open |
| SYS-ADV-11 | High | A purported hedge fails through basis/correlation/liquidity or counterparty disruption | Hedge credit requires explicit policy and coherent stress evidence; one-leg failure scenarios | Research requirements specified; no hedge policy approved |
| SYS-ADV-12 | High | Tax estimate causes automatic capital lock or payment | D-018 prohibits lock, forced reserve and payment authority | Design/decision accepted; negative implementation tests absent |
| SYS-ADV-13 | High | CARF reporting information is treated as proof of taxable income or liability | Separate provider reporting regime, transaction facts, tax classification and IRD assessment | Design specified; instrument tax interpretation open |
| SYS-ADV-14 | High | Spot-crypto tax treatment is incorrectly applied to perpetual futures | Instrument/contract-specific classification; specialist review and effective-dated rule pack | Open; no tax treatment selected |
| SYS-ADV-15 | High | Privacy exemption for owner is assumed to exempt all cloud/AI/bank processors | Separate agency/provider obligations, data minimisation, contracts and cross-border assessment | Design specified; legal review deferred |
| SYS-ADV-16 | High | Private financial data is silently added to model training or prompt retrieval | Separate data planes, least privilege, dataset eligibility and explicit training prohibition by default | Design specified; no runtime enforcement |
| SYS-ADV-17 | High | Data source is hashed correctly but contains fabricated/incomplete data | Digest is not truth; independent source identity, plausibility, sequence and cross-source checks | Design specified; provider-level assurance varies |
| SYS-ADV-18 | High | Health supervisor is compromised and asserts HEALTHY or initiates financial action | External observation; restrictive-only health channel; separate security incident authority | Design specified; common-mode risk remains |
| SYS-ADV-19 | High | Security incident controller is abused to cancel/flatten/transfer funds | Security authority limited to identity revocation/containment; no financial side effects | Design specified; runtime permission proof absent |
| SYS-ADV-20 | High | Cross-domain projection double-counts cash, holdings, derivative notional or P&L | Domain-owned ledgers; explicit valuation and ownership; anti-double-count rules | Design specified; worked examples/tests needed |
| SYS-ADV-21 | Medium | Missing FX is treated as zero or stale FX as current | Incomplete/UNKNOWN aggregate and consumer-specific freshness gate | Design specified; thresholds open |
| SYS-ADV-22 | Medium | Retention deletion removes audit evidence or audit immutability retains disallowed private data | Data-class retention, minimised tombstones, deletion across replicas/backups/derived data | Policy and periods unresolved |
| SYS-ADV-23 | Medium | Single owner/device loss blocks recovery or encourages unsafe reset | Manual owner recovery, independent recovery root, no automatic trust reset | Design specified; device/platform procedure open |
| SYS-ADV-24 | Medium | One provider outage globally disables unrelated domains | Dependency graph and scoped blast radius; preserve unaffected capabilities only if trust is intact | Design specified; actual topology untested |

Severity describes potential consequence if the path exists; it is not a claim that a vulnerability has been demonstrated in a running system.

## 5. Residual architecture blockers

### 5.1 Trust topology and root of trust
No physical deployment topology or recovery anchor is selected. A single-host process boundary cannot protect against host root/kernel compromise. The architecture must choose an explicit threat tier: accept this residual risk and remain dormant on host compromise, or introduce a separate gateway/watchdog/recovery trust domain. This decision must be based on the actual host and cost profile.

### 5.2 Capital policy semantics
D-006's denominator remains unresolved. D-008's handling of deposits/withdrawals, multi-currency valuation, funding/fees and exact UTC day-start snapshot semantics remains incomplete. No intermediate loss limits, portfolio caps, concentration caps, leverage limits or cross-domain allocations are approved.

### 5.3 Data freshness and point-in-time fidelity
The semantics are defined, but actual thresholds and source guarantees are not. Historical feeds may not provide the original publication/availability time or correction history. Any dataset lacking these fields must carry a limited-fidelity label; it cannot be promoted as fully point-in-time accurate.

### 5.4 Cross-domain accounting and aggregation
The logical ontology is clear, but worked examples are still needed for:
- bank transfer to exchange and back;
- collateral movement versus realised profit/loss;
- spot asset plus derivative exposure on the same underlying;
- multiple accounts/venues and separate legal ownership;
- multi-currency valuation and stale FX;
- tax estimate versus assessed liability and actual cash payment;
- pending bank transactions and journal posting.

### 5.5 Tax and legal interpretation
The tax domain remains informational and proposed. Crypto perpetual tax treatment requires contract-specific New Zealand analysis. Privacy Act section 27 is conditional and does not remove third-party obligations. No legal conclusion or IRD integration is approved.

### 5.6 Retention and audit
The audit architecture has a pre-dispatch atomicity requirement for any future consequential action, but cross-domain retention classes, durations, privacy deletion, legal holds, external witness and backup expiry need a single integrated policy.

### 5.7 Independent assurance
Current review is a single-agent desk review. Phase 02 exit requires a genuinely independent challenge of architecture simplicity, security/operations and maintainability/testability, plus explicit disposition of findings. No external penetration test is authorised or required at this design stage.

## 6. Owner decisions to defer and present together

Do not interrupt the owner with interim questions. The eventual architecture pack must present the following grouped decisions with evidence and consequences:

1. **Final scope and authority:** accept the integrated domain map and exact reserved owner actions; confirm which proposed domains remain deferred.
2. **D-006/D-008:** equity denominator and daily baseline/flow semantics; no value changes implied.
3. **Risk policy:** whether any future cross-domain risk budget exists; permitted netting sets and hedge-credit principles; warning/restriction/emergency states.
4. **Capital view:** scope of assets/liabilities and accounts included; valuation and FX conventions; owner-controlled budget categories.
5. **Bank data:** private Personal App path versus no integration/manual import; acceptable freshness and terms.
6. **Tax:** whether to commission specialist NZ tax advice for perpetual contracts and future asset classes; no automatic filing/payment.
7. **Data archive:** source licences, retention, training eligibility and deletion policy.
8. **Trust topology:** initial host compromise assumption, separate gateway/watchdog/recovery anchor and acceptable availability.
9. **Authenticator/recovery:** owner approval device, key custody, loss/replacement and manual recovery.
10. **Audit:** retention classes/durations, local durability objective and optional independent witness.
11. **Architecture baseline:** approve final logical/physical architecture and decide separately whether Phase 03 may be considered.

## 7. Phase 02 completion gate

Phase 02 cannot close until:
- system/domain map and status are consistent;
- all four foundation architectures are integrated with domain contracts;
- authority, data, health, security, risk, reconciliation and recovery state machines are cross-consistent;
- exact action, event, temporal, capital and ledger semantics are complete enough to implement without hidden assumptions;
- trust boundaries and failure topology are selected or explicitly bounded;
- all material requirements map to owners, controls and future tests;
- retention/privacy/licensing policy is integrated;
- worked examples and adversarial scenarios cover cross-domain interactions;
- independent architecture/security/operations/maintainability reviews are completed and findings resolved or explicitly accepted;
- GitHub content is read-back verified;
- the owner reviews and explicitly accepts the complete architecture baseline.

Implementation blueprint research is subsequent work, not a substitute for these gates. Phase 03 remains locked until a separate explicit owner decision.

## 8. Explicit non-authorisations

No implementation, runtime integration, dependency adoption, deployment, account/venue/bank connection, credentials, real financial records, paper/live execution, tax filing/payment, external security testing, paid infrastructure or phase advancement is authorised by this review.


## Checkpoint 081 — cross-state-machine closure extension

The integrated state-machine contract now defines separate state owners, policy/identity/data/health/security/risk/reservation/action/reconciliation/recovery lifecycles, conjunctive admission, version-vector binding and restrictive precedence. It preserves the exact-action dispatch linearisation point and no-exactly-once external-effect semantics.

This closes a logical composition gap at design level, not the platform-specific implementation gaps. See [Integrated State-Machine and Cross-Authority Contract Architecture](IDEAL_INTEGRATED_STATE_MACHINE_AND_CONTRACT_ARCHITECTURE.md).


## Checkpoint 082 — logical diagram coverage

The logical domain/evidence flow, trust zones, forbidden flows, action admission/dispatch, incident/recovery and temporal evidence lineage are now represented in [IDEAL System Architecture Diagrams](IDEAL_SYSTEM_ARCHITECTURE_DIAGRAMS.md). Physical deployment/network diagrams remain open until a host topology is approved.


## Checkpoint 083 — security assurance traceability

The dedicated [Security Control and Threat Traceability Matrix](IDEAL_SECURITY_CONTROL_AND_THREAT_TRACEABILITY_MATRIX.md) maps SEC-01–SEC-14 to protected assets, 28 threat paths, control owners, future verification and residual risks. This improves traceability but does not replace independent security review or runtime evidence.


## Checkpoint 084 — simplicity and maintainability review

[IDEAL Architecture Complexity and Maintainability Review](IDEAL_ARCHITECTURE_COMPLEXITY_AND_MAINTAINABILITY_REVIEW.md) recommends preserving logical bounded contexts and independent authorities while avoiding a direct translation into many services, databases, agents or always-on infrastructure. The provisional smallest viable build is a modular monolith with one authoritative store if proven durable, deterministic services, evidence manifests and a phone-first read/control UI. No original documents were deleted or consolidated.


## Checkpoint 085 — interface contract completeness

[IDEAL Canonical Contract Catalogue](IDEAL_CANONICAL_CONTRACT_CATALOGUE.md) expands the shared interface families into 22 owner/consumer contracts and defines event envelope semantics, money/time/identity values, typed errors, compatibility and transaction boundaries. Exact wire schemas and implementation technology remain deferred.


## Checkpoint 086 — requirement traceability closure

[IDEAL Requirement → Component → Control → Test Traceability](IDEAL_REQUIREMENT_COMPONENT_CONTROL_TEST_TRACEABILITY.md) now maps stable requirement aliases to component owners, controls/contracts and future deterministic test identifiers. This closes the requirement traceability deliverable at design level; test implementation/execution and independent review remain outstanding.


## Checkpoint 088 — canonical pack map and decision inventory

[IDEAL Phase 02 Architecture Document Map](IDEAL_PHASE_02_ARCHITECTURE_DOCUMENT_MAP.md) now formalises canonical document ownership, source-of-truth precedence and the grouped unresolved-decision inventory. It does not close the review blockers or replace independent challenge. The next gate is a final integrated architecture challenge; independent architecture/security/operations and maintainability review plus owner acceptance remain required.


## Checkpoint 089 — critical contract schema completeness

Field-level logical schemas are now specified for owner envelopes, security decisions, health interlocks, risk decisions/reservations, action intents/permits, dispatch receipts, reconciliation, personal-finance imports/journal postings, tax workpapers, audit events and recovery attestations. See [Critical Contract Field Schemas](IDEAL_CRITICAL_CONTRACT_FIELD_SCHEMAS.md). No wire format or implementation is selected.


## Checkpoint 090 — owner decision consolidation

The 12 grouped owner decisions are consolidated in [IDEAL Phase 02 Owner Decision Register](IDEAL_PHASE_02_OWNER_DECISION_REGISTER.md). Existing accepted decisions are preserved; the register is draft only and does not activate domains or approve implementation. Final presentation remains gated on independent review and the full Phase 02 exit criteria.


## Checkpoint 089 — final integrated challenge

[Final Integrated Architecture Challenge](IDEAL_PHASE_02_FINAL_INTEGRATED_ARCHITECTURE_CHALLENGE.md) records ten cross-pillar findings. The shared amount contract now uses canonical fiat/crypto AssetIds, with effective-dated provider mappings and explicit stablecoin/valuation semantics; traceability adds R-CONTRACT-001 and T-ASSET-01–06. Authority/dispatch, health/security, data trust, capital autonomy and recovery remain consistent at design level. Runtime proof, independent review and owner acceptance remain open.


## Checkpoint 090 — official source revalidation

[Official Source Reference Revalidation](IDEAL_PHASE_02_SOURCE_REFERENCE_REVALIDATION.md) confirms the current Privacy Act section 27 amendment conditions, distinguishes section 11 agent processing from IPP 12, records the CARF own-benefit exclusion and conflicting IRD registration dates, and rechecks NIST and Firecracker references. Legal/tax interpretation, provider role and exact retention scope remain open; no architecture or owner policy is changed.
