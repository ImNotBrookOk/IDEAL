# IDEAL Risk Architecture Reconciliation and Assurance Matrix

**Status:** Phase 02 working reconciliation; owner approval pending  
**Date:** 17 November 2026  
**Scope:** Active crypto-perpetual research domain; cross-foundation architecture  
**Authority:** Research and documentation only. No implementation, runtime integration, exchange/account access, paper/live execution, credentials, dependency adoption, paid infrastructure or phase advancement is authorised.

> This document consolidates the nine risk-research tranches and challenges their fit with IDEAL's four foundational pillars. It is a proposed architecture synthesis, not a frozen API contract or accepted change to numerical policy.

## 1. Executive conclusion

The research supports an independent, deterministic risk authority integrated with, but not owned by, strategy, execution, data, health or AI components. Risk evaluates financial exposure against approved policy. It is not the source of truth for market/account observations, the identity provider, the health monitor, or the execution mechanism.

The coherent control chain is:

1. **Security** establishes who or what is requesting an action and the permissions it holds.
2. **Data integrity** establishes whether observations and account-state evidence are valid, complete, fresh and traceable for the intended use.
3. **System health** establishes whether relevant dependencies and controls operate within declared contracts.
4. **Risk** evaluates the exact proposed action against approved policy, portfolio state, existing exposure and reservations.
5. **An authorised adapter** may perform only the exact action covered by a current approval.
6. **Reconciliation and audit** establish what actually happened and preserve attributable evidence.

A strategy, model or AI agent may propose an action but cannot approve itself, change risk policy, create permissions, release reservations, certify its own evidence or bypass an interlock.

The four foundations are mutually reinforcing but not interchangeable. Green health is not proof of security; a valid signature is not proof that data is true; valid data does not imply an action is within risk limits; risk approval does not prove an external venue executed the action.

## 2. Reconciled architecture and responsibility boundaries

| Capability | Owns | Must not own |
|---|---|---|
| Security | Principal identity, authentication, authorisation, permission scope, key lifecycle, policy-write protection, security incidents | Financial risk appetite, market truth, trade approval |
| Data integrity | Source registry, provenance, timestamps, schema/semantic validation, quality/freshness states, correction lineage, reconciliation evidence | Financial limits, security permissions, health certification |
| System health | Independent observation, dependency status, watchdogs, alerting, scoped restrictive interlocks, recovery evidence | Risk policy changes, trade approval, identity grants, financial actions |
| Risk authority | Approved risk-policy interpretation, exposure aggregation, decisions, reservations, restrictions, risk-state transitions | Authentication, source truth, component self-health, execution, its own independent assurance |
| Strategy/research/model | Candidate proposals, forecasts, backtests, model outputs, experiment manifests | Risk approval, policy mutation, execution permissions |
| Execution adapter (future only) | Translate an exact authorised decision into a bounded external/simulated action; report acknowledgements and fills | Broaden approval, change size/price/scope, override risk |
| Audit/evidence | Durable, attributable, ordered evidence and integrity verification | Policy decisions or certifying the truth of every upstream observation |

### 2.1 Authority hierarchy

Proposed hierarchy, subject to owner acceptance:

1. Owner-approved system scope and policy.
2. Security-enforced principal and permission scope.
3. Independent health/data validity interlocks.
4. Portfolio-level risk constraints.
5. Instrument/risk-cluster/strategy-family allocations.
6. Strategy and per-trade risk budgets.
7. Order-level reservations.
8. Venue rules and technical constraints as additional restrictions, never as a substitute for IDEAL policy.

Every applicable constraint must be satisfied. Venue margin capacity, leverage setting or liquidation price is never IDEAL risk approval.

### 2.2 Four-pillar separation

