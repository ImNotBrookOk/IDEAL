# Conversation 060 — Risk management research, Stage 7: emergency control and recovery

**Date:** 17 November 2026  
**Phase:** 02 — Architecture and contracts  
**Status:** Research/documentation only; findings provisional

## Work completed

Expanded `docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md` with:
- an independent deterministic emergency-control-plane design requirement;
- market/data, trading/account and system/security incident classes;
- safe-state and action-ordering requirements;
- separation of block-new-risk, order cancellation, risk reduction, flattening, credential isolation and manual fallback;
- incident lifecycle covering preparation, detection, containment, evidence preservation, eradication, isolated recovery, release and lessons learned;
- recovery requirements that go beyond process restart or green health;
- backup/restore integrity and isolation requirements;
- owner manual fallback procedures;
- tabletop, synthetic-data and technical incident exercises;
- explicit responsibilities across risk, data integrity, system health and security.

## Key sources

- NIST SP 800-61 Rev. 3 final (April 2025): https://csrc.nist.gov/pubs/sp/800/61/r3/final
- NIST incident response project: https://csrc.nist.gov/projects/incident-response
- CISA Federal Government Cybersecurity Incident and Vulnerability Response Playbooks: https://www.cisa.gov/sites/default/files/2024-08/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf
- FIA Best Practices for Automated Trading Risk Controls and System Safeguards (July 2024): https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf

## Important conclusions

1. Emergency control must remain independent of the strategy/AI process and be assessed across shared identity, network, host, storage and credential failure domains.
2. Cancel-on-disconnect is best-effort and session/venue-specific; it does not guarantee global cancellation.
3. Cancel-all, flatten and credential revocation can each create additional risk; action choice must be incident-specific and explicitly governed.
4. Recovery requires root-cause/scope analysis, evidence preservation, eradication, clean rebuild, integrity validation and authoritative account reconciliation.
5. A restart or healthy service indicator does not prove that financial state, permissions, data or credentials are trustworthy.
6. Manual fallback is necessary when IDEAL cannot observe or safely control external account state.
7. Each foundation must independently provide evidence for release; one pillar cannot certify another.

## Decisions and boundaries

- No new accepted decision added.
- D-006 remains 0.5% per trade; equity denominator unresolved.
- D-008 remains 10% of UTC day-start equity including realised and unrealised P&L, followed by 24-hour cooldown.
- No emergency action, credential operation, exchange integration, backup service or external scan approved.
- Phase 02 remains active; Phases 03–19 remain locked.
- No runtime implementation or execution authority authorised.

## Verification

The risk architecture and roadmap were committed. This audit record and conversation index were created. All paths must be fetched back from the default branch and content-checked before closeout.
