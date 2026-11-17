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
