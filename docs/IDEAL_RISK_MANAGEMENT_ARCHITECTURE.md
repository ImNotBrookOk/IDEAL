# IDEAL Risk Management Architecture — Research Draft

**Status:** Phase 02 working research draft; not owner-approved as a final architecture  
**Research started:** 17 November 2026  
**Scope:** Crypto perpetual futures only, consistent with D-001  
**Authority:** Research and documentation only. No implementation, exchange access, paper/live execution, dependency adoption or policy changes are authorised.

> This document records evidence, architectural implications and provisional design hypotheses. It does not silently change accepted decisions. Proposals remain proposals until reviewed and explicitly approved by the owner.

## 1. Purpose

Design an independent, deterministic risk authority that protects IDEAL's capital and constrains every future action that could create, increase or materially alter financial exposure. Risk management is an authority and control system, not merely a position-size calculator or a collection of stop-loss rules.

The risk architecture must be integrated with the other foundational pillars:

- **Data integrity:** risk decisions require correctly identified, reconciled, sufficiently fresh and provenance-backed positions, orders, balances, instrument rules and market observations.
- **System health:** independent supervision must detect when risk calculations, policy loading, market inputs, reconciliation or emergency controls are unavailable, stale or inconsistent.
- **Security:** identities, permissions, policy versions, risk decisions, credentials and audit evidence must be protected against unauthorised access or tampering.

A strategy or AI component may propose an action. It must not authorise itself, modify its own limits, grant itself permissions or bypass risk controls.

## 2. Scope and existing policy constraints

### 2.1 Active scope

D-001 remains unchanged: crypto perpetual futures are the only active initial market scope. Spot, equities, commodities and other domains remain deferred research only.

### 2.2 Existing accepted numerical decisions

The following existing decisions are inputs to this research and are not being changed here:

- **D-006:** initial per-trade risk target is 0.5% of equity.
- **D-008:** hard daily loss boundary is 10% of UTC day-start equity, including realised and unrealised P&L, followed by a 24-hour cooldown.

These values must be evaluated against the complete risk architecture, realistic execution costs, portfolio effects and failure scenarios before any future implementation. They are not evidence that intermediate warning thresholds, portfolio limits, leverage caps or other risk controls have been fully designed. The existing decision register already leaves earlier warnings and portfolio controls unresolved.

The daily hard loss boundary must not be treated as the sole capital-protection mechanism or as a desired operating loss. Earlier warning, throttling, exposure-reduction and strategy suspension controls require separate research and owner approval.

## 3. Evidence reviewed in this research tranche

### 3.1 Perpetual-specific supervisory reference

The Hong Kong Securities and Futures Commission's *High-level framework for virtual asset perpetual contracts offering by virtual asset trading platforms* was last updated 11 February 2026. It applies to SFC-licensed platform operators, not automatically to a private personal system. It is used here as an engineering reference, not as a claim about IDEAL's legal obligations.

Relevant principles include:
- transparent and enforceable trading, margining, default-management, liquidation and loss-allocation rules;
- orderly operation under extreme but plausible stress and regular system stress testing;
- timely, reliable and objectively verifiable mark, index, funding and valuation inputs;
- multiple independent price sources and contingency/failover arrangements for insufficient or disrupted inputs;
- automated pre-trade checks for required margin;
- margin requirements that consider concentration;
- predefined liquidation and loss-allocation priority;
- surveillance for mark/index divergence, abnormal funding and liquidation clusters;
- business-continuity arrangements and clear treatment of funding, basis divergence, liquidity gaps, cascading liquidations and ADL.

Source: https://www.sfc.hk/en/News-and-announcements/Policy-statements-and-announcements/A-high-level-framework-for-virtual-asset-perpetual-contracts-offering-by-VATP

### 3.2 Automated trading controls

The FIA's July 2024 *Best Practices for Automated Trading Risk Controls and System Safeguards* describes layered pre-trade, exchange, post-trade and testing controls. It discusses maximum order size, maximum intraday position, price tolerance, cancel-on-disconnect, kill switches, volatility controls, message throttles, drop-copy reconciliation and conformance testing.

Relevant implications:
- current positions and working orders both matter when checking limits;
- missing order-size limits should result in blocking the order;
- risk controls should be applied at multiple appropriate points;
- kill switches are a final backstop, not a substitute for ordinary pre-trade controls;
- a kill switch should not be overrideable by the strategy or automated trader it constrains;
- exchange-originated trade/order reports provide an independent reconciliation source;
- post-trade monitoring complements pre-trade prevention;
- material exchange-facing changes require appropriate conformance testing.

Source: https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf

### 3.3 Exchange-specific mechanics are not interchangeable

Official venue material demonstrates why a venue-neutral model needs explicit adapters and versioned rule data:

- Binance explains that mark price, rather than last traded price, is used for liquidation and unrealised P&L calculations, and that fast market movement can make actual liquidation outcomes differ from a displayed estimate. https://www.binance.com/en/support/faq/detail/360033525271
- Binance explains that insurance funds mitigate counterparty liquidation risk but are not insurance products and do not guarantee user losses. https://www.binance.com/en/support/faq/detail/360033525371
- Bybit documents isolated, cross and portfolio margin modes, mark-price liquidation, tiered maintenance margin and a liquidation sequence that can cancel increasing orders, partially reduce positions and ultimately close positions. https://www.bybit.com/en/help-center/article/UTA-Trading-Rules-Liquidation-Process
- Bybit's maintenance-margin documentation explains tier-dependent maintenance rates and deductions, with the applicable tier changing as marked position value changes. https://www.bybit.com/en/help-center/article/Maintenance-Margin-USDT-Contract
- OKX documents shared collateral/equity effects in cross margin and separation of position risk in isolated margin. https://www.okx.com/help/iii-single-currency-margin-cross-margin-trading
- OKX API documentation exposes account/position fields such as available equity, initial margin requirement, maintenance margin requirement, unrealised P&L and estimated liquidation price. The documentation warns that estimated liquidation prices can change with funding, other positions and market moves. https://www.okx.com/docs-v5/en/

These sources are examples, not venue selections or proof that every product/account mode has identical rules. Exact contract specifications and current venue rules must be captured and revalidated if a venue is ever selected.

### 3.4 Portfolio risk references

CME SPAN and SPAN 2 provide useful institutional references for portfolio-level risk rather than isolated position limits. SPAN evaluates hypothetical portfolio scenarios. SPAN 2 adds explicit consideration of historical risk, stress risk, liquidity and concentration.

Sources:
- https://www.cmegroup.com/solutions/risk-management/performance-bonds-margins/span-methodology.html
- https://www.cmegroup.com/clearing/risk-management/span-overview/span-2-methodology.html

These models are not drop-in crypto-perpetual solutions. Their principles should be studied and adapted only where the data, market structure and assumptions are valid.

