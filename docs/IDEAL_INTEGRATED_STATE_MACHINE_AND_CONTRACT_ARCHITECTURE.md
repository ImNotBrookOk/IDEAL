# IDEAL Integrated State-Machine and Cross-Authority Contract Architecture

**Status:** Phase 02 integrated contract draft; provisional, not owner-accepted or implementation-ready  
**Checkpoint:** 081 — 17 November 2026  
**Scope:** Canonical lifecycle states, cross-pillar gates, generation/version binding, transition ordering and failure precedence  
**Authority:** D-018, D-019, D-020, D-021, D-022, D-023  
**Boundary:** Design only. No schemas, code, runtime integration, credentials, accounts, external actions, paper/live execution or phase advancement are authorised.

## 1. Purpose

The individual Phase 02 documents define state machines for owner authority, policy, workload identity, security incident response, health, data quality, risk, reservations, actions, reconciliation and recovery. This document defines how those state machines compose without collapsing their authority into one status flag or one global state machine.

The system must distinguish:
- **authority:** whether the owner has granted a capability;
- **identity/security:** whether the actor and policy trust are valid;
- **data trust:** whether evidence is fit for the intended use;
- **health:** whether required services/dependencies are operational;
- **risk:** whether the exact financial action is acceptable;
- **reservation:** whether capacity/exposure is durably held;
- **action:** whether a specific side effect has been admitted or started;
- **reconciliation:** whether external reality matches the internal record;
- **recovery:** whether the affected trust domain is safe to release.

A pass in one state machine never implies a pass in another.

## 2. Canonical state ownership

| State machine | Authoritative owner | May restrict | May grant/approve |
|---|---|---|---|
| Owner authority/envelope | Owner + authority registry | Owner revocation/expiry | Only authenticated owner ceremony can approve or expand |
| Policy publication | Policy registry with separate publisher role | Revocation/supersession | Publisher signs; owner approval required for scope/policy changes |
| Workload identity | Security/identity control plane | Revoke/quarantine identity | Security issues narrowly scoped workload identity under approved policy |
| Security incident | Security incident-response control plane | Revoke identity, isolate workload/integration | No financial action or owner financial authority |
| Health | Independent health supervisor | Scoped restrictive interlock only | Cannot grant permission, risk approval or release critical incident hold alone |
| Data evidence/quality | Data Integrity/source registry | Quarantine source/record; invalidate dependent evidence | Cannot approve financial action or owner authority |
| Risk evaluation | Independent deterministic risk authority | Deny/restrict exposure increase | Approves exact action within current policy; reserves risk capacity |
| Reservation | Risk reservation ledger | Retain/hold capacity conservatively | Reserve/transfer/release only on defined reconciled transitions |
| Action gateway | Protected action boundary | Deny/fence/hold | Consumes exact one-use permit after all conjunctive gates |
| Reconciliation | Owning domain | Hold affected domain state | Resolves mismatch with evidence and authorised correction |
| Recovery | Incident process + scoped pillar attestations + owner release where reserved | Quarantine/restrict | Only designated owner release can restore owner-reserved authority |
| Audit | Local authoritative audit store; optional independent witness | Block consequential actions when required durable evidence unavailable | Cannot grant domain authority |

## 3. State-machine catalogue

These state names are the current logical vocabulary. A future implementation may choose different internal representations only if semantics and traceability remain equivalent.

### 3.1 Owner authority and policy

Owner envelope lifecycle: DRAFT → VALIDATED → OWNER_APPROVED → SIGNED → PUBLISHED → ACTIVE → SUPERSEDED or REVOKED.

- DRAFT and VALIDATED are non-authoritative.
- VALIDATED checks schema, canonical digest, scope, units, expiry, references, key purpose and forbidden combinations.
- OWNER_APPROVED binds the owner ceremony to the exact artefact digest, operation, environment, version and expiry.
- SIGNED is the separate policy-publisher role; signature is not owner approval.
- PUBLISHED is immutable and available but not active.
- ACTIVE requires a serialised activation event and new authority generation.
- SUPERSEDED remains historical evidence and cannot regain authority by rollback.
- REVOKED is denied even if a historical signature remains cryptographically valid.

Owner approval is mandatory for initial activation/reactivation, envelope/policy/limit/permission changes, new accounts/venues/integrations, credential privilege expansion, transfers/withdrawals/payments, safeguard disablement, designated irreversible actions and reserved incident recovery/release.

### 3.2 Workload identity

