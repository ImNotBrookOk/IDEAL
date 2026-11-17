# Checkpoint 070 — cross-document state-machine and authority consistency review

**Date:** 17 November 2026  
**Phase:** 02 — architecture/contracts (active)  
**Status:** Consistency review and architecture refinements documented; provisional design  
**Governance:** D-023 remains Accepted. No new owner decision or phase transition.

## Scope

Continue the owner-authorised autonomous Phase 02 plan. Reconcile the checkpoint 067–069 authority, revocation, host isolation, recovery, health, policy and audit work against the existing risk-management and data-integrity/health architecture. Do not ask the owner for input until the planned architecture work is complete.

## Consistency findings and corrections

### 1. Health supervisor versus security incident-response authority

Earlier wording could be read as allowing the health supervisor to revoke credentials. This was clarified:

- Health supervisor: read-only observer plus scoped restrictive interlock authority. It may request suspension of affected risk-increasing actions and narrowly scoped workload isolation. It cannot issue/revoke credentials, change security policy, create authority or initiate financial side effects.
- Security incident-response control plane: separately authenticated/audited authority may revoke compromised credentials/identities or isolate integrations/workloads under explicit incident permissions. It cannot grant financial authority or initiate cancellation, flattening, transfer, withdrawal or payment.
- A separate process identity does not protect against shared host root/kernel compromise.

Updated data integrity/health and security documents to remove ambiguity.

### 2. Action state machine now includes dispatch-start

The earlier action state sequence had ADMITTED → DISPATCHED without an explicit durable local boundary. It now distinguishes:
- ADMITTED: narrow one-use permit exists but has not been consumed.
- DISPATCH_STARTED: final generation check, one-use permit consumption and audit event are durably committed immediately before network write; this is the local linearisation point.
- DISPATCHED: adapter attempted external network write.
- ACKNOWLEDGED / UNKNOWN / RECONCILED: venue response and authoritative reconciliation states.

A crash after DISPATCH_STARTED is potentially in-flight/UNKNOWN unless non-dispatch can be proven. Revocation and dispatch-start serialize against the same authority generation.

### 3. Local transactional boundary clarified

Transaction A (intent, exact digest, authority evidence, risk reservation, audit event and outbox) must commit in one authoritative ACID transaction. Separate databases/services cannot be described as atomic without a verified transaction protocol. This aligns with the approved Modular Monolith direction: prefer one authoritative transactional store with module/schema ownership boundaries initially.

Transaction B atomically rechecks current generation, consumes one-use permit, commits DISPATCH_STARTED and its audit event before network write. Transaction C records definitive venue outcome/reconciliation and updates position/reservation state. External exchange side effects cannot be part of the local ACID transaction; no exactly-once remote claim is allowed.

Audit projection/witness may be asynchronous, but local pre-dispatch evidence is mandatory. Projection lag/backlog and outage behaviour must be bounded; exceeding the approved limit blocks new risk-increasing actions.

### 4. Unified version and reservation semantics

A global monotonic authority generation is proposed for the initial private single-owner design. It changes when owner authority, active policy, relevant signing trust or workload identity revocation changes. Separate risk-policy, health-interlock, security-incident, data-evidence, account-reconciliation and venue/instrument metadata versions are also bound to the action.

The local durable event/transaction order determines state transitions; wall-clock timestamps are evidence, not the sole ordering mechanism. Clock uncertainty denies time-dependent admission.

Reservation states are explicit: NONE, HELD, IN_FLIGHT, PARTIALLY_FILLED, TERMINAL_PENDING_RECONCILIATION, RELEASED and INCIDENT_HOLD. Filled quantity transfers to position exposure exactly once; residual stays reserved until authoritative terminal reconciliation.

### 5. D-023 owner approval boundary rechecked

A wording that could imply unapproved persistent policy narrowing was corrected. Temporary restrictive health/security interlocks may reduce capability without editing the owner envelope or hard policy. Persistent envelope/policy/limit changes, including narrowing or expansion, follow the owner-approval process under D-023. No interlock can grant authority or initiate a financial side effect.

Owner approval must be informed: a human-readable summary and before/after diff are derived from the exact canonical artefact digest. Challenge binds digest, operation, environment, audience, nonce and expiry. A valid WebAuthn assertion is not by itself proof that undisplayed scope was understood.

### 6. Additional adversarial case

ADV-39 covers an approval UI that displays a harmless summary while the signed artefact contains expanded scope, hidden fields or altered limits. Exact digest binding, same-source summary generation, full critical diff and rejection of ambiguous/truncated/mismatched presentation are required.

## Research basis

The design remains grounded in the primary sources recorded in the autonomy architecture: NIST SP 800-207, NIST SP 800-53 Rev. 5, NIST SP 800-57 Rev. 5, OWASP authorization/transaction authorization/logging guidance, Linux Landlock documentation, Firecracker design, TUF specification and AWS transactional outbox guidance. AWS is referenced for the pattern only; no AWS service is selected.

## Repository changes

- Extended autonomy authority architecture with unified state/event ordering and owner approval ceremony.
- Clarified health supervisor versus security incident-response authority in data integrity/health and security documents.
- Aligned risk reservation/dispatch handshake with DISPATCH_STARTED and final action gateway.
- Updated requirements and foundation traceability.
- Added ADV-39 to integrated adversarial review.
- Updated this checkpoint audit and index.

## Limitations and non-authorisations

No implementation, runtime, dependencies, accounts, credentials, exchange connections, paper/live execution, paid services, hosting or external tests. No database crash/fault injection, approval UI test, supervisor compromise test, key ceremony or venue reconciliation test. No claim of vulnerability-free design.

Phase 01 remains closed. Phase 02 remains active. Phases 03–19 remain locked. D-023 remains accepted. No technology is selected or adopted.

## Next autonomous work

Perform the final Phase 02 bounded-autonomy closure review across all open architecture decisions: root-of-trust and recovery anchor, owner approval, policy registry, workload identity, revocation SLO, authority transaction store, worker inventory, health/security interlocks, audit retention/privacy and deployment trust topology. Separate what can be specified technology-neutrally from decisions that require the eventual platform. Then update the acceptance checklist and report the exact remaining owner decisions without asking interim questions.