- **Risk ↔ data:** risk consumes evidence only with declared quality, provenance and freshness. Data integrity owns acceptance/quarantine and correction semantics. Risk may reject evidence as unsuitable but cannot rewrite source history or certify its own inputs.
- **Risk ↔ health:** health may apply a predeclared restrictive interlock to affected activities. It cannot raise limits, approve trades or initiate a financial action. Risk-increasing actions fail closed when a mandatory control dependency is unavailable.
- **Risk ↔ security:** security authenticates and authorises the caller and protects policy integrity. Risk evaluates financial permission under policy. A valid identity is not risk approval; a risk approval cannot grant identity permissions.
- **Risk ↔ execution:** the decision is exact-action-bound and short-lived. The adapter cannot alter the payload or treat a timeout/cancel request as a confirmed outcome. Reconciliation is required after action.
- **Health ↔ security:** security telemetry informs health, but security assurance remains a distinct status with separate evidence and incident handling.
- **Data ↔ security:** cryptographic integrity/provenance can support tamper detection but cannot establish that an external source's original claim was truthful.

## 3. Canonical risk control lifecycle — proposed, not frozen

1. **PROPOSED:** a strategy/research component submits an action proposal; no authority is implied.
2. **AUTHENTICATED:** security verifies principal, scope and permission to request this class of evaluation.
3. **EVIDENCE_VALIDATED:** data and account-state evidence satisfy consumer-specific identity, completeness, freshness, reconciliation and lineage requirements.
4. **HEALTH_ELIGIBLE:** mandatory dependencies and interlocks are acceptable for this action.
5. **EVALUATED:** deterministic risk calculation checks policy, current exposure, working-order reservations, stressed loss, margin/collateral and portfolio constraints.
6. **REJECTED / RESTRICTED / APPROVED:** decision is recorded with reason codes and exact payload/evidence/policy versions. Approval is not transferable to a changed action.
7. **RESERVED:** capacity is atomically reserved before the action can become executable. Concurrency cannot allow individually valid requests to exceed a shared limit.
8. **SUBMITTED / ACKNOWLEDGED / PARTIALLY_FILLED / FILLED / CANCEL_PENDING / CANCELLED / UNKNOWN:** adapter and venue lifecycle states are distinct. Unknown state retains conservative exposure/reservation until reconciled.
9. **RECONCILED:** actual orders, fills, fees, funding, positions and balances are compared with authoritative evidence.
10. **CLOSED / EXPIRED / REVOKED:** approval and reservation lifecycle closes only on confirmed terminal conditions or an explicitly defined safe-release process.

Critical semantics:
- A cancel request is not a cancellation confirmation.
- A timeout is not proof that an action did not occur.
- Partial fills move filled quantity into position exposure exactly once; unfilled residual remains reserved.
- Duplicate/replayed requests must be idempotent.
- A changed action, policy, instrument rule, material evidence state or expired approval requires re-evaluation.
- Risk decision and reservation must be transactionally consistent. If the system cannot prove this, it must not permit the action.
- No generic automatic flatten rule is assumed. Stop-new-risk, cancel risk-increasing orders, bounded risk reduction, flatten, credential revocation and manual intervention are separate incident actions.

## 4. Risk measurement model

### 4.1 Capital and equity semantics

Keep these measures separate:

- **Economic equity:** net economic value of explicitly included assets and liabilities, with valuation sources and timestamps.
- **Risk-adjusted equity:** conservative risk capital after approved collateral haircuts, liabilities, valuation uncertainty and deductions.
- **Venue margin equity:** exchange/account-mode-specific margin measure.
- **Available margin:** amount a venue currently reports as available for additional margin requirements.

These are not synonyms. Available margin is neither wealth nor a sufficient risk budget. Multi-currency values require explicit conversion source, timestamp, haircut and uncertainty. Cross-venue aggregation may measure economic exposure but must not imply margin netting or collateral transferability.

**Unresolved owner decision:** D-006's phrase “equity” has no canonical denominator. Research recommends evaluating risk-adjusted equity, not venue available margin or the largest displayed venue balance. This is not accepted policy. D-008 separately specifies UTC day-start equity including realised and unrealised P&L; capital-flow, conversion, valuation and clock semantics still require definition without changing the accepted 10% figure.

### 4.2 Exposure and risk dimensions

