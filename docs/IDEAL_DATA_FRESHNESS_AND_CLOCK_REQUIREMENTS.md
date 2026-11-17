# IDEAL Data Freshness, Clock Quality and Decision-Validity Requirements

**Status:** Phase 02 source/consumer contract; thresholds intentionally unselected  
**Checkpoint:** 091 — 17 November 2026  
**Scope:** Source-specific freshness, availability, clock uncertainty, decision validity and data-age measurement  
**Authority:** D-019, D-020, D-021, D-022, D-023  
**Boundary:** Design only. No feed, venue, bank provider, clock service, runtime monitor or threshold is selected or implemented.

## 1. Core rule

Freshness is not one system-wide number. A record is fit only if it is fresh enough for the consumer's purpose, decision horizon, source cadence, volatility/liquidity conditions and error tolerance.

A timestamp can be recent but wrong; a record can be valid but late; a feed can be connected but stale; a historical record can be correct but unavailable at the simulated decision time. IDEAL must measure these dimensions separately.

**No global TTL, global HEALTHY flag or “latest row” shortcut is acceptable.** Every consumer declares a versioned freshness/clock fitness contract.

## 2. Time dimensions and measured age

For each observation, preserve where available:
- source event time;
- source publication/availability time;
- source sequence/cursor;
- local receive time;
- durable ingest/commit time;
- processing time;
- decision-as-of time;
- source and local clock quality/uncertainty.

Derived measurements:
- **Source-to-receive latency:** received_at − source_published_time (or event time where publication time is unavailable, clearly labelled proxy).
- **Ingest latency:** ingested_at − received_at.
- **Processing latency:** processed_at − ingested_at.
- **Decision age:** decision_as_of − source_published_time/availability time.
- **Event age:** decision_as_of − source_event_time.
- **Sequence gap:** expected source sequence/cursor continuity versus observed.
- **Clock offset/uncertainty:** measured offset and error bound against trusted time source.

Never substitute event age for availability age. Never claim source-to-receive latency if only event time is known. If source publication/availability time is absent, mark point-in-time fidelity as limited.

## 3. Consumer freshness contract

Each consumer must declare:
1. Required source(s) and source priority.
2. Data type and expected cadence/update frequency.
3. Required timestamp semantics and source sequence/cursor.
4. Maximum acceptable decision age and event age.
5. Allowed clock offset/uncertainty.
6. Required completeness/coverage and gap policy.
7. Required quality dimensions and cross-source corroboration.
8. Behaviour when degraded, stale, late, conflicted or unavailable.
9. Whether historical use remains valid after correction.
10. Evidence required to restore validity after an outage.

Thresholds must be derived from measured source behaviour and consumer tolerance, not selected because a provider advertises a refresh interval. They must be versioned, reviewed and tested. A threshold change is a policy change where it affects risk or authority and follows owner approval.

## 4. Source-specific freshness requirements

| Data type | Required freshness/clock evidence | Staleness or uncertainty behaviour |
|---|---|---|
| L2 order-book snapshots/deltas | Exchange event time, local receive time, channel sequence/update ID, snapshot sequence, checksum where available, inter-update gaps, book age distribution | Gap/checksum/reset mismatch invalidates reconstructed state until authoritative resnapshot and reconciliation; never interpolate missing depth |
| Trades | Exchange event time, receive time, trade ID/sequence, duplicate/out-of-order and event-to-book alignment | Preserve late/out-of-order events; do not infer exact event order from equal timestamps alone |
| Candles/OHLCV | Bar open/close boundaries, timezone, completion status, source publication time, missing intervals and corrections | Partial bar cannot be treated as completed; missing bars remain gaps unless an explicit consumer-specific method handles them |
| Funding rates/events | Funding interval, scheduled/actual settlement time, rate publication time, settlement currency, source revision | Forecast funding is not realised funding; late corrections create revisions |
| Mark/index/basis | Price type, event/publication time, source and cross-source divergence | Divergence or stale mark/index invalidates dependent risk/liquidation calculations |
| Instrument/contract metadata | Version, effective-from/to, publication time, retrieval time, contract multiplier/tick/lot/margin rules | Metadata must be effective-dated; unknown changes invalidate dependent calculations |
| Account/positions/orders | Venue snapshot time, event cursor, client/venue IDs, reconciliation sequence, pending/unknown status | Unknown or stale state blocks dependent risk increases; retain conservative reservations |
| FX rates | Source, rate side, currency pair, timestamp, spread/haircut and conversion method | Missing/stale FX produces partial/unknown aggregate; never zero-fill |
| Bank account/transactions | Provider refresh time, statement coverage, pending/posted status, provider cursor, correction/deletion semantics | Provider snapshot is not real-time available cash; mark stale when outside contract/consumer threshold |
| Tax rules and assessments | Publication, enactment, commencement, effective date, tax year, source authority/status and retrieval time | Proposed/non-binding material cannot be treated as enacted/binding; old calculations retain original rule version |
| Health/security telemetry | Probe interval, receive/commit time, sequence, source independence, heartbeat age and clock quality | Missing/late/unverifiable critical heartbeat asserts scoped UNKNOWN/RESTRICTED state |
| AI/model outputs | Model/version, dataset manifest, generation time, retrieval snapshot, tool provenance and expiry | Output is advisory; stale context cannot be presented as current evidence or grant authority |

