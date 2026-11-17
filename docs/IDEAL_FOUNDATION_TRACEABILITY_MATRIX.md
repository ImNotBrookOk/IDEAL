# IDEAL Integrated Foundation Traceability Matrix

**Status:** Phase 02 working design; owner acceptance pending  
**Date:** 17 November 2026  
**Scope:** Integrated risk management, data integrity, system health and security  
**Authority:** Architecture research only. No implementation, runtime integration, external scanning, account access, paper/live execution, dependency adoption or phase advancement is authorised.

## 1. Purpose

This matrix translates the four owner-approved foundational directions (D-019, D-020 and D-021, together with the core-protection architecture) into system-level requirements, accountable components, interfaces and future verification evidence.

It complements the risk-specific RM-01–RM-20 matrix in [Risk Architecture Reconciliation](RISK_ARCHITECTURE_RECONCILIATION.md). It does not replace the detailed foundation designs or freeze API schemas.

A requirement is not complete merely because a component exists or a dashboard is green. Each requirement needs an accountable owner, a defined contract, observable evidence, a failure response and a reproducible verification method.

## 2. Foundational ownership

| Foundation | Primary responsibility | Authority it may exercise | Explicitly excluded authority |
|---|---|---|---|
| Risk management | Financial exposure, policy evaluation, reservations, restrictions and risk-state transitions | Approve/reject/restrict a specific action under owner-approved policy | Authenticate identities, establish source truth, certify health, execute actions |
| Data integrity | Source identity, provenance, validation, quality/freshness, correction lineage and reconciliation evidence | Accept, quarantine, classify or invalidate evidence for defined consumers | Set financial limits, grant permissions, approve actions |
| System health | Independent observation, dependency status, watchdogs, alerting, scoped interlocks and recovery evidence | Trigger predefined restrictive interlocks and escalation | Change financial policy, approve actions, initiate financial actions or grant permissions |
| Security | Identity, authentication, authorisation, secrets, trust boundaries, policy protection, incident response | Permit/deny access and tool/action capability within owner-defined authority | Set financial risk appetite, establish market truth or approve trades |

**Separation invariant:** No foundation may be the sole authority for certifying its own correctness. Cross-pillar consumers must independently validate the evidence and authority they rely on.

## 3. System-level requirements and traceability

Status labels:
- **Documented:** design direction exists in current foundation documents.
- **Partial:** principle exists, but operational semantics, interface or evidence criteria remain incomplete.
- **Open:** a material design decision or testable contract is not yet specified.