### 3.5 Broader risk and resilience references

- CPMI-IOSCO Principles for Financial Market Infrastructures cover comprehensive risk management, credit, collateral, margin, liquidity and operational risk. They are designed for financial market infrastructures; use as a reference proportionately, not as a claim that IDEAL is an FMI. https://www.federalreserve.gov/frrs/regulations/appendix-cpss-iosco-principles-for-financial-market-infrastructures.htm
- The Financial Stability Board's 2023 crypto-asset recommendations identify conflicts of interest, market manipulation, custody/client asset protection, cross-border risks, operational/technological risk and retail distribution as key areas. https://www.fsb.org/2023/11/policy-recommendations-for-crypto-and-digital-asset-markets/

## 4. Provisional risk authority model

The following is a design hypothesis for review, not an accepted final contract.

### 4.1 Authority hierarchy

1. **Owner-approved governance and policy:** defines permitted scope, hard constraints, approval requirements and policy-change authority.
2. **Independent risk authority:** deterministically evaluates proposals against current policy, portfolio state, market evidence and venue constraints. It may reject or constrain; it cannot expand owner-approved authority.
3. **Portfolio risk aggregation:** calculates aggregate exposure, concentration, stress loss, collateral and risk capacity across all strategies and instruments in the active scope.
4. **Strategy allocation:** receives a bounded risk budget and proposes actions within it. Strategy logic cannot change the allocation.
5. **Execution component:** can only act on a current, exact, authorised instruction. It cannot infer permission from a strategy signal.
6. **Independent health supervision:** monitors whether risk policy, calculation, input, reconciliation and containment controls are operating and current.
7. **Security enforcement:** protects identities, permissions, policy and decision records, secrets and audit evidence.

A lower level cannot override a higher-level rejection. Venue rules may be stricter than IDEAL policy; IDEAL must respect the stricter effective constraint.

### 4.2 Risk policy classes and change governance

Research should distinguish at least four classes of constraints:

- **Hard policy constraints:** owner-approved boundaries that cannot be weakened by strategies, models, automated optimisation or ordinary runtime configuration.
- **Warning/escalation thresholds:** earlier signals that trigger alerts, throttles, strategy restrictions or review before a hard boundary is reached.
- **Dynamic conservative constraints:** deterministic reductions in permitted risk when volatility, liquidity, concentration, data quality or venue conditions deteriorate. These may reduce capacity within pre-approved rules but must not silently increase hard limits.
- **Venue constraints:** instrument/account-specific requirements and limits imposed by the venue. The effective permitted action must satisfy both IDEAL policy and venue rules; the stricter applicable constraint governs.

Policy changes should be versioned, attributable, reasoned, effective-dated and auditable. A strategy or AI agent cannot change risk policy, thresholds, allocation or permission. No automated policy tuning may weaken hard constraints. Temporary exceptions, if ever allowed, require a separate owner-controlled process with scope, reason, expiry and audit evidence.

The existing D-009 principle that progression gates are predefined and deterministic is relevant: strategy eligibility and risk allocation cannot be changed by an AI component to bypass a gate. Unknown regime or absence of an eligible strategy remains a no-trade condition under D-004.

### 4.3 Action classification

Every proposed action should be classified by its effect, not merely by its order type:

- create or increase exposure;
- reduce or close exposure;
- amend an existing order;
- create, amend or cancel protective orders;
- cancel an exposure-increasing working order;
- change leverage, margin mode or collateral allocation;
- transfer or withdraw collateral;
- administrative/policy change.

An action described as "reduce-only" must still be checked against actual venue semantics, current position state and order behaviour. A close request is not proof that exposure has been reduced.

Collateral transfers/withdrawals and policy changes are not assumed to be ordinary trading actions; they require distinct permissions and approval boundaries.

### 4.4 Pre-action decision contract

A risk decision should be bound to:
- unique proposal and decision identifiers;
- exact instrument, side, quantity, order type, price constraints and intended effect;
- strategy identity and allocation;
- current policy version;
- portfolio/account snapshot and freshness;
- market and instrument evidence versions;
- open positions and working-order state;
- calculations and each control result;
- explicit approval, rejection or constrained approval;
- reason codes and restrictions;
- expiry/validity conditions;
- idempotency and replay protection;
- audit evidence.

A provisional approval should be narrow, short-lived, non-reusable and invalidated when material inputs change. The execution component must not broaden or mutate the approved instruction. This contract needs detailed interface design before implementation.

## 5. Provisional logical components

These are logical responsibilities, not a decision to create separate deployable services.

1. **Risk policy registry:** immutable, versioned, owner-approved limits, rules, thresholds, effective dates and permissions.
2. **Capital and portfolio state:** reconciled balances, equity, positions, orders, collateral, realised/unrealised P&L and funding.
3. **Market and instrument risk:** mark/index/reference prices, volatility, liquidity, funding, contract specifications and venue risk parameters.
4. **Exposure and margin calculator:** notional, gross/net exposure, margin, liquidation estimates, planned loss and stress calculations.
5. **Risk budget allocator:** portfolio, strategy and trade-level risk allocations.
6. **Pre-action decision authority:** deterministic approve/reject/constrain decision.
7. **Continuous risk monitor:** recalculates risk as positions, orders, prices, funding and venue rules change.
8. **Emergency control and recovery manager:** predefined containment, incident recording and recovery verification.
9. **Independent risk audit:** preserves policy, inputs, calculation version, decision, reasons and outcomes.

The final module boundaries should be chosen only after the wider system architecture and interface contracts are reviewed.

## 6. Portfolio and position risk model — research direction

### 6.1 Position sizing

For a simple linear contract, a preliminary sizing concept is:

planned risk budget = approved equity basis × approved risk fraction

quantity ≈ (planned risk budget − estimated costs) / (abs(entry price − stop price) × contract multiplier)

This is not a universal formula. Inverse contracts, contract multipliers, quote/settlement currencies, nonlinear structures, fee schedules and funding require contract-specific calculations.

A stop price is not a guaranteed maximum loss. Gaps, latency, market impact, partial fills, unavailable liquidity, exchange disruption and slippage can produce losses beyond planned risk.

The design should distinguish:
- **planned trade risk:** loss under the specified exit assumptions;
- **adverse execution risk:** estimated loss under stressed fill/exit conditions;
- **portfolio stress loss:** portfolio-level loss under coherent scenarios;
- **venue liquidation risk:** risk under the venue's actual margin and liquidation rules.

### 6.2 Working orders

Risk calculations must include current positions and all potentially executable working orders. A cancellation request is not a cancellation confirmation. Until the venue confirms the terminal state, the order must remain in the conservative exposure calculation.

The model must account for partial fills, amendments, duplicate submissions, delayed acknowledgements, conditional orders, simultaneous fills and orders from multiple sessions/strategies.

