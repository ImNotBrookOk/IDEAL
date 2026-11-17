# IDEAL Phase 02 — Final Integrated Architecture Challenge

**Status:** Internal integrated challenge; design-level findings only  
**Checkpoint:** 089 — 17 November 2026  
**Boundary:** No implementation, runtime tests, external security testing, provider/account access, credentials, paper/live execution, hosting, paid infrastructure or phase advancement.

## 1. Executive disposition

The architecture is substantially coherent at the technology-neutral design level. The major authority, data, risk, health, security, reconciliation and recovery boundaries are consistent across the canonical sources. The final challenge identified one material contract-semantic omission: the shared amount model referred to ISO currencies but did not define canonical identities for crypto-denominated assets such as BTC and USDT. That gap is corrected in the canonical contract catalogue and mapped to future deterministic tests.

This is not independent assurance, formal verification, legal/accounting advice or runtime evidence. Phase 02 remains active. Independent architecture/security/operations and maintainability review, disposition of findings, owner acceptance and separate implementation approval remain outstanding.

## 2. Integrated challenge findings

| ID | Severity | Area | Finding | Disposition |
|---|---|---|---|---|
| INT-089-01 | High | Money and asset identity | ISO 4217 alone cannot represent crypto-native assets, stablecoins or network-specific token identities. Ticker-only identifiers can conflate distinct assets. | Corrected at logical contract level in CT value semantics; exact registry/schema remains open. |
| INT-089-02 | Critical | Authority and dispatch | Revocation, policy activation and dispatch-start must serialize; local commit cannot make a remote exchange side effect atomic. | Consistent across authority, state-machine and contract sources. Keep UNKNOWN/in-flight after dispatch-start and reconcile; runtime proof absent. |
| INT-089-03 | Critical | Trust and containment | Same-host process isolation cannot resist host root/kernel compromise. | Explicitly bounded residual risk; host threat tier and separate trust-domain choice remain open. |
| INT-089-04 | High | Health versus security | Health is restrictive-only; security incident response can revoke identities/contain but cannot grant financial authority or initiate financial side effects. | Consistent. Physical failure-domain independence remains open. |
| INT-089-05 | High | Data and temporal evidence | Hashes prove byte identity, not source truth; publication/availability time and correction history may be unavailable from providers. | Semantics specified; provider-specific point-in-time fidelity, freshness thresholds and source rights remain open. |
| INT-089-06 | High | Capital and risk | Portfolio aggregation must not imply fungibility, netting, hedge credit or a single total when FX/ownership/valuation is incomplete. | Consistent with domain risk/capital architecture. D-006 denominator and D-008 flow/valuation semantics remain open. |
| INT-089-07 | High | Reconciliation and recovery | Restart, backup digest or local health success cannot prove external financial state or restore revoked authority. | Consistent; independent revocation anchor, worker inventory and owner recovery procedure remain open. |
| INT-089-08 | High | Privacy, retention and tax | Immutable evidence, deletion, legal holds, provider terms and NZ tax interpretation can conflict. | Policy boundaries specified, but exact retention periods, provider/legal review and derivatives tax advice remain open. |
| INT-089-09 | Medium | Document ownership | Overlapping summaries created drift risk. | Formalised by the canonical architecture document map; historical records retained. |
| INT-089-10 | High | Assurance | Planned test IDs and design matrices are not executed evidence; current integrated review is an internal desk review. | Open. Independent review and later deterministic verification are required. |

## 3. Contract correction — asset denomination

The canonical contract catalogue now requires an amount to bind to a canonical AssetId, not an ISO currency string alone.

Logical semantics:
- Fiat assets use ISO 4217 where applicable.
- Crypto-native assets and tokens use a canonical asset identity with a versioned mapping from venue/provider symbols; token identity includes network and contract address where applicable.
- Stablecoins remain distinct assets. No automatic 1:1 USD equivalence or interchangeability is assumed.
- An amount carries its asset identity, exact decimal/scale and precision/rounding context, source, account/owner and valuation time.
- A price binds an instrument plus canonical base, quote and settlement asset identities, price type, source and timestamp.
- Conversion/valuation is an explicit evidence-bearing operation with source, side, time, spread/haircut and completeness; missing or stale conversion remains UNKNOWN/PARTIAL rather than zero.
- Instrument multiplier, tick/lot precision and effective-dated specification remain separate from asset denomination.
- No binary floating-point value is authoritative for monetary/asset accounting.