| ID | Foundation | Requirement | Accountable owner | Cross-pillar dependency | Future verification evidence | Status |
|---|---|---|---|---|---|---|
| GOV-01 | Governance | No activity exceeds explicit owner-approved scope or phase authority | Governance | Security, Risk, all domains | Negative tests and governance audit show unauthorised action paths absent | Documented |
| GOV-02 | Governance | Recommendations, warnings and model outputs do not imply financial authority | Governance | Risk, Security, AI/tooling | Attempted implicit action/permission escalation denied and audited | Documented |
| RSK-01 | Risk | Every exposure-increasing action passes independent deterministic risk evaluation | Risk | Data, Health, Security | Reject/approve boundary and bypass tests | Partial |
| RSK-02 | Risk | Risk decision is bound to exact actor, action, parameters, account scope, evidence and policy version | Risk | Security, Data, Audit | Payload mutation, replay, expiry and revocation tests | Partial |
| RSK-03 | Risk | Working orders and uncertain order states consume conservative risk capacity | Risk | Data, future Adapter, Audit | Concurrent orders, partial fills, unknown ack/cancel, restart and replay tests | Partial |
| RSK-04 | Risk | Capital, margin, collateral, P&L, funding and FX measures remain semantically distinct | Risk | Data, ledger/accounting | Multi-currency, haircut, cash-flow and independent-oracle tests | Partial |
| RSK-05 | Risk | Portfolio stress includes liquidity, concentration, correlation, funding, basis and operational scenarios | Risk | Data, Research, Health | Scenario suite with coherent portfolio shocks and close-out assumptions | Partial |
| RSK-06 | Risk | Loss/drawdown controls resist reset, flow distortion and restart | Risk | Data, Audit, Health | UTC rollover, deposit/withdrawal, restart and policy-change tests | Partial |
| RSK-07 | Risk | Emergency restrictions and financial actions are separate and explicitly governed | Risk | Security, Health, Operator | Each action tested independently, including manual fallback | Open |
| DAT-01 | Data | Every decision-critical observation has source identity, provenance, event/retrieval/ingest timestamps and lineage | Data | Security, Risk, Audit | Missing/forged provenance and lineage reconstruction tests | Partial |
| DAT-02 | Data | Freshness and completeness are consumer-, source-, instrument- and session-specific | Data | Risk, Health | Stale, delayed, gap, out-of-order and session-boundary tests | Partial |
| DAT-03 | Data | Invalid, contradictory, incomplete or ambiguous observations are quarantined or explicitly classified | Data | Risk, Health | Fault injection and cross-source conflict tests | Partial |
| DAT-04 | Data | Corrections, deletions, cancellations and replacements are versioned, not silently overwritten | Data | Audit, Research | Replay before/after correction reproduces both historical states | Partial |
| DAT-05 | Data | Historical research uses point-in-time universe, instrument rules, source data and feature/label lineage | Data, Research | Risk, Security | Leakage, delisting, revision and look-ahead challenge suite | Partial |
| DAT-06 | Data | Financial events and time-varying valuations are distinct and cannot double-count P&L | Data/Ledger | Risk, Personal Finance (future) | Independent ledger reconciliation and duplicate-event tests | Open |
| DAT-07 | Data | Data use respects source licence, entitlement, privacy, retention and deletion constraints | Data governance | Security, Legal review | Entitlement/retention audit and prohibited-use tests | Partial |
| HLT-01 | Health | A separate supervisor observes critical components and dependencies independently | Health | Security, Data, Risk | Supervisor outage, false heartbeat and common-mode tests | Partial |
| HLT-02 | Health | Health state distinguishes healthy, degraded, stale, unavailable and unknown | Health | Data, Security, Risk | State-transition and stale-telemetry tests | Partial |
| HLT-03 | Health | Failures restrict only dependent activities unless a system-wide invariant is compromised | Health | All foundations/domains | Fault-injection matrix proves bounded blast radius | Partial |
| HLT-04 | Health | Backup, restore and recovery status is verified, not inferred from job success | Health | Data, Security, Audit | Restore drills, integrity checks and recovery-point verification | Partial |
| HLT-05 | Health | Security posture remains a separate assurance status from operational health | Health + Security | Audit | Compromised-but-available simulations do not report secure/green | Documented |
| HLT-06 | Health | Interlocks are restrictive only; health cannot approve actions or change financial policy | Health | Risk, Security | Attempted policy/approval mutation denied; interlock audit | Documented |
| SEC-01 | Security | Every human, service, agent and integration has an explicit identity and scoped permission | Security | All foundations | Unauthenticated, unauthorised and privilege-escalation tests | Partial |
| SEC-02 | Security | Authentication does not imply authorisation; deny by default and least privilege apply | Security | Risk, Health, Data | Resource-level permission matrix and negative tests | Partial |
| SEC-03 | Security | Secrets and encryption keys have separate lifecycle, rotation, revocation and recovery controls | Security | Health, Audit, Data | Rotation, revocation, stale-token and recovery exercises | Partial |
| SEC-04 | Security | Sensitive data is minimised, encrypted, access-controlled and excluded from ordinary logs/prompts | Security | Data, AI/tooling | Log/prompt/export inspection and access tests | Partial |
| SEC-05 | Security | Dependencies, source, build artefacts and CI/CD have provenance and integrity controls | Security | Engineering, Health | Dependency/secret scans, signed artefact and reproducible-build evidence | Partial |
| SEC-06 | Security | AI, retrieved content and external documents are untrusted; tools enforce permissions outside the model | Security | AI/tooling, Risk, Data | Prompt-injection and tool-abuse tests; sandbox escape challenge | Partial |
| SEC-07 | Security | Vulnerability discovery, triage, remediation, exception and disclosure lifecycle is defined | Security | Health, Engineering | Finding-to-fix traceability, SLA/severity policy and retest evidence | Partial |
| SEC-08 | Security | Incident response preserves evidence, scopes compromise, revokes trust and verifies recovery | Security | Health, Data, Risk | Tabletop and technical recovery exercises | Partial |
| AUD-01 | Audit | Consequential decisions and control transitions are attributable, ordered, durable and tamper-evident | Audit/Security | All foundations | Deletion/reordering/tamper and sink-outage tests | Partial |
| AUD-02 | Audit | Audit evidence excludes secrets and unnecessary personal/financial raw data | Audit/Security | Data, Privacy | Redaction, access and retention tests | Partial |
| XPL-01 | Cross-pillar | Shared event envelope identifies actor, source, event time, ingest time, schema, correlation and idempotency | Architecture | All foundations | Contract/schema conformance and replay tests | Open |
| XPL-02 | Cross-pillar | Clock, ordering, sequence and freshness semantics are explicit | Architecture/Data | Risk, Health, Security, Audit | Clock drift, skew, replay and ordering tests | Open |
| XPL-03 | Cross-pillar | Failure propagation and safe states are defined per dependency and action class | Architecture/Health | Risk, Data, Security | Dependency fault matrix and blast-radius tests | Partial |
| XPL-04 | Cross-pillar | Recovery re-establishes data, permissions, policy, audit and external state before release | Architecture | All foundations | Clean rebuild, reconciliation and staged-release evidence | Partial |
| XPL-05 | Cross-pillar | Policy changes are attributable, versioned, authorised and protected from runtime/AI mutation | Security + Risk | Audit, Governance | Signature, approval and prohibited-writer tests | Partial |
| XPL-06 | Cross-pillar | Every critical interface defines ownership, schema, units, version, permission, freshness, errors, timeout, idempotency and recovery | Architecture | All foundations | Contract review and negative conformance suite | Open |