Opposing orders must not be assumed to net safely if both can fill, if hedge mode permits separate legs, or if they create basis, venue, funding, liquidity or counterparty risk.

### 6.3 Portfolio aggregation

Research and define:
- gross and net notional by instrument and underlying;
- long/short directional exposure;
- collateral and settlement-currency concentration;
- strategy and signal-family concentration;
- common-factor and correlation exposure;
- basis and funding exposure;
- liquidity and liquidation concentration;
- venue/counterparty concentration;
- portfolio margin and available risk capacity.

Net exposure must not hide gross exposure or offsetting positions with distinct liquidation, funding, liquidity or counterparty risks.

### 6.4 Risk measurement

Investigate complementary methods rather than relying on a single score:
- deterministic exposure and limit checks;
- volatility and correlation measures;
- historical simulation and VaR;
- Expected Shortfall;
- historical and hypothetical stress scenarios;
- liquidity-adjusted close-out estimates;
- concentration charges;
- scenario-based liquidation and margin stress.

Statistical models are estimates, not guarantees. Correlations can change abruptly, historical data may omit new regimes, and tail events may be underrepresented. Risk decisions must retain explicit scenario and model limitations.

### 6.5 Stress scenarios

At minimum, investigate coherent combinations of:
- sharp BTC decline with rising altcoin correlations;
- abrupt volatility expansion and price gaps;
- mark/index divergence or reference-source failure;
- abnormal or rapidly changing funding;
- order-book depth collapse and spread expansion;
- maintenance-margin or risk-tier changes;
- collateral stablecoin depeg and haircut changes;
- exchange/API/WebSocket outage or delayed order state;
- simultaneous liquidation pressure across correlated positions;
- failed hedge execution;
- ADL or other venue loss-allocation events;
- exchange insolvency, withdrawal restrictions or counterparty impairment.

### 6.6 Capital and equity semantics

Official exchange documentation demonstrates that wallet balance, total equity, adjusted equity, margin balance and available balance are different measures with different purposes. Binance's Futures documentation distinguishes wallet balance (including realised P&L, funding and commissions) from margin balance (wallet balance plus unrealised P&L) and available balance. Bybit distinguishes total equity, margin balance and available balance, including collateral haircuts. OKX distinguishes total equity, adjusted equity after collateral haircuts and available equity.

Sources:
- Binance Futures balance definitions: https://www.binance.com/en/blog/futures/457299340443288694
- Bybit V5 Get Wallet Balance: https://bybit-exchange.github.io/docs/v5/account/wallet-balance
- Bybit UTA glossary: https://www.bybit.com/en/help-center/article/Glossary-Unified-Trading-Account
- OKX API account overview: https://www.okx.com/docs-v5

Provisional architecture implication: do not use one ambiguous field called "equity" as the basis for every risk rule. Investigate and explicitly define at least:
- **Economic equity:** best estimate of net economic value across the explicitly included account assets and liabilities, with valuation timestamp and source.
- **Risk-adjusted equity:** conservative risk-capital measure after applicable collateral haircuts, liabilities, uncertain valuations and other approved deductions.
- **Venue margin equity:** the exchange's own account-mode-specific measure used by its margin/liquidation system.
- **Available margin:** the amount the venue currently makes available for additional margin requirements.

These values must remain separately named and traceable. Available margin is not a measure of wealth or a sufficient standalone risk budget. Unrealised gains must not automatically be treated as cash or transferable collateral.

The future capital-state design should distinguish immutable financial events (transfers, realised P&L, fees, funding, rebates, liquidation charges and adjustments) from time-varying valuations (mark-to-market unrealised P&L and collateral conversion). Transfers between internal accounts must not be mistaken for profit or loss. Position P&L must not be double-counted in both the ledger and valuation layer.

The exact equity basis for D-006 and any future portfolio limits remains unresolved. D-008 already specifies UTC day-start equity for its daily loss boundary; that definition must be preserved unless the owner explicitly approves a superseding decision. D-006's "equity" basis requires clarification during policy design. Venue-specific account mode, collateral haircut, borrowing/liability and settlement-currency rules must be modelled explicitly.

Cross-venue or cross-account aggregation may be useful for economic exposure, but IDEAL must not assume margin netting, collateral transferability or immediate access to funds across venues/accounts unless this is separately proven and authorised.

### 6.7 Leverage, notional and liquidation buffer are distinct measures

Leverage should not be used as a standalone proxy for risk. The design must distinguish:
- **Configured leverage:** venue setting that influences initial margin and maximum permitted notional.
- **Gross notional exposure:** total absolute market exposure, before offsets.
- **Net directional exposure:** signed exposure after explicitly permitted aggregation.
- **Effective leverage:** a named exposure measure divided by a named equity basis.
- **Initial-margin utilisation:** initial margin consumed by positions and orders relative to the relevant venue margin base.
- **Maintenance-margin utilisation:** maintenance requirement relative to the venue's applicable margin equity.
- **Liquidation buffer/distance:** current mark-price distance to estimated liquidation, with the estimate's assumptions and freshness.
- **Stress liquidation buffer:** remaining buffer after applying stressed price, funding, fee, collateral and margin-tier changes.

A position with low configured leverage can still be too large relative to portfolio equity or liquidity. Conversely, raising configured leverage does not itself change the P&L sensitivity of an unchanged notional position, but it reduces initial margin posted and can reduce the loss buffer before liquidation. Therefore, risk policy must separately constrain notional/exposure, planned loss, portfolio stress loss, margin utilisation and liquidation distance.

The venue's liquidation price is an estimate under its current assumptions, not a guaranteed exit price or a fixed boundary. IDEAL must not treat distance to liquidation as a substitute for stop/exit risk, nor assume it can close at the liquidation price.

### 6.8 Margin mode, netting and hedge assumptions

Isolated and cross margin change how losses propagate through collateral:
- Isolated margin separates the collateral/risk assessment of a position, but the position can still be liquidated independently.
- Cross margin shares equity across positions using the applicable collateral pool; one position's loss can impair other positions.
- Portfolio margin may recognise offsets using a venue-specific model; those offsets are not automatically valid under IDEAL's own stress assumptions.

The architecture must represent the actual account and position mode, collateral scope, settlement currency and venue-specific treatment of long/short legs. It must not assume that opposite positions cancel risk or funding. It must not assume that margin is netted across separate accounts or venues.

Hedge credit should be granted only where the relationship is economically justified, executable under stress, supported by reliable data and explicitly represented in the stress model. Basis, correlation breakdown, funding mismatch, execution leg risk, venue failure and liquidation asymmetry can make a nominal hedge fail.

### 6.9 Funding and perpetual basis risk

