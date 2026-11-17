# IDEAL Integrated Adversarial Architecture Review

**Status:** Phase 02 review draft; autonomy governance decision accepted (D-023); remaining design gaps and independent review pending  
**Date:** 17 November 2026  
**Scope:** Cross-pillar threats, trust boundaries, authority conflicts, common-mode failures and recovery  
**Authority:** Read-only architecture review and documentation. No code, runtime integration, external scanning, account access, credentials, paper/live execution or phase advancement is authorised.

## 1. Review method and limitations

This review challenges the combined risk, data-integrity, system-health and security architecture using STRIDE-style threat categories, abuse cases, failure-mode analysis and recovery scenarios.

It uses the current IDEAL architecture documents and the two Phase 02 traceability artefacts:
- [Core Protection Architecture](IDEAL_CORE_PROTECTION_ARCHITECTURE.md)
- [Security Architecture](IDEAL_SECURITY_ARCHITECTURE.md)
- [Data Integrity and Health](DATA_INTEGRITY_AND_HEALTH.md)
- [Risk Management Architecture](IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md)
- [Risk Architecture Reconciliation](RISK_ARCHITECTURE_RECONCILIATION.md)
- [Integrated Foundation Traceability Matrix](IDEAL_FOUNDATION_TRACEABILITY_MATRIX.md)

This is a structured main-model review. No independent security assessor, penetration tester or subagent review has completed. It is not a certification, penetration test, proof of security or guarantee that all vulnerabilities have been identified.

## 2. Executive assessment

The four-pillar architecture is directionally sound: authority is separated, unknown states are explicit, risk-increasing actions fail closed on critical uncertainty, and security is not conflated with service health.

The main remaining weaknesses are not missing slogans or additional product features. They are unresolved enforcement details at trust boundaries:

1. **Bounded-autonomy enforcement:** the owner has selected the bounded-authority model (D-023). The governance ambiguity is resolved; its policy schema, signing, identity, revocation and enforcement mechanisms remain open design work.
2. **Supervisor independence:** a supervisor on the same compromised host/process/storage failure domain may provide false assurance.
3. **Policy root of trust:** signed/versioned policy is proposed, but bootstrap trust, key compromise, rotation, revocation and recovery are not designed.
4. **Action/audit atomicity:** the system has not decided when durable audit acknowledgement is mandatory relative to reservation and action submission.
5. **Time and ordering:** event time, receive time, monotonic deadlines, source sequence and UTC risk boundaries need one coherent contract.
6. **Privacy versus append-only evidence:** immutable audit and data retention must coexist with lawful deletion, minimisation and purpose limitation.
7. **Recovery authority:** independent evidence is required from each pillar, but the release authority and exact attestation criteria are not yet defined.

These are Phase 02 design gaps. They do not justify starting implementation before they are resolved.

## 3. Material authority conflict: autonomy versus human approval

### Observed ambiguity

The security architecture requires explicit human approval for sensitive permission grants, new integrations and consequential financial operations. IDEAL's strategic objective includes autonomous strategy operation under deterministic risk controls.

If every trade/order is classified as a consequential operation requiring a fresh human approval, the system is not autonomous in the intended sense. If all trades are treated as automatically approved, the human approval requirement could be bypassed in spirit.

### Owner decision — accepted as D-023

The owner selected the following three-layer authority model:

1. **Constitutional approval:** owner explicitly approves the domain, capability, account scope, operating mode, hard policy, maximum permissions, risk limits, stop conditions and duration. This grants a bounded capability, not unlimited authority.
2. **Autonomous in-envelope operation:** a future authorised engine may submit individual actions without per-action human approval only when every action is inside the pre-approved envelope and passes fresh security, data, health and risk checks.
3. **Human approval required:** policy/limit changes, new accounts or venues, credential creation/permission expansion, transfers/withdrawals/payments, disabling safeguards, recovery from a security incident, out-of-envelope actions and any action class expressly reserved to the owner.

Every autonomous action remains attributable, exact-action-bound, risk-approved, auditable and revocable. The owner can suspend the capability. No AI agent may expand the envelope or approve its own exception.

### Decision outcome

**Resolved:** the owner approved bounded, owner-authorised autonomy for the future architecture. Individual actions inside an active, explicitly approved envelope do not require per-action human approval, but still require fresh deterministic risk approval, exact security authorisation, trusted data, required health interlocks and durable audit. The owner retains approval of capability activation, envelope/policy/permission changes, new account/venue/integration scope, credential and privilege changes, transfers/withdrawals/payments, safeguard disablement and reserved irreversible or incident-recovery actions.