## 4. Critical interface contracts still required

These are conceptual boundaries, not frozen APIs.

| Interface | Producer → consumer | Required contract content | Failure response |
|---|---|---|---|
| Identity/permission | Security → every protected component | Principal, service identity, scope, purpose, expiry, revocation, authentication strength | Deny protected action; preserve safe read-only/diagnostic capability where possible |
| Evidence/quality | Data → Risk, Research, Health | Source ID, instrument/account scope, event and retrieval times, quality, completeness, lineage, correction/version state | Quarantine or reject affected decision; do not substitute stale/unknown silently |
| Health/interlock | Health → dependent components | Dependency, state, evidence age, reason, scope, restrictive action, recovery condition | Restrict dependent risk-increasing activity; escalate on uncertain supervisor state |
| Risk decision | Risk → future adapter | Actor, exact action hash, scope, policy/evidence versions, limits consumed, reservation, expiry, reason, idempotency | Reject changed, expired, revoked, duplicate or unverifiable action |
| Execution result | Future adapter/venue → Data, Risk, Audit | Request ID, venue order ID, ack state, fill IDs, quantities, fees, funding, timestamps, sequence and raw evidence refs | UNKNOWN retains conservative reservation until reconciliation |
| Policy registry | Owner-authorised change process → Risk/Security | Version, author, approver, signature, effective time, supersession, rollback and audit ref | Reject unsigned, stale, conflicting or unauthorised policy |
| Audit evidence | All foundations → Audit store | Event identity, actor, correlation, ordering, payload hash, source refs, policy version, retention class | Apply action-class-specific fail-closed rule when durable evidence is mandatory |
| Recovery status | Data/Health/Security → Risk/Governance | Reconciliation result, key/permission state, dataset continuity, audit integrity, unresolved exceptions | Do not release restricted activity until required pillars independently attest |

## 5. Integrated failure and threat scenarios

| Scenario | Foundations affected | Required containment | Evidence required before recovery |
|---|---|---|---|
| Stale or manipulated market feed | Data, Risk, Health, Security | Reject affected risk increases; quarantine source; retain last-known values as visibly stale only for non-critical display | Source investigation, corrected lineage, gap disposition and fresh independent evidence |
| Compromised service identity | Security, Risk, Health, Audit | Revoke identity/token; restrict dependent actions; preserve forensic evidence | Credential rotation, scope review, clean rebuild if needed, audit verification |
| Risk policy tampering | Security, Risk, Audit | Reject policy version; suspend affected authority; preserve prior trusted policy | Verified signed policy, key status, independent diff/review and owner approval |
| Health supervisor compromise/outage | Health, Security, Risk | Treat health state as unknown; apply predeclared restrictive interlock to dependent risk increases | Independent watchdog evidence, clean supervisor recovery and control validation |
| Audit store unavailable/tampered | Audit, Security, Risk, Health | Stop action classes whose evidence durability is mandatory; preserve local bounded evidence if approved | Integrity verification, sequence reconciliation, restored durability and gap disclosure |
| Host/device theft | Security, Data, Health | Revoke sessions/keys, isolate remote access, protect encrypted backups | Identity/key rotation, device rebuild, backup integrity and access audit |
| Backup ransomware/corruption | Security, Data, Health | Isolate backup path; prevent unverified restore from becoming authoritative | Clean restore, cryptographic integrity, data reconciliation and recovery exercise |
| AI prompt injection/tool abuse | Security, Risk, Data | Deny privileged tools; treat output as untrusted; restrict affected agent | Tool permission review, trace analysis, environment reset and negative regression tests |
| Venue API outage with open orders | Health, Data, Risk, Security | No new risk; preserve unknown order reservations; manual fallback under owner procedure | Authoritative order/position/balance reconciliation and explicit incident release |
| Cross-domain common dependency failure | All | Restrict only domains whose critical invariants are affected; broader stop only where shared trust is compromised | Dependency-specific evidence and independent checks by each affected pillar |

## 6. Architecture gaps and owner decisions

The following remain open and prevent final contract freeze:

1. Canonical event envelope, event ordering, idempotency and immutable evidence-reference format.
2. Clock discipline, monotonic deadlines, UTC boundaries and source-specific freshness thresholds.
3. Risk policy registry ownership/signing and key compromise recovery.
4. Durable reservation transaction boundary and crash/replay semantics.
5. Health supervisor/watchdog failure-domain independence.
6. Audit durability, external anchoring, retention, privacy and action-specific fail-closed semantics.
7. Data classification, deletion/retention and source entitlement rules across future domains.
8. Recovery attestations required from each pillar and who may authorise release.
9. Exact emergency actions and manual fallback authority.
10. D-006 equity denominator and D-008 capital-flow/valuation semantics.
11. Numerical portfolio limits and intermediate loss thresholds.
12. Independent design review of the complete integrated architecture.

No threshold, API schema, permission grant, action authority or implementation choice is accepted by this matrix.

## 7. Acceptance criteria for Phase 02 foundation design

