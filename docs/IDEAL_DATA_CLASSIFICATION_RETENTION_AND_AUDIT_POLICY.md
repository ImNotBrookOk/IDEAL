# IDEAL Data Classification, Retention, Deletion and Audit Policy Architecture

**Status:** Phase 02 policy architecture draft; provisional, no retention schedule adopted  
**Checkpoint:** 079 — 17 November 2026  
**Scope:** Data classification, access, retention, deletion, legal/contractual holds, audit evidence, backup expiry and third-party processing  
**Authority:** D-018, D-019, D-020, D-021, D-022, D-023  
**Boundary:** Design only. No real records, external processor, cloud/AI upload, provider connection, retention service, deletion job, backup system or implementation is authorised.

## 1. Policy objectives

IDEAL must preserve enough evidence to reproduce research, reconcile financial state, explain decisions, investigate incidents and meet applicable legal/contractual obligations, without retaining every byte forever or exposing private records to unrelated domains.

The policy balances five requirements:
1. Confidentiality and least-privilege access.
2. Evidence integrity, provenance and reproducibility.
3. Legal, tax, licence and provider-contract obligations.
4. Purpose limitation, data minimisation and secure deletion.
5. Recoverability without resurrecting deleted data or revoked authority.

Retention is a property of each data class and purpose, not a single global duration. No data is retained merely because storage is cheap.

## 2. Classification levels

| Class | Label | Examples | Default handling |
|---|---|---|---|
| C0 | Public | Public documentation, public market metadata, public law/guidance | Retain/use only within source terms and licence |
| C1 | Internal research | Strategy hypotheses, synthetic fixtures, derived public-market research, non-sensitive metrics | IDEAL workspace only; versioned, provenance-backed and purpose-limited |
| C2 | Confidential financial/personal | Bank statements, transaction histories, personal ledger, tax records, account balances, identifiable activity | Strong encryption, least privilege, no default AI retrieval/training, controlled export/deletion |
| C3 | Restricted security/authority | Credentials, tokens, private keys, recovery material, owner approval evidence, vulnerability details, security incident secrets | Dedicated secret/key systems, minimal exposure, no prompts/logs, tightly scoped access and rotation |

Classification applies to derived data too. Removing a name does not automatically make a dataset anonymous if the remaining fields can identify or re-link the person. C2 source data must not be copied into C1 research or C0 outputs without a documented transformation and privacy review.

## 3. Data ownership and purpose registry

Every source, dataset, record family, export, backup and model artefact must have a policy record:

- data owner and accountable bounded context;
- purpose and permitted use;
- classification and identifiable-person status;
- source/provider identity and acquisition method;
- licence, terms, permitted retention and derivative/training rights;
- legal/contractual basis and jurisdiction;
- access principals and least-privilege scope;
- data residency, processor and subprocessor information;
- retention trigger, retention period or review rule;
- deletion method and propagation scope;
- legal hold status and approving authority;
- backup expiry and encryption-key dependency;
- training/retrieval eligibility;
- export and disclosure controls;
- last review, policy version and evidence.

A record without a known purpose, owner or retention class is quarantined from new use until classified.

## 4. Retention schedule — proposed classes, durations mostly unresolved

