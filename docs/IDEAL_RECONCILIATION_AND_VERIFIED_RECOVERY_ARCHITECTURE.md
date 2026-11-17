# IDEAL Reconciliation, Incident Containment and Verified Recovery Architecture

**Status:** Phase 02 research/design draft; provisional and not owner-accepted  
**Checkpoint:** 076 — 17 November 2026  
**Scope:** Reconciliation authority, source-of-truth boundaries, mismatch lifecycle, incident containment, backup/restore and recovery release  
**Authority:** D-018, D-019, D-020, D-021, D-022, D-023  
**Boundary:** Documentation only. No runtime recovery, account/venue access, bank connection, credential operation, external scan, paper/live execution, hosting or implementation is authorised.

## 1. Purpose and governing rule

IDEAL cannot safely resume a dependent capability merely because a process restarted, an API reconnected, a database restored or a dashboard turned green. Recovery requires proof that the relevant identities, policies, evidence, ledgers, external state, audit history and control interlocks are trustworthy and reconciled.

**Reconciliation is a domain-owned comparison between independently sourced state representations. Recovery is a gated process that re-establishes trust and continuity. Neither is a generic “sync” operation.**

There is no universal source of truth across all domains. Authority depends on the fact being reconciled:
- local intent and policy decisions are authoritative within IDEAL's own authority boundary;
- exchange acceptance, fills and venue positions require authoritative venue evidence and independent reconciliation;
- bank-posted transaction and account data are external observations, while IDEAL's personal-finance journal remains the accounting record after controlled posting;
- IRD assessments are authoritative for assessed tax balances, while IDEAL calculations remain estimates/workpapers;
- raw market observations are source evidence, while canonical market state is a versioned reconstruction;
- security identity/policy trust and owner approval are distinct from operational health.

## 2. Reconciliation domains and authority boundaries

| Reconciliation type | Compared state | Authoritative evidence | IDEAL-owned state | Key limitation |
|---|---|---|---|---|
| Market feed continuity | Snapshot, deltas, trades, sequence/cursor and reconstructed book | Source messages, sequence/checksum and documented provider semantics | Raw archive, gap ledger, reconstructed canonical view | A later backfill does not prove original stream continuity |
| Instrument metadata | Contract size, tick/lot, settlement, margin tier, funding schedule and effective dates | Venue/provider effective-dated specification and version | Canonical metadata registry and prior versions | Current metadata cannot be applied silently to historical decisions |
| Orders and fills | Intent, submitted order, venue order, executions, cancel/replace and fees | Venue order/trade history, sequence/event IDs and explicit response semantics | Intent, exact action digest, outbox, order ledger and reservation | Lost acknowledgement means UNKNOWN, not rejected |
| Positions and balances | IDEAL position/account view versus venue account/position snapshot | Venue account state, trades, transfers, funding, fees and collateral evidence | Internal ledger, risk snapshot and reconciliation record | Venue view may lag; do not blindly overwrite internal state |
| Funding and settlement | Expected versus actual funding/fees/settlement | Venue settlement records and account ledger events | Funding/fee accrual and event journal | Mark/mid fallback is not settlement truth |
| Personal-finance import | Provider/statement rows versus imported observations and journal | Original statement/provider record and its documented cursor/correction semantics | Source observation registry, reconciliation case and double-entry journal | Missing row is not deletion without explicit source semantics |
| Personal-finance balance | Provider-reported balance versus journal-derived balance | Bank's reported balance snapshot plus statement coverage | Journal balance and reconciliation difference | Provider balance may be stale or include pending/uncleared items |
| Tax account | IDEAL estimate/workpaper versus IRD assessed account/return status | IRD assessment/acknowledgement and official account record | Tax classification, rule version, workpaper and estimate | A filed return or browser redirect is not an assessment/payment confirmation |
| Audit integrity | Local ordered events, checkpoints and external witnesses | Independent checkpoint/witness where configured | Append-only local event history and hash chain | A local hash chain is not independently trustworthy if attacker controls all keys/storage |
| Backup/restore | Restored data/configuration versus trusted source and current external state | Independent backup manifest, checksums, key/revocation anchors and external records | Restored copy in quarantine and reconciliation evidence | Backup restores data, not active authority |
| Identity/policy | Runtime identities, policy digest, key status and authority generation | Independent owner/root trust and current revocation state | Versioned policy registry and identity inventory | A valid signature on a revoked/old key does not establish current authority |
| Health/security | Expected components, controls and telemetry versus observed evidence | Independent probes, host/network evidence and incident control plane | Health/security status and interlock records | Self-reported HEALTHY or same-host process separation is insufficient |

