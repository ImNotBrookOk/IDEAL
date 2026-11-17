# IDEAL Critical Contract Field Schemas

**Status:** Phase 02 technology-neutral logical schemas; provisional  
**Checkpoint:** 092 — 17 November 2026  
**Scope:** Field-level semantics and constraints for critical cross-domain/pillar contracts  
**Authority:** D-018, D-019, D-020, D-021, D-022, D-023  
**Boundary:** Logical schema only. No JSON Schema, protobuf, SQL DDL, API, broker, serializer or runtime is selected.

## 1. Type conventions

| Logical type | Meaning / constraint |
|---|---|
| ID | Opaque stable identifier; not a display name or sequential public identifier |
| Version | Monotonic integer or immutable version token scoped to its owner |
| Digest | Algorithm identifier plus digest value; canonicalisation rules must be versioned |
| Decimal | Exact decimal/fixed-point value; never binary floating-point for authoritative money/quantity |
| AssetAmount | Decimal + canonical AssetId + precision/scale + rounding context + valuation metadata where converted |
| AssetId | Canonical fiat or crypto asset identity; fiat may map to ISO 4217, crypto-native/token identity includes network and contract address where applicable, with effective-dated provider/venue symbol mappings |
| Quantity | Decimal plus unit, precision and contract multiplier/specification version |
| Price | Decimal plus instrument, price type, canonical quote AssetId, source and timestamp |
| Instant | UTC instant plus source precision and original offset/timezone when relevant |
| Duration | Explicit unit and value; no ambiguous bare integer |
| Enum | Closed set for a contract version; unknown security/risk states fail closed |
| EvidenceRef | Opaque reference to immutable source/derived evidence, digest, revision and access classification |
| PrincipalRef | Human/service/provider identity plus issuer, audience and scope |
| Scope | Explicit domain, account/legal owner, venue, instrument, action/resource and environment dimensions |
| ReasonCode | Stable machine-readable code plus human-readable explanation |
| SignatureRef | Key identity, algorithm, signed digest, signing time and trust metadata; never raw private key |

Common rules:
- Every contract has contract ID/version, owner context and sensitivity/retention class.
- All timestamps declare what event they represent; a field named simply timestamp is prohibited in critical contracts. All monetary/asset amounts bind to AssetId; ISO 4217 is used for fiat identity only.
- Amounts carry canonical AssetId, unit, account/owner and valuation basis; fiat ISO 4217 codes are one AssetId family, not a universal amount type.
- Missing values are explicit absent/unknown states, not zero or empty-string defaults.
- Unknown enum values are rejected at authority/risk boundaries.
- Optional fields cannot silently change a default permission, risk limit or accounting meaning.

## 2. Common evidence reference

| Field | Type | Required | Semantics |
|---|---|---:|---|
| evidence_id | ID | Yes | Stable evidence object |
| evidence_type | Enum | Yes | Source observation, canonical record, derived record, dataset, document or external state |
| source_id | ID | Yes | Source/provider identity |
| source_revision | Version/ID | Yes | Exact source revision used |
| raw_digest | Digest | Where raw bytes exist | Integrity reference to captured bytes |
| source_event_time | Instant | If source event is timed | Time asserted by source |
| source_available_time | Instant | If known | Time source made evidence available |
| received_at | Instant | Yes | IDEAL receive time |
| ingested_at | Instant | Once committed | Durable commit time |
| sequence_or_cursor | ID/Decimal | If source supports | Source continuity position |
| quality_state | Enum | Yes | VALID/DEGRADED/STALE/INCOMPLETE/CONFLICTED/REVISED/UNVERIFIED/QUARANTINED/UNKNOWN |
| lineage_refs | EvidenceRef[] | For derived data | Exact upstream dependencies |
| licence_policy_ref | ID/Version | Where licensed | Rights/retention/training policy |
| classification | Enum | Yes | C0/C1/C2/C3 |
| retention_policy_ref | ID/Version | Yes | Retention and deletion rule |

## 3. Owner envelope / policy artefact

