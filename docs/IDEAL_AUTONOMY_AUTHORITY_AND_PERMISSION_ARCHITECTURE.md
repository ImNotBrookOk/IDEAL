# IDEAL Autonomy Authority and Permission Architecture

**Status:** Phase 02 research/design draft — not an approved implementation specification  
**Research date:** 17 November 2026  
**Governance basis:** D-023 Accepted — bounded, owner-authorised autonomy  
**Scope:** Future authority, identity, policy, permission enforcement, revocation and audit. No execution capability is currently authorised.

## 1. Purpose and design conclusion

D-023 establishes the intended future operating model: the owner explicitly grants a bounded, versioned and revocable operating envelope. A future engine may act without per-action owner approval only inside that envelope and only when independent controls also approve the exact action.

**Central design conclusion:** authority must be enforced at a dedicated action boundary outside strategy, model and agent processes. That boundary independently verifies the owner's grant, requesting workload identity, exact action scope, current policy and revocation state, risk decision/reservation, trusted data, health/security interlocks and audit preconditions. A model prompt, UI toggle, signed configuration file by itself, or policy-engine Allow result is never sufficient.

This document defines a technology-neutral control model. It does not select or adopt a policy engine, identity platform, key manager, cryptographic format or runtime dependency.

## 2. Non-negotiable invariants

1. **Owner is the authority root.** Only authenticated owner approval may create or expand an operating envelope or alter reserved owner-only controls.
2. **No self-grant.** An agent, model, strategy, execution adapter, policy evaluator or health supervisor cannot grant itself permission or broaden scope.
3. **Default deny.** Absent, malformed, ambiguous, expired, revoked, unverifiable or unsupported permission is denial.
4. **Authentication is not authorisation.** Workload identity proves which process is requesting; it does not prove the process may perform the action.
5. **Envelope is necessary, not sufficient.** An action must be inside the owner envelope and separately pass every applicable policy and risk gate.
6. **Exact-action binding.** Approval applies to one canonical immutable action, not a mutable strategy intent or broad reusable token.
7. **No stale authority.** Policy, envelope, key, identity, risk reservation, data evidence and interlock state must be current for the defined validity window.
8. **Independent enforcement.** The action boundary must not trust caller-supplied claims about identity, approval, risk status, account state or audit completion.
9. **Restrictiveness is monotonic during incidents.** Emergency controls may reduce or suspend authority. They cannot silently create authority or initiate a financial action.
10. **Unknown is not healthy.** Unavailable policy, revocation, clock, risk, data, health, security or required audit state cannot be interpreted as permission.
11. **No silent cross-domain inheritance.** Permission for one account, venue, asset class, ledger or domain implies no permission for another.
12. **Evidence is part of the decision.** Every consequential decision must be reconstructable without retaining secrets in audit records.

## 3. Authority hierarchy and trust boundaries

| Layer | Permitted responsibility | Prohibited authority |
|---|---|---|
| Owner | Approve/revoke envelope and reserved changes/actions | Implicitly delegate unrestricted authority |
| Owner approval interface | Authenticate owner; present exact change/action; capture explicit approval | Decide financial risk or obscure consequences |
| Authority registry | Store immutable envelope/policy versions and status | Invent or approve a grant |
| Identity issuer/verifier | Authenticate distinct workload identities and validity | Grant business permissions by identity alone |
| Policy decision component | Evaluate request against verified policy; return reason/version | Execute actions, mutate policy or override risk |
| Action enforcement boundary | Revalidate prerequisites and admit/reject exact action | Trust caller claims or permit alternate routes |
| Risk authority | Approve/restrict/deny exact risk-bearing action and reserve capacity | Grant owner or security authority |
| Data-integrity authority | Establish provenance, quality and reconciliation | Grant action permissions |
| Health/security interlocks | Signal restrictive states and block admission | Create financial authority or self-certify |
| Execution adapter | Perform admitted operation and report outcome | Change payload or expand permission |
| Audit/evidence service | Preserve attributable decision/action history | Be sole truth for whether external action occurred |

Strategy/AI submits an untrusted proposal to an internal command boundary. The boundary authenticates the caller, canonicalises and validates the action, checks owner envelope and policy, obtains fresh data/health/security evidence, obtains deterministic risk approval and reservation, records durable admission evidence, then permits a narrowly scoped adapter operation.

The adapter must be reachable only through this boundary. Network separation alone is insufficient if strategy can reach adapter credentials, sockets, databases, queues or operating-system interfaces by another route. Enforcement must exist at the lowest practical point controlling the side effect.

## 4. Owner-approved operating envelope

### 4.1 Required semantics and fields

The envelope is a versioned capability grant with at least:

- immutable envelope ID, monotonic version, schema version and content digest;
- owner identity and approval evidence reference;
- lifecycle state: draft, approved, active, suspended, revoked, expired or superseded;
- effective-from and expiry timestamps with explicitly defined trusted time;
- domain, environment, capability, account and venue scope using canonical identifiers;
- canonical instrument/contract scope;
- permitted action classes and explicit denied/reserved action classes;
- operating mode (research, simulation, paper, live), each a distinct capability;
- maximum notional/exposure, per-action and aggregate bounds, concurrency/rate limits and other owner-approved ceilings;
- permitted order types, time-in-force, reduce-only semantics and price/quantity constraints where relevant;
- explicit exclusions and integration scope;
- stop conditions, mandatory interlocks, escalation and expiry behaviour;
- revocation generation/epoch and audit/retention requirements.

Reject unknown critical fields, duplicate keys, invalid enums, contradictory scopes, missing values and unsupported schema versions. Never silently ignore a field that could widen authority.

### 4.2 Envelope rules

- Omitted capability means **not permitted**.
- Explicit deny takes precedence over allow.
- More-specific grants cannot exceed parent limits.
- Limits are ceilings, not targets or default allocations.
- Policy updates cannot widen authority without a separately authenticated owner-approved envelope change.
- Expiry/revocation must apply even when strategy is offline or retains cached state.
- New/changed envelopes remain inactive until owner approval, signature verification, registry publication and activation checks complete.
- Activation/reactivation is owner-reserved under D-023.
- Preserve prior versions and transition evidence; never overwrite historical authority state.

An illustrative future envelope might cover one approved domain, one account, one venue, a finite set of perpetual instruments and a narrow list of action classes. It would explicitly exclude withdrawals, transfers, account changes, API-key management, policy changes and all unapproved markets/domains. This is a schema illustration, not a proposed grant.

## 5. Identity, authentication and authorisation

### 5.1 Owner identity

Use phishing-resistant public-key authentication with user verification for sensitive approval ceremonies. WebAuthn Level 3 is a standards-based candidate for browser-mediated public-key credentials and user consent. A WebAuthn assertion is not automatically a complete signature over an IDEAL policy artefact: the application must bind the challenge to the exact operation, origin/RP context, nonce, expiry and content digest.

Recovery must not create an easier route to authority escalation. Device replacement, lost-authenticator recovery and credential revocation are high-risk owner operations requiring explicit design and tests.

### 5.2 Workload identity

Every privileged service has a distinct cryptographically verifiable identity. Prefer short-lived automatically rotated identity material. A process must not inherit the permissions of its launching user; internal services must not share one static API key.

SPIFFE/SPIRE is a candidate workload-identity model: workload attestation can issue short-lived X.509 SVIDs and the Workload API supports identity and mutual TLS. Full SPIRE server/agent infrastructure may be excessive for a single-user/local first deployment. Adopt the concepts first; defer the full control plane until deployment topology justifies it.

JWT bearer credentials are replay-sensitive. Prefer mutually authenticated channels with short-lived X.509 credentials where practical. If bearer tokens are unavoidable, bind them to audience, purpose, expiry, issuer and replay controls.

### 5.3 Authorisation

Authorisation asks whether this authenticated principal may perform this exact action on this exact resource under current context. Use deny-by-default and least privilege; validate permission at every consequential request.

A policy engine cannot replace owner-signed grants, trusted policy distribution/versioning, workload identity, current revocation, independent risk approval/reservation, side-effect-boundary enforcement or durable evidence.

## 6. Policy registry, root of trust and key hierarchy

### 6.1 Separate key purposes

Keep cryptographic roles separate:

1. Owner root/recovery authority — establishes/re-establishes the trust anchor; offline or hardware protected where feasible.
2. Owner approval credential — approves a specific envelope/policy change or reserved action.
3. Policy publication key — signs immutable policy releases; cannot approve new owner intent.
4. Workload identity keys — short-lived and scoped to one service identity.
5. Audit checkpoint key — signs evidence checkpoints; cannot approve policy/actions.
6. Data-encryption keys — encrypt stored data; never reused as signing or identity keys.
7. Future venue credentials — narrowly scoped and revocable; inaccessible to AI/strategy processes.