Proposed identity states: REQUESTED → ISSUED → ACTIVE → ROTATION_PENDING → REVOKED / EXPIRED / QUARANTINED.

Identity proves which workload is requesting; it does not grant action permission. Identity lifecycle is separate from policy and owner authority. Revocation invalidates outstanding admissions for that identity. A compromised identity is not restored from backup as active.

### 3.3 Data evidence and quality

Source/canonical evidence states include VALID, DEGRADED, STALE, INCOMPLETE, CONFLICTED, REVISED, UNVERIFIED, QUARANTINED and UNKNOWN. These are not necessarily a single linear state machine; they are explicit evidence/quality states with consumer-specific fitness rules.

A downstream risk decision must bind the exact evidence snapshot, source revisions, availability cutoff, quality assessment and transformation versions. A later correction creates a new latest-known view; it does not rewrite what was knowable at the original decision time.

### 3.4 Health and security

Health state is scoped to dependency/domain and may be HEALTHY, DEGRADED, RESTRICTED, FAILED or UNKNOWN. Health is not a security attestation.

Security incident lifecycle is separately governed. A practical proposed sequence is DETECTED → TRIAGED → CONTAINMENT → ERADICATION → RECOVERY → CLOSED, with INCIDENT_HOLD/REOPENED paths for uncertainty or recurrence. Only Security may revoke compromised identities or isolate integrations under its explicit incident permissions. Health may request restrictive interlocks only.

Critical security/data-integrity holds remain latched until independently cleared. A health supervisor cannot self-certify its own integrity or release its own critical interlock.

### 3.5 Risk evaluation and reservation

Risk result: APPROVED, DENIED or INDETERMINATE, bound to exact action, domain/account/instrument, policy, capital measure, evidence snapshot and validity.

Reservation lifecycle:
- NONE
- HELD
- IN_FLIGHT
- PARTIALLY_FILLED
- TERMINAL_PENDING_RECONCILIATION
- RELEASED
- INCIDENT_HOLD

Potentially executable working orders reserve risk before dispatch. Filled quantity transfers to position exposure exactly once; residual quantity remains reserved until authoritative terminal reconciliation. Timeout, restart, cancellation request or missing acknowledgement never releases uncertain exposure.

### 3.6 Action lifecycle

Canonical future consequential-action lifecycle:

PROPOSED → VALIDATED → AUTHORISED → RESERVED → ADMITTED → DISPATCH_STARTED → DISPATCHED → ACKNOWLEDGED or UNKNOWN → RECONCILED.

Terminal/restrictive states include REJECTED, EXPIRED, REVOKED and INCIDENT_HOLD.

- PROPOSED: untrusted intent; no side effect.
- VALIDATED: canonical action and required evidence assembled.
- AUTHORISED: owner envelope and security policy permit exact action; still no side effect.
- RESERVED: risk authority has durably held potential exposure/capacity.
- ADMITTED: all prerequisites and durable audit preconditions pass; one-use permit exists but is not yet consumed.
- DISPATCH_STARTED: final generation/interlock check, permit consumption and audit event committed immediately before network write. This is the local linearisation point.
- DISPATCHED: adapter attempted the network write; remote receipt is not assumed.
- ACKNOWLEDGED: definitive venue response received; still requires reconciliation.
- UNKNOWN: outcome ambiguous; retain reservation and reconcile.
- RECONCILED: external state matched; reservation/position state updated exactly once.
- REJECTED/EXPIRED/REVOKED: denied before dispatch; no external side effect.
- INCIDENT_HOLD: material trust/state uncertainty; restrict and recover.

No exactly-once remote effect is claimed. A request already transmitted cannot be recalled locally.

### 3.7 Reconciliation and recovery

Reconciliation case states: REQUESTED → COLLECTING → VALIDATING → COMPARING → MATCHED / MATCHED_WITH_TIMING_DIFFERENCE / MISMATCH / UNKNOWN / QUARANTINED → RESOLVED → CLOSED.

Recovery states: NORMAL → DEGRADED → RESTRICTED → INCIDENT_HOLD → RECOVERY_QUARANTINE → RECONCILIATION_REQUIRED → ATTESTATION_REQUIRED → OWNER_RELEASE_REQUIRED → NORMAL.

Not every incident traverses every state. Recovery must not bypass any required gate. A restart or successful restore alone cannot return to NORMAL.

## 4. Conjunctive admission contract

For any future risk-increasing external action, admission requires all applicable checks to pass at the same defined decision boundary:

