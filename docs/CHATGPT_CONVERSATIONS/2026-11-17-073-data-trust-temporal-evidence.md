# IDEAL Conversation / Work Audit — Checkpoint 073

**Date:** 17 November 2026 (Pacific/Auckland)  
**Workstream:** Phase 02 — data trust, temporal semantics and point-in-time evidence  
**Repository:** https://github.com/ImNotBrookOk/IDEAL  
**Authority:** D-018, D-019, D-020, D-021, D-022  
**Status:** Research/documentation only; Phase 02 active; Phases 03–19 locked.

## 1. Work completed

Researched and documented the system-wide evidence lifecycle and temporal contract, including immutable raw observations, linked corrections, source provenance, bitemporal valid/known-time semantics, event/publication/receipt/ingest/process/decision times, consumer-specific quality states, point-in-time datasets, retention classes and private-data separation.

Created:
- `docs/IDEAL_DATA_TRUST_TEMPORAL_AND_POINT_IN_TIME_ARCHITECTURE.md`

Updated:
- `docs/DATA_INTEGRITY_AND_HEALTH.md` — data lifecycle and point-in-time contract.
- `docs/PERSONAL_FINANCE_RESEARCH.md` §22 — refreshed Akahu, privacy and NZ tax findings.
- `ARCHITECTURE.md` — temporal evidence summary.
- `docs/IDEAL_FOUNDATION_TRACEABILITY_MATRIX.md` — checkpoint 073 controls and future tests.
- `ROADMAP.md` — checkpoint 073 and next tasks.
- `README.md` — data trust architecture link.

## 2. Material findings from current official sources

### Akahu
Official documentation distinguishes the free Personal App (one user/own account, ongoing account information, no payments/webhooks, daily refresh and one-hour manual-refresh rest period) from full enduring apps that go through a separate accreditation process. The full-app process includes privacy notice, consumer information page, security/penetration testing, application review, server-validated MFA, credential protection, revocation handling, account-status alerts and data deletion. Personal App supports identity verification/MFA, IPv4 IP allowlisting, token rotation and app deletion/revocation. This corrects/clarifies the earlier broad disposition: Personal App may be a private one-user research path, but it is not real-time and is not the same as a full production app. No integration is authorised.

Sources:
- https://developers.akahu.nz/docs/personal-apps
- https://developers.akahu.nz/docs/personal-apps-advanced
- https://developers.akahu.nz/docs/app-accreditation
- https://developers.akahu.nz/docs/data-refreshes

### NZ privacy
Privacy Act 2020 section 27 contains a conditional personal/domestic-affairs exception for an individual. It is not a blanket exemption for every third-party provider or processor. The architecture continues to design for minimisation, purpose limitation, correction, security, retention, access/export and secure deletion.

Sources:
- https://www.legislation.govt.nz/act/public/2025/53/en/latest/sections/LMS899135/LMS23347/
- https://www.privacy.org.nz/privacy-principles/5/
- https://www.privacy.org.nz/privacy-principles/9/
- https://www.privacy.org.nz/privacy-principles/12/

### NZ tax / CARF
IRD CARF guidance says relevant New Zealand-connected Reporting Crypto-Asset Service Providers collect/report from 1 April 2026, with first reporting period ending 31 March 2027 and first reports due 30 June 2027. Users do not register for CARF; RCASPs report. CARF reporting is not itself a tax charge or tax classification. IRD's cryptoasset guidance does not resolve the tax treatment of a crypto futures/perpetual contract; spot-crypto rules must not be copied to derivatives. The 2026–27 Taxation Bill remains proposed/select-committee-stage in the cited IRD status snapshot; proposed FIF changes must not be treated as enacted.

Sources:
- https://www.ird.govt.nz/international-tax/exchange-of-information/crypto-asset-reporting-framework/crypto-asset-reporting-framework-overview
- https://www.ird.govt.nz/updates/news-folder/2026/what-carf-means-for-crypto-asset-users
- https://www.taxtechnical.ird.govt.nz/overviews/cryptoassets
- https://www.ird.govt.nz/crypto-currency
- https://www.taxpolicy.ird.govt.nz/bills/2026-fbt-simplification-tax-bill
- https://www.taxpolicy.ird.govt.nz/publications/2022/officials-report-2021-taxation-bill

### Data architecture references
W3C PROV-DM/PROV-O provide a useful entity/activity/agent provenance vocabulary. Apache Iceberg provides snapshot/time-travel and schema evolution; MLflow provides dataset lineage/digests. These remain reference candidates, not adopted dependencies. The architecture explicitly prefers the smallest system that satisfies the requirements.

Sources:
- https://www.w3.org/TR/prov-dm/
- https://www.w3.org/TR/prov-o/
- https://iceberg.apache.org/docs/latest/
- https://mlflow.org/docs/latest/dataset/

## 3. Key design outcomes

- Event time is not availability time. Point-in-time research must preserve when data became knowable.
- Corrections are linked revisions; raw evidence is not overwritten.
- Valid time and knowledge/transaction time are separate where backdating/corrections matter.
- Data quality is a consumer-specific vector, not a global health flag.
- Bank records are source observations until reconciled into the personal-finance journal.
- Tax rules are effective-dated and tagged by legal status/source class.
- Market, private finance, security/audit and AI traces remain separate data planes.
- No technology, schema, bank provider or tax treatment was selected.

## 4. Governance boundaries preserved

No runtime ingestion, bank connection, real financial data, credentials, subscriptions, tax filing/payment, model training, paid infrastructure, external integration, implementation or phase advancement. D-001/D-006/D-008 and all accepted risk parameters remain unchanged. No tests were run; all verification catalogues are proposed future tests.

## 5. Next work

Reconcile evidence/time semantics with risk decision validity, account and portfolio reconciliation, audit retention and recovery. Then define domain-specific risk and capital aggregation contracts and conduct an integrated adversarial challenge. Group owner decisions for the complete architecture review; do not interrupt with interim questions.
