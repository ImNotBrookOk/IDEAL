# Checkpoint 067 — autonomy authority and permission architecture research

**Date:** 17 November 2026  
**Phase:** 02 — architecture/contracts (active)  
**Status:** Research/design draft documented; owner review and technical decisions remain open  
**Governance:** D-023 remains Accepted; no new governance decision was made.

## User-visible conversation

**User:** Yes

**Assistant:** I’ll continue with the **Autonomy Authority and Permission System** for IDEAL.

The objective is to make bounded autonomy enforceable by architecture, not merely by configuration or instructions to an AI agent. No component should be able to grant itself authority, bypass risk approval, or silently expand the owner-approved operating envelope.

This remains Phase 02 architecture research. I will not install tools, change runtime code, connect accounts, or activate execution capability.

**Assistant (research conclusion):** The first major architectural conclusion is that IDEAL needs two independent permissions before any future consequential action: (1) authority permission from the owner-approved envelope and security policy for the exact action/service/account/environment; and (2) independent risk permission for the exact action and reservation. Neither substitutes for the other. The action boundary must also verify trusted data, health/security interlocks, revocation and durable audit. Cedar policy errors require a stricter fail-closed wrapper; OPA signed-bundle verification must be explicitly enforced.

## Work performed

1. Read the installed Acumen research skill and queried current developments before public research.
2. Reviewed current OWASP authorization guidance; Cedar authorisation and policy-validation documentation; OPA release, signed-bundle and decision-log documentation; SPIFFE/SPIRE workload identity material; OpenBao Transit and release documentation; Sigstore/Cosign signing documentation; NIST SP 800-57 and SP 800-207; W3C WebAuthn Level 3; RFC 8785 and RFC 9052.
3. Queried GitHub repository metadata and current release information for Open Policy Agent, Cedar, SPIRE, OpenBao, Cosign and in-toto. Repository metrics are dated snapshots, not security/quality scores. GitHub open issue counts may include pull requests.
4. Read current IDEAL README, decision register, security/risk/architecture/requirements/roadmap and foundation/adversarial/traceability records before preparing changes.
5. Created the autonomy authority and permission architecture document with authority hierarchy, operating-envelope semantics, identity/authentication/authorisation separation, key hierarchy, signed policy lifecycle, exact-action contract, state machine, reservation/dispatch/reconciliation, revocation, cross-pillar contracts, audit/privacy, recovery, candidate comparison, threat scenarios, assurance tests and open decisions.
6. No software was installed. No runtime code, dependency, exchange connection, account, credential, financial record, paid service, hosting or external security test was changed or authorised.

## Main findings

- A dedicated action-enforcement boundary outside AI/strategy is required. UI/prompt-level constraints are bypassable and are not a security boundary.
- Owner grant, workload identity, policy evaluation, risk approval, data trust, health/security interlocks and audit are distinct prerequisites.
- The operating envelope must be immutable/versioned, signed, explicit, time-bounded, revocable, scoped by domain/account/venue/instrument/action/environment, and fail closed on ambiguity.
- Exact action approval must bind canonical parameters and a digest; any economically/security-relevant change invalidates the decision.
- Financial quantities require decimal/fixed-point semantics, not binary floating point.
- External exchange side effects cannot be made atomically transactional with IDEAL's local database. Use durable intent/reservation/outbox, idempotency, conservative UNKNOWN state and authoritative reconciliation.
- Revocation needs an independent control path, monotonic epoch/generation, online action-boundary checks and a measurable propagation target.
- Separate owner root, owner approval, policy publication, workload identity, audit checkpoint, data-encryption and future venue credential key purposes.
- Cedar is a strong policy-evaluator candidate if Rust integration fits, but its documented skip-on-error semantics must be wrapped as deny-on-any-error.
- OPA is a strong language-neutral alternative, but signed bundle enforcement has configuration subtleties; explicit unsigned-bundle rejection tests are mandatory.
- SPIFFE/SPIRE provides a strong workload-identity pattern, but full server/agent infrastructure may be excessive for a local single-user first deployment.
- OpenBao has useful central secrets/PKI/transit capabilities but creates a privileged service and operational recovery burden.
- Cosign/in-toto fit software supply-chain provenance more than private runtime owner authority.
- No policy engine, identity platform, key manager, cryptographic format or runtime dependency was selected or adopted.

## Repository changes

- Created docs/IDEAL_AUTONOMY_AUTHORITY_AND_PERMISSION_ARCHITECTURE.md.
- Updated cross-references and requirements in README, REQUIREMENTS, ARCHITECTURE, ROADMAP, security architecture, risk architecture, core protection architecture, integrated adversarial review and foundation traceability matrix.
- Created this checkpoint audit record and added it to docs/CHATGPT_CONVERSATIONS/README.md.
- All changes were fetched back and content-checked after commit. Exact commit/blob hashes are recorded in the final checkpoint evidence below.

## Unresolved decisions

The owner has not approved an envelope schema, key custody/recovery model, WebAuthn signing ceremony, signature/canonicalisation format, policy engine, workload-identity deployment, revocation propagation SLO, clock semantics, audit checkpoint scheme or final action state machine. These remain Phase 02 design questions.

## Current state and next step

- Phase 01 remains closed.
- Phase 02 remains active.
- Phases 03–19 remain locked.
- D-023 remains accepted; this checkpoint adds no new accepted decision.
- No implementation, runtime, dependency, account, credential, exchange connection, paper/live execution, paid service, hosting or external security testing is authorised.
- Next step: continue reconciling the authority/action state machine with risk reservations, cross-pillar contracts and recovery design, then subject the complete model to adversarial review before asking for owner acceptance.
