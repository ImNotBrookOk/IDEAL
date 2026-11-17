# IDEAL Canonical Contract Catalogue

**Status:** Phase 02 logical interface contracts; provisional, no wire schema frozen  
**Checkpoint:** 085 — 17 November 2026  
**Scope:** Cross-domain and cross-pillar contract ownership, semantics, failure behaviour, versioning and verification  
**Authority:** D-018, D-019, D-020, D-021, D-022, D-023  
**Boundary:** Design only. No API, database schema, message broker, serialization format, runtime integration or implementation is selected.

## 1. Contract design rules

1. Each contract has one authoritative producer/owner. Consumers cannot write into another context's canonical state.
2. Every consequential record is attributable, versioned and traceable to its evidence and policy context.
3. Data semantics are stable even if the eventual transport/schema changes.
4. Missing, stale, conflicting, revoked or unverifiable inputs remain explicit; no zero/default/last-write-wins fallback may create false confidence.
5. External side effects use exact-action binding, idempotency and reconciliation. Local ACID does not extend to remote providers.
6. Contract versions are immutable once published. Breaking semantic changes require a new version and migration/replay plan.
7. Unknown critical fields or incompatible semantics fail closed at authority/risk boundaries; harmless additive display fields may be ignored only under an explicit compatibility policy.
8. Each consumer declares a fitness contract: required fields, freshness, provenance, precision, confidence and permissible degradation.
9. Every contract has a negative test for missing, malformed, stale, replayed, cross-scope and unauthorised data.
10. No single generic event bus or universal schema is assumed.

## 2. Shared event envelope — logical semantics

Where a domain event is required, the common envelope should carry the following semantic fields. Exact names, types and encoding are not selected.

| Field | Meaning | Requirement |
|---|---|---|
| Event identity | Globally unique event identifier within the chosen system | Required for deduplication and audit |
| Contract/schema version | Exact semantic version | Required; incompatible version denied |
| Event type | Domain-owned event kind | Namespaced by owning context |
| Owner context | Canonical state owner | Required; prevents ambiguous ownership |
| Aggregate/entity identity | Domain object identity | Required for entity-level ordering |
| Aggregate version | Monotonic version within owner boundary | Required for stale-write detection |
| Source event time | Time asserted by source | Required where source event has time |
| Available/published time | When information became knowable | Required for point-in-time use where applicable |
| Recorded/received time | When IDEAL received/committed it | Required for audit and late-arrival detection |
| Durable sequence | Local event/transaction order | Required where ordered state transitions matter |
| Actor/principal | Human, service or provider actor | Required for consequential changes |
| Correlation/causation | Related workflow and parent event references | Required for multi-step traces |
| Idempotency reference | Stable duplicate-prevention key | Required for retriable operations |
| Evidence references | Source snapshots, hashes, documents or upstream event IDs | Required for derived/decision records |
| Policy/authority reference | Applicable policy/envelope/identity generation | Required for privileged actions |
| Sensitivity/retention class | C0–C3 and retention policy | Required for protected data |
| Payload reference | Inline or external payload location | Exact storage mechanism deferred |

The envelope is not a replacement for domain-specific payload semantics or the action version vector.

## 3. Canonical contract catalogue