| Data class | Retention trigger / rule | Duration disposition | Deletion/review condition |
|---|---|---|---|
| Public market raw data | Source licence, exchange/provider terms and research need | Per-feed; no global duration | Licence expiry, purpose end or source deletion requirement |
| Derived market data/features | Inherits source rights and transformation provenance | Per-source/per-derivative terms | Recompute/delete where rights or source restrictions require |
| Research manifests and experiment metadata | Reproducibility and research governance | Retain while research has a justified purpose; review periodically | Delete sensitive payloads; keep only permitted metadata/digests |
| Synthetic fixtures | Testing/research value | May be retained without personal data | Remove if they accidentally embed real identifiers or source material |
| Personal bank source observations/statements | Reconciliation, personal accounting and applicable legal/tax obligations | Owner-specific; no default indefinite retention | Delete when no longer required and no applicable hold/obligation |
| Personal-finance journal | Accounting history, correction/audit needs and applicable legal obligations | Owner-specific; review with legal/tax retention requirements | Preserve correction trail; controlled disposal when lawful and no longer required |
| Cryptoasset transaction tax evidence | IRD record-keeping guidance | At least 7 years where the transaction/record is within the applicable cryptoasset record-keeping requirement | Do not delete before the required period; confirm derivative/perpetual coverage with qualified NZ tax advice |
| Other tax workpapers/assessments | Applicable legislation, IRD guidance and professional advice | Per tax-year/jurisdiction; not assumed universal | Review after statutory period, disputes, audit or legal hold |
| CARF RCASP compliance records | Provider's statutory RCASP reporting/due-diligence obligations | IRD states RCASPs retain specified records for at least 7 years; this is a provider obligation, not automatically the individual user's retention rule | Provider-specific statutory schedule |
| Security and authority events | Security assurance, incident investigation, policy accountability | Duration by event class/severity; not yet selected | Minimise content; extend only for active incident/legal hold |
| Audit event metadata | Reproducibility and accountability for consequential transitions | Duration by action class; not yet selected | Preserve only necessary event fields and evidence references |
| AI prompts/tool traces | Debugging, safety and workflow quality | Transient by default; exact period not selected | Redact/minimise; do not retain private finance payload by default |
| Model training/evaluation datasets | Explicit research purpose, source rights and reproducibility | Dataset-specific and versioned | Remove ineligible sources; no default C2 inclusion |
| Backups and replicas | Disaster recovery | Bounded expiry; exact RPO/RTO and retention not selected | Expire after source retention/deletion window; never resurrect revoked authority |
| Exports/reports | User-requested purpose | Short-lived unless explicitly saved by owner | Expire/delete after purpose; watermark/classify where useful |

**Important legal distinctions**
- IRD's cryptoasset record-keeping guidance says relevant cryptoasset transaction records must be kept for at least seven years, even if the person no longer holds cryptoassets. It lists transaction type/date/units/NZD value, total units at year boundaries, exchange records, bank statements and wallet addresses. Whether a particular perpetual/futures contract falls within that exact guidance must be confirmed; do not assume spot guidance resolves derivative treatment.
- IRD's CARF seven-year retention statement applies to Reporting Crypto-Asset Service Providers' records and due diligence, not automatically to every individual user's own record retention.
- IRD's business record-keeping guidance is not automatically a blanket rule for every personal/domestic record. Determine the applicable taxpayer and record class.
- No general retention duration is chosen for personal-finance, AI trace, security or market data in this architecture.

## 5. Privacy and third-party processing — New Zealand context

The Privacy Act 2020 contains a conditional personal/domestic-affairs exception for an individual (section 27), but it is not a reason to design carelessly or to assume all processors are exempt.

Section 11 matters for third-party processors: where a service provider stores/processes personal information solely as an agent on behalf of another agency and does not use/disclose it for its own purposes, the principal is generally treated as holding the information. The principal remains responsible for what happens to it. If the provider uses/discloses information for its own purposes, both may be treated as holding it and further disclosure principles may apply.

IPP 11 limits disclosure; IPP 12 applies to certain disclosures to foreign persons/entities. The Privacy Commissioner explains that sending data to a cloud provider acting solely as an agent is generally not itself an IPP 12 disclosure, but the data-holding agency remains responsible. A processor's own-purpose use, including model training or cross-customer reuse, changes the analysis.

Architecture requirements:
- maintain a processor/subprocessor inventory and data-flow map;
- know whether the provider acts only as an agent or uses data for its own purposes;
- prohibit provider training/reuse of C2 data unless explicitly approved and lawfully supported;
- assess contracts, subprocessors, breach notification, deletion, access and export;
- assess cross-border disclosure where IPP 12 applies; do not assume local hosting is mandatory or offshore processing automatically prohibited;
- use data minimisation and purpose limitation regardless of exemption;
- avoid putting bank/tax/identity records into general-purpose prompts, telemetry or error logs.