Funding is a direct cash-flow component of holding perpetual contracts, not a cosmetic market indicator. Official venue documentation shows that:
- funding is calculated from position value and the applicable funding rate;
- positive and negative funding reverse which side pays;
- position value is venue/contract-specific and may use mark price, contract multiplier and inverse conversion;
- funding is charged only to positions held at the applicable funding time;
- settlement intervals and rate limits can vary by contract and may be adjusted during extreme market conditions;
- funding deductions can reduce available collateral or isolated margin and move liquidation risk closer.

Sources:
- Binance funding rates and settlement intervals: https://www.binance.com/en/support/faq/detail/360033525031
- Binance funding interval updates: https://www.binance.com/en/support/announcement/detail/98d6b24d3e5c4f84a8ed04087997d8d0
- Bybit funding fee calculation and dynamic interval behaviour: https://www.bybit.com/en/help-center/article/Funding-fee-calculation
- OKX funding fee mechanism, including linear/inverse valuation and dynamically adjusted settlement frequency: https://www.okx.com/help/perps-funding-fee-mechanism

Provisional implications:
- Funding estimates must be versioned with contract, rate, interval, settlement timestamp and source.
- The risk model should calculate projected funding cash flows under base and stressed funding scenarios, in the settlement asset and a reporting currency.
- It must distinguish predicted rates from final settled rates and reconcile actual funding events into capital state.
- It must not assume the usual funding interval remains fixed. A venue may change interval or limits.
- Funding received must not be treated as guaranteed income or assumed to offset unrelated funding liabilities.
- Funding costs should enter planned holding-period risk, stress loss and net expected trade economics.
- Perpetual basis risk must be measured separately from spot/index movement. A hedge can remain directionally neutral while suffering basis divergence, funding imbalance or venue-specific pricing dislocation.

### 6.10 Dynamic venue risk parameters

Bybit's published risk-limit material states that market-liquidity assessments can lead to changes in risk limits, initial and maintenance margin rates, maximum leverage and position limits. The applicable risk tier can also change as marked position value changes.

Source: https://www.bybit.com/en/help-center/article/Risk-Limit-Perpetual-and-Expiry-Contracts

Provisional implications:
- Instrument and account risk parameters are time-varying inputs, not static constants.
- Venue parameter changes need source, effective time, retrieval time, version and affected instruments/accounts.
- Risk calculations must recompute after a tier or parameter change.
- A risk-increasing proposal must be rejected or restricted if current applicable parameters cannot be established.
- Existing positions require continuous re-evaluation when maintenance margin, leverage caps, position limits or funding schedules change.
- Historical research and backtests must use point-in-time venue parameters where available, not today's values applied retrospectively.

### 6.11 Risk-budget hierarchy and reservation

Research a hierarchical risk-budget model:
1. owner-approved total portfolio risk capacity;
2. portfolio allocations by instrument, risk cluster or strategy family;
3. bounded strategy allocations;
4. per-trade planned and stressed risk budgets;
5. order-level reservations for all potentially executable quantity.

The sum of allocations and reservations must not exceed the applicable parent budget. An unused allocation must not be silently borrowed by another strategy. A reserve for model error, execution uncertainty and correlated stress should be considered explicitly rather than allocating the entire nominal risk budget.

A risk budget should be reserved when an order becomes potentially executable, not only after it fills. For partial fills, filled exposure transitions into position risk and the unfilled remainder continues to reserve order risk. The reservation is released only after a confirmed terminal order state or other verified state transition. Unknown acknowledgement/cancellation state retains the conservative reservation.

The risk engine must avoid double-counting a filled quantity as both an open order and a position, while preserving an auditable transition between the two. Multiple simultaneous orders must be tested under plausible fill combinations. Risk budgets should use explicit currency conversion sources, timestamps and conservative treatment of conversion uncertainty.

Dynamic risk allocation, if eventually permitted, must be deterministic, bounded by owner-approved policy and capable of reducing risk as conditions deteriorate. Strategy performance, recent losses or AI-generated confidence must not automatically expand risk capacity. Any change to the accepted D-006 or D-008 numerical policies requires explicit owner approval and a superseding decision record.

## 7. Provisional control lifecycle

### 7.1 Pre-action controls

A proposal should be rejected if required policy, instrument, portfolio, order or market inputs are missing, invalid, stale, contradictory or outside approved bounds.

Investigate hard checks for:
- permitted market/instrument/account scope;
- current policy and strategy eligibility;
- maximum order size and position size;
- per-trade, strategy and portfolio risk budgets;
- gross/net exposure and concentration;
- current and projected margin;
- venue risk tier and maximum leverage;
- price tolerance and market-data reasonability;
- liquidity and stressed close-out;
- duplicate/replayed proposal or order;
- working-order and partial-fill exposure;
- rate/message limits and venue constraints.

### 7.2 Continuous monitoring

Risk must be recalculated after material changes, including fills, cancellations, amendments, price changes, funding, balance movements, collateral valuation, margin-tier changes, venue notices and reconciliation discrepancies.

A pre-trade approval is not a permanent guarantee that the resulting position remains within risk limits.

### 7.3 Risk states — provisional

Research a state model that distinguishes at least:
- **Normal:** all required controls and evidence current; actions permitted only within policy.
- **Restricted:** risk-increasing actions blocked or constrained; only explicitly permitted risk-reducing actions considered.
- **Halted:** new exposure prohibited; emergency control policy invoked.
- **Recovery required:** normal authority remains disabled until reconciliation and integrity checks pass.
- **Unknown:** state or evidence cannot be trusted; fail closed for risk-increasing actions.

Operational health and security assurance states remain separately assessed. A risk state must not be inferred solely from a process heartbeat.

### 7.4 Kill switch and containment

A kill switch is a final backstop, not the primary risk control. Design it to be independently invocable, permission-protected, auditable and impossible for the strategy/agent being constrained to override.

Distinguish:
- stop authorising new risk;
- cancel unfilled risk-increasing orders;
- prevent order amendments that increase risk;
- preserve or permit specifically authorised risk-reducing actions;
- close positions only under a separately defined, owner-approved policy.

Do not assume that "cancel all" or "close all" is always safest: cancellation can remove protective orders, while market closing can incur severe slippage or be impossible during disruption. Each containment action needs explicit preconditions, limitations and recovery behaviour.

## 8. Cross-pillar contracts

### 8.1 Risk management ↔ data integrity

Risk consumes only reconciled and provenance-backed positions, orders, balances, instrument metadata and market inputs. Unknown/stale/contradictory data must be explicit. The risk engine must not validate its own source data as the sole assurance mechanism.

### 8.2 Risk management ↔ system health

Health supervision independently checks calculation freshness, risk-service availability, policy version, monitoring continuity, exchange connectivity, order reconciliation and recovery state. A failed or stale critical risk control must cause risk-increasing authority to be withheld.

### 8.3 Risk management ↔ security

