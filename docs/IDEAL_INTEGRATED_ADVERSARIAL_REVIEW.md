# IDEAL Integrated Adversarial Architecture Review

**Status:** Phase 02 review draft; owner decisions and independent review pending  
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

1. **Autonomy versus human approval:** the security document's requirement for human approval of consequential financial operations is ambiguous against the intended autonomous operating model.
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

### Proposed bounded-authority model — not accepted

Separate owner approval into three layers:

1. **Constitutional approval:** owner explicitly approves the domain, capability, account scope, operating mode, hard policy, maximum permissions, risk limits, stop conditions and duration. This grants a bounded capability, not unlimited authority.
2. **Autonomous in-envelope operation:** a future authorised engine may submit individual actions without per-action human approval only when every action is inside the pre-approved envelope and passes fresh security, data, health and risk checks.
3. **Human approval required:** policy/limit changes, new accounts or venues, credential creation/permission expansion, transfers/withdrawals/payments, disabling safeguards, recovery from a security incident, out-of-envelope actions and any action class expressly reserved to the owner.

Every autonomous action remains attributable, exact-action-bound, risk-approved, auditable and revocable. The owner can suspend the capability. No AI agent may expand the envelope or approve its own exception.

### Owner decision required

Does the owner intend bounded autonomous financial actions to be permitted in a future, separately approved operating mode, or should every consequential financial operation require individual human approval? Until resolved, do not design a final permission matrix or claim that the architecture supports autonomous execution.

## 4. Highest-severity findings

| ID | Severity | Finding | Failure/attack path | Required design response | Status |
|---|---|---|---|---|---|
| ADV-01 | Critical | Human-approval semantics conflict with autonomy objective | Every order requires approval, or an agent bypasses approval by labelling trades routine | Define bounded pre-authorised capability envelope and reserved human-approval classes | Owner decision |
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