| Contract ID | Owner / producer | Primary consumers | Required semantics | Failure response |
|---|---|---|---|---|
| CT-01 Source Observation | Source Registry / adapter | Data Integrity, archive | Source identity, raw payload reference/digest, event/publication/receive time, cursor/sequence, schema, licence/entitlement, correction identity | Quarantine invalid/unlicensed data; mark gap/stale/unknown |
| CT-02 Validation Result | Data Integrity | Canonical Evidence, consumers | Validator/ruleset version, findings, quality vector, disposition, evidence references | Fail validation or mark degraded; downstream cannot relabel |
| CT-03 Canonical Evidence | Data Integrity / domain owner | Market Intelligence, Risk, Finance, Tax | Canonical ID/revision, units/currency, valid/known time, lineage, freshness, confidence, source references | Preserve prior revision; mark conflicted/unknown |
| CT-04 Derived Record | Owning domain | Research, portfolio, tax, reporting | Input revisions, transformation/code version, parameters, output digest, created time, quality inheritance | Invalidate/recompute affected current projections; preserve history |
| CT-05 Point-in-Time Dataset | Dataset Registry | Backtest, ML research, model registry | Immutable manifest, availability cutoff, exact revisions, calendar/schema/licence, exclusions, label maturity, digest | Reject leakage/incomplete/unauthorised dataset |
| CT-06 Domain Projection | Owning bounded context | Portfolio View, UI | Read-only projection, source version, currency/units, ownership, valuation basis/time, completeness and quality | Display partial/unknown; no cross-context write |
| CT-07 Strategy Candidate | Strategy Research | Validation/registry | Hypothesis, code/config digest, universe, time horizon, features, constraints, lineage | Untrusted proposal; cannot access authority or execution |
| CT-08 Validation Result / Promotion Evidence | Backtest & Validation | Strategy Registry, owner review | OOS/walk-forward metrics, costs, assumptions, baseline, statistical uncertainty, limitations and reproducibility manifest | Candidate remains unvalidated; no self-promotion |
| CT-09 Risk Evaluation | Risk Authority | Action Boundary, portfolio diagnostics | Exact action digest, domain/account/instrument, capital basis, exposure snapshot, policy/evidence versions, reason codes, validity and outcome | DENIED/INDETERMINATE; no admission |
| CT-10 Risk Reservation | Risk Reservation Ledger | Action Boundary, reconciliation | Reservation ID, capacity/quantity, action digest, lifecycle state, partial-fill transfer, release evidence | Retain conservative exposure on UNKNOWN |
| CT-11 Health Interlock | Health Supervisor | Action Boundary / operations | Scope, dependency, reason, state, generation, evidence, expiry and clearance criteria | Restrict affected capabilities; never grant authority |
| CT-12 Security Authorisation | Security/Policy Enforcement | Action Boundary, sensitive data stores | Principal, action/resource scope, identity/key/policy versions, decision, reason, expiry | Default deny; quarantine on unverifiable identity |
| CT-13 Owner Grant / Policy Artefact | Owner ceremony + Policy Registry | Security, Action Boundary | Exact digest, scope, capabilities, hard limits, reserved actions, expiry, revocation generation, owner and publisher evidence | Non-active/invalid/revoked grant denied |
| CT-14 Action Intent / Admission Permit | Action Boundary | Risk, adapter, audit | Exact canonical action, idempotency, actor, authority vector, evidence, reservation, one-use permit, expiry | Reject stale/mutated/replayed permit |
| CT-15 Dispatch Receipt / Outcome | Narrow adapter + reconciliation | Action Ledger, Risk, Audit | Client/venue IDs, dispatch time, response, fills, errors, source sequence, UNKNOWN state | Preserve UNKNOWN; reconcile before retry/release |
| CT-16 Reconciliation Case | Owning domain | Risk, finance, tax, audit, health | Sources compared, coverage/cursors, differences, matching policy, disposition, correction, approvals | MISMATCH/UNKNOWN/QUARANTINED; no blind overwrite |
| CT-17 Personal-Finance Import | Personal Finance | Reconciliation, journal | Original provider/statement row, provider ID/revision, pending/posted/deleted status, amount/currency, dates, cursor, source refresh | Stage only; journal posting requires reconciliation |
| CT-18 Journal Posting / Reversal | Personal Finance | Portfolio, Tax, Audit | Debit/credit accounts, currency/amount, source evidence, posting/reversal link, accounting date and version | Reject unbalanced/duplicate/unattributed posting |
| CT-19 Tax Assessment / Workpaper | Tax Intelligence | Personal Finance, owner | Jurisdiction/tax year, facts, rule source/status/version, calculation, assumptions, confidence, reviewer and assessment/payment evidence refs | Mark uncertain; no forced reserve or payment |
| CT-20 Dataset/Model Release | Model Registry + owner release authority | Research/assistant workflows | Model/code digest, dataset manifest, evaluation/OOS evidence, licence/privacy eligibility, known limits, rollback and monitoring | No promotion; prior release remains |
| CT-21 Audit Event | Each owning context; audit store orders | Security, health, owner review | Actor/action/target, prior/new version, reason, evidence, sequence, correlation, sensitivity/retention | Block consequential side effect if required local commit fails |
| CT-22 Recovery Attestation | Security/Data/Health/Risk scoped authorities | Recovery controller, owner | Attesting pillar, scope, evidence, version, limitations, expiry and signer | Missing/stale/contradictory attestation keeps quarantine |