Security enforces least privilege for policy changes, risk decisions, execution permissions and emergency controls. Strategy and AI identities cannot change policy or override risk decisions. Policy and audit records require integrity protection.

### 8.4 Risk management ↔ execution

Execution receives only a precisely scoped, current authorisation. Order submission, acknowledgement, fill, partial fill, cancellation and rejection states must reconcile against independent venue evidence where available. Unknown submission outcome must not cause blind resubmission.

## 9. Failure modes requiring explicit design

- Market data is stale but appears syntactically valid.
- Mark price and independent reference price diverge.
- Instrument metadata or margin tiers change without notice.
- Account balance snapshot is incomplete or delayed.
- Exchange position differs from IDEAL's internal position.
- Order acknowledgement is lost after venue acceptance.
- Cancel request times out while the order remains live.
- Duplicate order is submitted after retry.
- Partial fills arrive out of order.
- Funding debit or fee is missing from account reconciliation.
- Collateral value changes or stablecoin depegs.
- Risk calculator, policy registry or risk monitor stops.
- Risk monitor and trading process share a common failure.
- System clock drifts and corrupts freshness/order sequencing.
- Audit write fails during a risk decision.
- Security incident compromises policy, credentials or market data.
- Kill switch is unavailable or has insufficient permissions.
- Recovery restores a stale or inconsistent portfolio snapshot.

For each, define detection evidence, immediate safe state, permitted risk-reducing actions, escalation, recovery checks and audit record.

## 10. Verification and testing research requirements

The eventual verification strategy should include:
- exact contract and margin formula tests against authoritative venue examples;
- property/invariant tests for exposure and position calculations;
- boundary tests at risk-tier transitions;
- precision, rounding and decimal arithmetic tests;
- linear and inverse contract tests;
- order lifecycle replay and idempotency tests;
- partial fill, duplicate, delayed and out-of-order event tests;
- stale, missing, corrupt and contradictory market/account data tests;
- portfolio correlation and concentration scenarios;
- stress and gap scenarios with fees, funding, spread, slippage and market impact;
- risk policy versioning and permission tests;
- kill-switch and fail-closed tests;
- fault injection for service, clock, network, storage and audit failures;
- reconciliation and recovery tests;
- independent calculation cross-checks;
- reproducibility of every recorded risk decision.

No backtest or simulation should be treated as proof of safe execution. Backtests must include realistic fees, funding, slippage, liquidity, latency, position sizing, survivorship and look-ahead controls, plus out-of-sample and regime analysis.

## 11. Unresolved research questions

1. What should the authoritative equity basis be for each risk limit: venue equity, reconciled account equity, conservative available equity, or multiple explicitly named measures?
2. How should unrealised P&L, funding, fees, collateral haircuts and pending transfers enter equity and risk budgets?
3. What portfolio stress methodology is proportionate and robust for crypto perpetuals without importing unjustified traditional-market assumptions?
4. How should correlations and offsets be recognised, capped or denied under stress?
5. What liquidity horizon and close-out assumptions are appropriate by instrument and position size?
6. Which warning, throttle, strategy suspension and portfolio drawdown layers should sit below the existing D-008 hard boundary?
7. What is the safe treatment of protective orders when a kill switch cancels working orders?
8. What independent venue evidence is available for order/position reconciliation for candidate exchanges?
9. How should policy changes, temporary exceptions and recovery approvals be governed?
10. Which venue and account modes, if any, will eventually be selected? No venue has been selected or authorised.

## 12. Research limitations and next work

This is an initial research tranche, not a complete risk architecture. The sources establish useful principles and demonstrate exchange-specific mechanics, but they do not settle IDEAL's equity semantics, portfolio model, numerical thresholds, venue, margin mode, execution policy or recovery authority.

Next research should deepen:
1. risk authority, policy governance and deterministic decision contracts;
2. capital/equity accounting and portfolio-state semantics;
3. exposure, risk-budget allocation and sizing across linear/inverse contracts;
4. margin, collateral, leverage, liquidation and risk-tier modelling;
5. portfolio stress, correlation, concentration and liquidity;
6. funding, basis, market and execution risk;
7. strategy/model risk and progression gates;
8. loss limits, drawdown and capital-preservation layers;
9. venue/counterparty and operational risk;
10. emergency controls, failure containment and recovery;
11. independent assurance, audit and test acceptance criteria;
12. cross-pillar contract review.

No implementation or runtime work is authorised by this draft.


## 13. Research tranche 2 — capital semantics and contract-aware sizing (17 November 2026)

**Status:** Provisional research findings. No owner-approved change to D-006, D-008, venue selection, account mode or execution authority.

### 13.1 Updated official evidence

- OKX API documentation distinguishes `totalEq`, `adjEq` and `availEq`. Adjusted equity deducts collateral haircuts and is used in the venue's margin-ratio calculation; available equity has separate restrictions. The same documentation describes initial margin and maintenance margin as separate requirements, with pending orders included in relevant margin calculations. https://www.okx.com/docs-v5/en/
- Bybit's V5 instrument endpoint exposes linear and inverse contract categories, contract type, settlement coin, leverage filters, price tick, quantity step, minimum notional, funding interval and funding-rate bounds. It warns that some order quantity limits are adjusted periodically and that market-data delivery can be delayed during extreme volatility. https://bybit-exchange.github.io/docs/v5/market/instrument
- Bybit's risk-limit endpoint publishes risk tiers, position limits, initial and maintenance margin rates, maximum leverage and maintenance-margin deductions. https://bybit-exchange.github.io/docs/v5/market/risk-limit
- Binance's official futures calculator documents different P&L and initial-margin equations for USDⓈ-margined linear contracts and COIN-margined inverse contracts. https://www.binance.com/en/support/faq/detail/360036498511
- Binance's P&L documentation states that USDⓈ-M and COIN-M contracts settle in different collateral currencies; unrealised P&L uses mark price while realised P&L uses last price in the described calculation. https://www.binance.com/en-AU/support/faq/detail/3a55a23768cb416fb404f06ffedde4b2
- Bybit's 12 August 2026 USDT-contract P&L guidance confirms average-entry-price treatment, settlement in USDT, and that leverage affects required collateral rather than directly multiplying P&L for unchanged position size. https://www.bybit.com/en/help-center/article/Profit-Loss-calculations-USDT-Contract
- Bybit's inverse-contract P&L guidance demonstrates reciprocal-price P&L and settlement in the underlying coin; it also separates position P&L from fees and funding in closed/realised P&L calculations. https://www.bybit.com/en/help-center/article/Profit-Loss-calculations-Inverse-Contracts

These are venue-specific examples. They must not be generalised across all products, contract specifications, account modes or future versions.

### 13.2 Authoritative capital semantics — provisional recommendation

The capital model should preserve at least four separately named measures:

1. **Economic equity:** best estimate of net economic value of explicitly included assets and liabilities, with valuation source, timestamp and uncertainty.
2. **Risk-adjusted equity:** conservative capital basis after approved deductions for collateral haircuts, liabilities, stale/uncertain valuations, concentration and conversion uncertainty.
3. **Venue margin equity:** venue/account-mode-specific value used by that venue's margin and liquidation system.
4. **Available margin/equity:** venue-reported capacity currently available for additional margin requirements, subject to venue rules and order reservations.

Do not use available margin as wealth, portfolio equity or a standalone risk budget. Do not treat unrealised gains as cash or transferable collateral. Do not assume cross-venue collateral or margin netting.

**Provisional recommendation for D-006:** if the existing 0.5% per-trade target is retained, define its denominator as an explicitly versioned IDEAL risk-adjusted equity measure, rather than venue available margin or a raw exchange headline equity field. This is a design recommendation only; the owner has not yet confirmed the intended equity basis. The 0.5% value itself is not validated by this research.

**D-008 preservation:** the hard daily-loss boundary remains exactly as accepted: 10% of UTC day-start equity, realised plus unrealised P&L, followed by a 24-hour cooldown. This research does not redefine its denominator or reset semantics.

Capital state should separate immutable financial events (deposits, withdrawals, realised trading P&L, fees, funding, rebates, liquidation charges and adjustments) from time-varying valuations (unrealised P&L, collateral marks and FX conversion). Internal transfers must not become P&L. A realised event must not be counted again in the valuation layer. Pending transfers must not be counted as settled spendable capital.

For multi-currency accounts, retain native-currency balances and liabilities as first-class records. A reporting-currency aggregate must identify each conversion source, timestamp, haircut and uncertainty. Missing/stale conversion blocks risk-increasing use of the affected value; it must not silently become zero or use an unlabelled cached rate.

### 13.3 Contract-aware P&L and position sizing

A single universal quantity formula is unsafe. The calculation must be selected by an immutable, versioned instrument specification that defines contract family, linear/inverse payoff, contract multiplier/face value, quantity unit, quote currency, settlement currency, tick/lot increments, minimum notional, fee basis, funding basis and venue risk tier.

For a simple linear contract, the venue's exact contract specification determines the payoff. A common base-quantity form is:

`PnL_settlement = side × quantity × multiplier × (exit_price − entry_price)`

For an inverse contract with fixed quote-currency face value, a common form is:

`PnL_coin = side × contracts × face_value × (1 / entry_price − 1 / exit_price)`

Here `side` is +1 for long and −1 for short, but the adapter must verify the venue's sign convention and contract multiplier. These equations are explanatory patterns, not universal venue formulas. The Binance and Bybit examples above show why settlement currency and inverse reciprocal-price conversion must be explicit.

For each proposed trade, calculate total loss in a single explicitly named risk-accounting currency under a defined adverse exit scenario. Include, as applicable:
- entry and exit taker/maker fees using the applicable fee tier and likely order type;
- spread crossing and expected slippage;
- depth-sensitive market impact and partial-fill/leg risk;
- funding paid over the intended holding horizon, plus stressed interval/rate changes;
- settlement-currency-to-risk-currency conversion at a conservative scenario rate;
- stop gap-through and adverse exit-price reserve;
- any venue-specific close, liquidation or other charges that can reasonably be modelled.

Do not treat a stop trigger as a guaranteed execution price. Planned stop loss, adverse execution loss and portfolio stress loss remain separate outputs. If the stop is absent, invalid, stale or cannot be mapped to a credible exit scenario, ordinary stop-based sizing is not available; a separately approved risk model would be required.

The general sizing contract should be:

- determine the approved trade budget from the named equity basis and policy version;
- calculate contract-specific loss for candidate quantity under base and adverse execution assumptions;
- find the largest permitted quantity whose relevant loss measure remains within the applicable budget and all parent portfolio/strategy reservations;
- round quantity down to the venue's valid lot increment using exact decimal arithmetic;
- recalculate all risk after rounding and after applying minimum notional, maximum quantity, price bands and risk-tier constraints;
- reject rather than round up if minimum executable size exceeds the permitted budget;
- reject if any critical instrument parameter, fee tier, conversion rate, market input or venue constraint is unknown, stale or contradictory.

For nonlinear inverse P&L, fee/funding conversion, tiered margin or other non-linearities, use a tested monotone search over valid discrete quantities rather than assuming a linear closed-form denominator. Verify monotonicity for the supported contract model; if it is not monotone, enumerate the bounded valid quantity domain or reject the unsupported case. Use decimal/fixed-point arithmetic with explicit rounding rules; binary floating point must not decide a hard limit.

### 13.4 Risk budget is not margin capacity

The sizing engine must calculate separate ceilings and use the strictest applicable result:
- trade planned-loss budget;
- stressed/adverse-execution loss budget;
- portfolio and correlated-risk allocation;
- gross/net exposure and concentration limits;
- venue initial-margin and maintenance-margin constraints;
- liquidation-buffer constraints under stressed prices, fees, funding and collateral haircuts;
- instrument order/position limits and quantity filters;
- liquidity/close-out capacity.

Configured leverage only affects margin requirements and venue constraints; it does not make an unchanged notional position safer or reduce its price sensitivity. A strategy must not increase size because a venue offers a higher leverage setting. Available margin is a venue constraint, not a substitute for IDEAL's risk budget.

### 13.5 Risk reservations and state transitions

A proposed order reserves the risk of its potentially executable quantity before submission. On partial fill, the filled quantity transfers from order reservation to open-position exposure atomically in the risk state; residual quantity remains reserved. Avoid counting the filled amount twice. Release residual reservation only after confirmed terminal venue state. If acknowledgement, cancel or reconciliation state is unknown, retain the conservative reservation and block conflicting risk increases.

Simultaneous orders must be assessed under plausible joint-fill combinations, including opposing orders, conditional triggers, hedge-mode legs and multiple strategies. Netting is allowed only under explicit, tested venue semantics and IDEAL stress assumptions. Otherwise, gross exposure and worst plausible fill state govern.

### 13.6 New failure and verification requirements

Add tests for:
- linear and inverse P&L across long/short, partial close, add-to-position and exact settlement currency;
- contract multipliers, quantity units, tick/lot rounding and minimum notional boundaries;
- reciprocal-price conversion and FX rate freshness for inverse settlement;
- maker/taker fee changes, funding interval changes and holding-period stress;
- monotonic discrete sizing and proof that rounded quantity never exceeds the risk budget;
- minimum executable quantity exceeding budget (must reject);
- risk-tier transitions that alter margin requirements or max leverage;
- collateral haircut changes, depeg scenarios and unavailable collateral;
- pending transfers and internal transfers not being misclassified as P&L;
- multi-currency equity without silent conversion or double-counting;
- concurrent orders and all-fill/partial-fill/cancel-timeout combinations;
- exact agreement with independently implemented venue formula examples.