D-023 is a future governance decision only. It does not activate an envelope or authorise implementation, exchange access, credentials, paper/live execution or phase advancement.

## 4. Highest-severity findings

| ID | Severity | Finding | Failure/attack path | Required design response | Status |
|---|---|---|---|---|---|
| ADV-01 | Critical | Bounded-autonomy enforcement is not yet specified | Envelope bypass, stale approval, privilege escalation or agent self-modification | Implementable policy schema, signed versioning, external permission enforcement, revocation and exact-action risk binding | Governance resolved by D-023; enforcement open |
| ADV-02 | Critical | Health supervisor may share host/process/storage trust with monitored system | Host compromise disables or falsifies both application and monitor | Define independent failure domains, external heartbeat/log path and out-of-band alert/recovery proportionate to deployment | Open |
| ADV-03 | Critical | Policy root of trust and bootstrap recovery unspecified | Attacker replaces policy and signing key, or legitimate key rotation locks out owner | Define offline/bootstrap trust, signing, approval, rotation, revocation, rollback and compromise recovery | Open |
| ADV-04 | Critical | Audit durability versus action atomicity unresolved | Action occurs but evidence is lost, or audit failure causes unsafe partial state | Define durable intent/decision/reservation/action protocol and per-action audit-ack requirement | Open |
| ADV-05 | Critical | Reservation and external side effect cannot be one ordinary local transaction | Crash between local reserve and venue submission/ack creates unknown exposure | Use explicit idempotent state machine, durable outbox/intent, reconciliation and conservative unknown-state reservation | Open |
| ADV-06 | High | Time semantics are fragmented | Clock skew, delayed events or UTC rollover changes expiry/loss calculations | Separate source event, receive, ingest and monotonic process times; define trusted UTC and skew bounds | Open |
| ADV-07 | High | Immutable evidence conflicts with deletion/retention duties | Append-only logs retain sensitive personal data indefinitely | Data classification, minimised event payloads, retention classes, redaction/tombstone and cryptographic-erasure strategy where appropriate | Open |
| ADV-08 | High | Recovery attestations and release authority are undefined | One restarted component declares system recovered while another pillar remains compromised | Require scoped attestations from Security, Data, Health and Risk plus explicit release authority | Open |
| ADV-09 | High | External data authenticity can be confused with integrity | Hash proves payload unchanged after receipt but not that provider's original value was true | Distinguish transport/source authentication, independent corroboration, plausibility and internal integrity | Partial |
| ADV-10 | High | Break-glass access and identity-provider outage are not specified | Owner is locked out during incident or emergency access becomes a permanent bypass | Define offline recovery identity, hardware/device trust, scope, expiry, dual evidence and post-use review | Open |
| ADV-11 | High | Security monitoring can be disabled or deceived | Compromised host reports healthy and suppresses local alerts | Independent heartbeat, external evidence destination, monitor self-protection and missing-telemetry alert | Partial |
| ADV-12 | High | Cross-domain data and permission leakage | Agent or service with one domain's access reads another domain's financial records | Separate domain scopes, resource-level authorisation, retrieval isolation and negative cross-domain tests | Partial |
| ADV-13 | High | Supply-chain trust is not bound to runtime identity | Approved source changes after review or untrusted build artefact is deployed | Pin dependencies, protect CI, provenance/attestation, signed release and deployment verification | Partial |
| ADV-14 | High | Unknown external order state can persist indefinitely | Venue API unavailable; local state cannot prove order cancellation or position status | Explicit manual reconciliation path and no-risk-increase state until authoritative evidence restored | Partial |
| ADV-15 | Medium | Vulnerability severity/exception policy not yet measurable | Findings remain open indefinitely or exceptions silently become permanent | Define severity, exploitability, remediation targets, owner, expiry and retest requirements | Partial |
| ADV-16 | Medium | Alert delivery may share compromised device/channel | Mobile notification is suppressed or device is lost | Independent secondary alert path and clear degraded alerting state | Open |
| ADV-17 | Medium | Backup encryption-key recovery may be weaker than backup encryption | Encrypted backup exists but key is unavailable or stolen | Separate key hierarchy, offline recovery, rotation and restore exercises | Partial |
| ADV-18 | Medium | Test coverage may not establish control effectiveness | Assertions mirror implementation or tests miss realistic mutation | Independent oracle, mutation testing, adversarial fixtures and reviewer challenge | Partial |