## 4. Shared value semantics

The following meanings are required independent of eventual serialization:
- **Asset amount (fiat and crypto-denominated):** exact amount bound to a canonical AssetId, precision/scale and rounding context, source, account/owner and valuation time. Fiat uses ISO 4217 where applicable; crypto-native assets and tokens require a canonical identity and versioned venue/provider-symbol mapping, including network and contract address where applicable. Stablecoins are distinct assets and are not assumed to equal USD or be interchangeable. Never use binary floating-point as authoritative amount representation.
- **Quantity:** unit, contract multiplier, precision/lot step and instrument specification version.
- **Price:** instrument plus canonical base, quote and settlement AssetIds, price type (last/mark/index/bid/ask/mid), source and timestamp. Conversion/valuation is an explicit evidence-bearing operation with source, side, time, spread/haircut and completeness; missing or stale conversion remains UNKNOWN/PARTIAL rather than zero.
- **Time:** event, publication/availability, receive, durable ingest, processing, valid/known, decision-as-of and clock quality remain distinct.
- **Identity:** principal, owner context, account/legal entity and scope are explicit; display names are not stable identifiers.
- **Status:** PENDING, POSTED, SETTLED, REVERSED, CANCEL_REQUESTED, CANCELLED, UNKNOWN and similar statuses are not interchangeable.
- **Confidence/quality:** quality is a vector and consumer fitness decision, not a single global confidence percentage.
- **Valuation:** native amount plus conversion method, FX side/source/time/spread/haircut and completeness.
- **Policy:** version/digest and authority generation are bound; policy text alone is not permission.
- **Evidence:** reference/digest and provenance do not by themselves prove source truth.

## 5. Error and denial semantics

A future implementation should preserve a typed reason taxonomy at the logical level:

| Result | Meaning | Default behaviour |
|---|---|---|
| INVALID | Malformed or semantically invalid input | Reject; no side effect |
| UNAUTHORISED | Identity or policy denies request | Deny and audit |
| OUT_OF_SCOPE | Outside owner envelope/domain/account/action | Deny and audit |
| EXPIRED | Evidence, permit, policy or credential past validity | Deny/re-evaluate |
| REVOKED | Grant, identity, key or policy revoked | Deny; invalidate dependent permits |
| STALE | Required evidence older than consumer threshold | Restrict affected action |
| INCOMPLETE | Required coverage/fields missing | Mark partial; deny if critical |
| CONFLICTED | Sources disagree materially | Quarantine or require reconciliation |
| UNKNOWN | State cannot be established | Fail closed for consequential action |
| UNAVAILABLE | Required service/source not reachable | Restrict dependent capability |
| QUARANTINED | Suspected compromise/corruption/licence breach | No consequential use until cleared |
| CONFLICT | Version/optimistic concurrency/idempotency mismatch | Reject; fetch/reconcile current state |
| DUPLICATE | Same idempotency key and same digest already processed | Return existing outcome |
| IDEMPOTENCY_MISMATCH | Same key with different action digest | Reject and security-audit |

Exact code names and wire format remain open.

## 6. Contract versioning and compatibility

