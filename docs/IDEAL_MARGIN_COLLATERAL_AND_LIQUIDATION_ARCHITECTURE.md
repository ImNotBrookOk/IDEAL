# IDEAL Margin, Collateral and Liquidation Architecture

**Checkpoint:** 099 — 18 November 2026  
**Phase:** 02 — Architecture and contracts  
**Status:** Research draft; no venue or margin mode selected  
**Scope:** Crypto perpetual futures only (D-001)  
**Authority:** Documentation/research only. No runtime, exchange access, credentials, paper/live trading or policy changes.

## 1. Purpose and non-goals

Specify a venue-neutral risk model for collateral valuation, initial/maintenance margin, tiered limits, portfolio stress, pending-order reservations, liquidation proximity and exchange liquidation outcomes. This is not a proposal to reproduce any venue's liquidation engine exactly, nor a claim that a displayed liquidation price predicts the eventual execution price.

Distinguish IDEAL's conservative capital/risk capacity; venue-reported account and position margin state; venue-specific rules and liquidation mechanics; and actual executable liquidity. Venue margin is not IDEAL's risk budget. A venue may permit more leverage than IDEAL policy; IDEAL must enforce the stricter constraint.

## 2. Evidence reviewed

Official primary documentation reviewed on 18 November 2026:
- Binance USDⓈ-M leverage/margin and liquidation protocol: https://www.binance.com/en/support/faq/leverage-and-margin-of-usd%E2%93%A2-m-futures-360033162192 and https://www.binance.com/en/support/faq/binance-futures-liquidation-protocols-360033525271
- Binance maintenance-margin/liquidation formula: https://www.binance.com/en/support/faq/how-to-calculate-liquidation-price-of-usd%E2%93%A2-m-futures-contracts-b3c689c1f50a44cabb3a84e663b81d93
- Binance insurance funds, updated 3 January 2026: https://www.binance.com/en/support/faq/introduction-to-futures-insurance-funds-360033525371
- Bybit Unified Trading Account liquidation process, updated 15 October 2026: https://www.bybit.com/en/help-center/article/UTA-Trading-Rules-Liquidation-Process
- OKX Futures mode/cross margin, updated 11 August 2026: https://www.okx.com/help/iii-single-currency-margin-cross-margin-trading
- OKX API v5 account/position risk and account mode documentation: https://www.okx.com/docs-v5/en/
- Hyperliquid margin tiers: https://hyperliquid.gitbook.io/hyperliquid-docs/trading/margin-tiers

These documents describe different account products, jurisdictions and rule versions. They are not interchangeable, and applicability must be rechecked if a venue is later considered.

## 3. Cross-venue findings

### 3.1 Mark price is a risk input, not an execution price

Binance and Bybit describe mark-price-triggered liquidation, while last traded price may differ. A mark-price breach can initiate liquidation even if the last-price candle does not show the trigger. Mark price is a model/index input; the liquidation order still has to execute in the market. Fast moves, basis divergence, spread widening, depth depletion and latency can make actual liquidation materially worse than the displayed estimate.

IDEAL must retain separate fields for index/reference price; mark price and source/method/version; last trade; executable bid/ask and depth; valuation timestamp and observation age; estimated liquidation threshold; and actual liquidation/close fills and fees.

Never use last trade as a silent substitute for a missing mark price in a critical risk calculation. If the approved fallback cannot be proven fresh and conservative, block risk-increasing actions and enter the defined restricted state.

### 3.2 Tiered maintenance margin is piecewise and can change with size

Binance, Bybit and Hyperliquid document notional tiers with increasing maintenance rates and deductions. A continuous piecewise function is represented as:

MM(N) = N × MMR_k − D_k, for N in tier k.

The tier table, rate, deduction, notional currency, position aggregation scope and effective time are venue/instrument/account-mode specific. IDEAL must not assume a single global maintenance rate or constant leverage cap. Tier transitions must be tested just below, at and just above boundaries, including fees and pending orders.

### 3.3 Margin mode changes the loss-sharing boundary

- Isolated margin segregates position-level allocated collateral, subject to venue-specific exceptions and mechanics.
- Cross margin shares eligible account equity across a defined settlement currency or account risk pool; losses in one position can consume capacity supporting another.
- Portfolio margin applies portfolio-level scenarios and offsets only within defined risk universes/netting sets. Collateral eligibility and haircuts can differ by asset and by initial versus maintenance use.