This is architecture research, not legal advice. Any later provider selection requires current contract and legal review.

## 6. Deletion and correction lifecycle

Deletion must be a controlled workflow, not a single database DELETE. Proposed states:

1. **REQUESTED** — source, owner or policy triggers deletion/correction.
2. **SCOPE_RESOLVED** — identify primary records, replicas, caches, indexes, exports, logs, backups, derived features, datasets and model artefacts.
3. **OBLIGATION_CHECKED** — determine applicable tax/legal retention, source licence, dispute, incident and legal hold.
4. **APPROVED** — verify authority and any required owner confirmation.
5. **DELETION_PENDING** — tombstone source record and block new use immediately.
6. **PROPAGATING** — remove or invalidate copies, caches, indexes, derived records and permitted downstream datasets.
7. **BACKUP_EXPIRY_PENDING** — wait for bounded backup expiry or apply approved cryptographic erasure where feasible.
8. **VERIFIED** — evidence confirms each required location is deleted, inaccessible or expired.
9. **CLOSED** — retain a minimal deletion event only if lawful and not itself disclosive.

A legal/contractual hold suspends deletion only for the scoped data and period. It must have an authority, reason, start, review date and release condition.

Corrections are not deletion by default: preserve old and new versions where lawful and necessary for audit/reproducibility, while clearly marking superseded data. If deletion is required, remove payloads and dependent copies rather than preserving a recoverable raw version.

## 7. Audit design and privacy minimisation

Audit events should record:
- actor/service identity and scope;
- action and target reference;
- timestamp plus durable event order;
- prior/new version or digest;
- reason and policy/approval version;
- source evidence references;
- outcome and reconciliation status;
- classification, retention class and correlation ID.

Do not log passwords, tokens, private keys, recovery codes, full bank statement payloads, unnecessary account numbers, tax identifiers or full prompt content. Prefer opaque references, field-level redaction and minimal event facts. Security incident evidence may require restricted detail in a separate store.

Audit immutability is not an excuse for indefinite personal-data retention. Use scoped retention, tombstones, redaction or cryptographic erasure where appropriate. Hashes of personal data can remain personal data if they are linkable or re-identifiable; hashing alone is not anonymisation.

For future consequential actions, local pre-dispatch audit durability remains mandatory under the autonomy contract. An external witness/checkpoint is a separate optional trust mechanism, not a substitute for local evidence or privacy policy.

## 8. Backup, key and deletion interactions

- Encrypt backups with keys separate from application and venue credentials.
- Separate key-encryption keys, data-encryption keys, signing keys and owner/recovery roots.
- Define key rotation, compromise response, backup-key escrow/recovery and destruction evidence.
- Backups must have a bounded expiry and be included in retention/deletion policy.
- A restore must not resurrect deleted records, revoked tokens, old policy generations or active admission permits.
- If deletion must propagate to immutable backups, use expiry windows or crypto-erasure only after analysing key replicas, escrow, exports, logs and snapshots.
- Test restore after deletion, key rotation, revocation and schema evolution.
- Backup retention must not exceed the underlying data retention without a documented legal/operational reason.
- No backup provider, key store, RPO/RTO or duration is selected.

## 9. AI, retrieval and learning policy

- C2 personal-finance/tax/identity records are excluded from default model training, fine-tuning, retrieval indexes, external AI tools and prompt logging.
- If a future use case requires private records for a user-requested analysis, access must be scoped to that task and data minimised; outputs must not leak sensitive values into reusable research traces.
- Agent traces should store structured task metadata and redacted tool summaries, not full private payloads by default.
- Model datasets require explicit source rights, purpose eligibility, lineage, point-in-time correctness, privacy assessment and deletion propagation.
- Do not train on credentials, recovery material, security incidents or identifiable private financial records.
- If a source must be deleted after it has influenced a model, the system must have avoided that source in training by default; post-hoc machine unlearning is not assumed to be reliable.
- Assistant workflow improvement and quantitative market-model training remain separate.