Before architecture acceptance, IDEAL must have:

- all requirements mapped to an accountable component/policy, interface, failure response and verification evidence;
- no unresolved authority overlap between risk, data, health and security;
- explicit trust boundaries and dependency/failure-domain diagrams;
- event, time, freshness, idempotency and correction semantics specified;
- threat model and abuse cases covering human, service, agent, dependency, device, data-provider and recovery paths;
- risk, data, health and security state models with safe transitions and unknown states;
- recovery procedures proving authoritative reconciliation, not merely restart;
- a test strategy covering positive, negative, boundary, concurrency, mutation, fault-injection and recovery cases;
- residual risks and owner decisions explicitly recorded;
- independent review and explicit owner acceptance.

Phase 02 closure is not automatic when the document set exists. Completeness, consistency, evidence quality, validation and owner acceptance must all be demonstrated.

## 8. Explicit boundaries

- D-001 remains the only active initial trading scope.
- D-006 and D-008 remain unchanged; their unresolved semantics are not decided here.
- No paper/live execution, exchange/account access, credentials, external scans, dependencies, runtime integration, hosting or paid service is authorised.
- Phase 02 remains active; Phases 03–19 remain locked.


## 9. Bounded-autonomy traceability (D-023)

The owner has selected bounded, owner-authorised autonomy as the future operating model. The following requirements make that decision testable; they do not authorise an active envelope or execution.

| ID | Foundation | Requirement | Accountable owner | Cross-pillar dependency | Future verification evidence | Status |
|---|---|---|---|---|---|---|
| GOV-03 | Governance | Every autonomous capability is constrained by an explicitly owner-approved, versioned, scoped, time-bounded and revocable envelope | Governance/Owner | Security, Risk, Audit | Invalid signature/version, expired scope, revocation, scope mutation and privilege-expansion tests | Partial |
| GOV-04 | Governance | Individual actions inside an active envelope may proceed without per-action human approval only after every required gate passes; reserved action classes require owner approval | Governance/Owner | Risk, Security, Data, Health | Positive in-envelope tests plus reserved-action and out-of-envelope denial tests | Partial |
| SEC-09 | Security | Envelope validity and exact action permissions are enforced outside AI/strategy processes at the action boundary | Security | Risk, Audit | Prompt injection, agent self-grant, replay, payload mutation, stale permission and bypass tests | Open |
| RSK-08 | Risk | Every autonomous risk-increasing action receives a fresh deterministic decision bound to exact payload, envelope version, policy version, evidence and reservation | Risk | Security, Data, Health, Audit | Changed payload, expired/revoked envelope, concurrent reservation, duplicate/replay and partial-fill tests | Partial |
| HLT-07 | Health | Unknown/degraded critical dependencies trigger predefined restrictive interlocks that cannot expand authority or initiate financial actions | Health | Risk, Security, Data | Supervisor outage, false heartbeat, stale telemetry and attempted authority expansion tests | Partial |
| AUD-03 | Audit | Owner approvals, envelope versions, autonomous action decisions, reservations, revocations and reserved-action approvals are attributable and tamper-evident | Audit/Security | All foundations | Missing/reordered/altered events, attribution and audit-sink outage tests | Partial |

### Reserved owner-approval classes

At minimum: initial capability activation/reactivation; envelope, policy, hard-limit or permission changes; new accounts, venues and integrations; credential creation and privilege expansion; transfers, withdrawals and payments; safeguard disablement; designated destructive/irreversible operations; and incident recovery/release where policy requires owner approval. The owner may reserve additional classes.

### Enforcement invariants

1. The envelope is a maximum authority boundary, never an obligation or target to consume capacity.
2. Strategy, AI, model and agent outputs cannot create, edit, sign, approve or expand the envelope.
3. Every action is checked against current envelope and permission state at the action boundary.
4. Risk authority is independent: envelope permission is necessary but not sufficient for financial action.
5. A changed payload, expired/revoked envelope, unknown permission, stale critical evidence or failed interlock denies the affected risk-increasing action.
6. Emergency controls may reduce authority; they cannot grant financial authority or initiate liquidation.
7. Owner approval of D-023 is not approval of any actual envelope, account, venue, credential or execution mode.


## Autonomy authority and permission traceability additions

| Requirement | Control | Responsible boundary | Required evidence/tests |
|---|---|---|---|
| Owner-only envelope creation/change | Strong owner authentication, exact-digest approval, immutable version and signature | Owner approval ceremony / authority registry | Wrong signer, replay, recovery, tamper, schema and semantic validation |
| No agent self-grant | Distinct workload identities; no policy/key mutation rights; sole action gateway | Security / action boundary | Prompt injection, confused deputy, privilege escalation and alternate-route tests |
| Exact-action permission | Canonical action digest binds parameters, scope, versions and evidence | Action boundary | Mutate each field; reject changed digest, wrong audience and stale decision |
| Risk authority remains independent | Risk approval and reservation required after security/owner authorisation | Risk authority | Deny when either gate absent; concurrency and reservation tests |
| Revocation takes effect | Monotonic epoch, independent propagation and online checks | Authority registry / action boundary | Partition, cache delay, restart and maximum propagation measurement |
| Safe external side effects | Durable intent/outbox, idempotency, UNKNOWN state and authoritative reconciliation | Risk/action boundary/adapter | Lost acknowledgement, duplicate, partial fill, cancel-unknown and recovery tests |
| Policy integrity | Signed immutable bundle, anti-rollback and fail-closed diagnostics | Policy registry / evaluator wrapper | Unsigned/invalid bundle, rollback and evaluator-error tests |
| Audit and recovery | Durable append-only evidence, protected checkpoints and revocation-preserving restore | Audit/security/health | Truncation, reorder, storage outage, backup restore and incident exercise |