## 5. Market-data freshness methodology

For each feed/instrument/channel/day and relevant market regime, measure:
- expected versus observed message/update cadence;
- median, p90, p95, p99 and maximum source-to-receive and inter-update gaps;
- missing/out-of-order/duplicate/late sequence counts;
- snapshot/reset frequency and time to valid reconstruction;
- book age at every derived feature/decision;
- time-of-day and volatility/liquidity-conditioned distributions;
- receive-to-durable-ingest and processing latency;
- cross-source divergence where independent references exist.

Do not rely on average latency alone. Tail distributions and clustered outages matter. A 10 ms median does not make a 500 ms maximum harmless if a decision can occur during the tail.

For the current historical OKX sample, the accepted conditional research disposition and measured age tails are documented in HISTORICAL_L2_SAMPLE_VALIDATION.md. Those findings support bounded historical market-structure research only; they do not prove FIFO queue position, exact event order, passive fills or execution-grade freshness.

## 6. Clock architecture and uncertainty

Logical requirements:
- Store UTC instants with source precision and original timezone/offset where relevant.
- Use a trusted wall-clock source for correlation, expiry and external event comparison.
- Use monotonic clocks for local elapsed-time/deadline measurement; do not compare monotonic values across reboot or machines without a defined mapping.
- Record clock source, sync status, measured offset, uncertainty and last successful sync.
- Detect wall-clock rollback/jump, leap-second handling differences, virtual-machine clock drift and suspend/resume effects.
- Never use a local timestamp as proof of venue event ordering.
- Source sequence IDs and durable local transaction order remain distinct from wall-clock chronology.
- If the clock's uncertainty interval overlaps an expiry boundary or exceeds the consumer's permitted uncertainty, deny time-dependent admission.
- If time sync is unavailable, retain historical evidence but mark current freshness/expiry decisions UNKNOWN where they depend on trusted time.

NTP is a likely baseline for ordinary host synchronization; PTP may be evaluated only if a measured workload requires tighter precision. Neither protocol, daemon nor provider is selected. Time synchronization is not a security trust root: a compromised host can falsify its local clock.

## 7. Decision validity and invalidation

A risk decision, strategy eligibility result, valuation or portfolio projection has an explicit validity interval and invalidation triggers.

A consequential risk decision expires at the earliest of:
- its explicit decision expiry;
- any bound source freshness threshold;
- policy/envelope/identity/security generation change;
- risk policy or reservation change;
- account/position/order reconciliation change;
- instrument/contract metadata change;
- relevant health/security interlock change;
- material source correction or quality downgrade;
- clock uncertainty breach.

The action boundary must re-evaluate all invalidation-sensitive versions immediately before dispatch. A cached “approved” result is not a reusable permission.

For research, a historical result may remain reproducible under its original as-known-then evidence even when the latest source record is revised. A current projection must disclose whether it uses latest-corrected or original data.

## 8. Freshness state model

Suggested consumer-facing states:
- CURRENT — within all declared thresholds and required evidence present.
- AGING — within threshold but nearing expiry; warning only.
- STALE — threshold exceeded; dependent use restricted.
- INCOMPLETE — coverage or sequence missing.
- LATE — received after expected availability; point-in-time eligibility may fail.
- CONFLICTED — source disagreement exceeds tolerance.
- CLOCK_UNCERTAIN — time validity cannot be established.
- UNKNOWN — required evidence/clock status unavailable.
- QUARANTINED — integrity/security/licence incident.

These states are separate from operational service health. A live connection can carry STALE data; an offline historical archive can be valid for a past as-of query.

## 9. Initial consumer profiles — relative, not numeric