| Field | Type | Required | Semantics |
|---|---|---:|---|
| envelope_id | ID | Yes | Stable grant identity |
| envelope_version | Version | Yes | Monotonic immutable version |
| canonical_digest | Digest | Yes | Exact canonical artefact |
| owner_principal | PrincipalRef | Yes | Owner identity |
| environment | Enum | Yes | Research/test/paper/live labels; paper/live remain unapproved until separately authorised |
| domain_scope | Enum[] | Yes | Explicitly approved domains only |
| account_scope | Scope[] | Yes | Legal owner/account and venue references |
| instrument_scope | Scope[] | Where applicable | Explicit instrument/universe constraints |
| permitted_action_classes | Enum[] | Yes | Positive allowlist |
| prohibited_action_classes | Enum[] | Yes | Explicit denylist/reserved actions |
| operating_mode | Enum | Yes | Capability mode |
| hard_limits | Structured limit set | Yes | AssetId, units, aggregation basis, conversion source and scope explicit |
| maximum_permissions | Structured scope | Yes | Upper bound; no inferred permissions |
| stop_conditions | Structured predicates | Yes | Deterministic trigger and safe-state mapping |
| starts_at / expires_at | Instant | Yes | Validity window |
| revocation_generation | Version | Yes | Current monotonic authority generation |
| owner_approval_ref | EvidenceRef | Yes | Exact owner ceremony evidence |
| publisher_signature_ref | SignatureRef | Yes | Separate policy publisher role |
| status | Enum | Yes | DRAFT/VALIDATED/OWNER_APPROVED/SIGNED/PUBLISHED/ACTIVE/SUPERSEDED/REVOKED |

Constraints:
- The envelope is an upper bound, not an instruction to use all capacity.
- Scope expansion and hard-limit changes require fresh owner approval.
- A valid historical signature does not override revocation, expiry or rollback.
- AI/strategy workloads cannot write this contract.

## 4. Security authorisation decision

| Field | Type | Required | Semantics |
|---|---|---:|---|
| decision_id | ID | Yes | Unique decision |
| principal | PrincipalRef | Yes | Authenticated actor/workload |
| action_class | Enum | Yes | Requested operation |
| resource_scope | Scope | Yes | Exact target/account/instrument |
| policy_id/version/digest | ID/Version/Digest | Yes | Evaluated policy |
| identity_generation | Version | Yes | Current identity/revocation generation |
| security_incident_generation | Version | Yes | Current incident state |
| result | Enum | Yes | ALLOW/DENY/INDETERMINATE |
| reason_codes | ReasonCode[] | Yes | Explanation |
| evidence_refs | EvidenceRef[] | Yes | Auth and policy evidence |
| decided_at / expires_at | Instant | Yes | Decision time and expiry |
| decision_digest | Digest | Yes | Immutable decision evidence |

Security ALLOW is not financial risk approval or owner consent.

## 5. Health interlock

| Field | Type | Required | Semantics |
|---|---|---:|---|
| interlock_id | ID | Yes | Stable interlock |
| supervisor_principal | PrincipalRef | Yes | Authenticated supervisor |
| affected_scope | Scope | Yes | Domain/dependency/action scope |
| state | Enum | Yes | CLEAR/DEGRADED/RESTRICTED/UNKNOWN |
| reason_codes | ReasonCode[] | Yes | Trigger |
| evidence_refs | EvidenceRef[] | Yes | Independent probes/telemetry |
| interlock_generation | Version | Yes | Monotonic scoped generation |
| issued_at / expires_at | Instant | Yes | Freshness/expiry |
| clearance_criteria | Structured predicates | Yes | Independent evidence needed to clear |
| signature_ref | SignatureRef | Yes | Supervisor message authentication |

A health interlock can restrict only. It cannot issue credentials, grant permissions, approve risk, or initiate financial actions. Critical interlocks cannot be self-cleared by the supervisor.

## 6. Risk evaluation