See [Autonomy Authority and Permission Architecture](IDEAL_AUTONOMY_AUTHORITY_AND_PERMISSION_ARCHITECTURE.md) for the full contract and adversarial test catalogue. These are proposed traceability requirements, not test results.


## Checkpoint 068 — adversarial assurance traceability

| Requirement | Control | Owner boundary | Required evidence |
|---|---|---|---|
| Revocation wins before dispatch | Linearizable generation check and durable DISPATCH_STARTED transition | Authority registry / action gateway | Race tests with dispatch paused at each instruction boundary |
| In-flight side effects remain honest | UNKNOWN/in-flight state and reservation retention | Adapter / risk authority | Crash around socket write, lost ACK, venue late receipt |
| All dispatchers fenced | Registered worker inventory, generation acknowledgements | Security / action gateway | Partition, omitted worker, stale cache, restart tests |
| Agent cannot reach credentials or venue | Separate trust zone, no credentials, host-enforced egress | Host OS / gateway | Procfs/FD/env scan, network bypass, SSRF/DNS rebinding tests |
| Sandbox escape contained | Layered OS controls or disposable VM for high-risk code | Host isolation boundary | Guest compromise, syscall, mount, namespace and lateral movement tests |
| Host root compromise handled | Separate gateway/credential trust domain or fail-safe disablement | Deployment trust boundary | Host-root compromise tabletop and recovery exercise |
| Backup cannot resurrect grants | Independent high-water anchor, epoch advance, restore quarantine | Recovery root / authority registry | Pre-revocation snapshot restore and offline-witness test |
| Recovery re-establishes trust | Clean rebuild, re-attestation, key rotation, audit validation and owner release | Security / owner | Full recovery drill and independent evidence review |

These are proposed controls and tests; no runtime tests have been performed.


## Checkpoint 069 — supervisor, policy and audit traceability

| Requirement | Control | Boundary | Required evidence |
|---|---|---|---|
| Supervisor cannot grant authority | Read-only observer plus scoped restrictive interlock channel | Health supervisor / action gateway | Forged healthy state, forged restriction, privilege and host-compromise tests |
| Supervisor failure is safe | Heartbeat and independent probes; scoped fail-closed interlock | Health / security | Kill, pause, partition, stale heartbeat and false-positive tests |
| Policy change is owner-authorised | Immutable artefact; owner digest approval; separate publisher signature; monotonic activation | Owner approval / policy registry | Wrong digest, role confusion, rollback, key compromise and update/dispatch race |
| No key-purpose confusion | Distinct owner, approval, publisher, workload, audit, encryption and venue key roles | Security / key registry | Cross-purpose signature and privilege tests |
| Pre-dispatch audit is durable | Atomic intent + reservation + audit + outbox transaction | Authority/risk/audit store | Disk full, fsync failure, DB crash and outbox atomicity tests |
| Dispatch-start is auditable | Atomic one-use permit consumption + generation check + DISPATCH_STARTED event before network write | Action gateway | Crash injection around commit/socket write |
| External side effect ambiguity is safe | UNKNOWN state, retained reservation and authoritative reconciliation | Adapter / risk authority | Lost ACK, duplicate delivery, venue late acceptance and restore tests |
| Audit sink compromise is detected | Separate privileges, append-only events, signed independent checkpoints | Audit/security | Truncation, rewrite, checkpoint substitution and sink outage |


## Checkpoint 069 — unified state-machine traceability

| Invariant | Required binding/state | Failure outcome | Evidence |
|---|---|---|---|
| Action uses current authority | Global authority generation + envelope/policy digest | Reject stale generation | Revocation/policy update races against dispatch-start |
| Action uses current data/control state | Data/account/instrument evidence + health/security generations | Re-evaluate or hold | Correction, interlock, account sequence and contract-version races |
| Reservation is conservative | HELD → IN_FLIGHT → PARTIALLY_FILLED / TERMINAL_PENDING_RECONCILIATION → RELEASED | Retain unknown residual | Duplicate/out-of-order fill, cancel-unknown, crash and replay |
| Ordering is deterministic | Durable event sequence/transaction order; clock-quality separately recorded | Deny when order/expiry unprovable | Clock rollback/skew, sequence gaps and restart tests |
| Cross-domain states are not conflated | Separate authority, identity, policy, risk, health, security, data and reconciliation state machines | Restrict affected action | Cross-product state and property-based tests |