## 3. Reconciliation lifecycle

Each reconciliation case has an immutable identity, scope and evidence set. Proposed states:

1. **REQUESTED** — a defined source pair/object/time range needs comparison.
2. **COLLECTING** — gather source snapshots, event ranges, cursors and local records.
3. **VALIDATING** — verify identity, schema, coverage, freshness, ordering and evidence integrity.
4. **COMPARING** — compute deterministic differences under a versioned matching policy.
5. **MATCHED** — all required fields/records agree within explicitly defined tolerances and timing semantics.
6. **MATCHED_WITH_TIMING_DIFFERENCE** — explained lag or pending/posted timing difference exists; no unsupported equivalence is asserted.
7. **MISMATCH** — material difference exists and requires disposition.
8. **UNKNOWN** — required source/evidence is unavailable, ambiguous or untrusted.
9. **QUARANTINED** — suspected corruption, tampering, duplicate side effect, account compromise or unresolved integrity incident.
10. **RESOLVED** — a documented correction/reconciliation action has been independently verified.
11. **CLOSED** — evidence, disposition, approvals and downstream state updates are complete.

No automatic transition from MISMATCH/UNKNOWN/QUARANTINED to MATCHED based solely on retry, timeout or process restart.

Each case records:
- source identities and their authority for the specific fact;
- source and local snapshot IDs, cursors, sequence ranges and timestamps;
- coverage window and known gaps;
- matching/correction ruleset version;
- exact differences and tolerances;
- confidence/quality state;
- proposed and applied correction;
- actor/approver, reason and owner-reserved action if any;
- before/after digests and audit correlation;
- downstream consumers invalidated/recomputed;
- unresolved residuals and release decision.

## 4. Mismatch handling rules

- Preserve both sides before changing either side.
- Never “last write wins” across independent financial or security records.
- Never overwrite raw source evidence to make a reconciliation pass.
- Corrections are explicit new events/revisions with source links and reason codes.
- Idempotency keys prevent duplicate application but do not prove semantic correctness.
- Matching heuristics may propose a candidate; they must not silently create an irreversible accounting or external financial side effect.
- A tolerance must be named, justified and versioned (currency rounding, timestamp lag, fee precision, provider pagination, etc.).
- A mismatch must identify its affected dependency blast radius.
- A corrected record invalidates dependent projections, risk decisions, tax calculations and research datasets as specified by lineage.
- Unknown external order/position state retains conservative exposure and reservation; no blind retry or timeout release.
- Unreconciled personal-finance transactions remain staged/unposted or explicitly marked as an exception; no silent deletion or forced categorisation.
- A tax estimate mismatch does not lock capital; IRD assessment evidence and the estimate remain distinct.
- Reconciliation does not grant authority to move money, trade, cancel, flatten, file or pay.

## 5. Trading and derivatives reconciliation

For any future separately approved execution capability:
- Persist canonical intent, action digest, owner/security authority, risk approval/reservation, audit and outbox before dispatch.
- Persist DISPATCH_STARTED and consume one-use admission before the network write.
- Use stable client order IDs and venue event/trade IDs; idempotent processing is required.
- Treat order acknowledgement, acceptance, fill, partial fill, rejection, cancel request, cancel confirmation, amend and expiry as distinct facts.
- Reconcile working, conditional, protective and reduce-only orders, including their potential exposure and cancellation state.
- Transfer filled quantity from order reservation to position exposure exactly once; keep residual quantity reserved until terminal reconciliation.
- Reconcile positions, wallet/collateral, realised/unrealised P&L, fees, funding, rebates, liquidation/ADL and transfers by currency and account scope.
- Do not assume venue snapshots are atomically consistent with every event stream; preserve sequence/cursor and snapshot time.
- If venue and IDEAL disagree, enter account-specific RECONCILIATION_HOLD; block dependent risk increases and preserve the more conservative plausible exposure until evidence resolves it.
- If a request may have reached the venue but no definitive acknowledgement exists, mark UNKNOWN and reconcile by client ID, venue history and account state. No exactly-once external execution claim.

## 6. Personal-finance and tax reconciliation

### Personal finance

- Original bank statement/provider rows are source observations, not journal postings.
- Import idempotency must support provider IDs and content/revision hashes; changed content under the same ID creates a revision case.
- Pending-to-posted, reversals, returns, deletions, pagination overlap, cursor resets, duplicate rows, transfer pairs and FX amounts require explicit handling.
- Balance reconciliation compares source snapshot timestamp and coverage with the journal's posted transactions plus known pending items; a difference is not automatically a missing transaction.
- Transfers are paired as two legs; they do not create income/expense or net-worth changes except fees/FX differences.
- Unmatched records remain visible and do not silently disappear.
- Bank token revocation/inactive status invalidates future retrieval but does not erase historical journal entries. Data retention/deletion follows the source contract and applicable policy.

