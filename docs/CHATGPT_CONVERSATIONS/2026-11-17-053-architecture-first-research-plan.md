# Checkpoint 053 — Architecture-first research and design plan

**Date:** 17 November 2026  
**Project:** IDEAL  
**Phase:** 02 — Architecture and contracts  
**Record type:** Owner direction, planning method and documentation verification  
**Implementation status:** Not authorised

## Owner direction

The owner confirmed the four-pillar foundation: risk management, data integrity, system health and security. The pillars must protect and reinforce one another. The owner wants the complete structure researched and mapped before any code is written. After the structure is correct, the project should research and collect suitable existing code and technology from GitHub, the web, Hugging Face, open source and other relevant sources, then determine what to reuse, adapt or build.

The owner asked that this direction and the proposed process be saved in the IDEAL repository before beginning the architecture research process.

## Agreed planning approach

1. Define the complete system, domain boundaries, authority, trust boundaries, dependencies and non-goals.
2. Research and specify all four foundations in depth.
3. Define cross-pillar interfaces, information flows, permissions, failure propagation, safe states, audit and recovery contracts.
4. Challenge the complete architecture through threat modelling, failure analysis, edge cases and independent review.
5. Complete requirements traceability and architecture acceptance criteria.
6. Only after the architecture baseline is accepted, research GitHub, official sources, Hugging Face, academic work and open-source candidates against the design.
7. Produce an implementation blueprint with licence, maintenance, security, dependency, compatibility, cost and verification evidence.
8. Obtain explicit approval before implementation or runtime changes.

The first detailed foundation research task is risk management, designed from the outset to integrate with data integrity, system health and security.

## Four-pillar scope retained

- **Risk management:** capital/exposure controls, portfolio risk, leverage/margin/collateral, liquidation, liquidity and execution risk, authority, vetoes, kill switches, fail-closed behaviour and recovery.
- **Data integrity:** provenance, source rights, timestamps, completeness/freshness, validation, corrections, reconciliation, lineage, point-in-time reproducibility, retention and evidence.
- **System health:** independent monitoring, dependency-aware health, stale data, watchdogs, degradation, containment, incident handling, backup/restore and verified recovery.
- **Security:** threat modelling, identity and least privilege, secrets/keys, encryption/privacy, network/application/host hardening, supply chain, AI/tool isolation, audit protection, vulnerability lifecycle and incident response.

All critical interfaces must declare ownership, schema/semantics, permissions, validity/freshness, failure behaviour, safe response, audit evidence and recovery verification.

## Technology research standard

No repository, package, model or dataset is selected by popularity alone. Candidate due diligence must cover exact licence and use rights, maintenance, project health, tests/documentation, security/advisories, dependency tree, compatibility, cost, portability, limitations and reproducible evidence. Candidates are classified as reuse, adapt, isolate, defer or reject. Deterministic software remains the authority for safety-critical calculations and permissions; AI is bounded assistance, not an enforcement boundary.

## Governance and approvals

- Phase 01: closed.
- Phase 02: active; architecture/contracts and research only.
- Phases 03–19: locked.
- No runtime code, dependency adoption, deployment, exchange credentials/connectivity, paper/live execution, paid services, external security testing or financial integrations authorised.
- Active market scope remains crypto perpetual futures only.
- Deferred domains do not expand current scope.
- Documentation changes do not constitute implementation or phase advancement.

## Scheduled research review

The weekly IDEAL research review automation was created successfully in this conversation. It is scheduled for Mondays at approximately 10:00 Pacific/Auckland time, beginning 23 November 2026. Its purpose is to surface relevant research developments and architecture implications; it does not authorise scope changes, adoption, code changes or phase advancement.

## Decision recorded

D-022 records the architecture-first development method: complete and challenge the integrated architecture before implementation-ecosystem selection; then produce a traceable implementation blueprint; obtain separate owner approval before building. This records process and planning direction only.

## Repository changes

The following paths were created or updated for this checkpoint:

- `docs/IDEAL_ARCHITECTURE_FIRST_RESEARCH_PLAN.md` — complete process, four-pillar research scope, integration contract requirements, candidate due diligence, acceptance criteria and governance.
- `docs/CHATGPT_CONVERSATIONS/2026-11-17-053-architecture-first-research-plan.md` — this audit record.
- `ROADMAP.md` — Phase 02 architecture-first sequence and exit criteria.
- `README.md` — architecture-first plan added to source-of-truth index.
- `REQUIREMENTS.md` — architecture completeness and traceability requirements.
- `docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md` — cross-pillar integration and architecture-first acceptance requirements.
- `DECISIONS.md` — D-022.
- `docs/CHATGPT_CONVERSATIONS/README.md` — checkpoint 053 index entry.

## Verification

Every changed or created path must be fetched from `main` after the write and checked for the expected content. Record the resulting commit/blob identifiers in this audit record only after successful read-back. No code, tests, dependencies, runtime configuration, credentials, external services, infrastructure or financial records are changed by this checkpoint.

## Final read-back verification

All eight paths below were fetched from `main` after the writes. The expected checkpoint markers were present in every fetched file. Blob SHAs are recorded from those read-back responses.

| Path | Read-back blob SHA | Marker check |
|---|---|---|
| `docs/IDEAL_ARCHITECTURE_FIRST_RESEARCH_PLAN.md` | `a06078f0a7558aa6ba474bc9cc57382206a2431b` | PASS |
| `ROADMAP.md` | `9771a77a6b99599b6f2c23bebb26387be5ee9e5b` | PASS |
| `README.md` | `297bc209aefb2581e4bb226ed335b298a08f2b83` | PASS |
| `REQUIREMENTS.md` | `8568ad8c4f3214159a3bbe2c924cfd3cc8ca93c0` | PASS |
| `docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md` | `a728eeffb3167d568ac975be1311b712cd73e895` | PASS |
| `DECISIONS.md` | `5bb802e3160c80176e5e0eee50afbe063cc00457` | PASS |
| `docs/CHATGPT_CONVERSATIONS/2026-11-17-053-architecture-first-research-plan.md` | `cccbd8ed2ea7c44231fca7b3dea590f75154d90d` | PASS |
| `docs/CHATGPT_CONVERSATIONS/README.md` | `bae77644bfc92e6b230bd1b95bc3536090757af9` | PASS |