| Consumer | Freshness posture | Degradation allowed? |
|---|---|---|
| Long-horizon macro/regime research | Completed bars and effective-dated macro facts; delayed data may be acceptable if declared | Yes, with source age and missing coverage disclosed |
| Intraday strategy research | Completed/partial bars distinguished; availability-time and sequence fidelity required | Only if the experiment explicitly models the limitation |
| L2 market-structure research | Message cadence, sequence, snapshot continuity, book age tails and event alignment required | Conditional descriptive research only; not execution calibration if required sequence/fill evidence is absent |
| Backtest/validation | Point-in-time availability cutoff and immutable dataset manifest | No silent leakage; limited-fidelity label if original availability time is absent |
| Future execution/risk increase | Current account/position/market/contract/FX evidence within approved consumer thresholds | No critical stale/unknown data; fail closed |
| Personal-finance dashboard | Provider refresh timestamp and statement coverage shown | Partial/stale view allowed if visibly labelled; never claim real-time available cash |
| Tax estimate | Effective-dated rule pack and source authority status | Uncertain estimates may be shown with review flags; no capital restriction |
| Recovery/release | Current identity/revocation, audit, external reconciliation and scoped attestations | No degraded release for critical trust conditions |

## 10. Required verification

Future tests:
- source clock skew, drift, rollback, suspend/resume and VM clock discontinuity;
- event time versus publication/availability time distinction;
- delayed, duplicated, reordered, missing and late-corrected source events;
- sequence gap/checksum failure and resnapshot recovery;
- candle completion and missing interval handling;
- funding forecast versus settlement;
- mark/index divergence and stale metadata;
- bank refresh age, cursor reset and provider correction;
- stale FX and partial portfolio totals;
- time-bound permit expiring during admission/dispatch race;
- source correction invalidating only dependent current calculations;
- NTP/PTP loss or host clock compromise remains UNKNOWN;
- per-consumer thresholds versioned and changed only through approved policy process.

No clock/freshness runtime tests have been performed.

## 11. Open decisions

- Source-specific SLAs, update cadence and availability-time guarantees.
- Numerical age thresholds by consumer/instrument/timeframe.
- Clock offset/uncertainty tolerance by action and data type.
- Time-sync provider/protocol and host clock assurance.
- Stale-tail treatment for L2 data and the historical OKX dataset.
- Bank provider freshness contract and acceptable dashboard age.
- FX source hierarchy and stale-rate fallback policy.
- Exact decision validity duration and invalidation rules by action class.

## 12. Disposition

Freshness and clock semantics are specified; numerical thresholds remain deliberately open until sources, host and consumer risk tolerance are known. No global TTL or source guarantee is assumed.

Phase 02 remains active; Phases 03–19 remain locked. No provider, feed, clock service, runtime monitor, threshold, implementation or execution is authorised.


## Asset identity in freshness and FX evidence — checkpoint 093

FX freshness is evaluated for an explicit canonical AssetId pair, not an ambiguous ticker/currency string. For crypto-native tokens and stablecoins, the network/contract identity and effective-dated provider mapping are part of the source contract. Price/FX freshness does not establish peg stability or asset equivalence. See [Critical Contract Field Schemas](IDEAL_CRITICAL_CONTRACT_FIELD_SCHEMAS.md).


## Funding schedule and mark-method revisions — checkpoint 110

Funding schedules are source data, not a global eight-hour timer. Retain effective-dated interval, next settlement time, cap/floor, publication time, observed settlement time and source revision. Forecast funding remains distinct from realised settlement. Mark-price observations must bind to the applicable effective-dated methodology/configuration revision; stale or missing revision invalidates dependent liquidation-risk decisions. See [Perpetual Funding and Mark-Price Semantics Source Refresh](IDEAL_PHASE_02_PERPETUAL_FUNDING_AND_MARK_PRICE_SEMANTICS_REFRESH.md).


## Funding schedule and mark-method revisions — checkpoint 110

Funding schedules are source data, not a global eight-hour timer. Retain effective-dated interval, next settlement time, cap/floor, publication time, observed settlement time and source revision. Forecast funding remains distinct from realised settlement. Mark-price observations must bind to the applicable effective-dated methodology/configuration revision; stale or missing revision invalidates dependent liquidation-risk decisions. See [Perpetual Funding and Mark-Price Semantics Source Refresh](IDEAL_PHASE_02_PERPETUAL_FUNDING_AND_MARK_PRICE_SEMANTICS_REFRESH.md).
