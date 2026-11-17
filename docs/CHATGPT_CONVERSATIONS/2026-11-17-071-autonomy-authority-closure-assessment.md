# Checkpoint 071 — autonomy authority closure assessment

**Date:** 17 November 2026  
**Phase:** 02 — architecture/contracts (active)  
**Status:** Consolidated workstream assessment; provisional, not owner-approved final architecture  
**Governance:** D-023 remains Accepted. No new decision or phase transition.

## Owner instruction

The owner authorised autonomous continuation of the existing IDEAL plan, asked not to be interrupted for questions until the planned work is complete, and asked that research and documentation continue independently. This authorisation does not override the established restrictions on implementation, runtime, dependencies, credentials, accounts, exchange integrations, paper/live execution, paid services, hosting or external security tests.

## Work completed in this checkpoint

Created docs/IDEAL_AUTONOMY_AUTHORITY_CLOSURE_ASSESSMENT.md to consolidate:
- accepted D-023 governance;
- technology-neutral authority, policy, identity, revocation, risk, health, audit and recovery invariants;
- provisional initial private-deployment recommendations;
- platform/runtime-dependent choices intentionally deferred;
- exact owner decisions to present together after the planned architecture work;
- workstream completion criteria and residual risks that cannot be designed away.

Updated the main autonomy architecture, roadmap, README, integrated adversarial review and foundation traceability matrix with cross-references and closure requirements.

## Main recommendations (provisional, not adopted)

- Single active action gateway and one authoritative writer initially; do not introduce multi-active dispatch/consensus until availability requirements justify it.
- One ACID transactional store for intent, authority evidence, risk reservation, audit event and outbox; exact database and durability configuration depend on later runtime selection.
- Separate workload identities and no credentials/generic venue egress in strategy/AI processes.
- Layered Linux controls and disposable microVM evaluation for high-risk arbitrary code; platform support must be verified.
- Cedar/OPA, SPIFFE/SPIRE, hardware-backed key storage, remote witness and Firecracker/gVisor/Kata remain candidates only.
- Health supervisor remains restrictive-only; security incident-response authority is separate.
- Recovery never restores active authority from backup; independent current revocation state is required.
- No technology or deployment has been selected.

## Technology-neutral invariants considered sufficiently specified

Owner envelope semantics, exact digest-bound approval, immutable policy lifecycle, distinct workload identities, non-bypassable action boundary, separate authority/risk gates, monotonic revocation generation, DISPATCH_STARTED linearisation point, no exactly-once external claim, trust zones, restrictive-only health interlock, security response separation, atomic local audit/reservation/outbox, UNKNOWN reconciliation and restore quarantine.

Schemas, runtime APIs, numerical SLOs, physical trust topology, key custody mechanisms, policy engine, workload identity implementation, retention periods and exact deployment remain open.

## Remaining owner decisions

The assessment deliberately defers all questions until the full architecture pack is ready. It lists nine grouped owner decisions, including final envelope semantics, single-active-gateway model, host-root trust assumption, authenticator/recovery, independent revocation anchor, propagation target, audit retention/external witness, policy/workload identity selection and final architecture acceptance/Phase 03 consideration.

## Residual risks explicitly preserved

- Already transmitted external requests cannot be recalled by local revocation.
- Shared host root/kernel compromise defeats local process isolation.
- Offline recovery checkpoint may be stale without independent reconciliation.
- Single owner cannot provide true two-person control without changing governance.
- Local audit chain is not independently trustworthy if attacker controls all storage and checkpoint keys.
- External venue state cannot be included in IDEAL's local ACID transaction.
- Research cannot prove all vulnerabilities have been discovered.

## GitHub changes

- Created docs/IDEAL_AUTONOMY_AUTHORITY_CLOSURE_ASSESSMENT.md.
- Linked it from the autonomy authority architecture, README and roadmap.
- Added residual-risk closure notes to the integrated adversarial review.
- Added workstream closure traceability to the foundation matrix.
- Created this audit record and indexed it.

## Current status and non-authorisations

Phase 01 closed. Phase 02 active. Phases 03–19 locked. D-023 accepted. This closes no project phase and does not authorise implementation or execution. No runtime, dependency, credential, account, exchange connection, financial record, paid service, hosting or external test was added or changed.

## Next autonomous work

Perform a final consistency and completeness audit of the entire authority workstream, verify all files from GitHub, update the audit trail, and present the completed workstream with a precise list of deferred owner decisions. Continue to keep Phase 02 active and later phases locked.