OKX documents cross-margin aggregation by settlement currency and account-level consequences. Bybit UTA supports isolated, cross and portfolio modes with distinct liquidation processes. No universal cross-margin or portfolio-margin semantics can be assumed.

### 3.4 Liquidation is a process, not one price

Bybit documents cancellation of risk-increasing orders, partial reduction from higher risk tiers, then position closure if maintenance requirements remain breached. Binance documents insurance-fund takeover of bankrupt positions and ADL when takeover capacity is insufficient. The insurance fund covers the difference between bankruptcy price and liquidation execution in the documented model; it is not insurance for the trader and does not reimburse ordinary trading losses.

IDEAL must model liquidation as a state machine with venue-specific transitions and an unknown/outcome-reconciliation branch. It must not assume an insurance fund guarantees solvency or that ADL cannot occur.

## 4. Canonical risk model (provisional)

Maintain separate quantities rather than one ambiguous equity field:
- gross asset value before eligibility/haircuts;
- eligible collateral value after asset-, size-, currency- and mode-specific haircuts;
- liability value including borrow, accrued interest, fees, funding payable and other obligations;
- unrealised PnL by instrument and settlement currency, with source and valuation basis;
- realised PnL event-sourced, including fees/funding;
- risk-adjusted equity as the conservative capital measure for sizing and drawdown;
- venue margin equity, never silently substituted for risk-adjusted equity;
- initial and maintenance margin requirements;
- open-order reservation for worst-case additional exposure from all active and uncertain orders;
- available risk capacity after positions, reservations and stress buffers.

A provisional risk-adjusted-equity representation is:

RAE = Σ_i (eligible_quantity_i × conservative_price_i × collateral_weight_i) + conservative_PnL − liabilities − accrued_costs − uncertainty_reserves.

This is a conceptual schema, not an accepted numerical formula. Exact weights, PnL recognition, cash-flow adjustment, FX hierarchy and thresholds remain open under ODR-02/03/05. Do not count positive unrealised PnL as fully available capital unless approved rules and venue settlement semantics support it. Negative PnL and liabilities must not be understated.

## 5. Collateral eligibility and valuation

Every asset requires a versioned collateral rule with asset/network/issuer identity; settlement currency and permitted account modes; eligibility and effective interval; oracle/mark source, quote currency, bid/ask side and timestamp; separate initial and maintenance haircuts; concentration/size-dependent haircut; depeg, volatility, liquidity and transferability stress; custody, encumbrance, borrow and withdrawal status; stale/missing price behaviour; rounding precision and conservative conversion direction.

A displayed market value is not equivalent to collateral value. Haircuts should reflect price volatility, market depth, liquidation horizon, concentration, depeg/counterparty risk and whether the asset can actually be mobilised in the relevant account. Collateral transfer between venues/accounts is not assumed instantaneous or available.

For multi-currency accounts, preserve native-currency sub-ledgers. Any consolidated risk view requires explicit FX source, side, age, spread, haircut and liability treatment. Missing or stale FX must not be silently zero-filled or replaced with a favourable rate.

## 6. Initial margin, maintenance margin and risk tiers

The future venue adapter must expose versioned instrument/account configuration: contract multiplier and linear/inverse settlement mechanics; notional valuation currency and mark-price source; initial and maintenance tier tables; tier deduction/offset and position aggregation rules; maximum position/notional and leverage constraints; fee-to-close and liquidation fee assumptions; funding and settlement rules; margin mode and hedge/one-way semantics; effective timestamps and source/API provenance.

Initial margin gates new or increased risk. Maintenance margin measures whether existing exposure can remain open. They are not interchangeable. Venue-reported IM/MM fields should be retained alongside IDEAL's independently recomputed estimates; differences beyond a defined tolerance become a data-integrity/risk incident, not an automatic override.

Pending orders must reserve worst-case risk. Include active orders, conditional/algo orders that can trigger, amendments that increase risk, and requests with uncertain venue outcomes. Avoid double-counting mutually exclusive reduce-only exits only where reduce-only semantics are verified. An order cannot be treated as cancelled until cancellation is confirmed and reconciled.

## 7. Portfolio stress and hedge credit

A conservative initial architecture should not grant cross-instrument or cross-venue hedge credit by default. Risk aggregation must include gross/net notional by instrument, direction, venue and settlement currency; concentration and correlated exposure; basis divergence between index, mark and executable markets; joint adverse price shocks and gaps; liquidity/depth deterioration and exit slippage; funding spikes and direction changes; collateral depeg and FX shocks; venue outage, withdrawal/transfer freeze and counterparty failure; correlated liquidation and market-wide volatility.

