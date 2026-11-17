# IDEAL Data Trust, Temporal Semantics and Point-in-Time Evidence Architecture

**Status:** Phase 02 architecture research draft; provisional, not schema-frozen  
**Checkpoint:** 073 — 17 November 2026  
**Scope:** Evidence lifecycle, provenance, timestamps, revisions, source reconciliation, point-in-time datasets, retention and data-plane isolation  
**Authority:** D-019, D-020, D-021, D-022; D-018 for user-controlled finance/tax semantics  
**Boundary:** Research/documentation only. No data-ingestion runtime, bank connection, real financial record, provider credential, subscription, model training or implementation is authorised.

## 1. Governing invariants

1. **Integrity is not truth.** A digest proves byte identity after capture, not that the source was correct, complete, timely or honest.
2. **Raw observations are immutable evidence.** Corrections create linked revisions or superseding observations; they do not overwrite history.
3. **Time is multi-dimensional.** Source event time, publication time, receipt time, ingestion time, processing time and effective/valid time are distinct.
4. **Point-in-time reproducibility is mandatory.** A backtest or model must use only information available at its simulated decision time, not merely records whose event date is earlier.
5. **Quality is explicit and consumer-specific.** A record may be structurally valid but stale, incomplete, conflicted, unverified, revised or unsuitable for a specific decision.
6. **A projection is not an authoritative ledger.** Each bounded context owns its canonical records and emits versioned projections.
7. **Private financial data is not a general-purpose training corpus.** Access, export, retention and training eligibility are purpose-limited.
8. **Retention is not indefinite by default.** Legal, contractual, privacy, evidential and economic constraints are recorded per data class.
9. **Unknown stays unknown.** No silent interpolation, forward-fill, synthetic timestamp, stale cache or zero default may turn missing evidence into apparently current truth.
10. **Reproducibility includes rules and code.** Preserve schema, transformation, source, instrument, calendar, FX, fee, funding, policy and software versions used to produce a result.

## 2. Evidence lifecycle

Canonical lifecycle:

SOURCE → RAW_OBSERVATION → VALIDATED_OBSERVATION → CANONICAL_RECORD → DERIVED_RECORD → POINT_IN_TIME_DATASET → DECISION_EVIDENCE → AUDIT/RECONCILIATION

Not every source follows every stage. Rejections and quarantines remain observable and traceable.

| Layer | Purpose | Mutation policy | Required metadata |
|---|---|---|---|
| Source registry | Identity, ownership, endpoint/feed, entitlement, terms, schema and known limitations | Versioned; never silently repoint source identity | Provider, source class, product/venue/account scope, licence, retention, auth class, schema and adapter version |
| Raw observation | Exact bytes/message/file/statement row as received | Immutable; append-only revisions/corrections | Raw digest, byte length, source identity, source cursor/sequence, receipt time, transport context, object reference |
| Validation result | Structural, semantic, sequence, plausibility, duplicate and completeness checks | New result per validator/version; prior results retained | Validator version, ruleset, findings, severity, disposition and time |
| Canonical record | Stable domain identity and normalised units/currencies/identifiers | Corrections create new revision; prior version retained | Canonical ID, source links, valid time, known time, revision, quality state |
| Derived record | Indicators, balances, features, classifications and valuations | Recomputed as new version; lineage to all inputs | Transformation/code version, parameters, input digests, output digest, creation time |
| Point-in-time dataset | Frozen research/training/backtest view | Immutable manifest; new version for changes | Cut-off, availability rules, row set, source revisions, schema, exclusions, licence, quality report |
| Decision evidence | Exact data snapshot used for a decision or recommendation | Immutable evidence reference | Consumer, decision ID, as-of time, source snapshot, model/policy version and validity |
| Audit/reconciliation | Evidence of import, corrections, decisions, disputes and external-state reconciliation | Append-only with controlled redaction/tombstone metadata | Actor, reason, source, prior/new revision, event ordering, retention class and correlation |

W3C PROV (Entity, Activity, Agent, derivation and attribution) is a useful conceptual vocabulary for lineage, not an adopted serialization or mandatory RDF dependency. Equivalent semantics can be represented in compact relational references.

## 3. Temporal contract

Every time-bearing record distinguishes these fields where applicable:

| Field | Meaning | Example |
|---|---|---|
| source_event_time | Time the event occurred according to source | Exchange trade timestamp |
| source_published_time | Time source made the event/record available | Official release publication |
| received_at | Time IDEAL ingress received it | Local receive timestamp |
| ingested_at | Time durable raw evidence was committed | Storage commit time |
| processed_at | Time validation/transformation ran | Worker processing time |
| valid_from / valid_to | Period the fact applies in the modeled world | Effective instrument specification |
| known_from / known_to | Period IDEAL knew/treated a version as current | Late correction or backdated rule |
| decision_as_of | Information cutoff for a decision/research event | Backtest decision instant |
| monotonic_sequence | Durable local ordering within a defined stream/transaction | Event journal sequence |
| clock_quality | Trusted-clock status, uncertainty and source | Synchronisation state |

The logical model is bitemporal where corrections/backdating matter: valid time describes when a fact applies; knowledge/transaction time describes when IDEAL learned or recorded it. Do not use one generic timestamp for both.

Store unambiguous UTC instants plus original offset/time-zone and source precision where needed. Calendar concepts (NZ tax year, exchange session, funding interval, UTC risk day) are separate versioned calendars. Local wall-clock display is presentation only.

For ordering and deadlines:
- durable sequence/transaction order is authoritative within its defined scope;
- source sequence/cursor is authoritative for source-stream continuity, not global order;
- wall-clock time alone is not a total ordering mechanism;
- monotonic process clocks support elapsed-time/deadline checks but do not survive reboot as a globally comparable timeline;
- clock skew, rollback, leap/smear differences and uncertainty are recorded;
- if expiry, event ordering or freshness cannot be proven within configured bounds, dependent risk-increasing actions are denied.

## 4. Source-specific temporal and correction rules

### 4.1 Market data

Preserve exchange event timestamp, local receive timestamp, channel sequence/update IDs, snapshot sequence, trade IDs, instrument metadata version, and provider publication/capture timestamp where available. Do not sort away sequence violations. A gap, checksum failure, duplicate, out-of-order event or reconnect snapshot mismatch opens a gap/incident record.

A backfill is new evidence, not proof that the original stream was continuous. Distinguish event-time chronology, arrival/availability chronology, reconstructed book state and later-corrected historical state.

For simulation, a datum is eligible only when its availability time is at or before the simulated decision time. If a historical provider delivers corrected records without original availability time, mark point-in-time fidelity as limited; do not claim leakage-free replay.

### 4.2 Bank and personal-finance data

Keep separate source dates/times for transaction initiation/authorisation, booking/posting, value date, pending/posted status, source refresh time and IDEAL receipt time. A bank's latest returned balance is a source snapshot, not necessarily real-time available funds.

A provider row ID is an idempotency key, not an immutable truth guarantee. Track changed payloads, deleted rows, pending-to-posted transitions, reversed/returned transactions, transfer legs, FX fields and provider pagination/cursor. A missing row in a later API response is not automatically a deletion unless the provider contract defines snapshot completeness or explicit deletion semantics.

Imported data first enters an observation/staging ledger. Only explicit reconciliation rules may post or amend the personal-finance journal. Keep original statement evidence and journal posting/reversal links. Never silently rewrite a previously reconciled transaction.

### 4.3 Tax and legal rules

Tax rules are effective-dated by jurisdiction, tax year, enactment/commencement, publication and applicability. Store source class (legislation, binding ruling, public guidance, issues paper, technical decision summary, adviser interpretation), status, version, retrieval date and applicability assumptions. A consultation paper or non-binding technical summary must not be represented as binding law.

Tax calculations must be reproducible under both the rule set applied and the current rule set where retrospective correction/reassessment is required. Keep source events, tax classification, calculation method, elections, FX, rounding, workpaper and reviewer evidence separate.

## 5. Quality and fitness-for-use model

Quality is a vector, not one green flag:
- authenticity/source identity;
- structural/schema validity;
- completeness and sequence continuity;
- freshness/age;
- semantic plausibility;
- cross-source consistency;
- correction/revision status;
- licensing/entitlement validity;
- point-in-time availability;
- reconciliation state;
- clock confidence.

Suggested states: VALID, DEGRADED, STALE, INCOMPLETE, CONFLICTED, REVISED, UNVERIFIED, QUARANTINED and UNKNOWN.