| Field | Type | Required | Semantics |
|---|---|---:|---|
| risk_decision_id | ID | Yes | Unique evaluation |
| action_digest | Digest | Yes | Exact proposed action |
| domain/account/instrument_scope | Scope | Yes | Risk perimeter |
| risk_policy_version | Version | Yes | Policy used |
| capital_measure | Enum | Yes | Named basis: economic equity, risk-adjusted equity, venue margin equity etc. |
| capital_value | AssetAmount | Yes | Value and valuation basis/time; conversion is explicit and evidence-bearing |
| exposure_snapshot_ref | EvidenceRef | Yes | Positions, orders, liabilities and reservations |
| market_evidence_refs | EvidenceRef[] | Yes | Prices, liquidity, funding, FX and metadata |
| data_quality_vector | Structured vector | Yes | Freshness, completeness, conflict, clock, source |
| stress_results | Structured metrics | Yes | Scenario loss/exposure and assumptions |
| result | Enum | Yes | APPROVED/DENIED/INDETERMINATE |
| reason_codes | ReasonCode[] | Yes | Deterministic explanation |
| valid_until | Instant | Yes | Earliest expiry among required inputs/policy |
| invalidation_versions | Version vector | Yes | Bound authority, identity, data, account, metadata and interlocks |
| reservation_request | Structured amount/quantity | If approved | Required potential exposure hold |
| audit_ref | EvidenceRef | Yes | Decision audit event |

Risk APPROVED does not grant security permission or owner authority.

## 7. Risk reservation

| Field | Type | Required | Semantics |
|---|---|---:|---|
| reservation_id | ID | Yes | Stable reservation |
| action_digest | Digest | Yes | Exact action |
| account/instrument_scope | Scope | Yes | Exposure perimeter |
| reserved_quantity | Quantity | If quantity-based | Remaining potential fill |
| reserved_margin/capital | AssetAmount | If capital-based | Explicit risk capacity and collateral asset identity |
| state | Enum | Yes | NONE/HELD/IN_FLIGHT/PARTIALLY_FILLED/TERMINAL_PENDING_RECONCILIATION/RELEASED/INCIDENT_HOLD |
| filled_quantity | Quantity | Yes | Filled portion transferred exactly once |
| residual_quantity | Quantity | Yes | Still reserved |
| created_at/updated_at | Instant | Yes | Event times |
| reconciliation_ref | EvidenceRef | On terminal transition | Proof for release |
| version | Version | Yes | Optimistic concurrency |

Cancellation request, timeout, restart or unknown acknowledgement cannot release residual reservation.

## 8. Action intent and admission permit

### ActionIntent

| Field | Type | Required | Semantics |
|---|---|---:|---|
| action_id | ID | Yes | Unique action intent |
| action_digest | Digest | Yes | Canonical exact payload |
| principal | PrincipalRef | Yes | Requesting workload |
| domain/action_class | Enum | Yes | Requested capability |
| account/instrument_scope | Scope | Yes | Exact scope |
| parameters | Typed structured object | Yes | Price/size/side/order type/etc. with units |
| idempotency_key | ID | Yes | Stable retry key |
| envelope_ref | EvidenceRef | Yes | Owner grant/version |
| security_decision_ref | EvidenceRef | Yes | Exact permission decision |
| risk_decision_ref | EvidenceRef | Yes | Exact risk result |
| reservation_ref | EvidenceRef | Yes | Durable reservation |
| data_evidence_refs | EvidenceRef[] | Yes | Decision snapshot |
| interlock_versions | Version[] | Yes | Current health/security interlocks |
| expires_at | Instant | Yes | Admission expiry |

### AdmissionPermit

| Field | Type | Required | Semantics |
|---|---|---:|---|
| permit_id | ID | Yes | One-use capability |
| action_digest | Digest | Yes | Exact action only |
| audience/adapter | ID | Yes | Only intended dispatcher |
| authority_generation | Version | Yes | Current owner authority generation |
| version_vector | Structured versions | Yes | All invalidation-sensitive state |
| nonce | ID | Yes | Unique one-use value |
| issued_at/expires_at | Instant | Yes | Narrow validity window |
| consumed_at | Instant | No | Set atomically at dispatch-start |
| status | Enum | Yes | ISSUED/CONSUMED/EXPIRED/REVOKED |

A permit cannot be reused, transferred to another action, or consumed under stale generation.

## 9. Dispatch receipt / external outcome