Portfolio margin may recognise offsets only within an explicit, enforceable netting set and only after stress scenarios include basis, correlation breakdown, liquidity, settlement, collateral and counterparty risk. Correlation estimates are not legal or operational netting rights. A hedge on another venue/account is not assumed to protect the liquidating venue's margin account.

This aligns with ODR-04's deferred recommendation: no unified risk budget and no implicit hedge credit across accounts, venues, legal entities, instruments or collateral pools.

## 8. Liquidation proximity and execution realism

IDEAL should calculate three distinct views: (1) margin-breach proximity under current validated mark and tier; (2) stress-breach proximity under adverse price, volatility, basis, collateral and liquidity shocks; (3) executable close capacity estimated from current validated order-book depth after conservative impact and latency assumptions.

A liquidation price is a threshold estimate, not a guaranteed fill. Stress tests must include gap-through, stale mark, mark/index divergence, spread widening, empty/one-sided book, partial fill, no fill, market impact, fee-to-close, funding boundary and simultaneous liquidations. The simulator's synthetic close price must never be presented as a venue liquidation result.

## 9. Liquidation lifecycle and uncertainty

Provisional states:
- HEALTHY
- WARNING
- RISK_INCREASE_BLOCKED
- ORDER_CANCELLATION_REQUESTED
- ORDER_CANCELLATION_UNCERTAIN
- PARTIAL_REDUCTION_REQUESTED
- PARTIAL_REDUCTION_IN_FLIGHT
- LIQUIDATION_TRIGGERED
- CLOSE_REQUESTED
- CLOSE_PARTIALLY_FILLED
- CLOSE_OUTCOME_UNCERTAIN
- VENUE_BANKRUPTCY_HANDOFF
- INSURANCE_FUND_HANDOFF (venue-reported only)
- ADL_REPORTED (venue-reported only)
- RECONCILIATION_REQUIRED
- RECOVERED / RECOVERY_HOLD

The lifecycle is not a single linear sequence: venue modes differ, and partial liquidation may return an account to a healthier state or proceed to full close. Every transition must be driven by authenticated venue evidence and a local durable event. On timeout/partition, reserve maximum plausible exposure, prohibit risk increases and reconcile before declaring recovery.

IDEAL cannot guarantee a cancellation or close request is received, nor that liquidation executes at the estimated price. It cannot prevent venue-side liquidation after connectivity is lost. Local kill/revocation controls do not recall already transmitted requests.

## 10. Data contracts required before implementation

A later implementation contract must define typed, versioned records for CollateralAssetState, CollateralEligibilityRule, CollateralValuation, FxConversionEvidence, InstrumentRiskTier, MarginModeState, AccountMarginSnapshot, PositionRiskSnapshot, OpenOrderRiskReservation, StressScenario, StressResult, LiquidationEvent, VenueRuleSet, VenueRuleEvidence, RiskDecision and RiskReservation.

Each record requires source identity, observation/event time, ingestion time, validity/expiry, schema version, venue/account/instrument scope, currency, provenance and integrity digest. Conflicting or incomplete snapshots must be represented as unknown/stale/inconsistent, not silently merged.

## 11. Failure behaviour

| Failure | Required behaviour |
|---|---|
| Missing/stale mark or index | Block risk increases; no silent last-trade substitution |
| Stale/missing collateral or FX price | Exclude or conservatively haircut; restrict if material capacity is unknown |
| Unknown venue/account margin mode | Block risk increases |
| Missing/unknown tier table | Block risk increases; no optimistic default |
| Local IM/MM disagrees with venue beyond tolerance | Reconcile; block risk increases; preserve both observations |
| Open order status unknown | Reserve worst-case risk until terminal status confirmed |
| Cancel/close acknowledgement lost | Mark uncertain, retain exposure/reservation, reconcile |
| Venue API unavailable | No new risk; local containment cannot guarantee venue state |
| Venue liquidation/ADL reported | Reconcile account, positions, fills, fees and balances from independent venue records |
| Clock skew or rule version stale | Reject stale evidence and restrict risk increases |
| Collateral depeg/withdrawal freeze | Apply preapproved conservative haircut/restriction; do not assume transferability |

