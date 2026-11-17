# IDEAL Work Audit — Checkpoint 090

**Date:** 17 November 2026  
**Workstream:** Phase 02 — official source reference revalidation  
**Repository:** https://github.com/ImNotBrookOk/IDEAL  
**Status:** Official-source research and documentation only.

## 1. Work completed

Created `docs/IDEAL_PHASE_02_SOURCE_REFERENCE_REVALIDATION.md` and rechecked primary New Zealand and security sources relevant to the current architecture.

## 2. Material clarifications

- Privacy Act 2020 section 27's current text includes the 2025/2026 amendments: the collection exception refers to IPPs 1–3A and 4(b); the holding exception covers information lawfully collected, received unsolicited or created by the individual, subject to the personal/domestic-affairs conditions and highly-offensive exception.
- Section 11 agent-only processing and IPP 12 overseas disclosure are distinct. The principal remains responsible for information processed by an agent; own-purpose use/disclosure changes the analysis.
- IRD's CARF framework excludes individuals/entities only engaged in crypto-asset activity for their own benefit. A private owner trading their own account is not an RCASP merely because they use exchanges; the role of counterparties/platforms is separate.
- IRD's CARF overview (updated 8 June 2026) says myIR registration from March 2027, while its more recent reporting-instructions page (updated 6 November 2026) says 3 December 2026. This source discrepancy is recorded; IDEAL must not hard-code either date.
- The 2026–27 Taxation Bill remains a proposal at Select Committee stage on the latest official status page checked (12 October 2026); no enactment is inferred.
- NIST SP 800-57 Part 1 Rev. 5 remains listed as final; Rev. 6 was an initial public draft with comments through 5 February 2026. NIST CSWP 39 was withdrawn 29 June 2026 and superseded by CSWP 39-upd1.
- Current Firecracker production-host guidance confirms jailer/equivalent restrictions, seccomp, cgroups/resource limits, host egress filtering, host/guest patching and microcode hygiene; Firecracker does not filter guest traffic itself.

## 3. Source updates

Added dated source-revalidation notes to:
- `IDEAL_DATA_CLASSIFICATION_RETENTION_AND_AUDIT_POLICY.md`;
- `IDEAL_DATA_TRUST_TEMPORAL_AND_POINT_IN_TIME_ARCHITECTURE.md`;
- `PERSONAL_FINANCE_RESEARCH.md`;
- `IDEAL_SECURITY_ARCHITECTURE.md`.

Updated the canonical document map, architecture-first plan, integrated review, roadmap and audit index.

## 4. Evidence and limitations

Primary-source pages were searched and the relevant IRD, Privacy Commissioner and NIST pages were opened/read where available. The Privacy Act section 27 page was retrieved through search snippets; direct open returned a cache miss. The Firecracker current upstream production-host page was retrieved in search results. The CARF overview and cryptoasset record-keeping pages were opened; the newer how-to-report page was identified in search results with its 6 November 2026 update date.

No legal advice was obtained. No tax conclusion was reached for perpetual/futures contracts. No provider eligibility determination was made. No external security test or runtime verification occurred.

## 5. Boundaries

No code, runtime, dependency, account, credential, provider connection, financial record, paper/live execution, hosting, paid infrastructure, external security testing or phase advancement.

## 6. Next work

Continue architecture pack assurance: reconcile source references against the canonical map and identify any remaining owner/independent-review blockers. Independent architecture, security/operations and maintainability reviews remain required before grouped owner decisions. Phase 02 remains active; Phases 03–19 remain locked.