| Field | Type | Required | Semantics |
|---|---|---:|---|
| dispatch_id | ID | Yes | Local attempt |
| action_digest | Digest | Yes | Exact action |
| client_reference | ID | If venue supports | Stable client order/request ID |
| venue_reference | ID | When returned | Venue order/trade/event ID |
| dispatch_started_at | Instant | Yes | Local linearisation point |
| network_attempt_at | Instant | If known | Adapter write time |
| response_state | Enum | Yes | ACKNOWLEDGED/REJECTED/UNKNOWN/PARTIAL |
| fills | Structured quantity/price/fee[] | If any | Individual execution evidence |
| source_sequence | ID | If available | Venue event cursor |
| error/reason_codes | ReasonCode[] | Yes | Transport/venue status |
| reconciliation_ref | EvidenceRef | On resolution | Authoritative match |
| audit_ref | EvidenceRef | Yes | Local durable audit |

A network attempt is not proof of venue receipt. UNKNOWN remains unresolved until reconciliation.

## 10. Reconciliation case

| Field | Type | Required | Semantics |
|---|---|---:|---|
| case_id | ID | Yes | Stable case |
| domain/object_scope | Scope | Yes | Object and coverage |
| source_refs | EvidenceRef[] | Yes | All compared sides |
| coverage_window | Structured time/sequence range | Yes | What is/was checked |
| matching_policy_version | Version | Yes | Deterministic comparison rules |
| differences | Structured difference[] | Yes | Exact mismatches/tolerances |
| state | Enum | Yes | REQUESTED/COLLECTING/VALIDATING/COMPARING/MATCHED/MATCHED_WITH_TIMING_DIFFERENCE/MISMATCH/UNKNOWN/QUARANTINED/RESOLVED/CLOSED |
| proposed_correction | Structured object | If needed | Never overwrite source evidence |
| approval_ref | EvidenceRef | If owner-reserved | Explicit authority |
| resolution_evidence | EvidenceRef[] | On resolved | Before/after and external proof |
| downstream_invalidations | ID[] | Yes | Affected projections/decisions |
| opened_at/closed_at | Instant | Yes | Lifecycle |

## 11. Personal-finance import and journal posting

### PersonalFinanceImport

| Field | Type | Required | Semantics |
|---|---|---:|---|
| import_id | ID | Yes | Local observation ID |
| provider_id | ID | If available | Provider row/account reference |
| provider_revision | ID/Version | If available | Provider update/correction marker |
| raw_evidence_ref | EvidenceRef | Yes | Original statement/API row |
| transaction_status | Enum | Yes | PENDING/POSTED/REVERSED/DELETED/UNKNOWN |
| amount/asset_id | AssetAmount | Yes | Native amount bound to canonical AssetId; fiat uses ISO 4217 mapping |
| initiated/authorised/posted/value_date | Instant/Date | Where available | Distinct source dates |
| source_refresh_time | Instant | Yes | Provider snapshot time |
| cursor/page | ID | If supported | Pagination/replay state |
| reconciliation_state | Enum | Yes | STAGED/MATCHED/MISMATCH/UNKNOWN/POSTED |

Import does not create a journal posting automatically.

### JournalPosting

| Field | Type | Required | Semantics |
|---|---|---:|---|
| posting_id | ID | Yes | Stable journal transaction |
| posting_date | Date | Yes | Accounting date |
| lines | Debit/Credit[] | Yes | Each line carries canonical AssetId; balancing is per asset/functional-currency policy with explicit conversion entries |
| source_import_refs | EvidenceRef[] | Yes | Source observations |
| reconciliation_ref | EvidenceRef | Yes | Matched case |
| correction_of | ID | If correcting | Original posting reference |
| reversal_of | ID | If reversing | Original posting reference |
| asset_amount/FX_refs | Structured | Where applicable | Native AssetId and evidenced conversion; no stablecoin peg assumption |
| status | Enum | Yes | DRAFT/POSTED/REVERSED |

## 12. Tax workpaper / assessment

