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


## GitHub read-back verification

All twelve affected/new files were fetched from the repository default branch. Required-content checks passed. One initial phrase check for the main architecture document used wording that differed from the actual equivalent control text; direct inspection confirmed the required same-transaction boundary is present. No content failure was found.

| File | Read-back blob SHA |
|---|---|
| docs/IDEAL_AUTONOMY_AUTHORITY_AND_PERMISSION_ARCHITECTURE.md | 0ba0e8b73488ba3a66dd7891d45598994d6f5194 |
| docs/DATA_INTEGRITY_AND_HEALTH.md | 1ff31234b4d8f09887bae0873b62f1b406c9248e |
| docs/IDEAL_SECURITY_ARCHITECTURE.md | c008d0d56eccb2da31b6579b3d8f5f670ba3d7a2 |
| docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md | 165c601bddbd358baced615e47ef6bbf052f4403 |
| docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md | 207ec6392df56c779f2f9d4f92e6da5d96ca0b58 |
| REQUIREMENTS.md | 751c5ee7ca4c6232af8c2011f0df716c5535ad29 |
| ARCHITECTURE.md | 652d01b8d2a717ea0be560b2ca5896f767f95cf8 |
| ROADMAP.md | 7e2b5e73d1385f50be133b45443fb6abe8e91978 |
| docs/IDEAL_FOUNDATION_TRACEABILITY_MATRIX.md | 3741a91d9350f361b970cc2d5a357936a9b0d1d5 |
| docs/IDEAL_INTEGRATED_ADVERSARIAL_REVIEW.md | fe849efb6d088b46afae85b6b8a579549aabe418 |
| docs/CHATGPT_CONVERSATIONS/2026-11-17-070-cross-document-state-machine-consistency-review.md (before evidence addendum) | c50b21733f2ddf31d763529713effc26c85516c6 |
| docs/CHATGPT_CONVERSATIONS/README.md | cf8556b8c9144aaef3bff87a93a797a9e7e33353 |

### Commit ledger

| Change | Commit SHA |
|---|---|
| Add DISPATCH_STARTED state and transaction-boundary clarification | 3acf8b7194d64bde70737c2bc3f52241a111f09f |
| Add unified authority/reservation event ordering | 999716e8cd31d8d8f04fc7a21d3e338820c10b89 |
| Align restrictive overlays with D-023 | f0403f441d63b6abe5b9086d50013cdb115a6ffc |
| Add owner approval ceremony | f0da431efeec96b22ebac5b377a27aa3855e5d83 |
| Requirements owner-approval presentation | 6aea0ba2e3f6e9a611e9a88bd2c9e6b9cb476c19 |
| Traceability owner-approval presentation | bd2f2d26019fb6aff9394711f2858a85157c96e6 |
| Clarify health supervisor/security controller separation | 1c83d1719cd7cc7188bcfc11fce04d83223da3f7 |
| Clarify security authority separation | 825891a292739e311376caa1f5b7493507fd153d |
| Align risk handshake with action gateway | a0c5e1a21779e42d3dd22fad693bac3db4e5df33 |
| Risk reservation lifecycle | 66728208bedaec1a02866c3d7c3355aba0199852 |
| Architecture unified state model | 3deb34fbd9ae37dfe646404b69baa80f1f49e58c |
| Roadmap unified state model | beeabf71b001aac3475f0028662eebbb06e51dbb |
| Traceability unified state model | ed307430eea2fe8869e5dac424b69809f1508eb5 |
| ADV-39 approval UI threat | 2a7d73a9a16d9cac18fd5b1b0f9156ae51ebb3fd |
| Create checkpoint 070 audit | 55641359ed4edb2759630ccf3c1e3f6bf8df1bda |
| Index checkpoint 070 | 56eaa01493ce4f6e25782256b534bcd9e90cfc1c |

This verifies repository content only. It does not constitute runtime, security, database durability, host isolation or exchange execution testing.
