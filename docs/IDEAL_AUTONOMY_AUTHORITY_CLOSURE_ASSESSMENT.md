# IDEAL Autonomy Authority — Phase 02 Closure Assessment

**Date:** 17 November 2026  
**Scope:** D-023 bounded owner-authorised autonomy technical workstream  
**Status:** Provisional closure assessment; not owner-approved final architecture  
**Phase:** 02 active; no later phase unlocked

## 1. Purpose

This document consolidates the technical authority, permission, revocation, isolation, audit, health and recovery design into a closure assessment. It distinguishes:
- invariants that can be specified now without selecting a platform;
- provisional architecture recommendations for a private single-user first deployment;
- choices that depend on a later language/runtime/host decision;
- decisions that remain reserved for explicit owner acceptance.

This assessment does not authorise implementation, runtime dependencies, accounts, credentials, exchange access, paper/live execution, paid services, hosting or external security testing.

## 2. Owner governance already settled

D-023 is Accepted. Future execution-capable IDEAL uses bounded, owner-authorised autonomy:
- owner explicitly approves the scope, accounts, venues, permissions, operating mode, hard limits, stop conditions, expiry and revocation path in a versioned operating envelope;
- in-envelope individual actions may proceed without per-action human approval only after independent security/authority, trusted data, health interlocks, deterministic risk approval/reservation and audit requirements pass;
- activation/reactivation, envelope/policy/limit/permission changes, new account/venue/integration, credential privilege expansion, fund movement, safeguard disablement, designated irreversible actions and specified incident release remain owner-reserved;
- agents, models and strategies cannot expand authority, change hard policy or approve themselves.

D-023 is governance approval only. It is not execution or implementation approval.

## 3. Technology-neutral invariants — sufficiently specified

| Area | Invariant | Status |
|---|---|---|
| Authority | Owner envelope is explicit, immutable, versioned, scoped, time-bounded, revocable and cryptographically verifiable | Specified; schema open |
| Owner approval | Approval binds exact canonical artefact digest, environment, operation, audience, nonce and expiry; UI presents exact scope/diff | Specified; ceremony/platform open |
| Policy | Policy artefacts are immutable; publisher signature is separate from owner approval; rollback/stale/invalid artefacts deny | Specified; engine open |
| Identity | Authentication is distinct from authorisation; each privileged service has a distinct least-privilege identity | Specified; mechanism open |
| Enforcement | All consequential actions pass through one non-bypassable action boundary outside strategy/AI | Specified; physical topology open |
| Risk | Owner/security authority and deterministic risk approval are independent gates; reservation required | Specified; detailed schemas open |
| Revocation | Revocation and DISPATCH_STARTED serialize against monotonic authority generation | Specified; numeric SLO/worker inventory open |
| Dispatch | Durable DISPATCH_STARTED plus audit commit occurs before network write | Specified; database/durability configuration open |
| External effects | No exactly-once remote claim; unknown outcomes retain reservation and require authoritative reconciliation | Specified |
| Host isolation | Untrusted workloads receive no credentials or generic venue egress; layered containment and host-level filtering | Specified; OS profile open |
| Host compromise | Shared root/kernel compromise defeats local process isolation; separate trust domain or dormant fail-safe required for that threat | Specified |
| Health | Health supervisor is read-only observer with scoped restrictive-only interlock authority | Specified; failure-domain topology open |
| Security response | Separate incident-response authority may revoke compromised identities/credentials; cannot grant financial authority or initiate financial side effects | Specified; role implementation open |
| Audit | Local intent, reservation, audit and outbox commit atomically; dispatch-start and audit commit before send | Specified; store open |
| Recovery | Backups do not restore authority; old permits invalidated; independent current revocation state required; uncertain trust remains RECOVERY_HOLD | Specified; anchor mechanism open |
| Privacy | No secrets in logs; minimise personal/financial data; separate audit/security/financial event purposes and retention classes | Specified; retention periods open |

## 4. Provisional architecture recommendation for initial private deployment

These are design recommendations, not accepted technology selections:

1. **Single active authority/action gateway.** Begin with one active gateway and one authoritative writer per trust domain. Do not introduce multi-active dispatch or distributed consensus until availability requirements justify it. A standby must be fenced from dispatch until it proves the current authority generation.
2. **One authoritative transactional store.** Keep action intent, authority snapshot, risk reservation, audit event and outbox in one ACID transaction boundary. In the initial Modular Monolith, prefer one database with explicit schema/module ownership rather than best-effort cross-service writes.
3. **Durable commit before side effect.** Require documented WAL/fsync/durability semantics. If durable commit cannot be proven, do not dispatch. Exact database engine and storage configuration remain open.
4. **No strategy credentials.** Strategy, AI, generated code, plugins and data parsers receive no exchange credentials, host control-plane access or arbitrary network route. The gateway exposes narrow typed operations only.
5. **Layered local containment.** If future host is Linux, evaluate dedicated UIDs, capabilities removal, namespaces/cgroups, seccomp, Landlock and/or SELinux/AppArmor, strict IPC and host-enforced egress. Verify actual kernel support at runtime. Containers alone are insufficient.
6. **Disposable VM for high-risk code.** Evaluate Firecracker/gVisor/Kata against the eventual host, threat model and operating cost. Firecracker is Linux/KVM-specific and still depends on host hardening/egress controls; it is not an Android runtime assumption.
7. **Logical identity first.** Use distinct OS/service identities in a local deployment. Evaluate SPIFFE/SPIRE only if multi-host workload identity and attestation justify its infrastructure.
8. **Policy engine deferred.** Cedar is a candidate for embedded typed policy if Rust fits; OPA is an alternative if language-neutral policy distribution is required. Whichever is chosen must fail closed on evaluator errors, missing attributes, invalid signatures and stale policy. Do not deploy both by default.
9. **Root key separated.** Keep owner root/recovery trust separate from operational signing, workload identity, audit checkpoint, encryption and venue credentials. Hardware-backed storage and offline recovery are preferred candidates, but exact devices/platforms are not selected.
10. **External witness optional.** A remote append-only witness can strengthen anti-rollback/audit evidence but adds privacy, availability and cost dependencies. Do not add it until the threat model and deployment justify it.
11. **Health supervisor restrictive only.** Separate process identity for local fault detection; separate host/VM/watchdog if protection against host root compromise is required.
12. **Manual recovery is mandatory.** If latest revocation generation, owner root, audit integrity or external financial state cannot be proven, remain dormant and require owner-led recovery.