1. Owner envelope is ACTIVE, unexpired, correctly signed/versioned and not revoked.
2. Exact action digest and domain/account/instrument/action class are inside the envelope.
3. Workload identity is authenticated, current, scoped and not quarantined/revoked.
4. Security policy permits the exact principal/action/resource.
5. Data evidence is trusted and fit for this action, including freshness, point-in-time availability, sequence/completeness and reconciliation.
6. Health interlocks for all critical dependencies are clear and current.
7. No security incident hold applies to the affected trust domain.
8. Independent deterministic risk evaluation returns APPROVED for the exact action and current capital/exposure snapshot.
9. Risk reservation is durably held and consistent with current orders/positions.
10. Audit intent, evidence references, reservation and outbox are durably committed.
11. One-use admission permit is valid, unexpired, audience/action-bound and not consumed.
12. Immediately before network write, the action boundary rechecks current authority generation and all invalidation-sensitive versions, consumes the permit and commits DISPATCH_STARTED plus audit atomically.

Any DENY, UNKNOWN, stale, expired, unverifiable or unavailable mandatory input means no admission. A positive result from another gate cannot override it.

## 5. Version/generation binding

Do not overload one global version number to represent every kind of state. Bind a version vector to each consequential action:

- owner authority generation;
- envelope/policy version and digest;
- policy signing-key trust generation;
- workload identity generation/revocation state;
- security incident generation/scope;
- health interlock generation/scope;
- risk policy version;
- risk decision and reservation ID/version;
- source/evidence snapshot and quality version;
- instrument/contract metadata version;
- account/position/order reconciliation version;
- schema/transformation/model version where applicable;
- audit sequence/checkpoint reference;
- clock quality and action expiry.

The owner authority generation is monotonic and serialises owner grant/policy/key/identity revocation with dispatch-start. Other domain versions remain separately attributable. The action boundary compares every relevant version at admission and immediately before dispatch. A material change invalidates the permit and requires re-evaluation.

Wall-clock timestamps do not replace durable ordering. Local transaction/event sequence determines local order; source sequence determines source-stream continuity; trusted time supports expiry/freshness. Unknown clock quality denies time-dependent admission.

## 6. Restrictive precedence and recovery semantics

- Owner revocation/expiry always denies future admission.
- Security revocation/quarantine denies affected identity/capability.
- Data UNKNOWN/STALE/CONFLICTED blocks only dependent actions according to declared criticality; it cannot be relabelled by a consumer.
- Health interlock may restrict only the affected dependency/domain; it cannot grant or change policy.
- Risk DENIED/INDETERMINATE blocks risk-increasing actions.
- Reservation conflict or unknown order state retains conservative exposure.
- Audit durability failure before dispatch blocks the consequential side effect.
- Reconciliation mismatch/unknown holds affected external state and dependent actions.
- Recovery quarantine prevents reactivation until every required trust, data, risk, health, security, audit and external-state check is current.
- Persistent policy/envelope changes require owner approval even when narrowing capability; temporary interlocks are restrictive and do not mutate policy.
- No incident control plane may initiate cancellation, flattening, transfer, withdrawal, payment or tax filing.

## 7. Cross-state transition invariants

| Invariant | Required behaviour |
|---|---|
| No self-authorisation | AI/strategy cannot create owner grants, policy changes, risk approvals or credentials |
| Exact-action integrity | Any payload mutation after approval invalidates admission and requires new evaluation |
| Revocation/dispatch serialisation | Revocation-first blocks DISPATCH_STARTED; dispatch-start-first remains in-flight/UNKNOWN |
| Reservation conservation | Filled exposure transfers once; residual remains held until terminal reconciliation |
| Data correction integrity | Historical decision retains as-known-then evidence; latest-corrected state is a new version |
| Restrictive-only supervision | Health/security incident controls reduce capability but never grant financial authority |
| Restore non-resurrection | Backup restore cannot revive revoked keys, permits, deleted data or stale authority generation |
| Pillar independence | Each foundation attests only to its own scope |
| No false recovery | Restart/health probe/backup digest alone cannot return system to NORMAL |
| No false aggregation | Missing FX/positions/ownership/valuation yields partial or UNKNOWN total, not zero |
| User capital autonomy | Tax estimate or budget label cannot lock/segregate/force owner funds |
| Audit before side effect | Required local evidence is durable before network write |
| No exactly-once fiction | External effects remain UNKNOWN until authoritative reconciliation |

## 8. Open semantics requiring final closure

