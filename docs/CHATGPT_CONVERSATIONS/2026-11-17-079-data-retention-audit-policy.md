# IDEAL Work Audit — Checkpoint 079

**Date:** 17 November 2026  
**Workstream:** Phase 02 — data classification, retention, deletion and audit policy  
**Repository:** https://github.com/ImNotBrookOk/IDEAL  
**Status:** Research/documentation only; Phase 02 active; Phases 03–19 locked.

## 1. Work completed

Created `docs/IDEAL_DATA_CLASSIFICATION_RETENTION_AND_AUDIT_POLICY.md`, defining:
- C0 public, C1 internal research, C2 confidential financial/personal and C3 restricted security/authority classifications;
- data ownership/purpose registry;
- per-class retention model with durations left open unless supported by specific law/contract;
- deletion and correction lifecycle across primary stores, replicas, caches, indexes, exports, derived datasets and backups;
- audit minimisation and privacy-preserving evidence references;
- backup/key lifecycle and restore interactions;
- AI prompt/retrieval/training exclusions for C2/C3 by default;
- processor/subprocessor and cross-border data assessment.

Updated:
- `docs/IDEAL_DATA_TRUST_TEMPORAL_AND_POINT_IN_TIME_ARCHITECTURE.md`;
- `docs/PERSONAL_FINANCE_RESEARCH.md`;
- `docs/IDEAL_SECURITY_ARCHITECTURE.md`;
- `docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md`;
- `docs/IDEAL_FOUNDATION_TRACEABILITY_MATRIX.md`;
- `ARCHITECTURE.md`;
- `ROADMAP.md`;
- `README.md`.

## 2. New official-source findings

1. Privacy Act section 11 and Privacy Commissioner guidance distinguish an agent-only processor from a provider using personal information for its own purposes. Where the processor acts only on behalf of the principal and does not use/disclose for its own purposes, the principal remains responsible for the data; IPP 12 generally does not treat the agent-only processing as a disclosure. Provider own-purpose use (including model training) changes the analysis.
2. IRD cryptoasset record-keeping guidance says records supporting cryptoasset tax positions must be retained for at least seven years, even after the assets are no longer held. It lists transaction details, NZD values, exchange records, bank statements and wallet addresses. Apply only to records within that guidance's scope; the precise treatment of perpetual/futures records needs separate interpretation.
3. CARF's seven-year retention duty is for RCASPs' provider records/due diligence, not automatically the individual's own retention obligation.
4. No universal retention period is chosen for all personal-finance, tax, audit, security, AI trace or market data.

Sources:
- https://www.privacy.org.nz/resources-and-learning/a-z-topics/working-with-third-party-providers/
- https://www.privacy.org.nz/responsibilities/disclosing-personal-information-outside-new-zealand/
- https://www.ird.govt.nz/cryptoassets/taxing/record-keeping
- https://www.ird.govt.nz/international-tax/exchange-of-information/crypto-asset-reporting-framework/crypto-asset-reporting-framework-overview
- https://www.privacy.org.nz/privacy-principles/9/

## 3. Boundaries preserved

No real financial data, provider/processor selection, bank connection, cloud/AI upload, retention/deletion runtime, backup service, credentials, tax filing/payment, external integration, implementation or phase advancement. No tests were run.

## 4. Next work

Continue host trust/recovery topology research against realistic low-cost PC/home-server options, then reconcile the topology with the independent health/security supervisor, owner recovery root, backup and privacy requirements. Do not provision or purchase anything.