Do not reduce portfolio risk to configured leverage or one scalar. At minimum, evaluate:
- gross/net notional; directional and factor/risk-cluster exposure;
- instrument, venue, strategy, model and counterparty concentration;
- initial/maintenance margin utilisation and stressed liquidation buffer;
- collateral asset, haircut, settlement-currency and FX risk;
- funding, basis and mark/index divergence;
- liquidity-adjusted close-out cost, spread, depth, participation and gap risk;
- realised/unrealised P&L, fees, funding and other cash-flow events;
- daily loss, rolling loss, high-water drawdown and capital-flow-adjusted return;
- correlated positions, shared model/data dependencies and common-cause failure;
- operational state, venue/API availability, unknown orders and reconciliation mismatch.

VaR/Expected Shortfall and historical correlations are diagnostics, not substitutes for coherent scenario analysis, stress testing or hard exposure constraints. Liquidation-price estimates are not guaranteed exit prices.

### 4.3 Position sizing, reservations and portfolio capacity

Proposed hierarchy: owner-approved portfolio capacity → risk cluster/instrument and strategy-family allocations → strategy allocation → per-trade budget → order-level reservation.

Working orders count as potential exposure. Reserve the worst permitted plausible exposure before submission. Partial fills transfer exposure to positions; residual order quantity remains reserved. Release only after authoritative terminal confirmation. Unknown acknowledgement/cancel/fill state retains a conservative reservation.

Reservation must be concurrency-safe across all requests drawing on the same budget. Test simultaneous requests and every plausible partial-fill ordering, including duplicate events and process restart. Never count the same filled amount both as a position and an open-order reservation.

### 4.4 Venue mechanics

Venue adapters must version contract specifications, settlement currency, tick/lot rules, funding interval/rate caps, margin tiers, maintenance rates, collateral haircuts, risk limits, mark/index definitions and liquidation mechanics. Record source, retrieval time, effective time, scope and version.

Isolated, cross and portfolio margin have different collateral-sharing and liquidation scopes. No cross-venue margin netting, collateral transferability or hedge credit may be assumed. Hedge offsets require economic and execution evidence under stress, including basis, correlation breakdown, liquidity and liquidation asymmetry.

## 5. Loss containment and emergency controls

D-006 (0.5% initial per-trade risk target) and D-008 (10% UTC day-start equity hard daily loss boundary including realised and unrealised P&L, followed by a 24-hour cooldown) remain accepted historical decisions. This research neither validates nor changes their values.

Required architecture beyond those numbers:
- earlier warning, throttling, strategy suspension and exposure-reduction levels;
- rolling loss and high-water drawdown controls that cannot be reset by UTC rollover;
- capital-flow-aware baselines and consistent fee/funding treatment;
- portfolio-wide limits and concentration controls;
- anti-reset protection across restart, account change, deposits/withdrawals and policy versions;
- deterministic handling of stale/unknown equity and conflicting account state;
- separate controls for stop-new-risk, cancel risk-increasing orders, permit bounded risk reduction, flatten, credential revocation and manual fallback.

The 10% threshold is an outer hard boundary, not a normal loss budget or desired operating target. No intermediate numerical thresholds are selected here.

## 6. Strategy, model and AI risk

Every strategy, predictive model, risk model, execution model and AI-assisted component needs a declared purpose, scope, inputs, assumptions, limitations, version, owner, validation record and retirement criteria.

- Retain every experiment and rejected trial to expose selection bias and multiple-testing effects.
- Use point-in-time data and instrument universe; realistic fees, funding, spread, slippage, liquidity, latency and fill assumptions; chronological walk-forward and untouched out-of-sample validation.
- Independently recompute key metrics and compare against simple baselines.
- Treat regime uncertainty as a valid no-trade state.
- Monitor drift, shared dependencies, model changes and regime instability; restrict or retire when validation no longer holds.
- AI-generated strategies/code are untrusted proposals and require deterministic validation and sandboxing.
- No online self-modification, autonomous policy tuning or risk-budget expansion is permitted by this architecture direction.

## 7. Requirements → controls → components → tests traceability

The identifiers below are proposed Phase 02 traceability IDs. They do not create implementation approval. “Future verification” describes evidence required before any future execution authority could be considered.