A service key must not mint owner approvals; an audit key must not authorise a trade; a data-encryption key must not sign policy.

### 6.2 Policy publication lifecycle

1. Create immutable envelope/policy candidate.
2. Validate schema, semantic constraints, parent limits and prohibited capabilities.
3. Present a human-readable diff and full effect to the owner.
4. Require strong owner verification and explicit approval of the exact digest.
5. Produce an owner approval artefact bound to digest, schema, intended environment and expiry.
6. Publish a new immutable version with a separate policy-publication signature.
7. Verify owner approval and publication signature against independently provisioned trust anchors.
8. Atomically activate the new version and record the transition.
9. Invalidate outstanding decisions/reservations affected by superseded policy.
10. Retain verification evidence. Rollback is a new owner-approved version, never history rewriting.

A signature proves that a key signed bytes. It does not prove the policy is safe, the owner understood it, or the key was uncompromised. Semantic validation, clear presentation, key custody and independent enforcement remain necessary.

### 6.3 Key lifecycle

Every key class needs an inventory, owner, purpose, algorithm, creation/activation/expiry, rotation rule, storage, access policy, backup/recovery, revocation and compromise response.

Rotation must support safe overlap without accepting revoked keys indefinitely. Revocation must propagate to the action boundary and invalidate grants signed by compromised authority under a documented epoch/version rule. Restoring a backup must not resurrect revoked keys, old envelopes or stale permissions.

Do not store secrets in GitHub, ordinary configuration, logs, model context or audit events. Prefer OS/hardware-backed key storage where supported. A self-hosted secrets manager may be justified later, but adds a privileged service with unseal, backup, upgrade, availability and compromise risks.

## 7. Exact-action authorisation contract

### 7.1 Canonical request

Every consequential request is transformed into a typed, schema-validated canonical action object containing:

- request/idempotency identifiers;
- authenticated principal/workload identity and channel context;
- action type and schema version;
- domain, environment, account, venue and canonical instrument identity;
- exact operation parameters (side, quantity, price/bounds, order type, time-in-force, reduce-only and client order identity);
- envelope ID/version/digest and policy version/digest;
- data-evidence references and freshness/quality states;
- health/security interlock snapshot/version;
- risk decision ID, policy version, exact action digest and reservation ID where applicable;
- creation time, deadline/expiry, trusted clock reference and audit correlation ID.

Financial quantities use decimal strings or fixed-point representations, not binary floating point. Units, contract multipliers, settlement currency, precision and rounding mode are explicit.

### 7.2 Digest and approval binding

Compute the digest from a canonical representation. RFC 8785 JSON Canonicalization Scheme is a candidate for JSON artefacts; RFC 9052 COSE is a candidate signature container. Neither is selected before compatibility, numeric semantics, parser behaviour and interoperability are tested.

The digest binds every field that could change the economic or security meaning of the action. Any change invalidates prior authorisation. Never trust a caller-supplied digest without recomputation.

### 7.3 Decision response

A future decision binds outcome/reason codes, exact action digest, principal/scope, envelope and policy versions/digests, owner approval reference, data/health/security/risk evidence, reservation ID, issue/not-before/expiry times, revocation epoch, unique decision ID/nonce, idempotency linkage, enforcement audience and durable audit correlation.

The result is a narrow, short-lived admission capability, not a general credential. It is audience-bound to one adapter boundary and unusable for a different action, account, instrument, venue or environment.

## 8. Admission, reservation and execution state machine

| State | Meaning | Required behaviour |
|---|---|---|
| PROPOSED | Untrusted intent received | No side effect; validate schema and identity |
| VALIDATED | Canonical action/evidence assembled | Continue only with trusted, fresh mandatory inputs |
| AUTHORISED | Envelope and security policy permit exact action | Still no side effect; obtain risk approval |
| RESERVED | Risk authority reserves potential exposure/capacity | Persist intent and reservation before dispatch |
| ADMITTED | All prerequisites and durable audit preconditions pass; one-use permit exists but is not consumed | Recheck generation and atomically consume permit at dispatch boundary |
| DISPATCH_STARTED | Durable local commit records the final generation check, one-use permit consumption and audit event immediately before network write | This is the local linearisation point; a crash after this point is potentially in-flight/UNKNOWN |
| DISPATCHED | Adapter has attempted the external network write and records the attempt outcome where possible | Track stable idempotency/client reference; do not assume remote receipt or exactly-once semantics |
| ACKNOWLEDGED | Venue returned definitive response | Reconcile with authoritative venue state |
| UNKNOWN | Timeout/disconnect/ambiguous response | Retain reservation; reconcile; do not blindly retry |
| RECONCILED | External state matched to internal records | Transfer/release reservation exactly once |
| REJECTED / EXPIRED / REVOKED | Admission denied/invalidated before side effect | No dispatch; record reason |
| INCIDENT_HOLD | Trust/state materially compromised or uncertain | Restrict new risk; owner-led recovery |

The local system cannot create a true atomic transaction spanning its database and an external exchange. Design for that limitation:

- Persist canonical intent, idempotency key and risk reservation in one local transaction before dispatch.
- Use stable client order IDs where supported, but do not assume universal exactly-once semantics.
- Use a transactional outbox or equivalent durable handoff.
- If response is ambiguous, retain reservation and reconcile authoritative venue order/position state before retry or release.
- Cancellation request is not confirmed cancellation; unknown order state remains reserved.
- Partial fills transfer filled exposure to the position exactly once; unfilled remainder stays reserved until definitive terminal state.
- Never release a reservation because a process restarted, timeout elapsed or agent claims the order is gone.
- Same idempotency key plus same digest returns existing outcome; same key with different digest is rejected and audited.

Revalidate revocation epoch and required interlocks immediately before the external side effect. If material policy, envelope, identity, account, data or risk state changed since admission, reject or obtain fresh approval under explicit semantics.

## 9. Revocation, suspension and emergency restriction

Revocation is a first-class control plane, not a database flag that an agent eventually notices.

- Maintain monotonic revocation epoch/generation.
- Check current status at admission and immediately before dispatch.
- Authenticate, attribute and durably record revocation events through a channel independent of strategy/AI.
- Short-lived admission capabilities limit exposure but do not replace online revocation checks for high-consequence actions.
- If current revocation state cannot be established, deny risk-increasing actions.
- Define and test a maximum revocation propagation window; invalidate caches and outstanding capabilities within it.
- Distinguish owner revocation, key compromise, expiry, policy-integrity failure and security incident.
- Emergency restriction can stop new risk and disable a compromised capability. It cannot transfer funds, withdraw or autonomously initiate liquidation.
- Provide a documented manual fallback if IDEAL's control plane is unavailable or suspected compromised.

Revocation latency is a measurable security requirement; the acceptable maximum remains an open Phase 02 decision.

## 10. Cross-pillar contracts

- **Risk:** necessary but not sufficient. Approval binds exact action digest, risk-policy version, evidence snapshot and reservation. Changed parameters require fresh approval. Unknown order/reservation state retains conservative exposure.
- **Data integrity:** decision evidence carries source identity, source/ingest times, lineage, quality/freshness, correction and reconciliation state. Action boundary verifies accepted evidence rather than trusting strategy summaries.
- **System health:** independent, versioned status may restrict affected actions. Health cannot authorise, approve risk, change policy or initiate financial actions. Supervisor failure requires an independent watchdog/heartbeat failure domain where practical.
- **Security:** verifies identity, authorisation, policy/key integrity, isolation and incident status. A service can be available while compromised; security is not a green process-health flag.
- **Audit:** durable evidence is an admission precondition. Record intent, digest, decisions, reservation, dispatch, response and reconciliation. If external side effect occurs but acknowledgement/audit write is lost, reconcile external state and append correction/incident evidence; never rewrite history.

## 11. Audit, privacy and retention

Use append-only event semantics with tamper-evident chaining or periodic signed checkpoints, independent backups and integrity verification. A hash chain alone is insufficient if an attacker can rewrite the entire chain and its anchor. Protect checkpoints separately and test restoration and truncation detection.

Record actor/workload identity (not credentials), safe/redacted action representation and digest, envelope/policy versions and signature outcomes, decision/reason codes, evidence references, risk reservation lifecycle, interlock/revocation state, adapter metadata and venue reconciliation, owner approvals, key lifecycle events, timestamps/clock quality, correlation IDs and corrections.