Every calculation result must retain the instrument-specification version, fee/risk-tier snapshot, source timestamps, FX inputs, policy/equity basis, scenario assumptions, rounding decisions and code/model version.

### 13.7 Open owner decision

The most important owner clarification remains: **what did D-006 mean by "equity" when the 0.5% per-trade risk target was accepted?** The current research recommendation is IDEAL risk-adjusted equity, calculated from explicitly included assets and liabilities with conservative collateral/valuation treatment. It is not yet accepted. No need to decide this during research; it can remain an explicit architecture decision until the capital-state contract is ready for review.

### 13.8 Next tranche

Continue with portfolio stress methodology, correlation and concentration; margin/collateral/liquidation buffers; liquidity-adjusted close-out; and loss/drawdown control layers. No numerical limits, venue, account mode or runtime implementation are adopted by this tranche.


## 14. Research tranche 3 — portfolio stress, correlation, concentration and liquidity (17 November 2026)

**Status:** Provisional research findings. No numerical thresholds, venue, account mode, margin methodology or risk-policy change is approved.

### 14.1 Evidence reviewed

- CME SPAN assesses portfolio loss across a set of market scenarios rather than treating each position independently. https://www.cmegroup.com/solutions/risk-management/performance-bonds-margins/span-methodology.html
- CME SPAN 2 describes a portfolio-margin framework combining historical risk, stress risk, liquidity and concentration. Its historical component uses volatility/correlation scaling; stress includes historical and hypothetical events; liquidity cost uses bid/ask evidence; concentration add-ons relate to holdings relative to market activity/average daily volume. https://www.cmegroup.com/clearing/risk-management/span-overview/span-2-methodology.html
- CME's SPAN reference materials describe a 16-scenario risk array. This is an example of a defined scenario grid, not a sufficient crypto stress set. https://www.cmegroup.com/solutions/risk-management/performance-bonds-margins/span-reference-documents.html
- A 2026 SSRN working paper examining Hyperliquid around the 10 October 2025 liquidation event reports that quoted spreads recovered faster than inside depth; the authors report persistent depth contraction in four of five studied contracts. This is a single-event, single-venue working paper and must be replicated before operational use. https://papers.ssrn.com/sol3/Delivery.cfm/6636998.pdf?abstractid=6636998&mirid=1&type=2
- A 2026 SSRN working paper on Bybit BTCUSDT reports that displayed depth was an incomplete proxy for executable liquidity during a studied liquidation cascade and that hidden liquidity estimates changed during the event. This is an author-specific inference from one venue/contract/event window, not a universal liquidity rule. https://papers.ssrn.com/sol3/Delivery.cfm/6891658.pdf?abstractid=6891658&mirid=1&type=2
- A 2026 SSRN working paper on the 10 October 2025 crash reports sharp intraday basis, spread and mark/reference-price dislocations across selected assets/venues. Treat as a scenario-generation lead, not independently established universal behaviour. https://papers.ssrn.com/sol3/Delivery.cfm/6579278.pdf?abstractid=6579278&mirid=1&type=2
- A 2026 peer-reviewed journal article studies temporal dynamics of funding-rate correlations and market integration across 26 exchanges and 812 symbols over November 2025–January 2026. Its reported gradual drift and heterogeneous integration support measuring dependence dynamically rather than assuming fixed cross-market relationships. https://www.mdpi.com/2227-7072/14/5/103
- A 2026 study of funding markets across 26 CEX/DEX venues reports materially different integration and information-flow patterns. Its sample is short relative to full market cycles, so it is evidence of fragmentation, not a stable long-run correlation matrix. https://www.mdpi.com/2227-7390/14/2/346

Institutional margin frameworks are references for methodology only. IDEAL is not a clearing house, exchange or financial market infrastructure and must not claim equivalent validation or regulatory status.

### 14.2 Portfolio risk must be scenario-based and multi-dimensional

A portfolio risk view should combine distinct measurements rather than compressing everything into one score:

1. **Deterministic exposure:** gross and net notional, direction, leverage/effective leverage, settlement currency, venue, strategy and risk-cluster exposure.
2. **Historical distribution:** realised portfolio P&L under point-in-time historical returns and observed cross-asset co-movements.
3. **Tail-risk statistics:** VaR and Expected Shortfall as supplementary distributional summaries with explicit horizon, confidence, sample and estimator.
4. **Hypothetical stress:** coherent shocks not adequately represented in the historical sample.
5. **Liquidity-adjusted close-out:** estimated cost and time to reduce exposure under normal and stressed market conditions.
6. **Concentration add-ons:** incremental risk from large participation, crowded exposure, shared factors, collateral, venue or settlement dependencies.
7. **Operational/venue stress:** delayed/corrupt data, exchange outage, margin-tier changes, mark/index divergence, funding changes and liquidation mechanics.

These measures answer different questions. A low historical VaR does not override a hard exposure limit, a severe scenario loss or an inability to exit. A high estimated correlation does not justify automatic netting, and a low recent correlation does not prove diversification.

### 14.3 Dependence and correlation treatment

A single static Pearson correlation matrix is inadequate as the sole portfolio diversification model. Research and define a layered dependence representation:

- rolling and exponentially weighted correlations as descriptive monitoring;
- downside/conditional correlation during negative market returns and volatility expansion;
- common-factor exposures (BTC beta, broad crypto market, sector/theme, stablecoin/settlement asset, funding and basis);
- stress-period co-movement and conditional dependence;
- liquidity correlation: whether several positions become difficult to exit at the same time;
- venue/counterparty dependence: shared venue, oracle/reference source, custody, collateral pool and infrastructure;
- strategy dependence: multiple strategies using the same features, signals, market data or trade direction.

Correlation estimates must be point-in-time and carry sample size, lookback, missing-data policy, shrinkage/estimator version, regime and confidence/uncertainty. Do not infer independence from insufficient history. New or illiquid assets should receive conservative exposure treatment until evidence supports otherwise.

**Conservative hedge-credit rule:** no diversification or hedge credit should be granted solely because two instruments have historically low or negative correlation. Credit requires economic rationale, reliable point-in-time data, executable hedge legs, basis/funding/settlement modelling, venue independence analysis and stress tests. Otherwise use gross exposure and adverse joint-fill scenarios.

### 14.4 Concentration taxonomy

Concentration should be measured across overlapping dimensions, because a portfolio can be diversified in one dimension and concentrated in another:

- single instrument and underlying;
- correlated underlyings, sectors, narratives and common market beta;
- long/short gross exposure and one-sided directional exposure;
- strategy, model, signal family and shared feature dependency;
- venue, account, margin pool, counterparty and execution route;
- collateral asset, stablecoin, settlement currency and FX conversion source;
- funding payer/receiver side and settlement-time clustering;
- order-book liquidity, market participation and close-out horizon;
- common oracle, mark/index source, data provider, network or operational dependency.