| ID | Requirement / invariant | Primary control | Owner component(s) | Required verification evidence |
|---|---|---|---|---|
| RM-01 | No action without approved authority | Explicit policy and action classification; deny by default | Security, Risk | Unauthorised principal/action negative tests; policy-version audit |
| RM-02 | Decision bound to exact action | Canonical payload hash, scope, validity and evidence references | Risk, Security | Mutated quantity/price/instrument/account invalidates approval |
| RM-03 | Inputs trustworthy for intended use | Provenance, quality, freshness, completeness and lineage gates | Data, Risk | Missing/stale/conflicted/corrected-source tests reject risk increase |
| RM-04 | Mandatory dependencies healthy | Independent scoped health interlock | Health, Risk | Supervisor outage/stale heartbeat/common-mode failure tests |
| RM-05 | Portfolio limits cannot be oversubscribed | Atomic reservations across concurrent proposals | Risk, durable state | Race/concurrency tests; no over-allocation under interleavings |
| RM-06 | Working orders count as exposure | Reserve unfilled potential exposure; reconcile order states | Risk, Adapter, Data | Partial fill, duplicate ack, timeout, cancel-pending and unknown-state tests |
| RM-07 | Partial fills counted exactly once | Atomic reservation-to-position transfer | Risk, Adapter, Reconciliation | Duplicate/reordered fills; restart and replay |
| RM-08 | Policy cannot be weakened by AI/strategy | Signed/versioned policy registry; separate write authority | Security, Risk | Agent policy mutation denied and audited |
| RM-09 | Venue parameters are point-in-time | Versioned effective-dated instrument/margin/funding rules | Data, Venue adapter, Risk | Parameter change/stale-rule tests; historical replay uses historical version |
| RM-10 | Capital measures not conflated | Explicit equity/margin types; currency/haircut semantics | Ledger/Data, Risk | Multi-currency, haircut, liability, transfer and unrealised-P&L tests |
| RM-11 | Daily and drawdown controls resist reset | Durable high-water and UTC baseline state; flow adjustment | Risk, Ledger, Audit | Rollover, restart, deposit/withdrawal, account/policy-change tests |
| RM-12 | Stress risk is portfolio-aware | Coherent scenario engine and liquidity-adjusted close-out estimates | Risk, Market data | Correlation break, gap, funding shock, depeg, depth collapse, venue outage |
| RM-13 | Emergency controls are not one ambiguous kill switch | Separate restrictive and financial actions with explicit authority | Risk, Health, Security, Operator | Failure-injection tests for each action and manual fallback |
| RM-14 | Recovery proves state before release | Rebuild/reconcile orders, positions, balances, permissions and evidence | Data, Health, Security, Risk | Restore/replay, discrepancy, compromised-key and partial-recovery exercises |
| RM-15 | Model/strategy approval is evidence-led | Immutable experiment manifest and independent validation | Research, Model registry, Risk | Leakage, multiple-testing, OOS, drift and baseline challenge |
| RM-16 | Audit is attributable and tamper-evident | Ordered durable events, integrity checks and independent anchoring | Audit, Security, Health | Deletion/reordering/tampering, sink outage and recovery tests |
| RM-17 | Failures are dependency-scoped | Explicit dependency graph and safe degraded states | Health, all domains | Fault injection confirms unrelated domains remain available where safe |
| RM-18 | Approval cannot be replayed or reused | Idempotency keys, expiry, revocation and one-time consumption | Risk, Security, Adapter | Replay, duplicate submission, expired/revoked approval tests |
| RM-19 | Numeric calculations are deterministic | Decimal/rounding/unit contracts and independent oracle checks | Risk, Data | Boundary/property tests, cross-platform deterministic replay |
| RM-20 | No execution authority by implication | Separate architecture, legal, security, venue and owner gates | Governance, Risk, Security | Governance audit confirms no connector/order path without approval |

## 8. Adversarial architecture review

This is a structured challenge performed in this review, not a completed independent third-party or subagent review.