Never record private keys, API secrets, access tokens, recovery codes, full authentication assertions or unnecessary personal/financial data. Store sensitive payloads in encrypted access-controlled evidence stores and reference by opaque IDs/hashes. Define separate retention classes for security, financial events, policy history and personal data. Immutability is not a reason to retain secrets or excessive personal data forever; use minimisation, redaction, crypto-shredding where appropriate and reviewed retention rules.

## 12. Recovery and compromise handling

1. Contain affected capabilities and revoke suspect identities/keys through an independent path where possible.
2. Preserve evidence without trusting compromised timestamps/logs as sole truth.
3. Establish scope: envelope/policy versions, identities, action attempts and external account state.
4. Rebuild critical controls from verified source and known-good artefacts.
5. Restore data while preserving revocation epochs and preventing resurrection of revoked grants.
6. Re-establish owner identity/root of trust through documented recovery.
7. Verify policy signatures, workload identity, key inventory, audit integrity and health/security controls.
8. Reconcile external orders, positions, balances and transfers against authoritative sources.
9. Run independent assurance and recovery tests.
10. Require owner approval to reactivate execution capability and any incident-specific reserved authority.

A healthy restart is not proof of trusted recovery. If external state cannot be reconciled, affected capability remains restricted and manual intervention is required.

## 13. Open-source and standards research

Snapshot as of 17 November 2026. Repository activity/release data are point-in-time observations, not quality guarantees. GitHub repository open-issue counts may include pull requests and are not defect-severity measures.

