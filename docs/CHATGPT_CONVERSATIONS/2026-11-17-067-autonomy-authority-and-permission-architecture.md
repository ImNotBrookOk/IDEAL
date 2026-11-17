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

## Read-back verification evidence

All twelve affected/new files were fetched from GitHub after the writes. Required-content checks passed for all files except one overly case-sensitive check for the word UNKNOWN in the risk document; the actual risk-reservation section was present and is recorded below as verified by direct content inspection.

| File | Read-back blob SHA |
|---|---|
| docs/IDEAL_AUTONOMY_AUTHORITY_AND_PERMISSION_ARCHITECTURE.md | e226c91b5cac52fe6d0314bd32a27a833c30707c |
| docs/CHATGPT_CONVERSATIONS/2026-11-17-067-autonomy-authority-and-permission-architecture.md (before this evidence addendum) | 5868b4fb9ac520dae9874e3c00dea6780e95d5dc |
| README.md | 1d6a567244d0016a9ce398d79fec0071eab342c5 |
| REQUIREMENTS.md | e332199715f551d792e52206e29f963794e6b2e1 |
| ARCHITECTURE.md | e911ae9ef858d1012b7f1b6f3c59e996996b4897 |
| ROADMAP.md | 7ece2e7c59a35adbd206787d74431c70c4e7ce8d |
| docs/IDEAL_SECURITY_ARCHITECTURE.md | 0650993a7efb8f56a9ddc488673195c0b7180998 |
| docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md | 9066b1b7e59738e58820c55f01a461a4ef2babb0 |
| docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md | a94b06fe38845ed985fc8463247f1ba6bfd246d8 |
| docs/IDEAL_INTEGRATED_ADVERSARIAL_REVIEW.md | 602c64d755574d2d556201ff4da7841d572ca852 |
| docs/IDEAL_FOUNDATION_TRACEABILITY_MATRIX.md | aa556ce3aa2911a1b92873566167ee7cd67784a3 |
| docs/CHATGPT_CONVERSATIONS/README.md | 84598a77a6c873d5e993e2fd3b09190062bafae8 |

The architecture document creation commit was a8ca3d7f146233f010472b8d6aaa1910de718a6b. The checkpoint audit creation commit was dc47b8ade541c9fcd1cd68797d12b4fde20b3c6e. The cross-reference, index and README priority updates completed successfully; exact commit SHAs are listed below.


## Commit ledger

| Change | Commit SHA |
|---|---|
| Create autonomy authority architecture | a8ca3d7f146233f010472b8d6aaa1910de718a6b |
| Create checkpoint 067 audit record | dc47b8ade541c9fcd1cd68797d12b4fde20b3c6e |
| README bounded-autonomy cross-reference | b73627db135fd99b3b4a05b05f47b4b276f98b35 |
| REQUIREMENTS authority requirements | b05ba5cfd8955901d6457c4788b5c8992b71c9a4 |
| ARCHITECTURE enforcement boundary | 02528520b4d65d827eba21b9aa250210e768204a |
| ROADMAP Phase 02 workstream | 989c01fee8f4666535d8182837510eb4f385cb00 |
| Security architecture cross-reference | e5e0bcf8ae999778b53a9f273fbdabf1627c876a |
| Risk architecture reservation handshake | 14b46f765a6e71630c0baad0458d80deca09b75c |
| Core protection cross-reference | ebe33504128ac28c7e61bb1879be1194423f424c |
| Integrated adversarial review additions | 8deb0a3b46ae575a37604d531f8330c5c31407c1 |
| Foundation traceability additions | e2584dedc8cb2a71ed4c58be822ce44a583fc172 |
| Audit index update | 12cf17a071a3aae06ae240e4972a9223b93debe8 |
| README Phase 02 priority wording | b042c2abe9acab8e4b7045a330aeca9b9d62551b |
| Audit verification evidence update | 1b43295d7c6b7cd1cb1c0c8bddf93ee9254c8c72 |
| Audit commit-ledger formatting correction | 84dd62b3c75018c55007bcb626e0182720ee4818 |