Each consumer declares required dimensions and thresholds. A derived feature inherits the worst relevant input status unless a documented transformation proves a specific defect immaterial. A downstream component cannot improve upstream quality by relabelling. Producer quality assessment and consumer fitness decision are separate.

## 6. Point-in-time datasets and research integrity

A dataset manifest identifies:
- immutable source observations and exact revisions;
- decision_as_of and availability-time cutoff;
- event-time range and timezone/calendar version;
- late arrivals, corrections and excluded intervals;
- schema, normalisation and transformation code versions;
- instrument/contract metadata effective at each time;
- corporate actions, delistings, symbol mappings and survivorship treatment where relevant;
- FX, fees, funding, spread, slippage, liquidity and execution assumptions;
- label horizon and label maturity/embargo rules;
- train/validation/test periods and walk-forward split definitions;
- licence, permitted purpose, retention and deletion restrictions;
- digest, quality report and reproducibility environment.

No feature may use information published after its decision time. Labels may use future outcomes only in target construction and must not leak into features or overlapping train/test windows. Overlapping labels require purging/embargo or another defensible leakage control. Survivorship, look-ahead, selection bias, regime selection and multiple-testing effects must be assessed.

For crypto derivatives, preserve funding schedule and realised funding events, mark/index/basis inputs, contract specification and fee tier as effective-dated data. A backtest using today's instrument metadata or fee schedule for historical periods must disclose the approximation.

## 7. Data archive and retention model

Separate at least these data planes:
1. Public/licensed market evidence and derived research.
2. Private personal-finance, bank, tax and identity records.
3. Security/authority/audit evidence.
4. AI/agent prompts, tool traces and retrieved private content.

Each source/data class receives a policy record containing purpose, owner, sensitivity, lawful/contractual basis, licence, permitted users/processes, residency/transfer constraints, retention trigger, deletion method, legal hold, backup expiry, export policy and training eligibility.

Retention classes are purpose-based, not one global duration: transient cache; operational state; raw market evidence; licensed historical market archive; research dataset/experiment; private financial source record; personal ledger/tax workpaper; security/authority/audit evidence; AI trace/model evaluation; backup and disaster-recovery copy.

Do not promise immutable retention that overrides lawful deletion, provider contract or source licence. Where an audit event must survive source-payload deletion, retain a minimised event with opaque reference and tombstone status only if this does not itself retain disallowed personal data. Cryptographic erasure is a candidate, not a universal answer: key backups, replicas, logs, caches and exported copies must be covered.

NZ legal note: Privacy Act 2020 Principle 9 limits retention to what is needed for a lawful purpose; Principle 5 concerns reasonable security safeguards; Principle 12 regulates disclosure outside New Zealand. Section 27 contains an exemption for an individual holding information solely for personal/domestic affairs, subject to its conditions and highly-offensive exception. Do not assume the whole IDEAL supply chain is exempt: a bank-data provider, cloud/AI vendor or other agency has its own legal and contractual duties, and facts can change if the system is used for business or other people. This is architecture research, not legal advice.

## 8. New Zealand provider and tax findings

### Akahu