### Tax

- Estimated tax, reviewed workpaper, filed return, IRD acknowledgement, assessment, account balance and confirmed payment are separate states.
- Only official IRD evidence confirms assessed balances/filing status; only bank/IRD evidence confirms payment.
- A changed source event, tax classification or rule version triggers a new calculation and a traceable difference, not silent mutation of prior workpapers.
- Filing/payment remain owner-approved and are not enabled by this architecture.
- D-018 prohibits technical lock/segregation or forced tax payment based on estimated liability.

## 7. Incident containment and recovery lifecycle

Proposed system-wide recovery states:

- **NORMAL** — all required trust, evidence, reconciliation and controls are current.
- **DEGRADED** — a known limitation exists; only unaffected, explicitly permitted capabilities continue.
- **RESTRICTED** — scoped risk-increasing or sensitive actions are disabled.
- **INCIDENT_HOLD** — compromise, tampering, material mismatch or unknown external state; preserve evidence and isolate.
- **RECOVERY_QUARANTINE** — restored/rebuilt components and data are not trusted for consequential use.
- **RECONCILIATION_REQUIRED** — local and external state must be compared and resolved.
- **ATTESTATION_REQUIRED** — independent pillar evidence and policy/identity checks are pending.
- **OWNER_RELEASE_REQUIRED** — all technical gates pass but owner-reserved approval is required.
- **NORMAL** only after the complete release conditions are met.

### Recovery sequence

1. **Detect and classify** — record symptoms, scope, confidence, severity and affected dependencies.
2. **Restrict and contain** — stop affected risk-increasing capabilities; preserve ability for explicitly authorised read-only investigation. Do not automatically cancel/flatten/transfer.
3. **Preserve evidence** — snapshot relevant logs, source observations, policy/key versions, host state and external identifiers; avoid destructive cleanup.
4. **Establish trust root** — use an independent owner/recovery root and current revocation/high-water state. If compromised, do not trust local state alone.
5. **Eradicate and rebuild** — clean environment, verified code/configuration/artifacts, least-privilege identities, rotated compromised secrets and patched vulnerabilities.
6. **Restore into quarantine** — restore data and audit history, but do not restore old permissions, credentials or active admission tokens.
7. **Verify integrity** — hashes, signatures, schemas, event ordering, backup lineage, key status, policy digest and audit checkpoints.
8. **Reconcile external reality** — venue orders/positions/balances, bank/provider status, tax/filing/payment records and source-feed gaps as applicable.
9. **Recompute dependent state** — derived records, valuations, risk calculations, portfolio projections, tax workpapers and dataset manifests using corrected evidence.
10. **Independent attestations** — Security, Data Integrity, System Health and Risk each attest only to their own scope with evidence and limitations.
11. **Owner release** — owner approval for reserved actions, policy reactivation or any authority restoration required by D-023.
12. **Monitored return** — limited scope, heightened monitoring, explicit rollback and incident review.

A successful process start, passing health probe, restored database or valid backup digest is insufficient to return to NORMAL.

## 8. Pillar-specific attestations and authority

| Pillar | May attest to | Cannot attest to |
|---|---|---|
| Security | Identity/key/policy integrity, containment, vulnerability disposition, host trust evidence and revocation state | Financial safety, correct positions, tax correctness or overall system health |
| Data Integrity | Source provenance, sequence/completeness, revision lineage, dataset reproducibility and fitness evidence | Source honesty beyond available corroboration, financial risk acceptance or security clearance |
| System Health | Component/dependency availability, telemetry continuity, storage/backup status and interlock functioning | Security uncompromise, financial approval, policy validity or external account truth |
| Risk | Exposure, sizing, loss/stress, margin/collateral and reservation state under its policy/evidence | Security permission, source truth, health status or owner consent |
| Owner | Scope, policy, authority activation/release and reserved decisions | Technical proof in place of independent evidence |

Attestations must be scoped, versioned, time-bounded and independently attributable. A single “all green” bit is prohibited as the sole recovery evidence.

## 9. Backup, restore and audit continuity