| Owner understands exact grant | Human-readable approval summary derived from signed artefact digest; explicit before/after diff and step-up confirmation | Owner approval interface / verifier | UI tampering, truncation, hidden scope, stale digest, replay and wrong-origin tests |


## Checkpoint 071 — workstream closure traceability

The autonomy authority closure assessment maps technology-neutral invariants, provisional controls, platform-dependent decisions, owner approvals and residual risks. Workstream acceptance requires all authority/action/risk/health/security/data/reconciliation state machines to align, each invariant to map to adversarial tests, and repository read-back verification. See docs/IDEAL_AUTONOMY_AUTHORITY_CLOSURE_ASSESSMENT.md. No test execution or implementation is implied.


## Checkpoint 072 — integrated domain and bounded-context traceability

| Requirement | Owning context/control | Required boundary | Required verification |
|---|---|---|---|
| Domain state has one authoritative owner | Each bounded context owns canonical records | Other contexts consume versioned projections; no direct cross-context writes | Forbidden-write tests, stale projection and replay tests |
| Future domains remain separately gated | Owner authority / decision register | Proposal status cannot activate a domain or grant capability | Scope/phase gate and negative activation tests |
| Cross-domain aggregation is honest | Portfolio & Capital View | Read-only projections; native currency, ownership, source, valuation and freshness preserved | Missing/stale projection, currency mismatch, no-netting and collateral isolation tests |
| Personal finance imports are not treated as truth | Personal Finance reconciliation | Source observations precede journal posting; corrections/deletions/pending rows remain visible | Duplicate, changed/deleted row, pending-to-posted and transfer tests |
| Tax intelligence cannot control user capital | Tax context / D-018 | Informational estimates only; no lock, forced reserve or payment authority | Attempted capital restriction/payment path must be impossible |
| Market, private finance and AI traces are segregated | Data archive / Security | Purpose-limited references and least-privilege access | Cross-domain retrieval and training leakage negative tests |
| Learning cannot self-promote | Model registry / owner release gate | Offline reproducible evaluation; no online weight updates or agent self-grant | OOS, provenance, rollback and self-promotion denial tests |
| Shared foundations constrain all domains | Risk, Data, Health, Security | Conjunctive gates; distinct authority and statuses | Cross-product state tests; health/security cannot approve financial action |
| UI is not a trust root | Mobile presentation / authority boundary | UI issues scoped requests and renders projections only | Device loss, stale display, replay and approval-digest mismatch tests |
| Failures remain within justified blast radius | Dependency registry / health supervisor | Consumer-specific safe state; unrelated contexts remain operational when isolated | Feed/provider failure propagation and containment tests |

See [Integrated System and Bounded-Context Architecture](IDEAL_INTEGRATED_SYSTEM_AND_DOMAIN_ARCHITECTURE.md), sections 2–11. These are proposed controls and tests; no runtime tests have been performed.


## Checkpoint 073 — data trust and point-in-time traceability

| Requirement | Control | Owner boundary | Required verification |
|---|---|---|---|
| Integrity is not confused with truth | Source authentication, independent plausibility and provenance; digest only proves captured-byte identity | Source Registry / Data Integrity | Correctly hashed but manipulated or incomplete source must remain untrusted |
| Raw evidence is preserved | Immutable raw observation and linked revisions | Evidence Archive | Correction, deletion, duplicate and replay tests |
| Temporal semantics are explicit | Event/publication/receive/ingest/process/valid/known/decision-as-of fields | Data Integrity / domain owner | Bitemporal, late-arrival, clock-skew and boundary tests |
| Backtests are point-in-time correct | Availability-time cutoff and immutable dataset manifest | Dataset Registry / Research | Look-ahead, label leakage, survivorship and late-correction tests |
| Quality is consumer-specific | Quality vector and declared fitness contract | Data Integrity / consumer | Stale/conflicted/unlicensed/unknown propagation tests |
| Private financial data is purpose-limited | Separate data plane, least privilege, retention and deletion policy | Personal Finance / Security | Cross-domain retrieval/training, deletion and backup-expiry tests |
| Bank records reconcile safely | Source observation before journal posting; explicit update/delete/pending semantics | Personal Finance | Duplicate, changed row, pending-to-posted and transfer tests |
| Tax rules are effective-dated | Rule status, source class, enactment and applicability interval | Tax Intelligence | Proposed-vs-enacted, retroactive change and historical replay tests |
| Market-data rights are enforced | Entitlement/retention/training rights attached to source and dataset manifests | Source Registry / Security | Licence expiry, export and training-denial tests |
| Clock uncertainty is bounded | Trusted clock evidence and monotonic local ordering | Health / Data Integrity | Clock rollback/skew and expiry denial tests |

See [Data Trust, Temporal Semantics and Point-in-Time Evidence Architecture](IDEAL_DATA_TRUST_TEMPORAL_AND_POINT_IN_TIME_ARCHITECTURE.md). These are proposed controls and tests; no runtime tests have been performed.