## 5. Platform-specific decisions intentionally deferred

| Decision | Why deferred | Required evidence before selection |
|---|---|---|
| Language/runtime and database | Existing architecture remains technology-neutral; ACID and durability must be verified in chosen stack | Crash-consistency tests, WAL/fsync guarantees, concurrency and restore tests |
| Android approval authenticator | WebAuthn/platform passkey/hardware key availability and backup semantics vary | Supported authenticator matrix, origin binding, user verification, recovery and anti-replay tests |
| PC/server trust anchor | TPM/secure element APIs, measured boot and anti-rollback differ by hardware/firmware | Actual device capability, reset/rollback behaviour, recovery procedure |
| Policy engine | Cedar/OPA fit depends on language, deployment and operational complexity | Licence/release/security review, wrapper semantics and negative test suite |
| Workload identity | Local OS identity differs from multi-host attestation needs | Threat model and deployment topology |
| Sandbox | Landlock ABI, LSM configuration, KVM availability and resource cost vary | Kernel feature probes, exploit/escape tests and egress validation |
| Gateway placement | Same-host process separation cannot survive host root compromise | Deployment failure-domain and credential isolation design |
| Revocation SLO | Depends on number of dispatch boundaries, storage consistency and network topology | Measured worst-case propagation under load, partition and crash |
| Audit checkpoint/retention | Privacy and resilience requirements depend on actual stored data and hosting | Data classification, recovery objectives, retention/legal review |
| External witness | Adds network and third-party trust dependency | Threat reduction versus privacy/cost/availability assessment |

## 6. Remaining owner decisions — defer until full architecture pack is ready

These are not questions to interrupt the owner with now. They are the exact decisions to present together at the end of the planned architecture work:

1. Accept or amend the final authority/envelope semantics and exact reserved action list.
2. Approve the proposed single-active-gateway/single-writer initial operating model or require higher availability.
3. Approve the initial host trust assumption and whether protection against host-root compromise requires a separate gateway machine/VM from day one.
4. Choose the owner approval authenticator/recovery approach after target device compatibility is tested.
5. Approve the independent revocation anchor approach (hardware, offline recovery, remote witness or combination).
6. Approve the maximum revocation propagation objective once the topology and worker inventory are known.
7. Approve audit retention classes/durations and whether an external checkpoint/witness is acceptable.
8. Select policy engine and workload identity mechanism only after language/runtime/deployment are selected.
9. Approve final architecture contract and permit Phase 03 planning/implementation to be considered separately.

No interim answer is required from the owner.

## 7. Workstream completion criteria

The bounded-autonomy workstream can be presented for owner review only after:
- all cross-document contradictions are resolved;
- exact action/authority/policy/risk/health/security/data/reconciliation state machines are consistent;
- owner approval, key roles, policy publication, revocation and recovery contracts are complete;
- transaction boundaries and unknown external outcome semantics are explicit;
- host trust zones and deployment-dependent assurance tiers are clear;
- every invariant maps to threat cases, requirements and future tests;
- unresolved platform-specific decisions are clearly separated from technology-neutral invariants;
- an independent adversarial review has challenged the complete design;
- GitHub documents are fetched back and verified.

This is workstream closure, not Phase 02 closure. Other Phase 02 architecture work and explicit owner acceptance remain required before Phase 03 can be considered.

## 8. Residual risks that cannot be designed away

- A request already transmitted to a venue cannot be recalled by local revocation.
- A compromised host root/kernel can defeat local process isolation.
- An offline recovery checkpoint may be stale unless independently reconciled.
- A single owner cannot provide true two-person control without changing the governance model.
- A local audit chain cannot independently prove integrity if the attacker controls both event storage and all checkpoint keys.
- Venue APIs and external account state remain outside IDEAL's transactional control.
- No finite research process proves all vulnerabilities have been discovered.

These risks require explicit owner acceptance, mitigations and/or reduced capability before any future execution approval.

## 9. Current boundary

Phase 01 closed. Phase 02 active. Phases 03–19 locked. D-023 accepted. No implementation, runtime, dependencies, credentials, accounts, exchange integrations, paper/live trading, paid services, hosting or external security tests authorised.