- Backups are encrypted, integrity-checked, versioned and tested; backup credentials/keys are separate from application credentials.
- At least one recovery path should be isolated from the primary failure domain where threat and cost justify it; exact technology remains undecided.
- Restore drills verify data, metadata, keys, schema migrations, audit continuity, retention/deletion, permissions quarantine and external reconciliation.
- Restored authority generations, tokens, envelopes and admission permits are invalidated or revalidated against an independent current revocation anchor.
- Local hash chains/checkpoints detect some tampering but cannot prove integrity if attacker controls all local storage and checkpoint keys.
- External witnesses/checkpoints are optional candidates; their privacy, cost, availability and independence must be evaluated.
- Audit events are minimised and classified. Secrets, raw tokens and unnecessary personal/financial payloads are excluded.
- Append-only evidence does not override retention, deletion, licence or privacy obligations. Tombstones/redaction/cryptographic erasure must be designed across backups, replicas, caches and derived data.
- Retention expiry must not silently delete evidence needed for a live incident/legal hold; legal holds must themselves be authorised, scoped and auditable.

## 10. Failure propagation and capability matrix

| Failure | Market research | Future execution | Personal finance | Tax intelligence | Portfolio view |
|---|---|---|---|---|---|
| One venue feed outage | Affected symbols/features degraded | Block dependent new risk | Continue | Continue | Mark affected valuation stale |
| Venue account/order unknown | Research may continue | Account-specific hold | Continue | Continue | Mark derivative projection unknown |
| Bank provider outage | Continue | Continue unless approved portfolio policy explicitly depends on bank cash | Stale source status; journal remains accessible | Continue with stated cash-data limits | Partial/incomplete |
| Tax rule ambiguity | Continue | No automatic trading restriction from estimate | Continue | Mark estimate uncertain/review required | Show uncertainty, not forced reserve |
| Local AI outage | Deterministic research/data/risk continue where possible | No impact on authority; no model action | Manual functions continue | Deterministic calculations continue | Read-only projections continue |
| Health supervisor failure | Affected dependent actions restricted | No new risk where required supervision missing | Read-only/manual availability per declared dependency | Read-only/manual availability per declared dependency | Show degraded trust status |
| Security/root compromise | Isolate affected trust zone | Disable affected authority and dispatch | Protect private data; isolate affected access | Protect taxpayer data | Do not present compromised projection as trusted |
| Audit store unavailable | Research may be limited by evidence requirements | Block actions requiring durable pre-dispatch audit | No unrecorded financial posting if audit is mandatory | No unrecorded filing/payment workflow | Show audit degradation |

This matrix is provisional. Each context must declare its own criticality, dependency and fallback; a global failure must not be inferred from one service's status.

## 11. Required verification

Future tests include:
- reconciliation case state-machine invariants and invalid transitions;
- source disagreement, partial snapshots, stale cursors and delayed events;
- duplicate/out-of-order/late corrections and replay idempotency;
- order dispatch crash points, lost acknowledgement, late venue acceptance and partial fills;
- bank row correction/deletion/pending/transfer reconciliation;
- tax estimate versus IRD assessment and payment evidence;
- restored pre-revocation snapshot cannot resurrect authority;
- backup restore with missing keys, corrupted audit tail or outdated schema remains quarantined;
- independent attestation cannot certify another pillar;
- supervisor and security control-plane common-mode failure;
- incident containment cannot initiate financial side effects;
- recovery release with one missing/expired attestation remains blocked;
- cross-domain blast-radius and unaffected-domain continuity;
- retention/deletion across primary, replicas, caches, logs, backups and derived datasets.

These are proposed tests, not executed results.

## 12. Open decisions and residual risks

- Physical independence of health/security watchdog and recovery root depends on eventual host topology.
- External audit witness/checkpoint and retention periods remain undecided.
- Reconciliation cadence, source priority and tolerance must be defined per provider/venue/domain.
- Manual owner recovery and device-loss procedure remains to be designed and tested.
- The system cannot recall a request already transmitted to an external venue.
- Host root/kernel compromise defeats same-host process separation.
- External providers can be unavailable, delayed, inconsistent or change semantics.
- Legal/contractual deletion may conflict with evidential retention; the policy must resolve this per data class and jurisdiction.
- No finite test set proves all vulnerabilities or every external-state transition correct.

## 13. Disposition and next work

The technology-neutral reconciliation and recovery lifecycle is specified at design level. It does not select a database, backup provider, watchdog topology, external witness, bank/venue provider, runtime or incident-response tool.

Next: run an integrated adversarial consistency review across the domain map, temporal evidence, domain risk/capital, autonomy authority, four pillars and reconciliation/recovery. Close cross-document contradictions, produce a consolidated owner-decision register and map every material invariant to future tests. Phase 02 remains active; Phases 03–19 locked. No implementation or external action is authorised.