## 5. STRIDE-style threat coverage

| Threat class | IDEAL assets/boundaries | Representative abuse cases | Principal controls/evidence needed |
|---|---|---|---|
| Spoofing | Owner, services, agents, venue/data adapters, device sessions | Stolen session; forged source; service impersonation; replayed identity | Strong authentication, service identity, peer verification, short-lived credentials, source provenance, replay protection |
| Tampering | Risk policy, code, configuration, market/account evidence, ledger, model artefacts, audit | Change risk limit; alter fill; poison data; replace model; rewrite logs | Signed/versioned policy, immutable evidence, hashes, protected builds, independent reconciliation and audit anchoring |
| Repudiation | Owner approvals, agent/tool actions, policy changes, orders, incidents | Deny approving a capability; ambiguous actor; missing tool trace | Attributable identity, approval record, correlation IDs, ordered audit, time synchronisation and protected logs |
| Information disclosure | Credentials, financial records, tax/identity data, private strategies, licensed market data | Log leakage; prompt exfiltration; cross-domain retrieval; backup theft | Classification, encryption, least privilege, redaction, retrieval isolation, retention and export controls |
| Denial of service | Data feeds, risk service, health supervisor, storage, audit, identity | API exhaustion; disk full; supervisor outage; lockout; alert flooding | Quotas, bounded retries, circuit breakers, resource limits, degraded modes, manual fallback and tested restore |
| Elevation of privilege | AI tools, CI/CD, service identities, admin interfaces, policy registry | Prompt injection; malicious dependency; stolen CI token; agent self-grant | External tool enforcement, sandboxing, branch/release protection, scoped credentials, policy-write separation and negative tests |

## 6. Cross-pillar attack paths

### 6.1 Compromised market-data source

A provider or transport may send plausible but manipulated prices. A hash can show that IDEAL retained the same bytes, not that the original source was honest.

Required layers:
- authenticate source/transport and record entitlement;
- preserve original observation and source timestamps;
- compare independent sources where economically and semantically valid;
- apply plausibility, sequence, spread, mark/index and cross-market checks;
- label disagreement as conflicted/unknown;
- reject risk increases when decision-critical source integrity is unresolved;
- preserve source incident evidence and downstream decision lineage.

### 6.2 Compromised application host

A compromised host may falsify local health, steal secrets, alter code/configuration and tamper with local audit data.

Required layers:
- minimise credentials and host permissions;
- keep critical keys outside ordinary application process memory where feasible;
- independent external heartbeat and evidence destination;
- protected release/build provenance;
- revocation and isolation path independent of the compromised host;
- clean rebuild, key rotation, data reconciliation and audit continuity checks before recovery.

### 6.3 Malicious or compromised AI agent

A malicious document or prompt injection may instruct an agent to reveal data, change risk settings or invoke tools.

Required layers:
- treat retrieved content and model output as untrusted;
- enforce tool allowlists and resource permissions outside the model;
- separate read/research/propose/approve/execute capabilities;
- do not expose raw credentials;
- require exact risk approval for any future action;
- audit tool requests, denials and output provenance;
- test cross-domain leakage and indirect prompt injection.

### 6.4 Concurrent risk and execution race

Two valid-looking requests can exceed portfolio capacity; a venue may accept an order while acknowledgement is lost; cancellation may remain pending.

Required layers:
- atomic risk reservation before submission;
- idempotent intent identity and durable state transitions;
- exact action-bound approval and one-time consumption;
- retain reservations for unknown/cancel-pending state;
- reconcile authoritative venue state before retry/release;
- exercise concurrency, crash points, duplicate/reordered events and partial fills.

### 6.5 Recovery and backup compromise

Ransomware or an attacker may corrupt primary and backup data or steal recovery keys.

Required layers:
- separate backup credentials and key hierarchy;
- offline/immutable recovery copy where proportionate;
- periodic restore test with integrity verification;
- verify code/configuration, identity, keys, data, ledger, audit and external account state independently;
- no automatic release of risk restrictions merely because services restart.

## 7. Architecture decisions needed before contract freeze