## Checkpoint 074 — domain risk and capital traceability

| Requirement | Control | Owner boundary | Required verification |
|---|---|---|---|
| Risk remains domain-specific | Separate risk contracts and policy scopes per domain | Domain risk authority / owner | No inheritance of derivatives limits into other domains |
| Capital concepts remain distinct | Typed balances/valuations with currency, owner, account, source and timestamp | Domain ledger / data integrity | Double-counting and semantic confusion tests |
| Consolidated view is read-only | Versioned domain projections; no cross-context writes | Portfolio & Capital View | Forbidden write/transfer/permission tests |
| No implicit netting | Gross exposure plus explicitly justified netting sets | Domain risk / portfolio view | Legal entity/account/venue/collateral isolation tests |
| Hedge credit is evidence-based | Basis, correlation, liquidity, expiry and counterparty stress | Portfolio risk authority | Hedge-breakdown and one-leg failure scenarios |
| D-006/D-008 scope is preserved | Policy scope explicitly limited to initial perpetual domain | Owner policy registry / derivatives risk | Negative tests for future-domain inheritance |
| Tax reserve is informational | D-018; no capital lock, deduction or forced payment | Tax Intelligence / Personal Finance | Attempted lock/payment path denied or absent |
| Unknown valuation/FX stays unknown | Consumer-specific quality and freshness gate | Data Integrity / consuming risk domain | Stale FX and missing-price aggregate tests |

See [Domain Risk and Capital Architecture](IDEAL_DOMAIN_RISK_AND_CAPITAL_ARCHITECTURE.md). Proposed controls only; no runtime tests performed.


## Checkpoint 076 — reconciliation and verified recovery traceability

| Requirement | Control | Owner boundary | Required verification |
|---|---|---|---|
| No universal source-of-truth assumption | Fact-specific authority matrix per domain | Owning bounded context | Conflicting source/ledger/venue facts remain distinct |
| Mismatch is not silently overwritten | Immutable source evidence, linked revisions and reconciliation cases | Data Integrity / domain owner | Late correction, duplicate, deletion and replay tests |
| Unknown venue state remains conservative | UNKNOWN order/position state and retained reservation | Risk / action boundary | Lost ACK, late venue acceptance, cancel-unknown and restart tests |
| Bank imports reconcile before posting | Staging observations and controlled journal posting | Personal Finance | Pending/posted, correction, transfer and balance mismatch tests |
| Tax estimate differs from assessment/payment | Separate estimate, workpaper, IRD assessment and confirmed payment states | Tax Intelligence / Personal Finance | No false filing/payment confirmation |
| Restore does not restore authority | Recovery quarantine, revocation high-water anchor, old capability invalidation | Security / owner authority | Restore pre-revocation backup and prove old permits fail |
| Recovery requires independent evidence | Scoped Security/Data/Health/Risk attestations | Four pillars | Missing, stale or contradictory attestation blocks release |
| Health cannot certify security | Separate security incident authority and health supervisor | Security / Health | Common-mode compromise and false healthy-state tests |
| Recovery cannot initiate financial actions | Restrictive containment and explicit owner-reserved action classes | Security / health / owner | Incident control attempts transfer/flatten/payment; deny |
| Unaffected domains remain available where safe | Dependency-aware blast-radius matrix | Health / domain owners | Feed/bank/provider failure isolation tests |

See [Reconciliation, Incident Containment and Verified Recovery Architecture](IDEAL_RECONCILIATION_AND_VERIFIED_RECOVERY_ARCHITECTURE.md). All verification entries are future requirements; no runtime recovery tests have been run.


## Checkpoint 077 — integrated adversarial architecture review

The integrated review maps 24 cross-domain attack/failure scenarios to required outcomes and classifies remaining blockers. Critical future-action scenarios include compromised AI/action mutation, revocation/dispatch races, audit commit failure, unknown venue acknowledgement, host-root compromise and stale backup authority resurrection. High-severity scenarios include point-in-time leakage, bank-row mutation, stale balances, false netting/hedge credit, tax/capital conflation, privacy scope errors and shared data-plane leakage.

See [IDEAL Phase 02 Integrated Architecture Review](IDEAL_PHASE_02_INTEGRATED_ARCHITECTURE_REVIEW.md). The review is an internal desk assessment only; it does not prove vulnerabilities absent or satisfy the independent-review exit gate.


## Checkpoint 078 — cross-domain accounting fixture traceability

| Scenario | Required invariant | Future test assertion |
|---|---|---|
| Bank-to-exchange transfer | Transfer is not income; in-transit leg not double-counted | Total wealth changes only for evidenced fee/FX effect |
| Spot plus perpetual | Spot market value differs from derivative notional | Net worth includes spot asset and derivative MTM, not derivative notional |
| Funding/fees/MTM | Settled cashflows and unrealised valuation are separate | Each venue event is booked once; no duplicate P&L |
| Collateral posted | Encumbrance is not new wealth or loss | Total units conserved; free/encumbered buckets reconcile |
| Pending-to-posted bank row | Same economic transaction posted once | Revised final amount, one journal posting |
| Tax reserve | Estimate/designation/assessment/payment remain separate | No lock, deduction or payment side effect |
| Stale FX | Missing conversion is unknown/incomplete | No silent zero or stale unlabelled total |
| Late source correction | As-known-then snapshot remains reproducible | New latest-corrected view without historical leakage |