| Candidate | Current evidence snapshot | Licence | Potential role | Limitations / disposition |
|---|---|---|---|---|
| [Open Policy Agent](https://github.com/open-policy-agent/opa) | 12,478 stars; v1.22.4 (12 Nov); pushed 17 Nov; 269 open issue/PR count | Apache-2.0 | General policy-as-code, bundles, decision logs | General-purpose separate service; do not expose server to untrusted networks. Bundle signature enforcement has configuration subtleties: top-level keys without an enforced signing block can permit unsigned bundles. Research only. |
| [Cedar](https://github.com/cedar-policy/cedar) | 1,878 stars; CLI v4.15.0 (16 Nov); pushed 16 Nov; 195 open issue/PR count | Apache-2.0 | Fine-grained application authorisation with typed schema/validation | Strong principal/action/resource/context fit. Cedar skips policy evaluation errors in decision combination; IDEAL wrapper must treat any diagnostic/error as hard denial. Cannot replace owner grant, revocation or enforcement. |
| [SPIRE](https://github.com/spiffe/spire) | 2,624 stars; v1.16.0 (5 Nov); pushed 16 Nov; 117 open issue/PR count | Apache-2.0 | Workload identity, attestation, short-lived X.509 identities | Server/agent/attestation infrastructure may be excessive for single-user/local deployment. Defer full adoption until topology justifies it. |
| [OpenBao](https://github.com/openbao/openbao) | 9,056 stars; v2.7.2 (26 Oct); pushed 12 Nov; 378 open issue/PR count | MPL-2.0 | Secrets, PKI, transit signing/encryption, external KMS/HSM | Privileged service with unseal, backup, upgrade and availability burden. Weak-copyleft licence requires dependency review. Do not deploy merely to avoid a small local key-store design. |
| [Cosign](https://github.com/sigstore/cosign) | 6,444 stars; v3.1.4 (20 Oct); pushed 16 Nov; 151 open issue/PR count | Apache-2.0 | Software artefact signing/verification and supply-chain provenance | Better for build/release integrity than private runtime owner grants. Public transparency can reveal metadata; assess privacy/trust model. |
| [in-toto](https://github.com/in-toto/in-toto) | 1,056 stars; v3.1.0 (4 May); pushed 27 Aug; 61 open issue/PR count | LICENSE file says Apache-2.0; GitHub API licence metadata returned NOASSERTION | Build/release process attestations | Older release cadence in this snapshot; reconcile metadata and exact package/transitive licences before adoption. Not a runtime permission engine. |

### 13.1 Primary-document findings

- OWASP recommends deny-by-default, least privilege and permission validation on every request.
- Cedar's principal/action/resource/context request model and forbid-overrides-permit semantics fit fine-grained application authorisation. Its documented skip-on-error behaviour means IDEAL must reject any decision containing evaluation errors.
- OPA supports signed policy bundles and decision logs. Its documentation warns that configuring keys without a bundle signing block does not enforce signature verification for unsigned bundles. Test unsigned, invalidly signed, wrong-scope and stale bundles.
- SPIFFE SVIDs provide cryptographically verifiable workload identities. X.509-SVIDs are short-lived and rotated; SPIFFE warns JWT SVIDs are replay-sensitive and recommends X.509 where possible.
- OpenBao Transit can sign/verify and encrypt/decrypt without storing application data; v2.7 introduced external HSM/KMS-backed key support. This still adds a privileged dependency that must itself be secured and recovered.
- Sigstore/Cosign uses identity-bound short-lived certificates and transparency evidence. This is useful for software artefact provenance, not a complete private owner-authority protocol.
- RFC 8785 defines canonical JSON for repeatable hashing/signing. It is informational, not Internet Standards Track, and numeric representation is limited to IEEE-754 double precision; high-precision financial values should be strings or another specified fixed-point format.
- RFC 9052 defines COSE signature structures and processing; it does not choose IDEAL's application trust model.
- WebAuthn Level 3 is a W3C Recommendation for scoped public-key credentials and user consent; transaction binding and recovery remain IDEAL responsibilities.
- NIST SP 800-57 Part 1 Rev. 5 is a key-management reference; NIST SP 800-207 provides a resource-centric zero-trust model with no implicit trust based on network location or ownership.

### 13.2 Provisional technology direction — no adoption

Keep the authority model technology-neutral until language/runtime and deployment topology are approved. Cedar is the strongest current candidate for embedded fine-grained application authorisation if Rust integration fits the eventual stack. OPA is an alternative if a language-neutral policy service/distribution plane is needed. Do not use both by default; duplicate evaluators create policy disagreement risk.

Treat SPIFFE/SPIRE as a workload-identity pattern and future candidate, not an assumed initial dependency. Prefer platform-backed key storage for a small local deployment; evaluate OpenBao only if centralised secrets/PKI/key lifecycle justifies another privileged service. Evaluate Cosign/in-toto separately for build/release provenance. No candidate is adopted, installed, pinned or integrated.

## 14. Threat and failure scenarios

| Threat/failure | Required control / expected outcome |
|---|---|
| Prompt injection requests out-of-scope action | Agent proposal remains untrusted; action boundary denies |
| Confused deputy invokes privileged adapter | Distinct workload identity and exact caller/action/resource authorisation |
| Stolen service credential | Short lifetime, audience/scope binding, revocation, limited permissions; no owner authority |
| Replayed approval/admission token | Nonce, expiry, one-use admission state, audience binding, idempotency and digest |
| Action parameters changed after approval | Digest mismatch; reject and obtain fresh authorisation/risk decision |
| Policy replaced or downgraded | Signature verification, monotonic version/epoch and anti-rollback |
| Unsigned OPA bundle accepted | Enforced signature-required mode and negative tests |
| Cedar policy error skipped | Wrapper inspects diagnostics and denies on any evaluation error |
| Owner credential compromised | Revoke credential, suspend affected grants and re-establish owner trust |
| Policy signing key compromised | Revoke key/epoch and quarantine grants signed under it |
| Clock rollback/time-source failure | Monotonic/version checks; deny time-dependent grants if validity unprovable |
| Revocation delayed/lost | Online boundary check; bounded propagation; fail closed if epoch unknown |
| Concurrent requests exceed limit | Atomic reservation at authoritative risk boundary |
| External order accepted but response lost | UNKNOWN; retain reservation; reconcile before retry/release |
| Audit sink unavailable | Do not admit new risk-increasing action; reconcile possible in-flight side effect |
| Health supervisor compromised | Independent watchdog/failure domain; health cannot grant authority |
| Backup resurrects revoked grant | Preserve/reconcile revocation epoch independently |
| Policy update races with dispatch | Recheck current version/epoch immediately before side effect |
| Cross-domain/account confusion | Canonical identifiers and explicit scope; no implicit inheritance |

## 15. Verification and independent assurance

Future verification must include schema/unknown-field/contradiction tests; signature wrong-signer/purpose/audience/environment/expiry/revocation tests; owner approval challenge/replay/recovery tests; policy precedence/missing-attribute/evaluator-error/rollback tests; action-digest mutation tests; prompt-injection/confused-deputy/alternate-route tests; revocation under partition/restart/cache delay/concurrent dispatch; time rollback/skew/expiry boundaries; concurrent reservation/duplicate/partial-fill/cancel-unknown/lost-ack tests; audit truncation/reordering/checkpoint substitution/storage outage/restore tests; key rotation/compromise/recovery tests; cross-domain isolation; and mutation testing.

Acceptance evidence must show not only that valid actions are admitted, but that unauthorised, ambiguous, stale, malformed, replayed, revoked or partially unverifiable actions are rejected at the actual side-effect boundary.

## 16. Open architecture decisions

1. Exact canonical envelope schema and domain/account/instrument identifier registry.
2. Owner approval ceremony: transaction-bound WebAuthn assertion, separate signing ceremony, or both.
3. Signature/canonicalisation format (RFC 8785/JWS/COSE or another verified format).
4. Root-of-trust custody, hardware-backed key availability across Android/PC/server, recovery and succession.
5. Whether initial private deployment needs a policy evaluator; if so, Cedar versus OPA and strict wrapper semantics.
6. Workload identity for local processes versus multi-host deployment; whether SPIRE is justified.
7. Policy registry storage, immutable versioning, anti-rollback and independent trust-anchor provisioning.
8. Revocation epoch, propagation target, offline behaviour and emergency owner fallback.
9. Exact action-admission state machine and transaction boundary with risk reservation.
10. Clock authority, acceptable skew, monotonic clock and expiry semantics.
11. Audit checkpoint format, independent storage, retention/privacy and recovery.
12. Additional owner-reserved actions beyond D-023 minimum list.
13. Secure mobile-first presentation of policy diffs and action consequences.
14. Whether multiple owner factors/dual-control are appropriate for high-impact policy changes.
15. External account/venue permission constraints without exposing credentials to strategy/AI.

## 17. Phase 02 completion criteria

This workstream is incomplete until IDEAL has an owner-reviewed envelope schema/semantics; threat-modelled root-of-trust/key lifecycle; workload identity/authentication design; precise authorisation request/decision contract; non-bypassable enforcement topology; exact-action digest/approval semantics; revocation state machine and measurable propagation target; conservative reservation/dispatch/reconciliation contract; cross-pillar interlock/failure behaviour; audit/privacy/retention/recovery contracts; adversarial tests mapped to requirements; independent review; and explicit owner acceptance.

Technology selection and implementation remain separate later gates.

## 18. Source register

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [Cedar authorization semantics](https://docs.cedarpolicy.com/auth/authorization.html)
- [Cedar policy validation](https://docs.cedarpolicy.com/policies/validation.html)
- [Cedar repository and Apache-2.0 licence](https://github.com/cedar-policy/cedar)
- [OPA releases](https://github.com/open-policy-agent/opa/releases)
- [OPA signed bundle documentation](https://www.openpolicyagent.org/docs/management-bundles)
- [OPA decision logs](https://www.openpolicyagent.org/docs/management-decision-logs)
- [SPIFFE concepts and SVIDs](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/)
- [SPIRE releases](https://github.com/spiffe/spire/releases)
- [OpenBao repository and MPL-2.0 licence](https://github.com/openbao/openbao)
- [OpenBao Transit documentation](https://openbao.org/docs/secrets/transit/)
- [OpenBao 2.7 release notes](https://openbao.org/docs/release-notes/2-7-0/)
- [Cosign signing and verification](https://docs.sigstore.dev/quickstart/quickstart-cosign/)
- [in-toto repository](https://github.com/in-toto/in-toto)
- [NIST SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)
- [NIST SP 800-207 Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)
- [W3C WebAuthn Level 3 Recommendation](https://www.w3.org/TR/2026/REC-webauthn-3-20260825/)
- [RFC 8785 — JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html)
- [RFC 9052 — COSE Structures and Process](https://www.rfc-editor.org/rfc/rfc9052.html)

---

**Current authority state:** D-023 remains the only accepted bounded-autonomy governance decision. This document is a provisional technical design. Phase 02 remains active; Phases 03–19 remain locked. No code, dependencies, runtime, accounts, credentials, exchange connections, paper/live execution, paid services, hosting or external security tests are authorised.

## 19. Adversarial deep review — revocation races and dispatch fencing

### 19.1 Fundamental limit and honest semantics

Revocation cannot recall a request already transmitted to an external venue. IDEAL can prevent queued work, fence dispatchers, invalidate unused admissions, and track/reconcile in-flight work. It cannot guarantee that a request already on a network path will not arrive after revocation is initiated. The system must not claim instantaneous global revocation.

Define the local action linearisation point as the durable transition from ADMITTED to DISPATCH_STARTED at the authoritative dispatch boundary. Revocation and dispatch-start transitions must be serialised against the same authoritative generation:

- If revocation commits first, the action must not transition to DISPATCH_STARTED.
- If DISPATCH_STARTED commits first, the request is in-flight and cannot be recalled by IDEAL; it enters in-flight accounting and reconciliation.
- A crash or lost acknowledgement around the boundary is treated as potentially dispatched, never assumed not dispatched.

This defines what IDEAL controls. It does not promise the remote exchange's receipt or processing order.

### 19.2 Revocation state machine

| State | Meaning | Required controls |
|---|---|---|
| ACTIVE | Envelope/identity may be used within scope | Normal per-action checks |
| REVOKE_REQUESTED | Authenticated request durably recorded | Deny new admissions immediately; reserve next generation |
| FENCING | Action boundaries and dispatch workers being fenced | Invalidate unused capabilities; reject stale generation |
| DRAINING | Workers acknowledge fence; queued actions invalidated; in-flight requests enumerated | Do not retry uncertain requests; retain risk reservations |
| EFFECTIVE | Every registered dispatch boundary acknowledges the new generation and no unstarted action can proceed | Report effective only with complete acknowledgements and durable evidence |
| RECONCILIATION_REQUIRED | Requests may have reached venue or a boundary is unreachable | Remain restricted; reconcile authoritative venue state |
| RECOVERY_HOLD | Authority store, epoch, key or boundary integrity cannot be established | No automatic reactivation; owner-led recovery |

A revocation request can be accepted and locally fail-closed while global effectiveness remains unconfirmed. Status must distinguish REQUESTED, EFFECTIVE and RECONCILIATION_REQUIRED. Never collapse them into a single green revoked state.

### 19.3 Serialisation and fencing protocol

1. The authority registry maintains a monotonic generation and durable append-only transition record.
2. Admission and dispatch-start use a linearizable compare-and-swap or serializable transaction against current generation, envelope version, identity state and action digest. Eventual consistency is insufficient.
3. A dispatcher receives a narrow, one-use permit bound to exact action digest, audience, generation, adapter, account, deadline and unique nonce.
4. Before the external network write, the boundary atomically consumes the permit and records DISPATCH_STARTED against the current generation. A permit cannot be consumed twice.
5. Revocation increments generation and fences dispatchers. A dispatcher unable to reach authoritative state or prove its generation is current must not start a new side effect.
6. Every worker reports acknowledged generation and in-flight request identifiers. Missing acknowledgements prevent global EFFECTIVE.
7. Queued but unstarted actions are invalidated. DISPATCH_STARTED actions remain in-flight/unknown until authoritative reconciliation.
8. Repeated revocation is idempotent. Generations never decrease or get reused.
9. Audit records request, actor, reason, generation before/after, worker acknowledgements, outstanding action IDs, venue reconciliation and final status.

The local store must provide required transactional/linearizable semantics. A distributed deployment must explicitly choose a strong-consistency/consensus design for authority state; an eventually consistent replica cannot authorise dispatch. A single-host design still needs durable commit ordering and crash-consistency tests.

### 19.4 Leases, partitions and time

Short-lived capabilities limit exposure but do not solve revocation. A partitioned dispatcher cannot assume a cached lease remains valid unless a formally bounded lease model, trustworthy monotonic time, bounded clock drift and safe expiry mechanism are proven. Otherwise fail closed.

The maximum revocation propagation objective remains unselected. Phase 02 must specify a measurable maximum for connected boundaries and explicit offline/partition behaviour. No finite network SLO can prove an already transmitted request will not arrive later. EFFECTIVE concerns IDEAL-controlled dispatch boundaries, not remote venue cancellation.

### 19.5 Required race and fault-injection tests

- Revocation wins immediately before dispatch-start: no network write.
- Dispatch-start wins immediately before revocation: request marked in-flight; no false claim of recall.
- Revocation between permit issue and consumption: stale generation rejected.
- Worker paused, partitioned, restarted or clock-shifted: cannot resume on stale state.
- Crash before/after dispatch-start and socket write: classify as not-started only when proven; otherwise UNKNOWN.
- Duplicate/reordered revocation: monotonic generation and idempotent result.
- Authority database failover/rollback: old generation cannot regain validity.
- Worker registry omits a live worker: no false EFFECTIVE.
- Audit sink failure: no new admission; possible in-flight side effects reconciled later without rewriting history.
- Concurrent revocation and policy update: serialised order; no stale-policy dispatch.
- Venue accepts request after local revocation changes: preserve in-flight semantics and reconcile.

## 20. Adversarial deep review — host, process and network isolation

### 20.1 Threat model and hard boundary

Treat every strategy, research script, model runtime, plugin, agent, generated-code process and downloaded artefact as potentially hostile. Prompt instructions, model alignment, application-level tool allowlists, process names and container labels are not security boundaries.

The authority/action boundary, policy trust anchors, risk authority and future venue credentials must not be available to those workloads. A compromised strategy process must be unable to read credentials, open arbitrary venue sockets, modify policy, signal privileged processes, access owner approval material or write directly to the audit trust anchor.

**Critical limit:** if a workload and action gateway share a host whose kernel or root account is compromised, local process isolation alone cannot guarantee the gateway remains trustworthy. Root/kernel compromise can inspect or alter local processes, memory, files, IPC and firewall state. Stronger assurance requires moving gateway and credentials into a separately protected trust domain (separate VM/host, hardware-backed service or external signing/authorisation device) with independently enforced network policy. No design removes this host trust assumption.

### 20.2 Required trust zones

| Zone | Trust level | Contents | Allowed connectivity |
|---|---|---|---|
| Z0 — untrusted workload | Hostile by default | AI/strategy agents, research code, plugins, downloaded data parsers, generated code | No venue network, credentials or host control plane; typed proposal channel only |
| Z1 — ingestion/normalisation | Constrained | External market-data parsers and normalisers | Explicit data-source egress; no authority keys or execution credentials |
| Z2 — deterministic research/risk | Trusted only after verification | Backtests, feature computation, deterministic risk evaluation | Narrow authenticated internal APIs; no direct side-effect credentials |
| Z3 — authority/action gateway | High trust | Owner envelope verifier, policy wrapper, revocation gate, risk reservation coordinator, adapter dispatcher | Minimal typed IPC; narrowly allowlisted outbound venue endpoints only |
| Z4 — trust anchors/recovery | Highest local trust / separately protected | Owner root/recovery keys, policy signing trust, revocation high-water anchor, independent audit checkpoints | No access from Z0; offline or hardware-protected where practical |

The exact number of physical machines is deployment-dependent; logical separation and forbidden flows are requirements. Process separation on one host is not equivalent to a separate hardware/administrative trust domain.

### 20.3 Layered host containment

For a future Linux host, evaluate a layered baseline:

- dedicated unprivileged Unix identity per service; no shared UID between agent and gateway;
- no ambient Linux capabilities; drop all not explicitly required;
- namespaces and cgroups for process, mount, PID, user, IPC, network and resource separation;
- per-workload seccomp syscall policy;
- Landlock and/or SELinux/AppArmor object-access policy;
- read-only runtime image and narrowly scoped writable scratch;
- no container-runtime socket, KVM device, block/raw device or privileged helper exposed to untrusted workloads;
- ptrace, process-tree, core-dump and resource-exhaustion controls;
- explicit network namespaces and host firewall policy; default-deny egress;
- no inherited environment secrets, SSH agent, cloud metadata access or host service tokens;
- bounded IPC schema, message size, rate, timeout and queue depth; authenticate peer credentials and reject unexpected file descriptors/ancillary data;
- patch/kernel/configuration inventory; startup self-test proves controls are active, not merely configured.

Do not silently downgrade when a required control is unsupported. Report actual kernel ABI and enforced control set; if the declared security profile cannot be achieved, the workload cannot receive that trust classification.

Linux Landlock is a useful unprivileged, stackable restriction layer, but kernel/ABI availability and documented limitations must be checked. Namespaces alone are not a complete access-control boundary. seccomp, LSM policy, network isolation and privilege dropping are complementary controls.

### 20.4 Stronger isolation for hostile or generated code

For arbitrary untrusted code, prefer a disposable VM boundary over relying on a conventional container alone where risk warrants the operational cost.

Firecracker is a candidate for Linux/KVM deployments. Its design treats guest vCPU threads as malicious, nests trust zones, recommends production launch through its jailer, and explicitly leaves guest egress filtering to host-level controls. A Firecracker VM is not a complete solution: host kernel/KVM, VMM/jailer, image provenance, host firewall, TAP configuration and lifecycle remain trusted attack surfaces.

gVisor and Kata Containers are comparison candidates, not assumed equivalent boundaries. Selection requires threat-model-specific evaluation, host compatibility, exploit history, maturity, resource cost, observability, patching and independent tests. No sandbox makes arbitrary code safe.

For high-risk workloads, use a fresh disposable environment, no persistent credentials, no shared writable workspace between unrelated tasks, no unrestricted host mounts, no shared agent coordination channel, strict CPU/memory/process/disk/time quotas and deny-by-default egress. Destroy the environment after extracting a small validated result artefact.

### 20.5 Network and credential containment

- Future venue credentials, if separately authorised, exist only in the adapter/gateway zone; never return them to agents, model context, logs or diagnostics.
- Strategy zone has no route to exchange REST/WebSocket endpoints, arbitrary DNS egress, cloud metadata, loopback admin ports or generic HTTP proxy.
- Gateway has explicit destination allowlists per venue/environment, TLS validation, DNS controls, private/link-local/loopback denial, redirect restrictions and DNS-rebinding/SSRF protection.
- Do not expose generic CONNECT proxy or arbitrary URL-fetch endpoint as a route to credentials.
- Egress policy is enforced outside untrusted process and, for stronger threat models, outside gateway host.
- Gateway schemas are narrow typed operations; no shell, arbitrary HTTP, arbitrary headers, raw signed payload or unrestricted exchange API passthrough.
- Inbound agent data is untrusted even over authenticated IPC; validate lengths, types, ranges, enums, identifiers, Unicode, canonicalisation and semantic invariants.
- Adapter responses and venue metadata are also untrusted; parse in constrained process and validate before changing financial state.

### 20.6 Host isolation failure tests

- Strategy process reads procfs/sysfs, environment, process memory, file descriptors, sockets and neighbouring service paths.
- Symlink/hardlink/path traversal, TOCTOU, mount namespace, procfs, device node, Unix socket and inherited-FD attacks.
- Access attempts to container-runtime sockets, KVM, host network namespace, cloud metadata and loopback admin services.
- DNS rebinding, IPv4/IPv6 alternate forms, redirects, proxy bypass, private/link-local targets and raw socket egress.
- ptrace, signal injection, shared-memory abuse, resource exhaustion, fork bombs, disk exhaustion and IPC queue flooding.
- Malicious output with forged IDs, oversized JSON, duplicate keys, noncanonical numbers and Unicode confusables.
- Compromise sandbox guest and test host containment; compromise one workload identity and test lateral movement.
- Direct venue connection from Z0 and credential discovery from memory, filesystem, logs, backups and environment.
- Disable/misconfigure one control at a time; health detects missing enforcement and blocks elevated trust.

## 21. Adversarial deep review — recovery, rollback and authority resurrection

### 21.1 Recovery restores data, not authority

A backup is evidence of past state, not proof of current permission. Restoring an old database, disk image, VM snapshot or configuration can resurrect an expired envelope, revoked key, compromised workload identity, old policy, unused admission token or stale revocation generation.

Therefore:
- no backup or snapshot alone can reactivate execution authority;
- ephemeral permits, sessions, workload credentials and one-use tokens are never restored as valid;
- restored authority records are quarantined until checked against a trust anchor independent of the backup;
- recovery increments a fresh authority generation and invalidates all pre-recovery capabilities;
- workload identities are re-attested/reissued or explicitly denied;
- policy/envelope versions and signing-key status are revalidated;
- missing, stale or contradictory revocation anchor means RECOVERY_HOLD, not best-effort activation.

### 21.2 Independent anti-rollback anchor

The latest trusted authority generation must be anchored outside ordinary application backup and outside any single restore path. Candidate mechanisms:

1. Hardware-backed monotonic state (TPM/platform secure element) if the target platform exposes a suitable, reliable and recoverable primitive.
2. Independently administered append-only remote witness/checkpoint service, accepting privacy, availability, connectivity and cost implications.
3. Owner-held offline signed recovery checkpoint and separate recovery key, with manual verification and no automatic activation while offline.
4. A combination of hardware anchor plus independently held owner recovery material; remote witness optional.

No mechanism is selected. A TPM/secure element is not automatically a monotonic-counter service; verify APIs, rollback properties, reset behaviour, wear limits, firmware assumptions and recovery support. A remote witness introduces a new dependency and must not become an unchecked authority source. An owner-held checkpoint can be stale; it must not be treated as latest unless reconciled or accompanied by fail-closed manual recovery.

TUF root rotation, threshold signatures, version monotonicity and expiry checks are useful patterns for policy metadata and software artefacts. They do not directly solve runtime revocation or hardware root-of-trust. Secure boot establishes a chain of authorised boot artefacts under its own key/configuration assumptions; it does not prove the restored application database or owner permissions are current.

### 21.3 Separate recovery trust from operational trust

Maintain separate key purposes and access paths:

- offline owner root/recovery key: authorises recovery of trust anchors, not routine dispatch;
- owner approval credential: authenticates a human approval ceremony bound to exact envelope/policy digest;
- policy publisher key: signs policy artefacts, cannot unilaterally expand owner authority;
- workload identity issuer: issues constrained short-lived service identities, cannot sign owner envelopes;
- audit checkpoint key: signs audit roots, cannot authorise actions;
- data-encryption keys: protect stored data, cannot grant authority;
- future venue credentials: confined to adapter boundary, cannot sign policy or owner grants.

WebAuthn can provide scoped, origin-bound user-presence/user-verification assertions, but an assertion is not automatically a general-purpose offline policy signature. If used for owner approval, the challenge binds nonce, exact envelope/policy digest, environment, operation, audience and expiry; verifier enforces origin/RP ID, user verification and credential status. Authenticator backup/sync properties and recovery must be evaluated for root-level approval. A separate hardware-backed signing credential may be required for the signed policy artefact. No ceremony or hardware is selected.

### 21.4 Recovery protocol

1. Disable dispatch egress and put all authority domains in RECOVERY_HOLD.
2. Preserve compromised host/storage and incident evidence; do not overwrite the only evidence copy.
3. Rebuild in an isolated clean environment from verified source, pinned dependencies, signed artefacts and known-good OS images.
4. Verify boot chain, firmware/security configuration, host patch level, kernel, gateway binary, policy evaluator and sandbox profile.
5. Re-establish owner root/recovery identity using separately protected recovery method; recovered application credential is not proof of trust.
6. Obtain newest independently trusted revocation generation/checkpoint. Compare with restored state and hardware/remote witness if configured. If latest state cannot be established, remain in RECOVERY_HOLD.
7. Advance authority generation; revoke all prior workload identities and invalidate old permits, sessions, leases, policy caches and queued actions.
8. Rotate affected operational keys and credentials. Suspected compromised keys are replaced with new identities, not simply re-enabled.
9. Verify signed policy/envelope artefacts; require fresh owner approval where integrity or current authority cannot be proven.
10. Verify audit chain/checkpoints, identify gaps and append incident/correction events without rewriting history.
11. Reconcile external orders, fills, positions, balances, transfers and venue settings from authoritative venue state; unknowns remain reserved/restricted.
12. Run independent host-isolation, revocation, key, audit and financial-reconciliation tests.
13. Require explicit owner approval to reactivate execution capability. If trust, key custody, audit or financial state remains uncertain, capability remains disabled.

### 21.5 Recovery test catalogue

- Restore snapshot from before key/envelope revocation: old grant remains invalid.
- Restore snapshot with lower epoch: boot into RECOVERY_HOLD.
- Restore after policy signing-key compromise: reject artefacts signed by revoked key.
- Roll back system clock/wall-clock metadata: no expired grant becomes valid.
- Restore old workload certificates/tokens: reject due to identity epoch/revocation.
- Replay old owner approval assertion/signature: reject nonce, replay and stale digest.
- Lose primary owner key: use only documented recovery root; no silent admin reset.
- Lose primary and recovery authority: remain dormant; no backdoor reactivation.
- Compromise ordinary backup credentials: cannot alter independent trust anchor/checkpoint.
- Corrupt/truncate audit store: detect mismatch and preserve incident state.
- Restore VM snapshot with pending order: reconcile venue before retry/release.
- Restore while disconnected from witness: no automatic execution activation.
- Rebuild clean binaries with compromised old configuration: verify policy and boot configuration independently.
- Recover after root compromise: re-attest host, rotate identities; never trust old in-memory/on-disk permits.

## 22. Consolidated adversarial conclusions and remaining gates

1. Revocation is a distributed side-effect control problem, not a Boolean. Define local dispatch linearisation and report in-flight uncertainty honestly.
2. Action gateway must be outside strategy/AI trust zones. Compromised host root/kernel remains a hard trust-boundary failure; high assurance requires a separate trust domain.
3. Containers/namespaces alone are insufficient. Layer OS controls; use disposable microVMs for high-risk arbitrary code where supported; filter egress outside the guest.
4. Strategy/agent environment must never possess venue credentials or a generic network route to exchange APIs.
5. Recovery must not restore authority from backups. Revocation high-water state must be anchored independently; if current state cannot be proven, remain dormant.
6. Hardware keys, WebAuthn, TPM, secure boot, remote witness, TUF-style metadata and microVMs are candidate controls, not adopted dependencies.
7. Exact physical topology depends on future deployment. Phase 02 can define trust invariants and tiered assurance profiles, but cannot claim an Android device, VM, host or cloud platform satisfies them without platform-specific verification.
8. These findings require updates to the integrated adversarial review, security architecture, risk handshake, requirements, architecture, roadmap and traceability matrix. They do not approve implementation or Phase 03.


### Additional primary sources for checkpoint 068

- [Linux kernel Landlock documentation](https://www.kernel.org/doc/html/latest/userspace-api/landlock.html) — unprivileged stackable filesystem/network restrictions, ABI feature detection, explicit handled-access semantics and limitations.
- [Firecracker design and threat containment](https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md) — nested trust zones, malicious guest vCPU assumption, production jailer guidance and host-level egress filtering.
- [OWASP Transaction Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html) — final execution-time authorization gate, TOCTOU prevention and operation-specific limited-time credentials.
- [TUF specification](https://theupdateframework.github.io/specification/latest/) — threshold root rotation, version monotonicity, rollback/freeze and metadata integrity patterns.
- [NIST SP 800-207 Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final) — resource-centric trust, separate authentication/authorization and no implicit trust based on network location.

## 23. Independent health supervisor and security interlocks

### 23.1 Independence is a failure-domain property

The supervisor must observe components from outside their own process boundary. A component's self-reported health is telemetry, not proof. The supervisor must independently probe critical dependencies, compare expected and observed state, monitor process/host configuration, and retain its own health evidence.

Logical module separation inside one process does not provide independent oversight. A separate process with a distinct service identity is a minimum logical boundary for a local deployment; a separate VM/host or hardware-backed watchdog is required when the threat model includes compromise of the application host/root/kernel. Exact topology remains open until deployment is selected.

### 23.2 One-way restrictive authority

The health supervisor receives read-only telemetry and has only a narrow restrictive output channel to the action gateway. It is not the security incident-response authority: a separately governed security control plane may revoke compromised credentials/identities or isolate a workload under its own audited incident authority, but it cannot create financial authority or initiate financial side effects. The health supervisor itself cannot revoke/issue credentials or change security policy:

- It may assert a scoped interlock such as DATA_STALE, ACCOUNT_STATE_UNKNOWN, SECURITY_INCIDENT, AUDIT_UNAVAILABLE or CONTROL_HEARTBEAT_LOST.
- It may request suspension of new risk-increasing actions in the affected domain/scope.
- It cannot create/modify owner envelopes, policy, hard limits, risk approvals, reservations or credentials.
- It cannot initiate cancellation, flattening, transfer, withdrawal, payment or any other financial side effect.
- It cannot release an interlock by itself after a critical incident; recovery evidence and the designated owner approval process apply.
- A supervisor message can reduce authority but never increase authority.

The action gateway independently validates the interlock message identity, scope, sequence/generation, freshness and signature. A malformed, replayed or unverifiable message is an incident, not a trusted state transition. Loss of the supervisor heartbeat causes the defined fail-closed restriction for affected risk-increasing actions.

### 23.3 Avoiding supervisor-as-single-point-of-failure

A compromised supervisor should at worst be able to cause a denial of service by asserting restrictions; it must not gain financial authority. To limit false restrictions, require reason-coded, scoped evidence and hysteresis/clearance rules for non-critical transient conditions. Critical security or integrity failures remain latched until independently cleared. The gateway must not accept a supervisor's self-issued HEALTHY status as proof that its own process or host is uncompromised.

Use independent signals where practical: host/process observations, data-source heartbeats, database integrity probes, external venue reconciliation, audit checkpoint verification and a separate watchdog heartbeat. No single monitor can certify every other foundation. If all monitors share a compromised host/kernel, their independence is limited and must be stated.

### 23.4 Health/security state contract

Keep separate:
- operational health (availability, liveness, resource capacity);
- data trust (freshness, completeness, lineage, reconciliation);
- security posture (identity/key/policy/host integrity, incident status);
- financial state trust (account/order/position reconciliation);
- authority state (envelope, policy, revocation generation and owner activation).

A component can be operationally healthy but security-compromised. A healthy supervisor cannot prove its own trustworthiness. A healthy system cannot infer that an external account state is reconciled.

## 24. Audit and external side-effect atomicity

### 24.1 The boundary cannot be one distributed ACID transaction

IDEAL cannot atomically commit a local database transaction and a remote exchange side effect. The design must not claim exactly-once execution across that boundary. It uses durable local intent, idempotency, conservative UNKNOWN state and authoritative reconciliation.

### 24.2 Three durable local boundaries

**Transaction A — admission preparation:** in one ACID transaction in the authoritative local admission store, persist canonical action intent, exact digest, owner/security decision reference, current authority generation, risk reservation, audit event and transactional outbox item. These records must share one transactional commit boundary; separate databases/services cannot be described as atomic without a verified transaction protocol. If any required record fails, roll back the entire local transaction and do not admit dispatch. In the initial modular-monolith direction, prefer one database transaction with schema/ownership boundaries rather than cross-service best-effort writes.

**Transaction B — dispatch start:** immediately before the external network write, atomically consume the one-use permit, verify the current revocation/policy generation and identity state, transition the action to DISPATCH_STARTED, and append the corresponding audit event in the same authoritative transaction. This commit is the local linearisation point shared with revocation. The network write occurs only after this transaction is durably committed.

**External side effect:** send the exact approved payload with stable client-side idempotency identity where the venue supports it. Do not expose generic request construction to strategy/AI. A timeout, crash or missing acknowledgement after dispatch-start is UNKNOWN.

**Transaction C — outcome/reconciliation:** after receiving a definitive venue response or authoritative reconciliation, atomically append the outcome event and update order/position/reservation state. Filled exposure transfers exactly once; residual reservation is retained until terminal venue state is authoritative. If this transaction fails after the venue accepted the request, retain UNKNOWN/in-flight state and reconcile again; never erase the prior dispatch-start record.

### 24.3 Audit precondition and failure policy

- The durable local audit/intent record is a precondition to dispatch.
- If the primary audit/transaction store cannot durably commit Transaction A or B, no new risk-increasing external side effect is permitted.
- A separate append-only audit projection or remote witness may be asynchronously updated from a committed outbox, but it does not replace pre-dispatch durable local evidence. Its maximum lag, backlog capacity and outage behaviour must be defined; exceeding the approved bound blocks new risk-increasing actions.
- If the external request may have been sent but the outcome/audit projection is unavailable, retain in-flight status and reservation; restore audit pipeline and reconcile before further related actions.
- An alternate audit path can preserve essential incident events during a primary sink outage, but it cannot be used to bypass the durable action-intent/dispatch-start requirement.
- Audit log storage, audit administration and action execution credentials are separate privileges. Agents cannot write trusted audit records directly.
- Hash chaining and signed checkpoints detect some tampering but do not prevent an attacker controlling both event store and checkpoint key from rewriting history. Store checkpoints independently and test truncation, reordering, substitution and restore.
- Security logs, business/financial event records and transaction/audit trails have distinct purposes and retention; correlate them without conflating them.
- Log safe identifiers, decision references and digests; never log private keys, API secrets, session tokens, recovery codes or raw authentication assertions.

### 24.4 Failure matrix

| Failure point | Expected state | Required recovery |
|---|---|---|
| Transaction A fails | No admission/dispatch; no reservation committed | Retry only after store health restored and request revalidated |
| Transaction B fails | No network write | Do not dispatch; investigate audit/authority store |
| Crash after B, before socket write | UNKNOWN unless non-dispatch is provable | Query venue by stable client identity; do not blindly resend |
| Venue accepts, response lost | UNKNOWN/in-flight; reservation retained | Authoritative venue reconciliation |
| Venue responds, Transaction C fails | UNKNOWN/in-flight; prior dispatch-start preserved | Reconcile and append outcome later |
| Audit projection/witness unavailable after local durable event | Local event retained; new admissions follow defined audit-degradation policy | Repair projection and verify chain/checkpoints |
| Primary audit and alternate audit unavailable | Block new risk-increasing actions | Restore audit trust before release |
| Disk full or fsync/durability error | No successful durable commit may be assumed | Fail closed; preserve possible in-flight state |
| Duplicate outbox delivery | Idempotent consumer; one external action identity | Deduplicate by action ID/digest; reconcile venue |
| Out-of-order event delivery | Sequence/generation checks reject invalid transition | Replay from durable ordered source |

## 25. Policy publication, root of trust and key lifecycle hardening

### 25.1 Separate authority roles

The root trust role is not a runtime policy editor or exchange credential. Keep separate roles for owner root/recovery, owner approval, policy publisher, workload identity issuer, audit checkpoint signer, data encryption and any future venue credentials. No one operational key should be able to both expand owner authority and dispatch financial actions.

### 25.2 Immutable policy publication lifecycle

A policy/envelope publication is an immutable artefact with a monotonically increasing version/generation and exact content digest. Proposed lifecycle:

DRAFT → VALIDATED → OWNER_APPROVED → SIGNED → PUBLISHED → ACTIVE → SUPERSEDED or REVOKED.

- DRAFT/VALIDATED are non-authoritative and cannot be consumed by the action gateway.
- Validation checks schema, semantic constraints, scope narrowing/expansion, expiry, key purpose, signature, version, references and forbidden combinations.
- OWNER_APPROVED binds the owner-authentication ceremony to exact artefact digest, environment, operation, version and expiry.
- SIGNED verifies the correct policy-publisher role; signing is not itself owner approval.
- PUBLISHED makes immutable metadata available but not active.
- ACTIVE requires a serialized activation event and new authority generation; dispatchers observe the activation atomically with revocation state.
- SUPERSEDED artefacts remain historical evidence but cannot regain authority through rollback.
- REVOKED artefacts and compromised signing keys are denied regardless of a valid historical signature.

Policy changes never edit a live record in place. Scope expansion, hard-limit changes, new account/venue/environment, credential permission expansion and reserved actions require owner approval under D-023. A policy publisher cannot enlarge the owner envelope by itself.

### 25.3 Root and delegated key design

A root/recovery key should be offline or hardware-protected and used rarely to establish/rotate delegated trust roles. Operational policy signing uses a delegated key with narrow purpose, short cryptoperiod, revocation and auditable rotation. Owner approval remains a separate authority event. Workload identity keys are short-lived and automatically replaceable; audit checkpoint and encryption keys have independent purposes.

A threshold signature scheme may reduce single-key risk but adds owner recovery/availability complexity. D-023 is a single-owner model; do not invent a second human approver or imply two-person control exists. Evaluate hardware-backed owner key plus independent recovery key, and whether a user-verification factor is required for each high-impact ceremony. The recovery path must be at least as carefully protected as the primary path.

### 25.4 Anti-rollback metadata and activation

Use TUF-inspired principles for root rotation, delegated roles, threshold verification where justified, monotonically increasing versions, expiry/freeze detection, consistent snapshots and explicit revocation. TUF is a pattern/reference, not an automatic runtime authority solution. The action gateway pins the currently active version/generation and fails closed if metadata is stale, expired, unverifiable, rolled back or contradictory.

Activation, revocation and dispatch-start share a single serialized authority generation. Policy publication cannot race a dispatch under a stale policy. A policy change that narrows authority may be applied as a restriction; any expansion waits for the owner approval and activation protocol.

### 25.5 Key compromise and recovery

Suspected compromise means revoke the key identity and all grants/artefacts whose trust depends on it according to a defined scope analysis. Do not simply restore the old key from backup or re-enable it. Generate a new key identity, rotate delegated trust, distribute updated trust metadata, invalidate old sessions/capabilities, verify clients have advanced their trusted root and retain signed evidence of the transition. Loss without compromise may permit documented recovery; suspected compromise requires replacement and independent validation.

## 26. Additional open decisions and closure criteria

- Exact transactional store and durability semantics for authority, risk reservation, audit event and outbox.
- Whether the local authority registry is single-writer or distributed; if distributed, consensus/linearizability and partition behaviour.
- Worker inventory/attestation and how a dispatch boundary proves the complete set of active workers.
- Health supervisor process/host failure-domain topology and independent watchdog design.
- Scoped interlock schema, freshness, signature, latching and clearance rules.
- Audit event schema, append-only storage, checkpoint cadence, independent witness and alternate logging capability.
- Exact policy root/delegated key roles, owner ceremony, cryptoperiod, recovery and compromise response.
- Whether hardware-backed key support is available consistently across future Android, PC and server targets.
- Required durability level and whether local-only storage is sufficient for the future action gateway.
- Numerical revocation propagation target and the exact set of boundaries included in the measurement.

Phase 02 cannot close until these semantics are reconciled across security, risk, health, data integrity, audit and recovery; mapped to adversarial tests; independently challenged; and accepted by the owner. No technology selection or implementation follows automatically.


### Additional primary sources for checkpoint 069

- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) — structured security event logging, separation of audit/security/transaction logs, event context, sanitisation, secret exclusion, log protection and failure testing.
- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) — audit protection, logging failure response and alternate audit capability control families.
- [NIST SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final) — key lifecycle, compromise scope, replacement and recovery planning.
- [AWS Prescriptive Guidance — Transactional Outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) — atomic local state/outbox commit and duplicate-delivery/idempotency handling. This is a distributed-systems pattern reference, not an endorsement of AWS infrastructure for IDEAL.


### 26.1 State-machine consistency rules

The authority/envelope lifecycle, policy lifecycle, action lifecycle, risk-reservation lifecycle and incident lifecycle are separate state machines connected by explicit versioned events. Do not merge them into one status flag.

- Owner envelope/policy state controls whether an actor may request an action.
- Workload identity state controls which service is making the request.
- Health/security interlocks can restrict action admission but cannot grant authority.
- Risk reservation state controls capacity and exposure accounting.
- Action state controls whether the external side effect may have started.
- Reconciliation state controls whether the external financial outcome is known.
- Incident/recovery state controls whether execution capability may be reactivated.

An action can be security-authorised but risk-rejected; risk-approved but authority-revoked; dispatched but not acknowledged; or reconciled financially while an incident hold remains active. Each dimension must retain its own evidence and cannot be inferred from another dimension's green state.

The only permitted path to a future external side effect is: owner envelope/policy active → workload identity authenticated → exact action canonicalised → data/health/security gates pass → risk approval and reservation committed → durable intent/audit/outbox committed → final generation check and DISPATCH_STARTED commit → narrow adapter network write → authoritative venue reconciliation → reservation transfer/release. Any failure before dispatch-start denies the side effect. Any uncertainty after dispatch-start is treated as potentially in-flight and reconciled.

If the future architecture splits the admission store across services or databases, it must replace the single-store transaction with a formally specified, tested coordination protocol. Merely writing to multiple services sequentially is not atomic and is not an acceptable substitute.

## 27. Unified authority, action and reservation event ordering

### 27.1 Separate state machines, shared versioned evidence

IDEAL must not compress authority, identity, policy, health, risk, execution and reconciliation into one status field. Each has its own state machine and evidence. A consequential action binds the current versions/generations of every decision-relevant dimension:

- owner envelope ID/version/digest and authority generation;
- policy ID/version/digest and policy publisher key identity;
- workload identity ID, issuer/credential generation and scope;
- risk policy/model version, risk decision and reservation ID;
- health interlock generation and scoped status;
- security incident/key-revocation generation;
- data evidence IDs, quality/freshness and correction versions;
- account/order/position reconciliation sequence;
- instrument/contract metadata version;
- exact canonical action digest and one-use nonce;
- trusted time/clock-quality evidence and event sequence.

A decision is stale if any required bound version changes before dispatch-start. Re-evaluation is required; the action cannot inherit an earlier approval.

### 27.2 Authority generation semantics

For the initial private single-owner design, prefer one monotonic authority generation for all events that can change the ability to act: owner envelope activation/suspension/revocation, policy activation/revocation, root/delegated key revocation, workload identity revocation and security-authority suspension. A global generation is conservative and easier to reason about than per-account epochs. Do not partition it for performance without a formal proof that cross-scope changes cannot invalidate an action.

Risk-policy version, health-interlock generation, data-evidence version and venue/instrument metadata version remain separately bound. They are not silently folded into the owner-authority generation.

Every activation/revocation transition is durably ordered and increments generation. Generations never decrease, repeat or reset after restart/restore. A missing, rolled-back or contradictory generation causes RECOVERY_HOLD.

### 27.3 Ordering without trusting wall-clock timestamps

The authoritative event sequence/transaction commit order determines local ordering. Wall-clock timestamps are evidence for human interpretation and expiry, not the sole ordering mechanism. Record event time, source time, receive time, processing time, monotonic sequence and clock-quality status separately.

Expiry decisions require a trusted time policy and bounded skew. If the clock moves backwards, time source is unavailable, or expiry cannot be proven, deny time-dependent admissions. Do not infer order from two timestamps generated by different hosts without clock-quality evidence.

### 27.4 Dispatch admission sequence

1. Receive proposal from authenticated workload; treat payload as untrusted.
2. Canonicalise and validate exact action; reject unknown/ambiguous fields.
3. Snapshot current authority, identity, policy, risk, health/security, data, account and instrument versions.
4. Evaluate owner/security authority and deterministic risk independently.
5. Atomically reserve capacity and commit Transaction A (intent, digest, evidence references, authority snapshot, reservation, audit event and outbox).
6. Immediately before network write, Transaction B rechecks every required version, consumes the one-use permit, serialises against revocation/policy activation, and commits DISPATCH_STARTED plus audit.
7. Only then may the narrow adapter write the exact payload to the approved venue endpoint.
8. Persist acknowledgement/fill/reject/cancel observations with venue sequence/source identity; never infer definitive terminal state from a client timeout.
9. Reconcile venue orders, fills, positions and balances; update position exposure and residual reservation exactly once.
10. Release only the definitively unused residual reservation after authoritative terminal reconciliation.

### 27.5 Reservation state semantics

| Reservation state | Meaning | Permitted transition |
|---|---|---|
| NONE | No capacity committed | Create only after risk approval |
| HELD | Capacity reserved for an admitted but not yet dispatched action | Dispatch-start, or release on definitive pre-dispatch rejection/expiry/revocation |
| IN_FLIGHT | Dispatch-start committed; remote outcome may be unknown | Reconcile; do not timeout-release |
| PARTIALLY_FILLED | Filled portion transferred to position exposure; residual remains reserved | Further fill, terminal reconciliation |
| TERMINAL_PENDING_RECONCILIATION | Venue indicates terminal state but authoritative reconciliation is incomplete | Retain conservative residual until reconciliation |
| RELEASED | Unused residual reservation released after proof | Terminal; never reopen same reservation |
| INCIDENT_HOLD | Integrity, identity, venue or account state compromised/contradictory | Owner-led recovery and reconciliation |

Filled quantity transfers from order reservation to position exposure exactly once using stable venue event identity and sequence. Duplicate or out-of-order fill reports must be idempotently deduplicated and reconciled. A cancel request, cancel acknowledgement without authoritative order-state reconciliation, or process shutdown does not automatically release residual reservation.

### 27.6 Invalidations and safe outcomes

- Authority generation changed before dispatch-start: reject; if no external side effect could have started, release the pre-dispatch reservation atomically with the rejection event.
- Risk policy/model version changed: require fresh risk decision and reservation.
- Health interlock became restrictive or stale: reject affected action; do not let old HEALTHY snapshot survive.
- Data correction, source conflict or account reconciliation sequence changed materially: re-evaluate or hold.
- Instrument contract/margin parameter version changed: reject risk-increasing action until recalculated.
- DISPATCH_STARTED already committed: do not simply reject/forget; retain in-flight state and reconcile.
- Audit/authority store cannot prove commit outcome: treat as ambiguous and fail closed; never assume commit did not happen.
- A valid owner envelope does not guarantee risk approval; a valid risk approval does not grant owner authority; a healthy supervisor does not certify security; a signed policy does not prove owner approval.

### 27.7 Cross-document acceptance condition

The requirements, risk architecture, security architecture, health architecture, core protection architecture and traceability matrix must all describe these same boundaries and state semantics. A change to the event sequence, generation scope, transaction boundary or reservation lifecycle is a material architecture change requiring impact analysis and independent review.