| Field | Type | Required | Semantics |
|---|---|---:|---|
| workpaper_id | ID | Yes | Stable calculation |
| jurisdiction/tax_year | Enum/Date range | Yes | Legal context |
| taxpayer_scope | Scope | Yes | Owner/account/asset scope |
| source_facts | EvidenceRef[] | Yes | Transaction and ownership evidence |
| asset/instrument_classification | Structured | Yes | Instrument-specific classification and confidence |
| rule_source/status/version | EvidenceRef/Enum/Version | Yes | Act/ruling/guidance/bill status and effective date |
| method/assumptions | Structured | Yes | Reproducible calculation inputs |
| fx/rounding_refs | EvidenceRef[] | Where applicable | Source and policy |
| result/uncertainty | AssetAmount / structured | Yes | Estimate with confidence/limitations and explicit tax reporting asset denomination |
| reviewer_ref | EvidenceRef | If reviewed | Human/adviser review |
| assessment_ref | EvidenceRef | If assessed | Official IRD evidence |
| payment_ref | EvidenceRef | If paid | Bank/IRD confirmation |
| capital_restriction | Enum | Must be absent/false | D-018: no software-imposed lock or forced payment |

## 13. Audit event

| Field | Type | Required | Semantics |
|---|---|---:|---|
| audit_event_id | ID | Yes | Stable event |
| durable_sequence | Version | Yes | Local order |
| event_type/owner_context | Enum/ID | Yes | Namespaced domain event |
| actor | PrincipalRef | Yes | Human/service/provider |
| target_ref | ID | Yes | Opaque object reference |
| action/reason | Enum/ReasonCode | Yes | What and why |
| prior_digest/new_digest | Digest | Where state changes | Before/after integrity reference |
| evidence_refs | EvidenceRef[] | Yes | Supporting proof |
| policy/authority_refs | EvidenceRef[] | For privileged actions | Exact approval context |
| correlation/causation | ID | Yes | Workflow linkage |
| sensitivity/retention | Enum/ID | Yes | C0–C3 and policy |
| redaction/tombstone_state | Enum | Yes | Deletion/privacy status |

No secrets, raw credentials or unnecessary private payloads are stored in the audit event.

## 14. Recovery attestation

| Field | Type | Required | Semantics |
|---|---|---:|---|
| attestation_id | ID | Yes | Stable attestation |
| pillar | Enum | Yes | SECURITY/DATA_INTEGRITY/HEALTH/RISK |
| attesting_principal | PrincipalRef | Yes | Independent scoped authority |
| affected_scope | Scope | Yes | Domain/component/data/account |
| evidence_refs | EvidenceRef[] | Yes | Tests, probes, reconciliation, audit |
| version_vector | Structured versions | Yes | Current policy/identity/data/account/interlock versions |
| limitations | Text/ReasonCode[] | Yes | What was not verified |
| result | Enum | Yes | PASS/FAIL/INDETERMINATE |
| issued_at/expires_at | Instant | Yes | Time-bounded validity |
| signature_ref | SignatureRef | Yes | Attribution/integrity |

Each pillar attests only to its own domain. Missing/stale/contradictory critical attestation blocks recovery release.

## 15. Cross-contract invariants

- ActionIntent, SecurityAuthorization, RiskEvaluation, Reservation, AdmissionPermit and DispatchReceipt all bind the same canonical action digest.
- All required version-vector elements are checked at admission and again immediately before dispatch.
- Any material change invalidates the permit; no silent mutation.
- Risk reservation is durable before admission; dispatch-start and audit are atomic before network write.
- PersonalFinanceImport cannot become JournalPosting without reconciliation evidence.
- TaxWorkpaper cannot carry a capital restriction or payment command under D-018.
- DomainProjection is read-only; it cannot mutate the source journal or risk ledger.
- EvidenceRef must preserve source revision, availability time and quality state for point-in-time replay.
- RecoveryAttestation cannot be issued by a pillar about itself without independent evidence and cannot substitute for another pillar's attestation.
- Audit fields are minimised and classified; hash-only references are not assumed anonymous.

## 16. Open schema decisions