## 12. Verification plan (not executed)

Mandatory future tests: tier boundaries at N−ε/N/N+ε including continuity and rounding; linear/inverse contracts and long/short; one-way/hedge mode; isolated/cross/portfolio margin; asset/size/concentration and initial/maintenance haircuts; native-currency accounting and adverse FX; funding/fee-to-close/liquidation fees/accrued liabilities; pending/conditional orders and uncertain cancellation; mark/index/last divergence and stale-price rejection; gap-through/no-depth/partial-fill/slippage/simultaneous liquidation; insurance-fund exhaustion and ADL as external venue events; restart/recovery with stale snapshots and unknown order outcomes; deterministic replay; property tests for conservative monotonicity; independent oracle comparison against venue formulas and API snapshots for any later selected venue.

No tests were run for this checkpoint; this is architecture research, not implementation.

## 13. Unresolved owner and platform decisions

ODR-02: risk-adjusted equity denominator and haircut/FX formula for D-006. ODR-03: flow-adjusted UTC day-start equity and valuation semantics for D-008. ODR-04: future cross-domain netting/hedge credit deferred; initial conservative no-credit rule. ODR-05: broader consolidated portfolio view remains future-domain scope. ODR-09: host topology and availability. ODR-12: final architecture baseline and Phase 03 consideration. Venue-specific contract/account mode, tiers, haircuts, API semantics and liquidation rules remain unselected.

## 14. Evidence limits

Binance insurance-fund FAQ notes it may be outdated and directs readers to exchange rules/contract specifications effective 5 January 2026; those binding legal terms were not fully reviewed here. Exchange support pages are mutable and account/jurisdiction applicability varies. Hyperliquid tier documentation is not evidence for another venue. No live API response, account state or exchange entitlement was inspected. No venue selection or legal eligibility determination is made.

## 15. Authority boundary

Research only. No venue, margin mode, collateral asset, haircut, risk limit, formula, policy engine, provider, dependency or execution permission selected. D-006 and D-008 unchanged. Phase 02 active; Phases 03–19 locked.


## 12. Funding and mark-price source refresh — checkpoint 110

The [Perpetual Funding and Mark-Price Semantics Source Refresh](IDEAL_PHASE_02_PERPETUAL_FUNDING_AND_MARK_PRICE_SEMANTICS_REFRESH.md) records current official-source evidence that funding intervals/caps may vary by contract and change, and that mark-price methods are more specific than generic help-page summaries. Treat funding schedules, mark methodology and tier tables as effective-dated, instrument-specific evidence. Funding forecasts are not realised ledger events; funding settlement may affect available balance or position margin. Missing/stale configuration or settlement evidence invalidates dependent calculations. Added conformance cases cover interval changes, funding boundary ordering, corrections, mark-method revisions and mode-specific tier changes. No venue, formula or runtime is selected.


## 12. Funding and mark-price source refresh — checkpoint 110

The [Perpetual Funding and Mark-Price Semantics Source Refresh](IDEAL_PHASE_02_PERPETUAL_FUNDING_AND_MARK_PRICE_SEMANTICS_REFRESH.md) records current official-source evidence that funding intervals/caps may vary by contract and change, and that mark-price methods are more specific than generic help-page summaries. Treat funding schedules, mark methodology and tier tables as effective-dated, instrument-specific evidence. Funding forecasts are not realised ledger events; funding settlement may affect available balance or position margin. Missing/stale configuration or settlement evidence invalidates dependent calculations. Added conformance cases cover interval changes, funding boundary ordering, corrections, mark-method revisions and mode-specific tier changes. No venue, formula or runtime is selected.


## 16. Account-mode-specific liquidation pathways — checkpoint 113

The generic lifecycle in §9 is an event vocabulary, not a universal ordered liquidation sequence. Official Bybit UTA rules (updated 15 October 2026) demonstrate material differences by account mode:

- **Isolated:** liquidation is position-scoped and mark-triggered. At the lowest risk tier, risk-increasing orders are cancelled before full closure if maintenance remains breached. Above the lowest tier, the venue may first submit an IOC partial reduction to move the position into a lower risk tier, then close if still deficient.
- **Cross:** liquidation is account-scoped. The documented UTA sequence includes restrictions on additional margin borrowing, risk-increasing order cancellation, liability auto-repayment, cancellation of remaining orders, treatment of fully hedged positions, then unhedged position reduction ordered by venue liquidity. Its displayed liquidation price is dynamic and depends on account equity, unrealised PnL, positions, maintenance requirements and available margin.
- **Portfolio margin:** the account is assessed as a portfolio. Bybit documents cancellation of all orders (including closing orders and TP/SL), auto-repayment, staged asset/position liquidation, and a takeover threshold distinct from the initial liquidation threshold. It may simulate partial closes and select the position with greatest MMR reduction. This is not equivalent to a simple position-level liquidation-price formula.