| Severity | Attack/failure scenario | Why a superficial design fails | Required architectural response |
|---|---|---|---|
| Critical | Two concurrent orders each pass against the same remaining budget | Per-request checks race and both approve | Atomic portfolio-level reservation before action |
| Critical | Venue accepts an order but acknowledgement is lost | Client assumes failure and retries, duplicating exposure | UNKNOWN state, idempotency, query/reconcile before retry; retain reservation |
| Critical | Cancel request times out while order remains executable | Reservation released prematurely | Cancel-pending retains exposure until authoritative terminal state |
| Critical | Partial fill event is duplicated or reordered | Position and reservation double-count or disappear | Event identity, sequence/version checks, atomic accounting semantics |
| Critical | Market/account evidence is stale but plausible | Risk calculation produces a confident but invalid result | Consumer-specific freshness and reconciliation gate; fail closed |
| Critical | Risk approval is replayed with larger quantity or altered price | Approval treated as reusable token | Exact canonical payload binding and one-time consumption |
| Critical | Policy/signing key is compromised | Correct-looking decisions can be maliciously authorised | Separate policy-write trust, key revocation, signed versions, independent audit and incident lockout |
| Critical | Health supervisor and monitored service share a failure domain | Both report healthy or fail together | Independent watchdog/failure-domain analysis and manual fallback |
| High | UTC rollover resets daily loss while rolling drawdown remains severe | Daily limit circumvention | Durable high-water and rolling loss state; anti-reset tests |
| High | Deposit/withdrawal distorts equity-based loss calculation | Capital flow appears as profit/loss | Separate flow ledger and flow-adjusted baselines |
| High | Stablecoin collateral depegs while haircut rises | Nominal collateral overstates risk capital | Asset-specific stressed conversion/haircut and concentration limits |
| High | Correlation collapses and nominal hedge fails | Historical beta/offset hides joint tail risk | Coherent multi-factor stress and conservative hedge credit |
| High | Venue changes maintenance tiers or funding interval | Old cached parameter understates margin/funding | Effective-dated version registry; reject risk increase on unknown version |
| High | Risk service unavailable during a position incident | Fail-closed prevents new risk but does not manage existing exposure | Separate emergency/manual action plan; do not assume automatic flatten is safe |
| High | Audit sink fails while decisions continue | Evidence gaps cannot be reconstructed | Define which actions require durable audit acknowledgement; fail closed where evidence is mandatory |
| High | Recovery restarts processes but restores stale order/position state | System resumes from internally consistent but externally false state | Reconcile authoritative venue state and permissions before release |
| High | AI prompt injection attempts to change policy or invoke tools | Model instruction mistaken for authority boundary | External permission enforcement, isolated tools, signed policy and human approval |
| Medium | Model metrics degrade slowly across regimes | One-time approval remains trusted indefinitely | Drift triggers, review windows, suspension and revalidation |
| Medium | FX conversion is stale or uses wrong currency/side | Aggregate equity and risk budget are wrong | Explicit FX provenance, side, timestamp, haircut and stale-state rejection |
| Medium | Tests pass but do not detect weakened controls | Coverage badge masks ineffective assertions | Mutation testing, adversarial tests and independent oracle calculations |

### 8.1 Residual design weaknesses

Contracts are not ready to freeze. Open areas include:
- canonical event envelope and immutable evidence references;
- exact decision state machine and reason-code taxonomy;
- policy registry ownership, signing, rotation and recovery;
- clock discipline, monotonic deadlines, UTC boundary and source sequence semantics;
- freshness thresholds by data type, venue, account state and action;
- approval expiry, revocation and invalidation triggers;
- reservation atomicity, durability, crash recovery and concurrency model;
- watchdog topology and independence against common-mode compromise;
- audit durability, anchoring, retention and privacy;
- multi-currency and multi-account aggregation boundaries;
- owner-defined emergency actions and manual fallback procedures;
- intermediate loss thresholds, portfolio caps, concentration limits and leverage constraints.

## 9. Cross-document consistency findings

### 9.1 Execution-authority wording conflict

Current governance and roadmap state that no paper or live orders are authorised. However, REQUIREMENTS.md described paper trading as the only permitted execution mode and said the system operates strategies in paper trading; ARCHITECTURE.md listed a Paper broker and depicted a risk-approval → paper-simulator order flow. These descriptions can be read as execution authority.

The correction is to describe paper execution as a future proposed capability, not authorised now. This is documentation alignment, not a new owner decision.

### 9.2 Other consistency checks