- Each contract has an owner, semantic version, schema reference, compatibility policy and deprecation window.
- Additive fields may be backward-compatible only if consumers can safely ignore them and the field does not alter authority/risk semantics.
- Changes to units, timestamps, ownership, rounding, default values, status meaning, risk interpretation or permission scope are breaking semantic changes.
- Security, risk, authority and money fields fail closed on unknown/incompatible semantics.
- Every published contract version has immutable examples and positive/negative tests.
- Historical records retain the version used at creation; migrations create new versions/events and preserve lineage.
- No central schema registry or broker is selected.

## 7. Transaction and ownership boundaries

- Internal domain writes occur only through the owning context.
- Cross-domain read models consume versioned projections; no direct shared-table mutation.
- A single ACID store may be used initially with schema/module ownership if selected later.
- Risk reservation and local action intent/audit/outbox share the required local transaction boundary.
- Dispatch-start and its audit event share the final local transaction immediately before network write.
- External provider/venue state is reconciled asynchronously; no distributed ACID or exactly-once remote guarantee.
- Personal-finance journal posting is an owner-domain transaction; a bank import is not a posting.
- Tax estimate changes are not financial side effects and cannot lock capital under D-018.

## 8. Required contract verification

Before implementation:
- schema/semantic validation and version compatibility;
- unit/currency/precision and timezone boundary tests;
- duplicate, replay, stale, unknown and cross-scope negative tests;
- producer/consumer forbidden-write tests;
- correction/revision and as-known-then replay;
- risk approval invalidation on action/evidence/policy change;
- reservation concurrency and partial-fill lifecycle;
- interlock scope and restrictive-only permission tests;
- journal double-entry and duplicate-import tests;
- tax estimate/assessment/payment separation;
- audit durability failure before dispatch;
- restore, deletion, revocation and recovery-attestation tests.

No contract runtime tests have been run.

## 9. Open decisions

- Exact serialization/canonicalisation and schema technology.
- Whether an envelope is shared across all event families or generated per context.
- Exact monetary/quantity/time data types and rounding policy.
- Contract registry location and version compatibility tooling.
- Error code naming and transport mapping.
- Which internal events require durable audit and which may be ephemeral.
- Whether the modular monolith uses one database with schemas or a single schema with ownership conventions.
- Which contract families are needed in the initial active research domain versus future proposals.

## 10. Disposition

This catalogue defines semantic ownership and interface expectations, not a final API or schema. It is sufficient for a cross-document architecture review but remains provisional until owner acceptance and platform-specific design.

Phase 02 remains active; Phases 03–19 remain locked. No implementation, schema, database, broker, API, credentials, external integration, paper/live execution or phase advancement is authorised.


## Freshness and clock contract reference — checkpoint 091

CT-01/02/03/05/09/14 require source event/publication/availability/receive/ingest times, sequence/cursor, clock quality and consumer fitness rules where relevant. Freshness thresholds are per consumer and versioned; they are not a shared global TTL. Decision validity is invalidated by bound source age, clock uncertainty, correction, account or policy state change.

See [Data Freshness, Clock Quality and Decision-Validity Requirements](IDEAL_DATA_FRESHNESS_AND_CLOCK_REQUIREMENTS.md).


## Field-level logical schemas — checkpoint 091

Critical contract field semantics are expanded in [IDEAL Critical Contract Field Schemas](IDEAL_CRITICAL_CONTRACT_FIELD_SCHEMAS.md), including common evidence references, owner envelopes, security authorisation, health interlocks, risk decisions/reservations, action intents/permits, dispatch receipts, reconciliation cases, personal-finance imports/journal postings, tax workpapers, audit events and recovery attestations.

The schemas define logical types and constraints only; no serialization, database or API format is selected.


### 4.1 Canonical asset identity requirement — checkpoint 089

Asset identity is not a display ticker or ISO currency string. The logical AssetId must distinguish fiat, native crypto assets and network/contract-specific tokens, with effective-dated mappings from provider/venue symbols. The eventual identifier and registry schema remain open. Instrument multiplier, tick/lot precision and settlement denomination are separate effective-dated instrument metadata. All derived conversions preserve source, side, timestamp, spread/haircut and quality; no stablecoin peg or FX rate is assumed.