| Decision | Proposed direction | Why it matters |
|---|---|---|
| Autonomous authority | Bounded, owner-approved capability envelope; human approval for policy/permission expansion and reserved action classes | Resolves autonomy/security conflict without unrestricted agent authority |
| Supervisor topology | Start with independent process and separate evidence/alert path; assess host-level separation for deployment | Reduces common-mode failure without prematurely adding costly infrastructure |
| Policy trust | Owner-controlled signing root with protected recovery and versioned policy | Prevents runtime/agent policy mutation and defines recovery |
| Audit/action protocol | Durable intent and reservation before external side effect; explicit acknowledgement rules | Prevents unaudited or duplicated actions |
| Time model | UTC wall-clock for external chronology plus monotonic deadlines for in-process expiry; source sequence where available | Prevents skew, replay and boundary errors |
| Privacy/audit | Store references/hashes and minimal decision evidence; keep sensitive payloads in separately governed stores with retention/deletion rules | Balances reproducibility with privacy and licence constraints |
| Recovery authority | Each pillar supplies scoped evidence; owner-controlled release for high-impact incidents | Prevents one component certifying the whole system |
| Break-glass | Offline, tightly scoped, time-limited recovery capability with mandatory audit and post-incident review | Avoids both lockout and permanent bypass |

These are proposals for owner review, not accepted architecture decisions.

## 8. Prioritised closure sequence

1. Resolve autonomy versus human-approval semantics.
2. Define security policy root of trust, key lifecycle and break-glass recovery.
3. Define health supervisor failure-domain topology and out-of-band evidence.
4. Define durable audit/reservation/action transaction semantics.
5. Define time, ordering, freshness and UTC boundary contracts.
6. Define privacy, retention, deletion and immutable-audit strategy.
7. Define per-pillar recovery attestations and release authority.
8. Complete STRIDE/abuse-case coverage for all interfaces and domains.
9. Obtain independent architecture/security review.
10. Only then consider formal Phase 02 acceptance.

## 9. Explicit boundaries

- No policy decision in this review is owner-approved.
- No numerical risk threshold or permission grant is changed.
- No code, scanner, penetration test, dependency, runtime, host, account, venue or integration is selected or activated.
- No paper or live trading is authorised.
- Phase 02 remains active; Phases 03–19 remain locked.


## 10. D-023 governance decision incorporated

The owner has explicitly selected bounded, owner-authorised autonomy. The architecture must therefore distinguish:
- **Owner constitutional authority:** approves the future capability envelope and reserved action classes.
- **Autonomous in-envelope authority:** permits individual actions without per-action human approval only after all deterministic and security gates pass.
- **Reserved owner actions:** activation, scope/policy/permission changes, credentials/privilege expansion, fund movement, safeguard disablement and specified irreversible/recovery actions.

This resolves the policy ambiguity identified in ADV-01. It does not resolve the engineering controls needed to make the envelope tamper-resistant and enforceable. Those remain critical Phase 02 work, including policy root of trust, key recovery, action-bound permission checks, risk reservations, audit/action atomicity and independent health/security interlocks.


## Checkpoint 067 — autonomy authority and permission design follow-up

The bounded-autonomy ambiguity identified in ADV-01 is resolved at the governance level by D-023, but technical enforcement remains an open Phase 02 design risk. The authority design now requires a non-bypassable action boundary, separate owner/security and risk gates, exact-action digest binding, independent workload identity, signed/versioned envelope and policy artefacts, revocation epochs, conservative reservation/dispatch semantics, and audit-before-admission. New explicit attack cases include Cedar policy-error skip semantics, OPA unsigned-bundle configuration, replayed owner approval, stale/revoked admission, key-purpose confusion, revocation partition, backup resurrection, clock rollback, policy-update/dispatch race and external side-effect acknowledgement loss. See [Autonomy Authority and Permission Architecture](IDEAL_AUTONOMY_AUTHORITY_AND_PERMISSION_ARCHITECTURE.md). These are design findings, not runtime test results.


## Checkpoint 068 — adversarial closure review: revocation, host isolation and recovery

### A. Revocation race finding

A single revoked flag and short-lived token are insufficient. IDEAL must serialize revocation against the dispatch-start transition at one authoritative boundary. The durable transition to DISPATCH_STARTED is the local linearisation point:

- Revocation committed first: dispatch is denied.
- Dispatch-start committed first: the request is in-flight and cannot be recalled by IDEAL.
- Crash/acknowledgement ambiguity: classify as potentially dispatched, retain reservation and reconcile.