- D-001 active crypto-perpetual scope is consistent with risk research. Future spot/equity/commodity/personal-finance domains remain deferred.
- D-006 and D-008 are repeated without modification. Their semantics remain incomplete; D-006's denominator is unresolved.
- D-020/D-021 and the core-protection document align with the risk cross-pillar contracts. Health and security assurance remain separate statuses.
- Security owns identity, permissions and policy integrity; risk owns financial approval.
- Data integrity owns source evidence, quality and correction lineage; risk owns suitability of evidence for a risk decision.
- Health may apply restrictive interlocks but cannot approve financial actions or alter policy.
- The modular-monolith/hexagonal direction is compatible with the boundaries, but module ownership, event contracts and transaction boundaries remain unfrozen.
- ROADMAP.md contains older historical status notes that say Phase 01 is in progress and Phase 02 locked, while its current-state block says Phase 01 closed and Phase 02 unlocked. Historical entries need explicit supersession labels or an auditable correction. Readers should rely on the current-state block and decision register.

## 10. Owner decisions still required

1. **D-006 equity denominator:** accept risk-adjusted equity as the 0.5% sizing basis, choose another explicitly defined measure, or defer the numerical decision until accounting semantics are complete.
2. **D-008 baseline semantics:** define deposits/withdrawals, multi-currency conversion, valuation source/age, fees/funding and UTC boundary while preserving the accepted 10% figure unless separately changed.
3. **Risk policy envelope:** approve categories of hard portfolio/instrument/strategy limits and warning/throttle/reduction states before numerical thresholds are chosen.
4. **Emergency actions:** define which restrictive and risk-reducing actions may be automatic, which require owner confirmation, and the manual fallback. No automatic flattening is presumed.
5. **Audit availability:** decide which future action classes require durable audit acknowledgement before proceeding and what happens if the audit sink is unavailable.
6. **Aggregation scope:** define whether future risk views observe one account, multiple subaccounts or multiple venues, without assuming margin netting or collateral transferability.
7. **Architecture contract details:** settle event envelope, policy registry trust, clock/freshness rules, approval lifecycle and reservation transaction boundary only after evidence and failure analysis.

## 11. Proposed next sequence

1. Owner review of this synthesis and unresolved decisions.
2. Correct the execution wording and roadmap historical-status ambiguity.
3. Resolve D-006/D-008 capital semantics and emergency-control authority.
4. Freeze cross-pillar ownership and risk decision/reservation semantics.
5. Produce the final requirements-to-control-to-component-to-test matrix across all four foundations, not risk alone.
6. Conduct a separate adversarial review of the integrated system and security threat model.
7. Complete formal architecture validation and obtain explicit owner acceptance before Phase 02 closure.
8. Only after acceptance, research and propose the implementation stack/blueprint. Implementation and execution remain separately gated.

## 12. Explicit boundaries

- No change to D-001, D-006, D-008 or any other accepted decision.
- No new numerical risk limit or policy threshold is accepted.
- No exchange, broker, account, testnet, API key or credential is selected or connected.
- No paper or live order is authorised.
- No runtime integration, code, dependency, infrastructure, paid service or external security scan is authorised.
- Phase 02 remains active; Phases 03–19 remain locked.


## Checkpoint 077 — supersession of historical consistency findings

The earlier §9.1 execution-authority wording conflict is now resolved by later repository updates:
- `REQUIREMENTS.md` explicitly says no paper or live execution is currently authorised and any future paper simulator requires separate approval/gates.
- `ARCHITECTURE.md` explicitly marks the paper-execution simulator as future proposed/not authorised and states no paper or live order flow is active.
- `RULES.md` was corrected at checkpoint 075 to prohibit paper and live execution until separate owner approval.
- Current roadmap and decision register remain consistent with Phase 02 architecture-only authority.

Therefore, §9.1 is a historical finding, not an open current contradiction. The older §11 sequence (immediate owner review) is superseded by the user's standing instruction and D-022: continue Phase 02 research autonomously and present unresolved owner decisions together only after the full architecture pack is ready.

Other findings in this document remain open unless explicitly closed by later checkpoint evidence. The integrated domain map, temporal evidence, domain risk/capital and reconciliation/recovery documents add further contracts that must be included in the next system-wide adversarial review.
