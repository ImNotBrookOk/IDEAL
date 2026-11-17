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


## GitHub commit and read-back evidence

All twelve affected/new files were fetched from the repository default branch after writes. Required-content checks passed for all twelve. Read-back blob SHAs:

| File | Read-back blob SHA |
|---|---|
| docs/IDEAL_AUTONOMY_AUTHORITY_AND_PERMISSION_ARCHITECTURE.md | ce687aae1ad4bc4cbf43ebe3820b4b8022f49897 |
| docs/IDEAL_INTEGRATED_ADVERSARIAL_REVIEW.md | d17f831e3ca1a24b932ce0a4fa9354bdf24574cc |
| docs/IDEAL_SECURITY_ARCHITECTURE.md | bc37fd4172ea972e515a650e668b397fef3ec65c |
| docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md | be7903795881f1b000fb3c6accc416a1bc11bd2f |
| docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md | cd1300e4b7c4408515db955647121161484daaa8 |
| REQUIREMENTS.md | 554008cc84398eac24f98668d24828dd62a02934 |
| ARCHITECTURE.md | 4e024a48c73383d944510e7ed2afd81c89a804fc |
| ROADMAP.md | 9dfdf7f77e286b0ee180b01adb67bb085f9cfac1 |
| docs/IDEAL_FOUNDATION_TRACEABILITY_MATRIX.md | a9df5c1e43a669a279abaafa0d42009724de9b72 |
| docs/CHATGPT_CONVERSATIONS/2026-11-17-068-adversarial-revocation-isolation-recovery-review.md (before evidence addendum) | 04b7055536b89d4a662978decfd1a66940e0db34 |
| docs/CHATGPT_CONVERSATIONS/README.md | bbbc25b84cb9d20858c33d82b26fd3cad4170129 |
| README.md | 37987d6ad45534d10525f96b88e01a30549454f9 |

Commit ledger:

| Change | Commit SHA |
|---|---|
| Autonomy architecture §§19–22 | 09f8872011b17b790173a4586949e83bb03c2cef |
| Add primary sources to autonomy architecture | 699c9620dd8ed35050f03e78847d5ff636d8452b |
| Integrated adversarial review | 135271597e86a2f544ca9b948054cf1e17fc1acc |
| Security architecture | 2f948900c605cca5cb17ac992375675d6d833c80 |
| Risk architecture | 554e2ed35f57b91e86df0db0c0e594aa629df8db |
| Core protection architecture | bf36b2d27e4b67e95cf0303d42f7dc02842d397f |
| Requirements | 3a958e3986d0dd1f14c46b77b84297c4a413b22c |
| Architecture | 1579d46dac98d7fbab288485bf7cacb2fb18d0a2 |
| Roadmap | 7d9f31ba2140b6dba3d765efc17d661e4e009ad6 |
| Foundation traceability matrix | be904f409239b89411827b627d95d072bce62041 |
| Create checkpoint 068 audit | 832e8969ac090c86bf0c111206af59218ae89658 |
| Index checkpoint 068 | aac5541d04240009ae90b022e9749a7106257ee5 |
| README Phase 02 security focus | 5f05d2d4edce8d2e2cd659ba994b712ee2643b88 |

Audit evidence addendum commit is recorded after its read-back below. No runtime test or security exercise is represented by this documentation verification.