Revocation lifecycle is ACTIVE → REVOKE_REQUESTED → FENCING → DRAINING → EFFECTIVE, with RECONCILIATION_REQUIRED or RECOVERY_HOLD when worker acknowledgement, external outcome or authority integrity is uncertain. Global EFFECTIVE requires all registered dispatch boundaries to acknowledge the new monotonic generation and all unstarted actions to be fenced. A network partition prevents a false EFFECTIVE claim. The venue may still receive a request already transmitted.

### B. Host compromise finding

A strategy/AI process must not share credentials, UID, writable trust-anchor storage, unrestricted sockets or privileged IPC with the authority/action gateway. Logical trust zones Z0–Z4 are now defined in the autonomy architecture. For Linux, evaluate separate UIDs, capabilities removal, namespaces/cgroups, seccomp, Landlock/SELinux/AppArmor, read-only images, strict IPC and default-deny egress. Namespaces/containers alone are not a sufficient security boundary.

For hostile generated code, evaluate disposable microVMs. Firecracker's own design treats guest vCPU code as malicious, recommends its jailer in production and leaves guest egress filtering to host-level controls. Firecracker does not protect a compromised host kernel/root. If the gateway and agent share a root-compromised host, local process separation cannot guarantee gateway integrity. Stronger assurance requires a separately protected gateway/credential trust domain and independently enforced network policy.

### C. Recovery and rollback finding

Backups restore historical data, not current authority. A restored snapshot can resurrect revoked envelopes, keys, identities, policy, epochs or one-use capabilities. All restored authority state is quarantined; ephemeral capabilities are invalidated; recovery advances the generation; the latest revocation state must be checked against a trust anchor independent of ordinary backup. If current authority cannot be established, remain in RECOVERY_HOLD. Rebuild, re-attest, rotate identities, validate audit, reconcile external venue state and require explicit owner approval before reactivation.

### D. New prioritised attack cases

| Case | Attack | Required outcome |
|---|---|---|
| ADV-19 | Revocation commits after permit issuance but before dispatch-start | Generation mismatch; no network write |
| ADV-20 | Revocation and dispatch-start race concurrently | One serialised winner; in-flight semantics if dispatch-start wins |
| ADV-21 | Partitioned worker resumes using cached authority | Deny; no stale-generation dispatch |
| ADV-22 | Worker omitted from revocation registry | No global EFFECTIVE; inventory/attestation discrepancy triggers hold |
| ADV-23 | Strategy escapes container and reaches host gateway | Independent boundary/network isolation prevents privileged action |
| ADV-24 | Agent reads gateway credential through procfs, FD, environment or shared mount | No credential exists in agent trust zone; access denied |
| ADV-25 | DNS rebinding/redirect/proxy abuse reaches venue API from Z0 | Host-enforced egress denial |
| ADV-26 | Root/kernel compromise on shared host alters local gateway | Treat host trust as lost; disable capability and recover in separate trust domain |
| ADV-27 | Restore old snapshot predating revocation | Independent high-water anchor rejects old generation |
| ADV-28 | Restore while disconnected from trust witness | RECOVERY_HOLD; no execution activation |
| ADV-29 | Old workload token/owner assertion replayed after recovery | New generation/nonce/credential state rejects replay |
| ADV-30 | Backup attacker alters both authority DB and local checkpoint | Independent trust anchor detects or forces manual recovery hold |

### E. Evidence and limitations

The analysis is grounded in NIST SP 800-207's resource-centric zero-trust model, OWASP transaction authorisation guidance requiring a final execution gate and operation-specific short-lived authorisation, Linux Landlock documentation (including kernel ABI/feature limits and its warning that namespaces alone are not designed as complete access-control), Firecracker's own threat-containment and egress-filtering design, and TUF anti-rollback/freeze-attack protections. See the source register in the autonomy architecture.

This is a design review only. No sandbox escape, penetration test, kernel test, external scan, recovery exercise or runtime fault injection was performed. The threat model is not proof that every vulnerability is known or prevented.

### F. Remaining gates

- Physical topology and gateway separation depend on deployment decision and are not frozen.
- Revocation propagation SLO, worker inventory authority and strong-consistency store remain open.
- Root/recovery key custody and independent high-water anchor remain open.
- Exact OS sandbox profile, microVM selection and egress implementation remain open.
- These are Phase 02 architecture decisions; no runtime implementation or Phase 03 advancement is authorised.


## Checkpoint 069 — supervisor, policy root and audit atomicity challenge

The architecture now specifies the following additional invariants:

1. The health supervisor is an observer with a one-way restrictive interlock channel. It can deny/restrict affected risk-increasing actions, but cannot create authority, edit policy, approve risk, release restrictions after critical incidents, or initiate financial side effects.
2. A separate process identity is not independent against shared host root/kernel compromise. Stronger threat models require a separate host/VM/hardware watchdog or an explicit loss-of-trust response.
3. Policy/envelope lifecycle is immutable: DRAFT → VALIDATED → OWNER_APPROVED → SIGNED → PUBLISHED → ACTIVE → SUPERSEDED/REVOKED. Owner approval binds exact digest and context; publisher signature is a distinct role. Activation, revocation and dispatch-start share a monotonic serialized generation.
4. Transaction A atomically commits canonical intent, authority evidence, risk reservation, audit event and outbox. Transaction B atomically consumes the one-use permit, checks generation and commits DISPATCH_STARTED plus audit before network write. Transaction C appends authoritative outcome/reconciliation and updates reservation/order state.
5. The local store and remote exchange cannot share an ACID transaction. A potentially transmitted request with missing acknowledgement remains UNKNOWN; idempotency and reconciliation replace impossible exactly-once claims.
6. Audit projection/witness outage does not erase durable local pre-dispatch evidence; failure to commit required local intent/dispatch-start evidence blocks new risk-increasing side effects.

### New adversarial cases

| Case | Attack/failure | Required outcome |
|---|---|---|
| ADV-31 | Compromised health supervisor asserts HEALTHY to hide failure | Gateway does not trust self-attestation; independent signals/heartbeat and scoped fail-closed controls |
| ADV-32 | Compromised supervisor issues a financial action | No interface/permission exists; restrictive-only channel |
| ADV-33 | Supervisor false-positive floods restrictions | Scoped reason codes, rate limits/hysteresis; availability impact is visible and owner-resolved |
| ADV-34 | Policy publisher signs an owner-unapproved scope expansion | Exact owner approval missing/mismatched; activation denied |
| ADV-35 | Owner approval for one digest is replayed against another policy | Digest/context/nonce mismatch; reject |
| ADV-36 | Policy update races dispatch-start | Shared generation serialises; stale policy cannot dispatch |
| ADV-37 | Audit/outbox write fails but adapter still dispatches | No durable Transaction A/B, therefore no network side effect |
| ADV-38 | External venue accepts but Transaction C/audit projection fails | Preserve DISPATCH_STARTED/UNKNOWN and reservation; reconcile and append outcome later |

### Residual risks

- A single-owner root/recovery design cannot obtain true two-person separation without changing the ownership model. Hardware-backed possession plus user verification may reduce risk but is not equivalent to dual control.
- A local-only host cannot independently prove its own root/kernel integrity after root compromise. A separate trust domain or fail-closed dormant state is required for that threat.
- Audit hash chains do not prevent rewrite if attacker controls both event store and checkpoint trust. Independent checkpoint storage and recovery tests are required.
- Local transactional durability is not the same as external side-effect atomicity. The adapter boundary remains an uncertainty boundary.

No runtime fault injection, supervisor compromise test, key ceremony, database crash test or venue reconciliation exercise was performed.


### Additional owner-approval interface attack

| Case | Attack/failure | Required outcome |
|---|---|---|
| ADV-39 | Approval UI displays a harmless summary while the signed artefact contains expanded scope, hidden fields or altered limits | Approval challenge binds exact digest; summary generated from same immutable artefact; critical diff shown; ambiguous/truncated/mismatched presentation denied |

A valid authenticator assertion is not proof of informed consent if the owner was not shown the exact scope and consequences. The approval interface, challenge and verifier are one security protocol and require end-to-end tests.


## Checkpoint 071 — consolidated residual-risk and workstream closure assessment

The new [Autonomy Authority Closure Assessment](IDEAL_AUTONOMY_AUTHORITY_CLOSURE_ASSESSMENT.md) distinguishes design invariants from provisional deployment recommendations and platform-dependent owner decisions. The following cannot be designed away and must be explicitly accepted/mitigated before any future execution approval: already transmitted venue requests cannot be recalled; host root/kernel compromise defeats same-host process isolation; offline recovery checkpoints may be stale without an independent anchor; one owner cannot provide true two-person control; local audit integrity is not independently provable if all storage and checkpoint keys are compromised; external venue state remains outside IDEAL's ACID transaction; research cannot prove every vulnerability has been found.

Workstream closure is not Phase 02 closure. Explicit owner acceptance and other Phase 02 foundation/architecture work remain required.