These are Bybit-specific current examples, not rules for IDEAL or another venue. They prove the need for a versioned state-transition policy keyed by venue, product, account mode, position mode, settlement currency, risk tier and effective time. The architecture must not encode one global ordered list of liquidation actions. An observed action can be absent, reordered, repeated or venue-specific; reconcile actual event evidence rather than forcing it through an assumed sequence.

### Required design controls

1. Split the generic lifecycle into a common event vocabulary plus venue/account-mode transition graphs. Each graph has a source rule revision and effective interval.
2. Represent the liquidation scope explicitly: position, settlement-currency pool, cross-margin account or portfolio netting set.
3. Distinguish cancellation of risk-increasing orders from cancellation of all orders; do not assume reduce-only or closing orders survive every mode.
4. Model auto-repayment, asset conversion, hedge settlement, partial IOC reduction, liquidation, bankruptcy-price closure, venue takeover and ADL as separate event types. Do not infer that one occurred from another.
5. Preserve venue action priority, liquidity ordering, tier transitions and stopping thresholds as effective-dated rule data; no generic 100% MMR threshold is assumed across products.
6. Liquidation-price display is an estimate with explicit scope/time/mode; for cross/portfolio margin it can change with unrelated positions, collateral, liabilities, orders and haircuts. Never treat it as a fixed stop or guaranteed exit.
7. Unknown account mode, incomplete portfolio state, stale rule revision or conflicting liquidation events blocks risk increases and enters RECONCILIATION_REQUIRED.

## 17. Session settlement and margin-state discontinuities — checkpoint 113

Bybit's official UTA liquidation documentation describes a USDC perpetual session-settlement mechanism: at settlement, average entry price may be reset to the settlement-time mark price, while session realised PnL is transferred into initial margin and the displayed initial-margin basis may remain anchored to the original position value. Fee-to-close and maintenance-margin calculations are recomputed using the updated entry/mark basis. This means a naive replay based only on fills plus current average entry can misattribute PnL or calculate an incorrect liquidation threshold.

IDEAL must represent session settlement as an explicit, ordered account/position event with prior and new entry basis, settlement mark and method, session realised PnL, margin adjustments, fee-to-close basis, event timestamp and source revision. It must reconcile before/after position and wallet snapshots. Do not synthesise settlement from a daily candle or funding timestamp. Venue/product support and applicable terms must be verified before using this pattern.

### Additional future conformance tests

- Same exposure under isolated, cross and portfolio modes must produce different risk scope and transition graph where venue rules specify it.
- Cross/portfolio liquidation must react to an unrelated position, collateral haircut, liability or order change without a price move.
- Verify mode-specific cancellation scope, including closing orders and TP/SL; uncertain cancel results retain worst-case reservations.
- Verify tier-down partial IOC size and stopping conditions at exact tier boundaries; distinguish partial reduction from final liquidation.
- Verify venue-specific takeover thresholds and action sequence; unknown transition remains unresolved rather than coerced into a generic state.
- Replay USDC session settlement around boundary with before/after average entry, realised PnL, initial margin, fee-to-close and maintenance margin reconciliation.
- Verify displayed liquidation-price movement after external account state changes; reject treating it as a static risk limit.

**Sources (reviewed 19 November 2026):**
- Bybit UTA Trading Rules: Liquidation Process, updated 15 October 2026: https://www.bybit.com/en/help-center/article/UTA-Trading-Rules-Liquidation-Process
- Bybit UTA introduction and margin-mode scope: https://www.bybit.com/en/help-center/article/Introduction-to-Bybit-Unified-Trading-Account/
- OKX API V5 account fields for account IMR/MMR, equity and forced liquidation: https://www.okx.com/docs-v5/en/
- Binance USDⓈ-M margin tier update, 12 September 2026 (demonstrates live tier revisions): https://www.binance.com/en/support/announcement/detail/2adc4f459022496db814a96b93215a1e

No venue or mode selected. These findings are architecture requirements only.
