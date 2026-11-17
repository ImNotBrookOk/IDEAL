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
| ADMITTED | All prerequisites and durable audit preconditions pass | Issue one narrow adapter admission |
| DISPATCHED | Adapter attempted external side effect | Track stable idempotency/client reference |
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