See [Cross-Domain Accounting and Valuation Worked Examples](IDEAL_CROSS_DOMAIN_ACCOUNTING_AND_VALUATION_EXAMPLES.md). No fixture tests were executed.


## Checkpoint 079 — data classification, retention and audit traceability

| Requirement | Control | Owner boundary | Required verification |
|---|---|---|---|
| Every dataset has purpose/classification/owner | Data policy registry and quarantine for unclassified sources | Data owner / Security | Unknown class denied from new use |
| C2/C3 data remains isolated | Least privilege; no default prompt, telemetry, retrieval or training path | Security / AI boundary | Cross-domain access and training-denial tests |
| Retention follows legal/licence purpose | Per-class retention schedule and source entitlement | Data owner / legal policy | Expiry, legal hold and licence-expiry tests |
| Deletion covers all copies | Primary, replica, cache, index, export, derived dataset and backup lifecycle | Data Integrity / operations | End-to-end deletion and restore-after-deletion tests |
| Processor role is explicit | Agent-only processing distinguished from own-purpose use | Security / provider governance | Contract/processor-role and subprocessor review |
| Tax evidence retained appropriately | IRD cryptoasset 7-year requirement applied only within scope; RCASP duty not misapplied to individual | Tax Intelligence / owner | Scope-specific retention tests and tax-adviser review |
| Audit minimises sensitive payload | Opaque references, redaction, retention class and tombstone | Audit / Security | Secret/PII leakage and hash re-identification review |
| Backup cannot resurrect revoked/deleted state | Bounded expiry, key lifecycle and restore quarantine | Security / Health | Restore after deletion, revocation and key rotation |

See [Data Classification, Retention, Deletion and Audit Policy Architecture](IDEAL_DATA_CLASSIFICATION_RETENTION_AND_AUDIT_POLICY.md). These are future controls; no retention/deletion runtime tests have been performed.


## Checkpoint 080 — host trust topology traceability

| Requirement | Control / candidate | Limitation | Required verification |
|---|---|---|---|
| Phone remains control plane, not safety-critical worker | Android UI, approval and notifications | Background work, battery and mobile-data constraints | Device loss, background restriction and network outage tests |
| WSL2 is not treated as a sandbox | Treat WSL code as same trust level as Windows user | Windows host/user compromise reaches WSL trust domain | Negative boundary tests; no secrets in untrusted workloads |
| Hyper-V VM trust boundary is explicit | Guest isolation, Secure Boot/vTPM candidates | Same host administrator/root can control VM | Host compromise and VM disk/configuration access tests |
| KVM/Firecracker hardening is complete | Jailer, seccomp, cgroups/namespaces, host egress firewall | Host kernel/hardware and network policy remain trusted | Escape, egress, resource-exhaustion and host-root tests |
| Action gateway survives worker compromise | Separate physical trust domain candidate | Added cost, network and operational complexity | Worker compromise cannot access gateway keys/adapter |
| Recovery root and watchdog are independent enough | Offline/hardware/remote anchor candidates | No topology or anchor selected | Host compromise, restore rollback and watchdog independence tests |

See [Host Trust Topology and Recovery Options](IDEAL_HOST_TRUST_TOPOLOGY_AND_RECOVERY_OPTIONS.md). No device inspection or isolation tests were performed.


## Checkpoint 081 — integrated state-machine traceability

| Requirement | Contract | Required verification |
|---|---|---|
| State authority is not conflated | Each state machine has one owner; no pass implies another pass | Cross-machine negative/deny tests |
| Policy publication is immutable | DRAFT → VALIDATED → OWNER_APPROVED → SIGNED → PUBLISHED → ACTIVE | Role separation, digest mismatch and rollback tests |
| Action admission is conjunctive | Owner, identity, security, data, health, risk, reservation and audit gates | Deny/UNKNOWN injection at each gate |
| State changes invalidate stale permits | Version vector bound to action and rechecked at dispatch | Concurrent policy/data/account/interlock changes |
| Revocation serialises with dispatch | Shared monotonic authority generation and DISPATCH_STARTED boundary | Race, partition and crash-point tests |
| Reservations conserve exposure | Partial fills transfer once; unknown residual stays held | Concurrency, partial-fill and cancel-unknown tests |
| Corrections preserve historical knowledge | As-known-then snapshot and latest-corrected view separate | Late source correction replay |
| Recovery cannot self-release | Quarantine, scoped pillar attestations and owner release where reserved | Missing/stale/contradictory attestation tests |

See [Integrated State-Machine and Cross-Authority Contract Architecture](IDEAL_INTEGRATED_STATE_MACHINE_AND_CONTRACT_ARCHITECTURE.md). No runtime tests performed.