## 10. Operational controls and future tests

Future controls/tests:
- every data class has an owner, purpose, classification and retention rule;
- unclassified data is denied from new use;
- provider terms/licence expiry blocks restricted ingestion/retention/training;
- third-party processor own-purpose use is distinguished from agent-only processing;
- C2 data cannot enter default AI prompt/training/retrieval paths;
- retention expiry and legal hold are tested against every copy;
- deletion propagates to primary stores, replicas, caches, indexes, exports, logs, datasets and backups;
- tombstone/audit evidence does not disclose the deleted payload;
- cryptographic erasure includes all key copies and replicas;
- restore cannot resurrect deleted or revoked state;
- tax record retention follows applicable IRD guidance without over-applying RCASP obligations to the individual;
- privacy access/correction/export/deletion workflows are auditable;
- breach response identifies affected processors/subprocessors and notification duties;
- market-data licence and derived-data rights propagate to dataset manifests.

No retention/deletion runtime tests were performed.

## 11. Open policy decisions

- Exact retention periods by personal-finance, tax, audit, security, AI trace and research data class.
- Whether to retain raw market feeds, and under which source licences.
- How long to retain private bank source statements after journal reconciliation.
- Legal-hold authority, review cadence and closure.
- Whether external audit checkpoints are justified and acceptable.
- Backup expiry, RPO/RTO, key destruction and restore objectives.
- Processor/subprocessor approval and cross-border data assessment.
- Whether any private-data retrieval workflow is ever justified beyond one-off owner-requested analysis.
- Tax professional interpretation of record retention for crypto perpetual contracts.

## 12. Disposition

This document defines the integrated policy model but deliberately does not choose universal retention periods or a storage/backup provider. Legal minimums and provider contracts must be applied to the specific data class; privacy minimisation applies across all domains.

Phase 02 remains active; Phases 03–19 remain locked. No data processor, bank connection, cloud service, AI data upload, retention job, deletion job, backup system, implementation or external action is authorised.

## Sources

- NZ Privacy Act 2020, section 11 and section 27: https://www.legislation.govt.nz/act/public/2020/31/en/latest/
- Privacy Commissioner — third-party providers: https://www.privacy.org.nz/resources-and-learning/a-z-topics/working-with-third-party-providers/
- Privacy Commissioner — Principle 9 retention: https://www.privacy.org.nz/privacy-principles/9/
- Privacy Commissioner — Principle 11 disclosure: https://www.privacy.org.nz/privacy-principles/11/
- Privacy Commissioner — Principle 12 disclosure outside NZ: https://www.privacy.org.nz/privacy-principles/12/
- Privacy Commissioner — sending information overseas: https://www.privacy.org.nz/responsibilities/disclosing-personal-information-outside-new-zealand/
- IRD — cryptoasset record keeping: https://www.ird.govt.nz/cryptoassets/taxing/record-keeping
- IRD — CARF overview and RCASP record obligations: https://www.ird.govt.nz/international-tax/exchange-of-information/crypto-asset-reporting-framework/crypto-asset-reporting-framework-overview
- IRD — business record keeping: https://www.ird.govt.nz/records
- Akahu — app accreditation and data deletion: https://developers.akahu.nz/docs/app-accreditation


## 11. Privacy Act source clarification — checkpoint 090

The current consolidated Privacy Act 2020 text (in force as at 8 October 2026) reflects amendments to section 27. The personal/domestic-affairs collection exception refers to IPPs 1–3A and 4(b). The holding exception for IPPs 5–12 applies where an individual holds information solely for personal/domestic affairs and the information was collected lawfully, received unsolicited or created by the individual. Both are conditional and do not apply where the collection, use or disclosure would be highly offensive to a reasonable person. This does not automatically exempt separate processor agencies or providers. Section 11 agent-only processing and IPP 12 overseas disclosure must be assessed separately. See [Official Source Revalidation](IDEAL_PHASE_02_SOURCE_REFERENCE_REVALIDATION.md).
