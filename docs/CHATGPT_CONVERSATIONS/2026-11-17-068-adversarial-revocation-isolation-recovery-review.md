# Checkpoint 068 — adversarial revocation, host isolation and recovery review

**Date:** 17 November 2026  
**Phase:** 02 — architecture/contracts (active)  
**Status:** Deep adversarial design review documented; architecture remains provisional  
**Governance:** D-023 remains Accepted. No new owner decision or phase transition.

## User instruction and scope

The owner authorised autonomous continuation of the existing plan and explicitly asked not to be interrupted for questions until this work is finished. Continue without asking for input, stay within the documented plan, and record meaningful findings. This permission is to continue research and documentation; it does not override prior prohibitions on implementation, runtime changes, dependencies, accounts, credentials, exchange access, paper/live execution, paid services, hosting or external security testing.

## Review scope

Three difficult failure domains from checkpoint 067 were investigated:

1. Revocation racing with final dispatch and external side effects.
2. Host/process/network isolation against compromised or malicious strategy/AI workloads.
3. Backup restore, rollback and resurrection of revoked authority.

## Main conclusions

### 1. Revocation is not instantaneous

- A network request already transmitted cannot be recalled by IDEAL.
- The durable DISPATCH_STARTED transition at the authoritative gateway is the local linearisation point.
- Revocation and dispatch-start must serialize against one monotonic authority generation.
- Revocation-first means no dispatch. Dispatch-start-first means in-flight, potentially externally accepted, and subject to authoritative reconciliation.
- A crash/lost acknowledgement around socket write is UNKNOWN, not assumed unsent.
- Revocation state machine: ACTIVE → REVOKE_REQUESTED → FENCING → DRAINING → EFFECTIVE, with RECONCILIATION_REQUIRED or RECOVERY_HOLD when uncertainty persists.
- EFFECTIVE requires every registered dispatch boundary to acknowledge the new generation and all unstarted work to be fenced. Missing worker acknowledgement/partition means no false success.
- A maximum propagation objective remains an open Phase 02 decision; remote exchange receipt cannot be bounded by IDEAL's local revocation acknowledgement.

### 2. Host isolation requires explicit trust zones

- Every strategy, research script, model runtime, plugin, agent, generated-code process and downloaded artefact is treated as hostile.
- Z0 untrusted workloads have no credentials, direct venue route, host control-plane access or privileged gateway interface; only a narrow typed proposal channel is allowed.
- Z1 ingestion/normalisation, Z2 deterministic research/risk, Z3 authority/action gateway and Z4 trust anchors/recovery have separate trust responsibilities and forbidden flows.
- Linux containment is layered: distinct unprivileged service identities, capability removal, namespaces/cgroups, seccomp, Landlock and/or SELinux/AppArmor, read-only images, restricted IPC, resource limits and default-deny host egress.
- Namespaces/containers alone are not a complete access-control boundary.
- For high-risk arbitrary code, evaluate disposable microVMs. Firecracker is a candidate, not selected; its own design still requires a hardened host/jailer and host-level egress filtering.
- A compromised host root/kernel can defeat local process separation. Stronger assurance requires a separately protected action gateway/credential trust domain and independently enforced network policy.
- No strategy/agent process ever receives exchange credentials or generic HTTP proxy capability.

### 3. Recovery must not restore authority from backup

- Backups restore historical data, not current authority.
- Restored envelopes, keys, identities, policy versions, epochs, sessions and one-use permits are quarantined/invalidated.
- Recovery advances authority generation and validates latest revocation state against an independent trust anchor outside ordinary backups.
- If current high-water state cannot be proven, system remains RECOVERY_HOLD; no offline best-effort activation.
- Rebuild/attest from verified source and images, re-establish owner root via separate recovery, rotate operational identities/keys, validate audit, reconcile external state and require explicit owner approval to reactivate.
- TPM/secure element, remote witness, owner-held offline checkpoint and TUF-inspired anti-rollback metadata are candidate patterns only; no mechanism selected.

## Research sources and limitations

Primary sources reviewed:
- NIST SP 800-207 Zero Trust Architecture.
- Linux kernel Landlock documentation, including ABI/feature detection and limitations.
- Firecracker design/threat containment, including malicious guest assumption and host egress requirement.
- OWASP Transaction Authorization guidance on final execution-time gate, TOCTOU and limited-time operation-specific authorisation.
- The Update Framework specification for threshold root rotation, rollback/freeze and metadata versioning.

Sources are linked in the IDEAL autonomy authority architecture. They support design principles, not proof of IDEAL runtime security.

No external sandbox escape, penetration test, kernel test, security scan, recovery drill, fault injection or runtime test was performed. No vulnerability-free claim is made.

## GitHub changes

- Extended the autonomy authority architecture with §§19–22: revocation linearisation/state machine, host/process/network trust zones, recovery/anti-rollback and consolidated gates.
- Updated the integrated adversarial review with checkpoint 068 and ADV-19 through ADV-30.
- Updated security architecture with revocation, isolation and recovery requirements.
- Updated risk architecture with the dispatch race contract.
- Updated core protection architecture with cross-foundation requirements.
- Updated REQUIREMENTS.md, ARCHITECTURE.md, ROADMAP.md and the foundation traceability matrix.
- Created this audit record and updated its index.

## Current phase and approval boundary

- Phase 01 remains closed.
- Phase 02 remains active.
- Phases 03–19 remain locked.
- D-023 remains the accepted bounded-autonomy governance decision.
- This checkpoint adds no new accepted decision and selects no technology.
- No code, runtime, dependency, account, credential, exchange integration, paper/live execution, paid service, hosting or external test was authorised or changed.

## Next autonomous work

Continue the Phase 02 plan by integrating these findings with the authority state machine, trust-anchor/key lifecycle, policy publication, risk reservation/outbox, health supervisor independence and audit atomicity. Then perform a second cross-document consistency and adversarial closure review. Do not ask the owner for input until the planned work is complete; at that point provide a concise evidence-based review and clearly separate completed research from unresolved owner decisions.