- Exact canonical serialization and digest algorithm/version.
- Exact field names and optional/required compatibility.
- Currency/asset code registry and decimal precision/rounding.
- Time precision, offset and timezone representation.
- Schema versioning/deprecation tooling.
- Whether some domain-specific contracts require additional subtypes.
- Storage representation and database constraints.
- Signature algorithms, key formats and trust metadata.

These decisions must be made only after platform research and owner approval. This document is technology-neutral.

## 17. Disposition

Critical contract field semantics are now specified to a reviewable level. They remain logical schemas, not deployable API/DB schemas. Phase 02 remains active; Phases 03–19 remain locked. No implementation, runtime, credentials, integrations, paper/live execution or phase advancement is authorised.

 
## 18. Margin, collateral and liquidation logical schemas — checkpoint 100

These are required logical field groups, not wire schemas or selected database tables. All monetary/asset quantities use canonical AssetId and exact decimal semantics from the existing denomination contract. All evidence is source-bound, time-bound, versioned and integrity-referenced.

| Record | Required logical fields | Safety semantics |
|---|---|---|
| CollateralAssetState | asset_id, account_scope, native_quantity, encumbrance, borrow/liability, custody/location, observed_at, source_ref | Native units preserved; no assumed transferability or stablecoin par |
| CollateralEligibilityRule | asset_id, venue/account_mode, eligible, initial_weight, maintenance_weight, concentration_tier, effective_from/to, source_ref, rule_digest | Separate IM/MM weights; effective-dated and fail closed if absent/stale |
| CollateralValuation | asset_id, quantity, price, quote_asset_id, price_type, source_ref, observed_at, age, haircut, valuation_amount, quality_state | Conservative side/rounding; stale/missing price cannot inflate capacity |
| FxConversionEvidence | from_asset_id, to_asset_id, rate, side, source_ref, observed_at, spread, haircut, quality_state | Conversion is explicit; no silent FX or peg assumption |
| InstrumentRiskTier | instrument_id, margin_mode, settlement_asset_id, notional_lower/upper, max_leverage, initial_rate, maintenance_rate, maintenance_deduction, effective_from/to, source_ref, rule_digest | Boundary continuity and exact account/product scope |
| AccountMarginSnapshot | venue/account_scope, margin_mode, settlement_asset_id, equity, available_margin, initial_margin, maintenance_margin, margin_ratio, observed_at, source_ref, quality_state | Venue-reported values kept distinct from local risk-adjusted equity |
| PositionRiskSnapshot | position_id, instrument_id, side, quantity, entry_price, mark_price, index_price, last_price, unrealised_pnl, tier_id, IM, MM, liquidation_estimate, observed_at, source_ref | Mark, index, last and executable prices remain distinct |
| OpenOrderRiskReservation | order_id, action_digest, remaining_quantity, worst_case_exposure, state, venue_order_state, reservation_ref | Unknown/cancel-pending orders retain conservative reservation |
| StressScenario / StressResult | scenario_id, version, shocks, basis/liquidity/collateral/funding/FX dimensions, result, worst_loss, evidence_refs | No hedge credit outside approved netting set; scenario provenance retained |
| LiquidationEvent | venue_event_id, account_scope, instrument_id, event_type, trigger_price_type, trigger_price, requested_quantity, filled_quantity, bankruptcy_price, fee, insurance/ADL status, observed_at, source_ref, reconciliation_ref | Venue report is evidence, not final state; reconcile fills and account |
| VenueRuleSet | venue, product, account_mode, instrument_scope, rules_version, effective_from/to, fetched_at, source_ref, content_digest, approval_ref | Rule changes invalidate decisions; no unversioned live defaults |

No wire format, database, numeric haircut or venue has been selected.


## Canonical serialization profile requirement — checkpoint 109

The logical Digest type remains incomplete until the byte-level canonical profile is approved. See [Canonical Serialization and Digest Contract Research](IDEAL_PHASE_02_CANONICAL_SERIALIZATION_AND_DIGEST_CONTRACT_RESEARCH.md). In particular, exact Decimal/Quantity/Price/AssetAmount values must not pass through unconstrained IEEE-754 JSON numbers. Any future JCS use requires canonical decimal strings and a strict application profile; deterministic CBOR also requires an IDEAL profile for tags, optionality and semantic encoding. No format selected.