The portfolio state should preserve both gross and net values. Netting can conceal large offsetting gross positions that carry separate liquidation, funding, liquidity, venue and basis risks.

### 14.5 Coherent stress scenario design

Stress scenarios must apply internally consistent shocks across all affected positions and risk factors. Do not shock each instrument independently and then sum impossible combinations; equally, do not assume that historically correlated instruments will maintain a hedge in stress.

Initial scenario families to research and later parameterise:

**Market and correlation**
- BTC market-wide shock with altcoin beta and downside correlations increasing;
- simultaneous BTC/ETH/major-altcoin gaps and volatility expansion;
- sector/theme-specific shock with contagion to correlated tokens;
- correlation inversion or hedge breakdown;
- abrupt basis divergence between spot, index, mark and perpetual prices.

**Liquidity and execution**
- spread widening plus multi-level depth depletion;
- displayed depth cancellation before or during the close-out;
- market impact increasing non-linearly with participation;
- partial fills, delayed fills and failed hedge leg;
- liquidation flow competing with IDEAL's exit orders;
- venue-specific liquidity fragmentation and cross-venue price dislocation;
- time-to-liquidate extending beyond the intended risk horizon.

**Funding, collateral and margin**
- funding-rate shock, interval shortening and adverse payer-side exposure;
- stablecoin depeg or collateral haircut increase;
- settlement-currency depreciation against the risk-accounting currency;
- risk-tier migration that increases initial/maintenance margin or lowers maximum position size;
- isolated position liquidation versus cross-margin contagion;
- collateral or transfer unavailable when needed.

**Venue and operational**
- exchange outage, API throttling, WebSocket gap and delayed order/cancel acknowledgements;
- stale or divergent mark/index inputs;
- venue withdrawal restrictions, counterparty impairment or insolvency;
- simultaneous liquidation/ADL and degraded market data;
- internal risk monitor or audit storage unavailable during stress.

Each scenario must define shock source, calibration date, factor mapping, horizon, affected positions, price/volatility/funding/liquidity/margin assumptions, valuation and conversion rules, close-out sequence, and known limitations. Preserve both scenario results and the exact input versions.

### 14.6 Liquidity-adjusted close-out model

Displayed order-book depth is an observation, not a guarantee of executable liquidity. The model should not assume all displayed orders remain available, and should not assume hidden liquidity will be present. Historical liquidation-event papers provide reasons to test both effects, but not enough evidence to hard-code a universal adjustment.

Estimate close-out cost and capacity by:
- side-aware spread and depth at the intended decision time;
- walking multiple book levels for the proposed size;
- participation relative to recent traded volume and volume distribution;
- empirical impact/slippage residuals where representative parent-order/fill data exists;
- order-book update age, gaps, sequence integrity and feed-source reliability;
- volatility, spread and depth response under stress;
- time-to-liquidate under conservative participation limits;
- partial-fill and residual-position risk;
- multi-venue execution only if venue access, legal eligibility and transfer/hedge assumptions are separately approved.

Normal conditions and stress conditions need separate liquidity estimates. A static percentage haircut on current top-of-book depth is not adequate. If reliable liquidity evidence is absent, apply a conservative cap or reject the risk increase rather than inventing capacity.

Concentration charges should reflect the incremental close-out cost of larger positions. Average daily volume can inform a threshold but is not immediate executable capacity; intraday volume seasonality, order-book depth, market impact and event conditions also matter.

### 14.7 Historical risk, VaR and Expected Shortfall limitations

Historical VaR/Expected Shortfall can summarise observed losses but cannot guarantee coverage of unobserved tails. Their outputs are sensitive to lookback, sampling frequency, horizon, missing data, regime mix, stale/biased venue prices and the quality of point-in-time instrument universe data.

Provisional requirements:
- use point-in-time universe and delisted/expired instruments where available;
- avoid look-ahead, survivorship and revised-data leakage;
- retain full return and portfolio-construction provenance;
- distinguish close-to-close, intraday and event-driven horizons;
- assess tail estimates with confidence intervals and sample sufficiency;
- supplement historical scenarios with hypothetical and reverse stress tests;
- use filtered/scaled historical shocks only with documented calibration and independent validation;
- never allow VaR/ES to override hard limits or fail-closed controls.

A short, highly overlapping sample can create an illusion of a large sample. Effective independent observations and regime coverage matter more than raw row count. Crypto's continuous market, structural breaks, token listings/delistings, venue fragmentation and liquidation mechanics require explicit handling.

### 14.8 Proposed portfolio risk outputs

The portfolio risk state should expose auditable, separately named values rather than a black-box score:
- gross and net notional by instrument, underlying, factor, strategy and venue;
- current and stressed directional/factor exposure;
- concentration measures and applicable limits;
- base and stress portfolio P&L/loss by scenario;
- historical VaR and Expected Shortfall with model metadata;
- liquidity-adjusted close-out cost, participation and estimated liquidation horizon;
- funding and basis exposure;
- collateral, settlement-currency and venue concentration;
- margin and stressed liquidation buffer by venue/account mode;
- unallocated risk capacity and reserved order risk;
- data/model freshness, confidence/coverage and explicit unknowns.

The decision authority must preserve the component outputs and reason codes behind any restriction. It must not let an opaque composite score hide a failed hard control.

### 14.9 Verification requirements

Add independent tests and scenario fixtures for:
- correlated downside shocks and correlation convergence during stress;
- diversification disappearing under joint market/liquidity stress;
- no hedge credit when history is insufficient or inputs are stale;
- common factor and shared venue/collateral concentration;
- gross exposure remaining visible despite net offsets;
- nonlinear market impact and depth depletion at increasing order sizes;
- displayed depth vanishing, partial fills and time-to-liquidate extension;
- liquidity cost sensitivity to order size, spread, volatility and participation;
- funding shock plus adverse price/basis movement;
- collateral depeg/haircut and risk-tier migration;
- scenario reproducibility from immutable point-in-time inputs;
- VaR/ES backtesting and exception analysis without using it as sole risk control;
- reverse stress tests identifying conditions that breach capital, margin or close-out capacity;
- independent recomputation and metamorphic invariants for portfolio aggregation.

### 14.10 Research limitations and next tranche

CME materials describe mature listed-derivatives margin methodologies; they are not direct crypto perpetual implementations. Recent liquidation-event and liquidity studies include working papers, single-event windows and single-venue samples. They are useful for identifying failure modes and scenario candidates, not for adopting fixed haircuts or thresholds.

Next research: margin/collateral/liquidation-buffer mechanics across account modes; risk-limit migration; liquidity horizon calibration; drawdown and loss-containment layers; model/strategy risk; and independent assurance. No numerical policy, venue, account mode or implementation is adopted.
