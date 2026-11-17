# Checkpoint 069 — supervisor, policy root and audit atomicity review

**Date:** 17 November 2026  
**Phase:** 02 — architecture/contracts (active)  
**Status:** Provisional design expanded; no technology selected or implementation approved  
**Governance:** D-023 remains Accepted. No new owner decision or phase transition.

## Scope

Continue the owner's autonomous research instruction without interruption. This checkpoint extends checkpoint 068 by resolving conceptual gaps in:
1. Independent health supervisor authority and failure-domain separation.
2. Policy publication, root trust and key lifecycle.
3. Audit/action atomicity and the local-to-external side-effect boundary.

## Findings

### 1. Health supervisor is restrictive-only

- The supervisor is an observer, not an authority issuer.
- It receives read-only telemetry and has a narrow authenticated channel to assert scoped restrictions on risk-increasing actions.
- It cannot create/modify owner envelope, policy, hard limits, risk approvals/reservations, credentials, or initiate cancel/flatten/transfer/withdrawal/payment.
- It cannot clear critical latched restrictions without independent recovery evidence and the designated owner release process.
- A separate process identity is a minimum logical boundary, not protection against shared host root/kernel compromise.
- A compromised supervisor can cause denial of service but cannot gain financial authority.
- Operational health, data trust, security posture, financial-state trust and authority state remain distinct.

### 2. Policy publication is immutable and multi-role

Proposed lifecycle:
DRAFT → VALIDATED → OWNER_APPROVED → SIGNED → PUBLISHED → ACTIVE → SUPERSEDED or REVOKED.

- Owner approval binds exact artefact digest, environment, operation, version and expiry.
- Policy publisher signature is a separate role; it cannot expand owner authority by itself.
- Policy artefacts are immutable and monotonically versioned.
- Activation, revocation and dispatch-start serialize against one authority generation.
- Root/recovery, owner approval, policy publisher, workload identity, audit checkpoint, data encryption and future venue credentials have separate key purposes.
- Suspected key compromise means revoke and replace the key identity, not restore/re-enable the old key.
- Threshold signing, WebAuthn, hardware-backed keys and TUF-inspired metadata remain candidates; none selected.

### 3. Audit/action atomicity

IDEAL cannot atomically commit a local database transaction and a remote exchange side effect. It must not claim exactly-once execution across that boundary.

- Transaction A: atomically commit canonical intent/digest, authority evidence, generation, risk reservation, audit event and transactional outbox.
- Transaction B: immediately before network write, atomically consume one-use permit, recheck generation and commit DISPATCH_STARTED plus audit event. This is the local dispatch linearisation point.
- External network write occurs only after Transaction B commits durably.
- Transaction C: after definitive venue response/reconciliation, append outcome and update order/position/reservation state atomically.
- If A or B fails, no dispatch.
- If venue may have accepted and C/acknowledgement fails, state remains UNKNOWN/in-flight, reservation retained and authoritative reconciliation required.
- Duplicate outbox delivery is idempotent. No blind retries.
- Audit projection/witness may be asynchronous, but required durable local evidence is a precondition to dispatch.

## Research sources

- OWASP Logging Cheat Sheet — structured security events, separation of audit/security/transaction logs, secret exclusion, tamper protection and failure testing.
- NIST SP 800-53 Rev. 5 — audit information protection and alternate audit capability.
- NIST SP 800-57 Part 1 Rev. 5 — key compromise, replacement and recovery.
- AWS Prescriptive Guidance — transactional outbox and duplicate-delivery/idempotency handling.
- NIST SP 800-207 — resource-centric zero-trust and separation of authentication/authorization.
- Primary sources linked in the autonomy authority architecture.

The AWS outbox reference is a distributed-systems pattern only; it does not select AWS infrastructure. None of these sources proves IDEAL implementation security.

## Repository changes

- Extended autonomy authority architecture with §§23–26.
- Updated data integrity/health document with restrictive-only supervisor design.
- Updated security architecture with policy root, audit atomicity and supervisor boundaries.
- Updated risk architecture with three durable local transaction boundaries.
- Updated core protection architecture, REQUIREMENTS, ARCHITECTURE, ROADMAP and foundation traceability matrix.
- Updated integrated adversarial review with ADV-31 through ADV-38.
- Added primary source references and this audit/index entry.

## Limitations and non-authorisations

No runtime code, dependency, service, key, account, exchange connection, financial record, hosting, paid service or external security test was added or changed. No supervisor compromise test, key ceremony, DB crash test, external venue test, recovery exercise or fault injection was performed. Phase 02 remains active; Phases 03–19 remain locked. No new owner decision was created.

## Next autonomous work

Continue with a cross-document consistency and state-machine audit: validate policy/revocation/dispatch generation ordering, risk reservation transitions, audit durability, health/security interlocks and recovery semantics against one coherent authority lifecycle. Identify contradictions and missing failure states, then update traceability and the adversarial review. Do not request owner input until the planned architecture work is complete.