## 19. Funding configuration and settlement evidence — checkpoint 110

| Logical record | Required fields | Invariant |
|---|---|---|
| FundingRuleSnapshot | venue, instrument_id, settlement_asset, contract_multiplier, funding_interval, next_funding_at, cap, floor, position_basis, effective_from/to, observed_at, source_ref, revision | Effective-dated; no global interval or cap assumption |
| MarkMethodSnapshot | venue, instrument_id, method_id/version, index_method/constituents, inputs, effective_from/to, observed_at, source_ref, revision | Every mark used for critical risk binds to its method revision |
| FundingEstimate | instrument_id, rate, estimated_signed_amount, settlement_asset, position_snapshot_ref, schedule_revision, observed_at, valid_until | Forecast only; cannot post to authoritative ledger |
| FundingSettlementEvent | venue_event_id, instrument_id, position_ref, signed_amount, settlement_asset, rate, basis, event_at, effective_at, received_at, source_ref, correction_of | Immutable/idempotent; correction is a linked event, never silent overwrite |

Amounts use exact signed decimal semantics and canonical AssetId; timestamps and revisions follow the approved canonical profile. The fields are logical only; no wire encoding or runtime is selected.


## 19. Funding configuration and settlement evidence — checkpoint 110

| Logical record | Required fields | Invariant |
|---|---|---|
| FundingRuleSnapshot | venue, instrument_id, settlement_asset, contract_multiplier, funding_interval, next_funding_at, cap, floor, position_basis, effective_from/to, observed_at, source_ref, revision | Effective-dated; no global interval or cap assumption |
| MarkMethodSnapshot | venue, instrument_id, method_id/version, index_method/constituents, inputs, effective_from/to, observed_at, source_ref, revision | Every mark used for critical risk binds to its method revision |
| FundingEstimate | instrument_id, rate, estimated_signed_amount, settlement_asset, position_snapshot_ref, schedule_revision, observed_at, valid_until | Forecast only; cannot post to authoritative ledger |
| FundingSettlementEvent | venue_event_id, instrument_id, position_ref, signed_amount, settlement_asset, rate, basis, event_at, effective_at, received_at, source_ref, correction_of | Immutable/idempotent; correction is a linked event, never silent overwrite |

Amounts use exact signed decimal semantics and canonical AssetId; timestamps and revisions follow the approved canonical profile. The fields are logical only; no wire encoding or runtime is selected.


## 20. Funding observation and historical coverage schema refinement — checkpoint 112

The checkpoint 110 records remain the base logical schema. This refinement prevents one overloaded rate/timestamp field from hiding venue event state.

| Logical record | Required fields | Invariant |
|---|---|---|
| FundingObservation | venue, instrument_id, formula_type, method_id, api_schema_revision, predicted_rate, realised_rate, assessed_rate, prior_settled_rate, funding_time, next_funding_time, min_rate, max_rate, settlement_state, premium, source_event_time, received_at, observed_at, source_ref, payload_digest | Predicted/realised/assessed/settled values are distinct; unknown enum or contradictory times invalidates dependent calculations |
| FundingHistoryCoverage | venue, instrument_id, dataset_type, first_event_at, last_event_at, retrieved_at, page_cursor_state, known_gaps, duplicate_count, correction_count, retention_limit, licence_ref, source_refs, completeness_state | A retrieval window is not proof of complete history; missing/expired history is UNKNOWN, never zero |
| MarkSeriesEvidence | venue, instrument_id, price_type, interval, first_event_at, last_event_at, observed_at, source_revision, known_gaps, payload_digest, source_ref, completeness_state | Mark candles and trade candles are distinct; incomplete series cannot silently stand in for point-in-time mark inputs |

FundingObservation fields are venue-normalised logical concepts, not a claim that every venue publishes every field. Missing fields remain explicitly absent/unknown; do not synthesise them. FundingHistoryCoverage records public API retention constraints and local permitted archive coverage separately. Linear/inverse PnL and funding amounts remain denomination-specific and use exact signed decimal values.