- Exact schema/canonical encoding for action, evidence, owner envelope, version vector and reason codes.
- Whether validation and review need additional explicit substates for policy publication; current lifecycle is DRAFT → VALIDATED → OWNER_APPROVED → SIGNED → PUBLISHED → ACTIVE.
- Exact state model for security incident severity, containment and release.
- Exact interlock priority, scope, latching, expiry and clearance criteria.
- Data freshness and clock-uncertainty thresholds by source/action.
- D-006 equity denominator and D-008 day-start/flow semantics.
- Reservation concurrency, transaction store and crash durability.
- Worker inventory completeness and revocation propagation objective.
- Recovery root, external witness and owner authenticator.
- Audit retention classes/durations and deletion/hold interactions.
- Manual owner recovery, device loss and failure when owner approval is unavailable.
- Domain-specific risk and capital policies for any future non-derivatives domain.

These remain open design items; this document does not invent numerical values or platform decisions.

## 9. Required verification catalogue

Before any implementation blueprint is accepted, create deterministic tests for:
- every valid/invalid transition and state-machine race;
- policy publication with owner/publisher role separation and digest mismatch;
- owner authority generation, revocation and stale permit;
- identity expiry/rotation/revocation during admission;
- stale/conflicted data, late correction and point-in-time replay;
- health/security interlock scope, replay, expiry and common-mode failure;
- risk approval invalidation after account/metadata/evidence change;
- reservation concurrency, partial fill, unknown cancel and crash recovery;
- audit failure at every local transaction boundary;
- network write crash before/after dispatch-start and lost acknowledgement;
- reconciliation correction and idempotent replay;
- restore after revocation/deletion/key rotation;
- recovery with one missing/expired/contradictory attestation;
- forbidden cross-domain writes and no tax/capital restriction;
- device/network loss and manual owner recovery.

No runtime tests have been run.

## 10. Disposition

The integrated state-machine composition is sufficiently specified for an architecture challenge, but schemas, numeric thresholds, topology, platform-specific mechanisms and several owner decisions remain open. It is not implementation-ready and does not authorise any execution.

Phase 02 remains active; Phases 03–19 remain locked. No implementation, dependencies, runtime, accounts, credentials, external integrations, paper/live execution, paid infrastructure or phase advancement is authorised.


## Canonical interface contracts — checkpoint 085

The contract catalogue in [IDEAL Canonical Contract Catalogue](IDEAL_CANONICAL_CONTRACT_CATALOGUE.md) defines the payload semantics and ownership for the state transitions in this document. In particular, action permits bind exact action/evidence/policy versions; dispatch outcomes preserve UNKNOWN; health interlocks are restrictive-only; reconciliation and recovery attestations remain domain-owned.

 
## Margin and liquidation composition — checkpoint 100

Margin/position risk is owned by the risk authority; venue-reported liquidation and ADL events are external evidence; reservation lifecycle remains owned by the reservation ledger; account/position truth is resolved by reconciliation. These authorities must not be collapsed.

- A mark-price/tier/margin change invalidates affected risk decisions and admission permits before dispatch-start.
- A liquidation warning or venue trigger imposes the applicable restrictive risk state; it does not itself prove a close or terminal position state.
- Risk-increasing orders are blocked while liquidation, account uncertainty or reconciliation hold is active.
- Cancellation/close requests retain the full conservative reservation until terminal order state, fills, remaining position and account balances are reconciled.
- Partial fills transfer filled quantity into reconciled position exposure exactly once; unfilled residual remains reserved.
- Venue insurance-fund or ADL notices are recorded as external venue events. They cannot grant IDEAL permission, release unrelated reservations or establish final account state without reconciliation.
- A venue-reported bankruptcy/liquidation handoff does not mean IDEAL can control the venue's liquidation engine or guarantee execution price.
- If venue event sequence, fill totals, position snapshot and balance evidence conflict, retain INCIDENT_HOLD / RECONCILIATION_REQUIRED and do not infer a terminal state.
- Recovery after liquidation requires current venue/account state, local journal continuity, current policy/authority generation and scoped health/security/data attestations.

The canonical logical records are in [Critical Contract Field Schemas](IDEAL_CRITICAL_CONTRACT_FIELD_SCHEMAS.md) §18 and the detailed risk requirements in [Margin, Collateral and Liquidation Architecture](IDEAL_MARGIN_COLLATERAL_AND_LIQUIDATION_ARCHITECTURE.md). These are design contracts only.
