# Conversation 061 — Risk management research, Stage 8: independent assurance

**Date:** 17 November 2026  
**Phase:** 02 — Architecture and contracts  
**Status:** Research/documentation only; findings provisional

## Work completed

Expanded `docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md` with:
- assurance cases structured as claim, context, argument, evidence and residual risk;
- independent challenge and separation of implementation from validation;
- requirements-to-hazard-to-control-to-test traceability;
- layered static, unit, property, contract, integration, replay, stress, fault-injection, recovery and adversarial testing;
- candidate critical safety invariants;
- mutation testing and test-quality requirements;
- quantitative model/strategy assurance;
- ongoing control-effectiveness monitoring;
- release/change-control evidence gates;
- open architecture and cross-foundation assurance gaps.

## Key sources

- FIA Best Practices for Automated Trading Risk Controls and System Safeguards: https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf
- CFTC Concept Release on Risk Controls and System Safeguards for Automated Trading Environments: https://www.cftc.gov/PressRoom/PressReleases/6683-13
- Federal Reserve Supervisory Guidance on Model Risk Management: https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm
- NIST SP 800-61 Rev. 3: https://csrc.nist.gov/pubs/sp/800/61/r3/final

## Important conclusions

1. Risk assurance must be a reproducible evidence case, not a green test badge or a one-time sign-off.
2. Independent challenge must examine assumptions, models, data, control semantics, failure paths and the tests themselves.
3. Hard controls need positive, boundary, negative/adversarial and recovery tests.
4. Critical invariants include fail-closed behaviour on missing/stale/contradictory state, exact action-bound approvals, conservative order reservations, policy immutability, anti-reset protections and durable audit evidence.
5. Mutation testing helps establish whether tests can detect realistic safety defects; coverage percentage alone is inadequate.
6. Model/strategy metrics must be independently recomputed and tied to immutable experiment/data manifests.
7. Material changes require impact assessment, regression/revalidation, independent review and explicit owner approval.

## Decisions and boundaries

- No new accepted decision added.
- D-006 remains 0.5% per trade; equity denominator unresolved.
- D-008 remains 10% of UTC day-start equity including realised and unrealised P&L, followed by 24-hour cooldown.
- No implementation, validator invocation, test environment, exchange integration, deployment or phase advancement authorised.
- Phase 02 remains active; Phases 03–19 remain locked.

## Verification

The risk architecture and roadmap were committed. This audit record and conversation index were created. All paths must be fetched back from the default branch and content-checked before closeout.