This is a logical semantic correction only. No asset registry, identifier format, schema, database or serialization technology is selected.

### Required future verification

| Test ID | Expected result |
|---|---|
| T-ASSET-01 | Ticker-only or ambiguous asset identity is rejected for consequential accounting/risk use. |
| T-ASSET-02 | Fiat ISO 4217, native crypto assets and network/contract-specific tokens remain distinct. |
| T-ASSET-03 | Stablecoin valuation does not assume par; depeg, missing FX or stale evidence yields explicit valuation uncertainty. |
| T-ASSET-04 | Amount precision, rounding and lot/contract multiplier are deterministic; binary floating-point cannot become canonical state. |
| T-ASSET-05 | Historical venue-symbol mappings are effective-dated; later remapping cannot rewrite prior decisions. |
| T-ASSET-06 | Cross-domain ledger, portfolio and risk projections preserve asset identity and cannot double-count converted/native amounts. |

## 4. Cross-pillar invariants challenged

1. Owner authority, policy, identity, security incident, health, data quality, risk, reservation, action, reconciliation and recovery are separate state machines.
2. Admission is conjunctive; no green state in one pillar substitutes for another.
3. Every consequential action binds the exact action digest and current authority, policy, identity, risk, health/security, data, account/instrument, audit and clock evidence.
4. Revocation-first denies dispatch; dispatch-start-first remains potentially in flight and cannot be recalled locally.
5. Local intent, reservation, audit and outbox commit before dispatch; dispatch-start and its audit commit before network write.
6. Uncertain remote outcomes retain reservations until authoritative reconciliation; no timeout-based release or exactly-once claim.
7. Health interlocks restrict only their declared scope; security containment cannot grant financial authority or initiate financial side effects.
8. Restored data remains quarantined until current revocation, audit, identity, data, risk, health/security and external-state evidence are reconciled.
9. Cross-domain projections preserve ownership, asset denomination, valuation basis/time and completeness; no implicit netting or collateral portability.
10. D-018 keeps tax estimates informational and prevents software-imposed capital locks or forced payment.

## 5. Remaining blockers and residual risks

- D-006 equity denominator; D-008 UTC day-start, capital-flow, multi-currency and valuation semantics.
- Owner authenticator, root/recovery custody, device-loss path and independent revocation anchor.
- Host-root/kernel threat tier, physical action-gateway placement and independent watchdog failure domain.
- Worker inventory completeness and measurable revocation propagation objective.
- Transactional store, single-writer/consistency model, WAL/fsync durability and restore semantics.
- Exact canonical encoding, asset registry, contract schema/version representation and error-code mapping.
- Source-specific point-in-time guarantees, freshness thresholds, licences, retention and cross-vendor comparison.
- Audit retention classes/durations, legal holds, deletion propagation and optional independent witness.
- NZ derivatives tax classification and provider/processor legal review.
- Independent architecture, security/operations and maintainability/testability review.
- Explicit owner acceptance of the full Phase 02 baseline.

These are not silently resolved by the contract correction or this challenge.

## 6. Evidence limitations

- No application code was executed or changed.
- No runtime, integration, contract, security, recovery or performance tests were run.
- No external penetration test or host inspection was performed.
- No live provider terms, legal interpretations or external source URLs were revalidated in this checkpoint.
- The document map's local links were checked manually on the current GitHub main tree; this was not a complete automated Markdown link crawl.
- Independent review is not complete; this report is an internal challenge.

## 7. Disposition and next gate

The logical asset-denomination contract gap is corrected and traceable. The other findings are either consistent design invariants or explicitly open platform/owner/assurance decisions.

Next: obtain independent read-only reviews across (a) architecture simplicity and maintainability, (b) security and operations, and (c) maintainability and testability; reconcile their evidence-backed findings without weakening controls. Only after independent review and finding disposition should the grouped owner decision pack be finalised. Phase 02 remains active; Phases 03–19 remain locked.