Official Akahu developer documentation distinguishes:
- Personal App: free, one user (the owner's own Akahu account), ongoing account-information access, no payments, no webhooks, daily scheduled refresh and a one-hour manual-refresh rest period. Identity verification and MFA are prerequisites; IP allowlisting is available; app tokens can be rotated and the app deleted to revoke access.
- Full enduring account-information app: separate accreditation process. Current documentation describes privacy notice and consumer information page, security review, server-validated MFA, token revocation handling, account status alerts, recent relevant security/penetration testing, and ongoing deletion of data no longer reasonably required. Initial application review is free; subsequent reviews after the first may cost NZ$1,000 each.

The Personal App may be a plausible private one-user research path, but its daily refresh/no-webhook model is not real-time bank data and its suitability for any eventual production topology/terms must be confirmed. Full App accreditation is a distinct and materially more demanding path; do not assume it is required for a private Personal App or assume it is waived. No Akahu path is selected or authorised.

### New Zealand privacy

The statutory personal/domestic affairs exemption is fact-dependent. Even if the individual owner qualifies, third-party providers and processors are not automatically exempt. Design to strong privacy principles regardless: minimisation, purpose limitation, correction, retention limits, security, access control, export and secure deletion. Cross-border processing requires a separate assessment; local inference is not automatically compliant, and overseas API processing is not automatically prohibited.

### New Zealand tax and crypto

IRD cryptoasset guidance treats cryptoassets as property and says they are generally excepted financial arrangements except those economically equivalent to debt arrangements. A crypto futures/perpetual contract is not simply the underlying cryptoasset; its tax classification must not be inferred from spot guidance. IRD's 2022 officials' report discussed futures over cryptoassets being subject to financial-arrangements rules, but that historical policy material is not a substitute for checking current legislation, contract terms and specialist advice.

IRD CARF guidance says New Zealand-based Reporting Crypto-Asset Service Providers must collect/report from 1 April 2026, with the first reporting period ending 31 March 2027 and first reports due 30 June 2027. Provider reporting is not itself a new tax charge or a user registration requirement. IRD says users do not register for CARF; RCASPs report. The user's own trading for their own benefit is not, by itself, an RCASP business activity under IRD's published description, but the exact counterparty/provider role must be assessed separately.

The Taxation (Annual Rates for 2026–27, FBT Simplification, Foreign Investment Funds, and Remedial Measures) Bill was introduced 10 September 2026 and is recorded by IRD Tax Policy at select-committee stage as at 12 October 2026. Proposals such as a FIF de minimis threshold change must be treated as proposed until enactment and effective-date confirmation. Tax rule packs therefore need legal status and effective dates, not just publication dates.

## 9. Candidate standards and technology references — no adoption

| Candidate/reference | Useful property | Limitation / disposition |
|---|---|---|
| W3C PROV-DM / PROV-O | Domain-agnostic entity/activity/agent provenance and derivation vocabulary | Conceptual reference; RDF is not required |
| Apache Iceberg | Snapshot/time-travel queries, schema evolution and partition evolution for analytic tables | Potentially over-sized for a personal single-host initial system; not selected |
| MLflow dataset tracking | Dataset digests, source lineage, schema/profile and experiment linkage | Candidate for later model research; not an authoritative data archive or ledger |
| Append-only raw object store + metadata catalogue | Simple evidence preservation and source-level traceability | Must solve revision indexes, access controls, deletion, licence, backup and query economics |
| Relational bitemporal tables | Explicit valid-time and knowledge-time semantics | Requires disciplined schema/index/query design; no database selected |

Prefer the smallest architecture that satisfies provenance, point-in-time replay, retention and recovery. Do not adopt Iceberg, MLflow or a distributed lakehouse merely because data volume may grow. Benchmark storage economics against actual retained feeds and use cases before selecting formats.

## 10. Required verification

Future acceptance tests must include raw-byte/source identity mismatch; duplicate/late/reordered/missing market events; sequence gap/checksum/reconnect mismatch; late correction and as-known-then versus latest-corrected queries; bitemporal query correctness; clock skew/rollback/timezone/tax-year/funding boundaries; bank pending-to-posted/changed/deleted/duplicate/transfer/FX corrections; provider refresh age/account inactive/token revocation/no-webhook detection; licence expiry/retention deletion/backup expiry; point-in-time feature availability and label leakage; immutable dataset digest and exact replay; private finance excluded from default AI retrieval/training; privacy deletion across stores/cache/logs/backups/derived data; revised tax rule status/effective date and reproducible prior calculation; CARF provider reporting kept separate from tax-liability calculation.

No such runtime tests have been run.

## 11. Open questions

- Which feeds and source tiers are licensed for raw retention, derived features, research, model training and deletion?
- What event-time/availability-time guarantees do each chosen venue/provider expose?
- What clock uncertainty bound is required for each future use?
- What retention periods apply to personal ledgers, tax workpapers and security/audit records under the owner's actual circumstances?
- Which bank provider route is contractually available for private use versus production use, and what are its exact correction guarantees?
- What is the authoritative tax interpretation for crypto perpetual instruments and the owner's actual contract/account/residency facts?
- Which data stores and formats meet workload needs without unnecessary infrastructure?

## 12. Disposition and next work

Technology-neutral evidence and temporal invariants are sufficiently specified for cross-document challenge, but no implementation schema is frozen. Next: reconcile these semantics with risk decisions/reservations, account reconciliation, security/audit retention and the integrated domain map; then define domain-specific risk and capital aggregation contracts.

Phase 02 remains active. Phases 03–19 remain locked. No implementation, data subscription, bank connection, real-record handling, provider credential, model training, paid infrastructure or external integration is authorised.

## Sources

- W3C PROV-DM: https://www.w3.org/TR/prov-dm/
- W3C PROV-O: https://www.w3.org/TR/prov-o/
- Apache Iceberg: https://iceberg.apache.org/docs/latest/
- MLflow dataset tracking: https://mlflow.org/docs/latest/dataset/
- NZ Privacy Act 2020, section 27: https://www.legislation.govt.nz/act/public/2025/53/en/latest/sections/LMS899135/LMS23347/
- NZ Privacy Commissioner, Principle 5: https://www.privacy.org.nz/privacy-principles/5/
- NZ Privacy Commissioner, Principle 9: https://www.privacy.org.nz/privacy-principles/9/
- NZ Privacy Commissioner, Principle 12: https://www.privacy.org.nz/privacy-principles/12/
- Akahu Personal Apps: https://developers.akahu.nz/docs/personal-apps
- Akahu Personal Apps advanced: https://developers.akahu.nz/docs/personal-apps-advanced
- Akahu app accreditation: https://developers.akahu.nz/docs/app-accreditation
- Akahu data refreshes: https://developers.akahu.nz/docs/data-refreshes
- IRD cryptoassets overview: https://www.taxtechnical.ird.govt.nz/overviews/cryptoassets
- IRD cryptoasset tax guidance: https://www.ird.govt.nz/crypto-currency
- IRD CARF overview: https://www.ird.govt.nz/international-tax/exchange-of-information/crypto-asset-reporting-framework/crypto-asset-reporting-framework-overview
- IRD CARF user guidance: https://www.ird.govt.nz/updates/news-folder/2026/what-carf-means-for-crypto-asset-users
- IRD Taxation Bill status: https://www.taxpolicy.ird.govt.nz/bills/2026-fbt-simplification-tax-bill
- New Zealand Legislation, 2026–27 Taxation Bill: https://www.legislation.govt.nz/bill/government/2026/344/en/latest/
- IRD financial arrangements rules: https://www.ird.govt.nz/income-tax/income-tax-for-businesses-and-organisations/types-of-business-income/interest-and-dividends/financial-arrangements-rules
- IRD officials' report on cryptoasset derivatives: https://www.taxpolicy.ird.govt.nz/publications/2022/officials-report-2021-taxation-bill


## Privacy processor and tax-record retention clarification — checkpoint 079

Further official-source review clarifies two retention/privacy details:
- Privacy Act section 11 treats information held by a third-party processor solely as an agent for the principal differently from a provider using the data for its own purposes. Where the provider acts only on the principal's behalf and does not use/disclose for its own purposes, the principal remains responsible for the information; IPP 12 generally does not treat the agent-only processing as a disclosure. If the provider uses/discloses data for its own purposes (including its own model training), both may be treated as holding the information and IPP 11/12 analysis may apply.
- IRD's cryptoasset record-keeping guidance says records supporting cryptoasset tax positions must be kept at least seven years, even if the person no longer holds cryptoassets. It lists transaction type/date/units/NZD value, opening/closing unit totals, exchange records, bank statements and wallet addresses. This duration must be applied to records within the guidance's scope; the precise treatment of perpetual/futures contracts requires separate interpretation. The separate CARF seven-year record obligation applies to RCASPs, not automatically to individual users.

Sources:
- https://www.privacy.org.nz/resources-and-learning/a-z-topics/working-with-third-party-providers/
- https://www.privacy.org.nz/responsibilities/disclosing-personal-information-outside-new-zealand/
- https://www.ird.govt.nz/cryptoassets/taxing/record-keeping
- https://www.ird.govt.nz/international-tax/exchange-of-information/crypto-asset-reporting-framework/crypto-asset-reporting-framework-overview


## Consumer-specific freshness and clock requirements — checkpoint 088

Freshness is a consumer-specific fitness contract, not a global TTL. Each consumer declares source cadence, event/availability semantics, maximum decision/event age, clock uncertainty, completeness/gap rules, degradation behaviour and restoration evidence. Market L2, trades, candles, funding, mark/index, contract metadata, account state, FX, bank data, tax rules and health telemetry have distinct source-specific requirements.

See [IDEAL Data Freshness, Clock Quality and Decision-Validity Requirements](IDEAL_DATA_FRESHNESS_AND_CLOCK_REQUIREMENTS.md). Numeric thresholds remain open until sources, host and decision tolerance are known.
