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


## 15. Research tranche 4 — margin, collateral and liquidation-buffer architecture (17 November 2026)

**Status:** Provisional research findings. No venue, margin mode, collateral asset, margin parameter, numerical buffer or execution control is selected or approved.

### 15.1 Official evidence and limits

- Bybit's UTA documentation describes isolated, cross and portfolio margin modes with materially different liquidation scopes. Its isolated process uses mark price, tier-dependent maintenance margin and a staged response that can cancel position-increasing orders, partially reduce positions and then liquidate. https://www.bybit.com/en/help-center/article/UTA-Trading-Rules-Liquidation-Process
- Bybit's collateral value ratio documentation explains that supported assets are valued using an index price and an asset-specific collateral ratio, with tiered ratios and periodic changes. Positive balances may receive discounted collateral value; negative balances are treated differently. https://www.bybit.com/en/help-center/article/Assets-Collateral-Value-Ratio-List-UTA
- Bybit's UTA FAQ distinguishes margin balance from available balance and explains that margin valuation includes index-price conversion and collateral ratios; unrealised profit may be available for trading but not transferable. https://www.bybit.com/en/help-center/article/FAQ-Unified-Trading-Account
- OKX API documentation identifies separate account modes (futures, multi-currency margin and portfolio margin), and exposes account configuration, margin-mode and leverage scopes. Account mode and margin scope are not universal account-wide constants. https://www.okx.com/docs-v5/en/
- Binance's liquidation protocol describes cancellation of open orders, an IOC reduction attempt and transfer of residual bankrupt position to its insurance fund to the extent possible. The insurance fund is part of the venue's loss-allocation mechanism; it is not a guarantee that a trader's own position will exit at a chosen price. https://www.binance.com/en/support/faq/detail/360033525271
- The Bank of England's near-final supervisory statement published 16 November 2026 for supervised CCPs explains that large unexpected increases in initial margin can amplify liquidity strains. It discusses a trade-off among margin coverage, margin cost and margin reactivity, and anti-procyclicality measures. This is a supervisory reference for CCPs, not a rule directly applying to IDEAL. https://www.bankofengland.co.uk/paper/2026/ss/near-final-supervisory-statement-on-ccp-margin
- CPSS-IOSCO PFMI materials emphasise conservative collateral haircuts, concentration limits, risk-based margin and liquidity resources. These are principles for financial market infrastructures, not a classification of IDEAL. https://www.federalreserve.gov/frrs/regulations/appendix-cpss-iosco-principles-for-financial-market-infrastructures.htm
- CME SPAN 2 describes distinct historical/stress risk, liquidity and concentration components; its liquidity and concentration components illustrate why margin adequacy is not just a volatility calculation. https://www.cmegroup.com/clearing/risk-management/span-overview/span-2-methodology.html

### 15.2 Margin concepts that must remain separate

The system model must distinguish:
- **Initial margin (IM):** venue- or model-defined collateral requirement to open/increase exposure.
- **Maintenance margin (MM):** minimum equity/collateral requirement for maintaining exposure under the venue's rules.
- **Venue margin ratio / utilisation:** venue-defined account or position risk ratio; exact numerator, denominator and thresholds vary by mode and venue.
- **IDEAL risk budget:** owner-approved loss/exposure capacity. It is not derived from the amount of margin the venue permits.
- **Liquidation trigger estimate:** venue-reported or independently reconstructed estimate under current assumptions. It is not a guaranteed exit price.
- **Liquidation buffer:** distance and loss capacity between current market state and a modelled liquidation threshold, assessed under adverse changes in price, margin, fees, funding, collateral and liquidity.
- **Available margin:** venue-reported capacity for additional margin use, after venue-specific reservations and restrictions.

A position can be within its planned trade-loss budget and still be dangerously close to venue liquidation because the venue's collateral, margin tier, account mode or mark price differs from the assumptions used in sizing. Conversely, abundant venue margin does not mean the position is within IDEAL's portfolio risk budget.

### 15.3 Account and margin mode semantics

The adapter must discover and version actual account configuration rather than infer it from a default:
- isolated margin generally allocates margin to a position or instrument scope, limiting direct collateral contagion to other positions but not eliminating venue, settlement, liquidity or operational risk;
- cross margin shares eligible collateral across a defined venue account/currency scope, so a loss or haircut change in one position/asset may reduce the margin supporting others;
- portfolio margin applies a venue-specific portfolio risk model and may recognise offsets; its margin outcome is model-dependent and can change sharply if correlations, risk arrays, offsets, eligible products or model parameters change.

Do not assume that "hedged" positions cancel margin or liquidation risk. Venue hedge-mode semantics, netting, offsets, collateral pools and liquidation sequencing must be captured explicitly. Cross-venue netting or collateral transfer is never assumed.

For the initial architecture, model isolated, cross and portfolio margin as distinct adapter capabilities. Unsupported or incompletely understood modes must be rejected for risk-increasing actions, not approximated by a generic margin formula. The eventual supported subset is an owner decision after the venue and product scope are researched.

### 15.4 Collateral quality and haircut model

Collateral is not equivalent to cash at spot mark. For each collateral asset, preserve:
- native units and liability/borrow balance;
- valuation price/index and independent reference sources;
- settlement and conversion currency;
- venue eligibility and collateral scope;
- current venue collateral ratio/haircut and tier boundaries;
- IDEAL's separate conservative risk haircut;
- market depth, spread, volatility, stressed liquidity and time-to-liquidate;
- issuer, custodian, chain, bridge, reserve and redemption dependencies where applicable;
- concentration and wrong-way risk with the portfolio and the positions being margined;
- source, version, effective timestamp, retrieval timestamp and validity/freshness.

Venue haircuts are venue rules, not IDEAL's risk assessment. IDEAL may apply a more conservative internal haircut; it must never assume the venue will recognise the internal valuation. Collateral eligibility can change, and the value of an asset can fall at the same time its haircut worsens or the venue removes it from eligible collateral. This is a wrong-way / wrong-time liquidity risk.

Stablecoins must not be treated as risk-free cash. Model depeg, redemption/issuer stress, venue-specific conversion basis, liquidity gaps and collateral ratio changes. Correlated exposure matters: collateral that falls with the underlying position can fail precisely when margin is needed.

Tiered haircuts require marginal treatment at the correct quantity/value bands; applying one average ratio to the entire holding can overstate collateral. Negative balances, borrowings, liabilities and accrued fees/funding must be represented separately and not hidden by net asset presentation.

### 15.5 Collateral stress and availability

Stress collateral jointly with the portfolio:
- market price shock and volatility increase;
- spread/depth deterioration and delayed conversion;
- stablecoin depeg or loss of redemption access;
- collateral haircut increase or eligible-asset removal;
- oracle/index/FX divergence or stale pricing;
- venue withdrawal, transfer or internal conversion suspension;
- chain congestion, bridge impairment or custody/issuer failure;
- concentration tier crossing;
- simultaneous adverse movement in collateral and the margined positions.

Do not count funds as immediately available merely because they appear in economic equity. Distinguish owned, settled, venue-held, pledged, borrowed, encumbered, transferable, withdrawable and actually available margin. A transfer between wallets/accounts is not complete until confirmed by authoritative source evidence. Do not assume collateral can be moved between venues quickly enough to meet a margin shortfall.

### 15.6 Liquidation buffer and distance-to-liquidation

IDEAL should calculate more than a single liquidation price. Proposed separately named outputs:

1. Venue-reported liquidation trigger/price and timestamp, if available.
2. Independently reconstructed venue liquidation estimate using versioned venue rules and inputs.
3. Price-distance buffer in absolute and percentage terms, with direction-specific interpretation.
4. Equity/collateral buffer above estimated maintenance requirement.
5. Stressed liquidation buffer after joint price, mark/index basis, funding, fees, collateral haircut and risk-tier shocks.
6. Liquidity-adjusted buffer after estimated close-out impact, spread, depth depletion and gap-through.
7. Estimated time-to-liquidate under normal and stressed participation assumptions.
8. Model disagreement between venue-reported and independently reconstructed estimates.

A simple price distance can be misleading for cross/portfolio margin, inverse contracts, multi-currency collateral or tiered risk limits. In those cases, scenario-recompute account equity and maintenance requirement under each shock; do not rely on a one-dimensional price distance.

The venue's liquidation trigger is a last-resort boundary, not IDEAL's target operating boundary. IDEAL's own warning, restrict, reduce and stop states must activate with enough stressed headroom to act before the venue begins its liquidation process. Exact thresholds require later calibration and explicit approval; no numerical buffer is adopted here.

### 15.7 Venue liquidation mechanics and loss-allocation waterfall

For each venue/product/account mode, document the actual sequence and trigger semantics:
- mark/index/price source and trigger;
- order cancellation scope (risk-increasing only, all orders, instrument, currency or account);
- partial reduction / staged liquidation rules;
- close-out order type, time-in-force, price and execution assumptions;
- bankruptcy price / residual position treatment;
- insurance fund use and limitations;
- auto-deleveraging (ADL) or other counterparty loss-allocation mechanism;
- fees, penalties, settlement and residual liability treatment;
- event notifications, state transitions and reconciliation evidence.

Do not assume insurance funds protect a trader against losses or guarantee full recovery. Do not assume ADL will be predictable or avoidable. Venue liquidation can execute at materially different prices from a displayed estimate during fast markets, gaps or liquidity failures. IDEAL must model the trader's own adverse close-out path and residual loss; it must not rely on the venue's waterfall as a personal safety mechanism.

### 15.8 Independent shadow margin and reconciliation

Provisional architecture recommendation: maintain an IDEAL-side shadow calculation of venue margin and liquidation state, independently derived from versioned official rules and current account/position/instrument state. It is a monitoring and discrepancy-detection model, not a claim that IDEAL can reproduce every proprietary venue calculation exactly.

Reconcile at least:
- venue account mode and position/margin mode;
- wallet, equity, adjusted equity and available margin fields;
- positions, average entry, mark price, unrealised P&L and settlement currency;
- active orders, conditional orders and reserved margin;
- risk tier, IMR/MMR, maintenance deduction and leverage scope;
- collateral balances, haircuts, liabilities and borrowings;
- funding, fees, session settlement and other account adjustments;
- liquidation estimate and account risk ratios.

Compare the independent estimate with venue outputs using a versioned tolerance model. Explain differences caused by timing, rounding, hidden venue adjustments or incomplete public rules. If critical disagreement, stale inputs, missing positions/orders, unknown account mode or unversioned margin parameters exist, risk-increasing actions fail closed. Preserve the last known state but mark it stale; never silently substitute it as current.

### 15.9 Margin procyclicality and liquidity preparedness

Margin can rise when volatility, concentration or risk tiers worsen—exactly when liquidity is scarce and collateral is falling. The Bank of England's 2026 CCP guidance highlights the trade-off among coverage, cost and reactivity. IDEAL is not a CCP and should not copy regulatory initial-margin buffers mechanically, but should incorporate the failure mode into its own capital planning.

Requirements:
- simulate plausible margin increases before they occur;
- monitor margin parameter/tier changes and collateral haircuts;
- stress simultaneous position loss, collateral depreciation and higher maintenance requirements;
- retain liquidity headroom for adverse margin changes rather than sizing to the current minimum;
- do not assume margin can be funded by selling the same stressed asset at its displayed mark;
- avoid a risk policy that automatically increases position size whenever current margin appears cheap;
- review model responsiveness, false comfort in calm periods and sudden capacity collapse in stress.

A conservative buffer is not a cap on venue margin increases. If the venue increases requirements beyond IDEAL's capacity, the correct response is to reduce or prohibit risk increases and follow the approved containment process—not to weaken the model.

### 15.10 Verification and adversarial test requirements

Add deterministic fixtures and independent checks for:
- isolated, cross and portfolio margin semantics and their distinct contagion scopes;
- tiered initial/maintenance margin and threshold crossing in both directions;
- simultaneous position P&L, funding, fee, liability and collateral changes;
- collateral haircut tiers, concentration thresholds and eligible-asset removal;
- negative balance treatment and borrowed/encumbered collateral;
- stablecoin depeg and correlated collateral/position shock;
- stale, divergent or unavailable mark/index/FX prices;
- venue-reported vs independently reconstructed liquidation estimate;
- inverse contract, multi-currency and portfolio-margin nonlinearity;
- active/conditional orders and pending cancellations in margin calculations;
- liquidation ladder, IOC partial fill, failed close and residual position;
- insurance-fund/ADL event interpretation without assuming user protection;
- abrupt margin requirement increase under low liquidity;
- no risk increase when account mode, margin tier, collateral ratio or key state is unknown;
- fail-closed behaviour and audit trail under reconciliation failure.

Use boundary-value, property-based, metamorphic and fault-injection tests. Where venue-specific formulas are published, compare with official examples and independently implemented calculations. Any unresolved venue-specific calculation must be marked unsupported, not approximated without disclosure.

### 15.11 Research conclusions and unresolved choices

Provisional conclusions:
- Margin capacity is a venue constraint, not IDEAL's risk budget.
- Collateral quality, concentration, liquidity and wrong-way risk are first-class portfolio risks.
- Account mode determines the scope of margin contagion and liquidation; it must be discovered and modelled explicitly.
- Liquidation price is a moving estimate, not a guaranteed execution price or adequate standalone control.
- IDEAL should maintain independent shadow margin estimates and reconcile them against venue state, while treating proprietary/undocumented mechanics as uncertainty.
- Stress margin increases and collateral haircuts jointly with market losses and reduced liquidity.
- Venue insurance funds and ADL are loss-allocation mechanisms, not user guarantees.

Unresolved and deliberately not selected:
- exchange/venue and legal availability for the owner;
- account mode and margin mode;
- collateral assets or collateral concentration limits;
- internal haircut methodology and values;
- warning/restrict/reduce thresholds and liquidation-buffer minimums;
- whether any portfolio-margin or hedge offset capability will ever be supported;
- operational actions permitted during a margin or liquidation emergency.

Next tranche: drawdown controls, loss containment and capital preservation; then strategy/model risk and emergency controls. No numerical limits, venue, account mode or implementation is adopted by this tranche.


## 16. Research tranche 5 — drawdown controls, loss containment and capital preservation (17 November 2026)

**Status:** Provisional architecture research. No new threshold, cooldown, drawdown policy or emergency execution authority is approved.

### 16.1 Evidence reviewed

- FIA's July 2024 automated trading controls paper describes pre-trade maximum order size, maximum intraday position, price tolerance, cancel-on-disconnect, kill switches, order management, post-trade drop-copy reconciliation and conformance testing. It reinforces layered controls before and after order entry. https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf
- SEC Rule 15c3-5 guidance for US broker-dealers with securities market access requires pre-set aggregate credit/capital thresholds and rejection of erroneous/duplicative orders, access restrictions, immediate post-trade reports and regular control review. This rule does not directly apply to IDEAL's initial crypto-perpetual research scope; it is a control-design reference only. https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions/divisionsmarketregfaq-0
- The SEC's market-access final rule explains the rationale for controls that systematically limit financial exposure and prevent erroneous orders before they enter a market. Again, this is not a claim that IDEAL is subject to this securities-market rule. https://www.sec.gov/rules-regulations/2011/06/risk-management-controls-brokers-or-dealers-market-access
- FIA exchange risk-control material lists order/position limits, margin limits, kill switches, cancel-on-disconnect, throttles and order/trade drop-copy reconciliation as distinct controls. https://www.fia.org/sites/default/files/2025-01/Exchange%20Risk%20Controls%20%E2%80%93%20Overview%20of%20CME%20and%20ICE%20risk%20controls.pdf

### 16.2 Loss-control hierarchy

Risk controls should be layered from broad portfolio boundaries down to individual orders:

1. **Owner-level capital protection:** approved maximum portfolio loss/drawdown and permitted domain authority.
2. **Portfolio limits:** aggregate exposure, loss, concentration, liquidity, margin and correlated risk.
3. **Strategy/family limits:** allocations and containment for shared signals, models, instruments or execution dependencies.
4. **Instrument/position limits:** notional, direction, risk budget, leverage/margin and close-out constraints.
5. **Order controls:** maximum size/notional, price collar, duplicate/repeat order, message rate, stale-price and potential-fill checks.
6. **Runtime supervision:** market-data integrity, order/position reconciliation, loss and drawdown monitoring, heartbeat/disconnect controls.
7. **Emergency containment:** stop new risk, cancel specified orders, preserve/restrict risk-reducing actions, and separately authorised close-out procedures.

A lower-level control cannot override a higher-level boundary. Strategy-level stop logic is supplementary; the independent portfolio authority must be able to reject a strategy's risk increase even if the strategy believes its own stop remains valid.

### 16.3 Loss and drawdown are different measurements

Preserve separate metrics and baselines:

- **Realised P&L:** booked trading outcomes after venue accounting rules, including realised fees and funding where applicable.
- **Unrealised P&L:** current mark-based valuation with source, timestamp and price basis.
- **Net trading P&L:** realised plus unrealised P&L after applicable fees, funding and charges, without double-counting settled events.
- **Daily loss:** loss measured from a fixed UTC day-start baseline under the accepted D-008 definition.
- **Rolling-period loss:** loss over a defined rolling window; this is not reset at UTC midnight.
- **Peak-to-trough drawdown:** decline from a versioned equity high-water mark, with the peak and current equity measured on a consistent basis.
- **Capital impairment:** reduction in owner-defined risk-adjusted capital after external flows and approved valuation changes are treated consistently.
- **Stress loss:** scenario loss under specified adverse assumptions; it is not an observed P&L figure.

Daily loss can reset while a larger drawdown persists. A portfolio can be below its high-water mark while today's loss is small or positive. No one metric is sufficient. Keep all measures visible and separately governed.

### 16.4 Baseline, flow and accounting semantics

Loss and drawdown calculations must define how to treat:
- deposits and withdrawals;
- transfers between internal accounts/venues;
- realised P&L, unrealised P&L, fees, funding, rebates and liquidation charges;
- settlement and session resets;
- collateral revaluation and FX conversion;
- stale/missing valuations and corrections;
- account migration or venue reconciliation differences.

External cash flows must not be misclassified as trading profit/loss. Internal transfers must not create profit or loss. High-water-mark updates should be based on a consistent equity definition and flow-adjustment method. The system must preserve both raw equity observations and adjusted performance series so that an accounting convention cannot hide an actual loss.

D-008 remains unchanged: the hard daily-loss boundary is 10% of UTC day-start equity, realised plus unrealised P&L, followed by a 24-hour cooldown. Its precise reset, valuation, missing-data and recovery semantics must be formalised in the final contract before implementation; this research does not silently redefine them. This 10% is an outer hard boundary, not a target, a recommended normal drawdown or the only loss control.

### 16.5 Proposed loss-containment states

A deterministic state machine should govern the response. The final number and naming of states remain subject to architecture review, but the following separation is important:

- **Normal:** all required evidence and controls valid; actions remain within every approved limit.
- **Caution:** warning thresholds approached, volatility/liquidity deteriorating or loss accumulation abnormal; increase monitoring and constrain discretionary risk expansion.
- **Restricted:** block new risk or reduce permissible size; allow only actions explicitly classified as risk-reducing under reliable state.
- **Risk-off:** strategy-level activity stopped and risk-increasing orders prevented; cancel orders that could increase exposure where cancellation semantics are known.
- **Emergency:** critical control/data/security/reconciliation failure, hard loss breach or imminent uncontrolled exposure; invoke the pre-approved emergency policy and preserve evidence.
- **Recovery pending:** no automatic return to normal. Reconciliation, cause analysis, control-health checks and required owner approval must be completed.

Transitions must be monotonic in severity when evidence degrades. Recovery must be explicit and evidence-backed. A brief improvement in P&L or a single healthy heartbeat must not clear a risk-off state.

### 16.6 Separate the emergency actions

These actions have different effects and must not be represented by one ambiguous "kill switch":

1. **Block new risk:** reject new positions and orders that can increase exposure.
2. **Cancel risk-increasing orders:** submit cancellation for identified working/conditional orders; retain reservations until terminal cancellation/fill is confirmed.
3. **Cancel all orders:** may remove protective exits as well as risk-increasing orders. This must not be the default unless the approved emergency scenario requires it.
4. **Permit risk-reducing orders:** allow only validated actions that reduce exposure under conservative fill assumptions; a nominal reduce-only flag is not sufficient if venue semantics/state are unknown.
5. **Flatten/close positions:** market close-out can realise severe slippage and may be impossible during outage or illiquidity. It requires explicit pre-authorised policy, bounded execution logic and separate tests; it is not synonymous with stopping new orders.
6. **Disable automation/credentials:** isolate a compromised or malfunctioning component; security incident response may require revoking credentials independently of portfolio liquidation.

A kill switch should have defined scope (strategy, instrument, venue, account or entire system), trigger, authority, order/position treatment, timeout behaviour, audit record and recovery path. It must remain effective if the strategy process fails. No unapproved external operator or AI agent can release it.

### 16.7 Drawdown response and capital preservation

Potential controls to research and later calibrate:
- reduce risk allocation as portfolio drawdown or stress loss increases;
- prohibit risk-budget expansion during drawdown recovery;
- cap simultaneous correlated exposure and new order reservations;
- impose strategy-level loss and execution-error limits;
- detect loss clustering, repeated stop slippage and abnormal funding/fee leakage;
- suspend strategies whose realised execution diverges from the validated model;
- require a fresh out-of-sample/replay review after material strategy or market-regime failure;
- maintain unallocated risk capacity and collateral liquidity rather than using all available margin;
- define maximum acceptable recovery time and capital impairment scenarios.

Do not automatically increase size to recover losses, double after losing trades, widen stops to avoid booking losses or allow an AI/strategy to modify its own loss thresholds. Any dynamic risk scaling must be deterministic, bounded, monotonic in the conservative direction under worsening conditions, versioned and owner-approved. Improved recent performance cannot automatically raise hard risk limits.

### 16.8 Trigger integrity and anti-reset protections

Risk-limit state must not be bypassed by:
- UTC day boundary or timezone changes;
- process restart, app reinstall, machine reboot or lost local state;
- venue/account/sub-account switching;
- changing strategy identifiers or splitting one order into smaller orders;
- moving collateral or positions between linked accounts;
- resetting model state, rolling windows or high-water marks;
- stale or delayed P&L updates;
- partial fills or cancellation races;
- manual trade activity outside IDEAL.

The system should reconstruct portfolio-wide state from authoritative event history and reconcile venue evidence. A missing or conflicting state must trigger conservative restriction, not reset the loss counter to zero. External/manual positions and fees must be incorporated where the approved scope requires them; unknown external exposure must be treated as a material blind spot.

### 16.9 Verification and independent assurance

Required tests include:
- exact D-008 baseline and boundary semantics, including realised/unrealised P&L and fees/funding;
- daily reset while rolling drawdown remains active;
- UTC/timezone changes, daylight-saving boundaries and leap/calendar edge cases;
- deposits, withdrawals and internal transfers without P&L distortion;
- high-water mark and flow-adjusted drawdown calculations;
- process restart, state loss, account switching and external/manual trades;
- simultaneous positions/orders and partial fills at the loss boundary;
- stale mark prices, missing funding, late fee events and corrected venue history;
- risk-state escalation and no premature de-escalation;
- cancel-on-disconnect, cancel timeout, duplicate orders and uncertain order state;
- kill-switch scope, idempotency and independence from the strategy process;
- risk-reducing actions during restriction and emergency;
- all-order cancellation accidentally removing protective exits;
- close-out under gap, thin depth, exchange outage and partial fill;
- compromised agent/strategy attempting to reset or weaken limits;
- immutable audit evidence for trigger, decision, attempted action, venue acknowledgement and recovery approval.

Use fault injection, replay, property-based tests and independent recomputation. A control is not proven merely because its normal path works; test race conditions, partial failures and contradictory sources.

### 16.10 Policy preservation and open questions

- D-006 remains 0.5% per trade; equity denominator unresolved.
- D-008 remains exactly 10% of UTC day-start equity including realised and unrealised P&L, followed by 24-hour cooldown. No threshold changed.
- Existing 1:3 reward/risk objective remains a research objective, not a guaranteed or independently validated result.
- No new daily, rolling, weekly, monthly or peak-to-trough threshold is adopted.
- No automatic flattening, cancellation scope, kill-switch trigger or restart/recovery authority is approved.
- Drawdown thresholds, warning bands, cooldown extension, high-water mark basis, external/manual exposure capture and recovery criteria remain to be researched and owner-reviewed.

Next tranche: strategy/model risk, including AI-generated strategies, model drift, validation and promotion gates; then emergency control and incident-recovery contracts. No runtime implementation or phase advancement is authorised.


## 17. Research tranche 6 — strategy, statistical-model and AI-agent risk (17 November 2026)

**Status:** Provisional architecture research. No strategy, model, AI agent, framework or execution capability is approved for deployment.

### 17.1 Evidence reviewed

- Federal Reserve SR 26-2 (17 April 2026) supersedes SR 11-7 for the banking organisations to which the revised guidance is relevant. It emphasises risk-based model governance, conceptual soundness, validation, outcomes analysis, ongoing monitoring and clear accountability. Its regulatory applicability is limited to supervised banking organisations; IDEAL uses it as a model-risk design reference, not as a claim of regulatory coverage. https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm
- The revised Federal Reserve model-risk guidance explains that model risk includes misuse and misapplication even where a model performs as designed; it recommends assessing model risk individually and in aggregate, including shared data, assumptions and dependencies. It also notes that generative/agentic AI is outside that specific guidance's scope. https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm
- NIST AI RMF 1.0 organises AI risk around Govern, Map, Measure and Manage, with risk management continuing across the AI lifecycle. NIST says the framework is being updated; the current published material remains a voluntary framework, not a certification. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- NIST's Generative AI Profile provides additional risk considerations for generative AI systems across design, development, use and evaluation. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- Bailey, Borwein, López de Prado and Zhu's work on Probability of Backtest Overfitting explains why ordinary holdout approaches can be unreliable after extensive strategy selection and proposes combinatorially symmetric cross-validation as one diagnostic. https://escholarship.org/uc/item/4w1110bb
- Bailey and López de Prado's Deflated Sharpe Ratio addresses performance inflation from multiple testing/selection bias and non-normal returns. It is a statistical diagnostic, not proof of future profitability. https://doi.org/10.3905/jpm.2014.40.5.094

### 17.2 Model and strategy inventory

Every model-like component must be registered, including:
- deterministic strategy rules and signal combinations;
- regime classification and market-state models;
- statistical forecasts and feature transformations;
- machine-learning prediction, ranking and allocation models;
- portfolio risk, volatility, correlation, liquidity and margin models;
- execution, slippage, fill-probability and transaction-cost models;
- anomaly detection and system-health models;
- LLMs, agents, prompts, tool policies, retrieval pipelines and generated strategy proposals.

Each registry record should state:
- unique immutable model/strategy identifier and version;
- intended purpose, supported instruments, horizon and operating context;
- explicit prohibited uses and known failure conditions;
- owner, developer/source, approval authority and independent reviewer;
- code, configuration, dependency and model-artifact hashes;
- training/validation/test dataset IDs, provenance and point-in-time policy;
- feature definitions, labels, transformations and data freshness requirements;
- parameters, random seeds, environment and reproducibility instructions;
- baseline/challenger comparisons, validation evidence and limitations;
- risk allocation, maximum permitted authority and dependencies;
- status, effective dates, promotion/revocation reason and audit history.

A model's approval is limited to its declared scope. Approval for one contract family, venue, timeframe or regime does not automatically extend to another.

### 17.3 Separate prediction, strategy and authority

Maintain distinct interfaces and responsibilities:
- **Prediction model:** estimates a specified quantity or probability with uncertainty and horizon.
- **Regime model:** estimates market-state probabilities/labels and uncertainty; it does not declare a regime with certainty.
- **Strategy logic:** converts eligible inputs into a proposed position/action under its own constraints.
- **Portfolio allocator:** allocates only within already-approved capital/risk capacity.
- **Risk authority:** independently approves, restricts or rejects the exact proposed action.
- **Execution control:** validates order semantics, limits, reservations and venue state.

No predictive score, AI confidence, backtest Sharpe, regime label or strategy conviction can override the risk authority. A model cannot set its own risk budget, approve its own validation or promote itself. A strategy may propose a trade; it cannot create permission to take it.

### 17.4 Backtest and research-selection risk

The strategy research process must record the entire experiment population, not only winning variants:
- every tested strategy family, parameter combination, feature set, label, universe filter and selection rule;
- rejected/failed experiments and the reason for rejection;
- data versions, code/configuration hashes and random seeds;
- all lookbacks, validation windows and performance metrics inspected;
- manual research iterations and model/AI-generated candidate trials;
- how the final candidate was selected from the trial population.

Controls against overfitting and selection bias:
- chronological train/validation/test separation;
- purging and embargo where labels or holding periods overlap;
- nested model/parameter selection within training/validation data;
- a final untouched out-of-sample holdout used sparingly and not repeatedly tuned against;
- walk-forward evaluation across multiple market regimes;
- point-in-time universe and instrument metadata, including delisted/expired contracts where available;
- realistic fees, maker/taker mix, funding, spread, slippage, latency, partial fills, market impact and risk limits;
- explicit treatment of missing data, survivorship, corporate/token events, exchange outages and price-source revisions;
- comparison with simple baselines, no-trade and buy/hold or passive references where appropriate;
- stability checks across nearby parameter values, time windows, instruments and execution assumptions.

PBO/CSCV, Deflated Sharpe Ratio, Probabilistic Sharpe Ratio, bootstrap and other selection-bias diagnostics may be used where assumptions fit. They are not magic pass/fail certificates. Record number of trials, dependence among trials, return non-normality, sample length, effective sample size and uncertainty. A large search followed by one impressive result is evidence of selection risk, not necessarily an edge.

### 17.5 Statistical and ML model validation

Before a quantitative model can be considered for any consequential use, validate:
- conceptual soundness and economic/market rationale;
- input data quality, point-in-time correctness, representativeness and leakage;
- label definition, horizon, overlap and survivorship handling;
- calibration and discrimination where probabilities are produced;
- forecast error and directional/decision utility at the intended horizon;
- residual structure, tail behaviour and regime conditional performance;
- sensitivity to parameters, missing/stale inputs and distribution shifts;
- stability across assets, venues, market regimes and execution assumptions;
- comparison against simpler alternatives and a no-model baseline;
- reproducibility from immutable data/code/environment records;
- the difference between predictive accuracy and net trading profitability after costs.

For classification, measure calibration and class imbalance, not just accuracy. For regression, report scale-aware error and forecast intervals where meaningful. For ranking, assess stability and turnover/cost implications. For volatility/risk forecasts, perform coverage and exceedance analysis at the stated horizon. Metrics must correspond to the actual decision use; no universal metric is sufficient.

### 17.6 Regime and uncertainty handling

Regime classification is inherently uncertain and can lag abrupt transitions. It must expose probabilities/uncertainty, data quality and model age rather than a single authoritative label. Research requirements:
- regime definitions and transition assumptions documented before testing;
- out-of-sample and walk-forward regime stability;
- sensitivity to features, thresholds and lookback;
- transition/unknown states and no-trade handling;
- tests for false stability, rapid label flipping and delayed detection;
- performance conditional on regime and transition periods;
- no forced allocation where posterior confidence or data sufficiency is inadequate.

D-004's no-trade requirement for no eligible strategy or unknown regime remains in force. A model must not invent certainty to avoid a no-trade outcome.

### 17.7 Execution and cost-model risk

Execution models are material risk models, not cosmetic backtest settings. They must be validated against representative market data and, only after separately authorised future testing, observed fills. Model:
- order type and maker/taker probability;
- queue position and adverse selection where data supports it;
- spread crossing and depth walking;
- market impact and participation;
- latency, stale data, throttling, rejects and cancel races;
- partial fills, residual exposure and hedge-leg failure;
- funding timing and fees;
- mark/index/last price divergence;
- stressed liquidity and close-out cost.

Avoid optimistic assumptions such as fills at candle close, fills at touch without queue modelling, unlimited depth, zero latency, perfect stops or no market impact. If empirical execution data is unavailable, report a conservative uncertainty range and avoid claiming validated execution performance.

### 17.8 Drift, degradation and model retirement

Monitor model performance and assumptions after approval for the relevant future use:
- input/data drift and schema/semantic changes;
- feature distribution and missingness;
- label/target drift and concept drift;
- forecast calibration and residual changes;
- strategy expectancy, tail loss, drawdown and turnover;
- execution cost, fill ratio, slippage and rejected/cancelled orders;
- regime coverage and previously unseen market states;
- dependency, runtime, model artifact and prompt/tool changes.

Define warning, restricted, suspended and retired states per model class. Drift alarms should trigger investigation and, where risk warrants, restriction or suspension. Recalibration is a new version with documented evidence and revalidation; it is not a silent in-place mutation. A model that stops performing must not continue because its historic backtest remains attractive.

### 17.9 AI and agent-specific risk

AI agents and LLMs introduce risks beyond conventional predictive models:
- hallucinated facts, citations, formulas, assumptions or source interpretations;
- prompt injection through market data, websites, documents, code, issue text or connected tools;
- data exfiltration, secret disclosure and unauthorised tool invocation;
- non-deterministic outputs and model/provider updates;
- context loss, memory errors, stale research and fabricated continuity;
- reward hacking, metric gaming and hidden multiple-testing/selection bias;
- self-modification, permission escalation or attempts to bypass hard controls;
- unsafe code generation, dependency confusion and supply-chain compromise.

Required architecture boundaries:
- agents operate with least privilege and isolated, explicitly scoped tools;
- untrusted market/news/repository content is treated as data, never as instructions;
- no direct exchange trading credentials or unrestricted order tools are exposed to research agents;
- agents cannot edit accepted risk policy, decision records or their own approval state;
- AI-generated code/strategies are untrusted proposals until independently reviewed and tested;
- prompts, model/provider/version, tool schemas, retrieved sources and outputs are logged as appropriate without exposing secrets;
- sensitive data is minimised and protected; no secret is inserted into model context;
- output schemas are validated, source claims checked and critical calculations recomputed deterministically;
- model/provider outage or uncertainty degrades to safe non-action, not an invented answer.

AI may assist research and explain evidence. It is not a substitute for deterministic accounting, risk checks, model validation or owner approval.

### 17.10 Model lifecycle and promotion gates

Provisional lifecycle states:
1. **Research:** exploratory, no operational authority.
2. **Candidate:** purpose and data contract defined; initial tests reproducible.
3. **Validated:** independent validation completed for a declared use and scope.
4. **Approved for bounded use:** owner-authorised, risk limits and monitoring specified. This status does not imply live execution authority.
5. **Restricted:** use limited due to uncertainty, drift, data or performance concerns.
6. **Suspended:** no new use until a defined issue is resolved and approval renewed.
7. **Retired:** no longer eligible; artifacts and evidence retained for audit.

Promotion requires documented evidence, independent challenge, explicit acceptance of residual risk, version pinning, monitoring/rollback plan and separate owner approval. Passing a backtest is not promotion. A new model version, feature pipeline, prompt, model provider, venue, instrument universe or execution assumption can be a material change requiring revalidation.

No online self-learning or self-modifying strategy is proposed. Training and research remain offline and reproducible. Any later automated research loop must be separated from deployment authority and may only generate candidates for controlled review.

### 17.11 Aggregate and correlated model risk

Models may fail together because they share:
- data vendors, exchange feeds, index/mark sources or preprocessing;
- common features, labels, training windows or instrument universe;
- identical model families, embeddings or base models;
- common assumptions about liquidity, volatility, correlation or funding;
- shared execution and runtime infrastructure;
- similar prompts, agent policies or retrieved sources.

Maintain a dependency graph and evaluate aggregate model risk. Model diversity is not real diversification if components share the same hidden inputs or failure modes. A model ensemble must be tested for correlated errors, not assumed robust because it contains multiple models.

### 17.12 Verification and assurance requirements

Required test families:
- reproducibility of model artefacts and strategy experiments from immutable manifests;
- leakage, survivorship, future-data and overlapping-label detection;
- trial-count accounting and selection-bias diagnostics;
- untouched holdout protection and repeated-inspection detection;
- walk-forward and regime-specific performance;
- baseline comparison and parameter perturbation;
- sensitivity, stress, calibration and uncertainty checks;
- model drift, missing inputs and distribution-shift detection;
- execution cost under spread/depth/latency/funding stress;
- strategy/model dependency and correlated failure;
- invalid output, hallucinated source, prompt injection and malicious retrieved content;
- agent least privilege, denied tool access and secret isolation;
- model version change, provider change, rollback and suspension;
- independent recomputation of risk-critical outputs;
- assurance that no model can change limits, permissions, capital or its own approval.

### 17.13 Conclusions and boundaries

- Treat every strategy, statistical model, risk model, execution model and AI agent as a governed component with declared purpose and limitations.
- Track all experiments and selection attempts; evaluate backtest overfitting and selection bias.
- Validation must include conceptual soundness, point-in-time data, outcomes, ongoing monitoring and independent challenge.
- Regime models must express uncertainty and support no-trade states.
- AI-generated strategies are untrusted research candidates; agents never receive direct authority over capital, policy or execution.
- Model changes, drift and dependency failures require controlled restriction, revalidation, rollback or retirement.

No strategy/model is selected or promoted by this research. No AI runtime, framework, model weights, trading integration or execution capability is approved. Phase 02 remains active; Phases 03–19 remain locked.


## 18. Research tranche 7 — emergency control, incident response and verified recovery (17 November 2026)

**Status:** Provisional architecture research. No emergency execution, credential revocation, exchange connection, automatic flattening or recovery authority is approved.

### 18.1 Evidence reviewed

- NIST SP 800-61 Rev. 3 (final April 2025) integrates incident response into the NIST Cybersecurity Framework 2.0 and describes preparation, detection, response, recovery and continuous improvement across cybersecurity risk management. It supersedes SP 800-61 Rev. 2. https://csrc.nist.gov/pubs/sp/800/61/r3/final
- NIST's incident-response project explains that preparation (Govern, Identify, Protect) supports the incident lifecycle (Detect, Respond, Recover), while lessons learned feed continuous improvement. https://csrc.nist.gov/projects/incident-response
- CISA's incident and vulnerability response playbooks emphasise coordinated containment, evidence preservation, eradication of persistence, rebuilding from clean sources, credential resets and monitoring for re-entry before restoring normal operations. These are federal-government playbooks and are used as technical reference material, not a claim of applicability to IDEAL. https://www.cisa.gov/sites/default/files/2024-08/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf
- FIA's automated trading risk-control guidance describes cancel-on-disconnect as best-effort and notes that the scope of cancellation depends on session semantics. It also notes that a kill switch may block new orders, cancel working orders and/or permit risk-reducing orders; cancellation of protective orders can itself add risk. https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf

### 18.2 Emergency control plane must be independent

Provisional architecture recommendation: critical risk containment should not depend on the strategy process, model, agent or primary user interface that may have failed or been compromised.

Define a small, deterministic emergency-control plane with:
- independently observable heartbeat and health state;
- a separately controlled permission to request emergency actions;
- immutable policy/configuration and bounded action scope;
- idempotent action requests and explicit action acknowledgement states;
- durable audit evidence independent of the affected component;
- a minimal dependency footprint and a safe behaviour when dependencies are unavailable;
- no AI authority to activate, disable, override or release hard emergency controls.

A control plane is not independent merely because it runs in another process if it shares the same credentials, host failure domain, mutable configuration, data source or compromised administrator identity. Independence must be assessed across software, identity, network, storage, credentials and operational dependencies.

### 18.3 Incident classes and triggers

The risk and security foundations should share a classified incident model. Examples include:

**Market/data incidents**
- stale, missing, out-of-order or corrupted market data;
- mark/index/last price divergence beyond approved tolerance;
- funding, contract specification, risk tier or collateral metadata changed without verified update;
- historical data or account reconciliation mismatch;
- abnormal spread/depth, volatility, liquidity or market dislocation.

**Trading/account incidents (future capability only)**
- order acknowledgement unknown, duplicate or contradictory;
- cancellation request not confirmed;
- position/working-order mismatch;
- unexpected manual/external position or trade;
- unexpected margin ratio, collateral haircut or liquidation estimate;
- venue outage, API throttling, WebSocket loss or session disconnect.

**System/security incidents**
- risk engine, health supervisor, audit storage or critical dependency unavailable;
- unauthorised login, permission escalation, secret leakage or suspicious API use;
- code/dependency tampering, malicious update or supply-chain compromise;
- agent prompt injection, tool misuse or attempted policy modification;
- ransomware, destructive malware, data exfiltration or backup integrity failure;
- backup restore failure or unexplained data hash mismatch.

Each incident type requires severity, confidence, scope, affected domains, evidence, containment owner, permitted actions, communication path and recovery criteria. Unknown or conflicting critical state is itself a risk event.

### 18.4 Safe-state design and action ordering

A safe state must be defined for each failure mode rather than assuming "stop everything" is always safe.

The control decision should distinguish:
1. preventing new risk-increasing activity;
2. retaining or cancelling existing working orders according to their verified purpose and venue semantics;
3. allowing only validated risk-reducing actions where position/order state is reliable;
4. isolating compromised components and revoking compromised credentials;
5. preserving positions and evidence when an action could worsen risk;
6. invoking an owner-controlled manual venue process when IDEAL cannot safely determine or execute the required action.

For example, cancelling all orders can remove protective exits. Cancelling only risk-increasing orders may be impossible if order purpose cannot be determined. A market close can incur extreme slippage or fail during outage. Disabling a credential may prevent new malicious orders but may also prevent IDEAL from cancelling existing venue orders. The correct response depends on incident type, venue capability, state certainty and the separately approved playbook.

Do not assume a local "cancel all" button can cancel orders after a network or exchange outage. Do not equate a cancellation request with confirmed cancellation. Maintain conservative exposure reservations until authoritative terminal state is reconciled.

### 18.5 Incident lifecycle and evidence

Proposed controlled lifecycle:

1. **Prepare:** maintain threat/failure scenarios, current system maps, contact and account-recovery procedures, clean recovery artefacts, tested backups and incident runbooks.
2. **Detect and validate:** collect telemetry and source evidence; classify severity; distinguish false positive, degraded service and confirmed compromise.
3. **Contain:** isolate affected component/session/credential/domain; stop relevant risk-increasing activity; preserve safe access for response and account-state verification.
4. **Preserve evidence:** snapshot logs, event sequences, hashes, code/configuration versions, access records, order/account observations and relevant timestamps before destructive remediation where feasible.
5. **Eradicate:** remove malicious persistence, revoke/rotate compromised credentials, patch root cause, rebuild affected components from verified clean sources and validate dependencies.
6. **Recover in isolation:** restore data/services into a restricted state; validate integrity and provenance; reconcile authoritative external account state; test controls before reconnecting dependencies.
7. **Return to service:** require explicit release conditions and owner approval for consequential capabilities; monitor heightened telemetry after restoration.
8. **Learn:** document root cause, impact, timeline, control failure, recovery evidence and corrective actions; update threat model, risk controls, tests and roadmap.

For a security compromise, restoring service before understanding persistence and credential exposure can reintroduce the attacker. For a trading/account incident, restoring the application without reconciling venue orders, positions and collateral can recreate unknown exposure.

### 18.6 Recovery is not restart

A process restart, new deployment or healthy status indicator does not establish that a system is safe to resume.

Before any future trading capability can leave recovery-pending:
- identify the complete incident scope and root cause or document residual uncertainty;
- verify all relevant identities, credentials, sessions and permissions;
- prove affected code, dependencies, configuration and model artefacts are clean and version-pinned;
- verify data integrity, audit sequence and backup provenance;
- reconcile positions, working/conditional orders, fills, balances, fees, funding, collateral and margin against authoritative venue records;
- account for manual/external activity during the outage;
- verify no stale or duplicated order can unexpectedly execute;
- validate risk, security, health and data controls independently;
- run required replay/conformance/recovery tests;
- document residual risk and obtain the required owner approval.

If authoritative account state cannot be obtained or reconciled, the system remains restricted. It must not infer a flat position from missing data.

### 18.7 Backup, restore and disaster-recovery boundaries

Backups must protect both data and the ability to trust the restored system:
- encrypted, access-controlled, versioned and integrity-checked backups;
- separate backup credentials and failure domains where feasible;
- immutable/tamper-resistant audit and configuration snapshots;
- tested restoration of application state, ledger/events, model artefacts, configuration and audit history;
- recovery-point and recovery-time objectives defined by data criticality and future approved use;
- restore into isolation before reconnecting exchange, bank or other external integrations;
- detect rollback, missing event ranges, duplicate events and sequence gaps;
- reconcile restored state with external source-of-truth records.

A backup that has never been restored is not proven. A restored backup can contain malware, stale permissions or corrupted source data; restore verification must include security and integrity, not just file availability.

### 18.8 Manual fallback and owner procedures

The system should document a manual fallback path for situations where IDEAL is unavailable or cannot be trusted. This may include:
- how the owner identifies the correct venue/account and obtains current position/order state independently;
- how to secure account access and revoke compromised sessions/keys using the venue's own controls;
- how to identify protective vs risk-increasing orders;
- how to avoid duplicate actions during uncertain acknowledgement;
- how to preserve statements, fills, timestamps and evidence;
- how to record manual actions so the system can reconcile them after restoration.

This is a future design requirement only. No exchange account, credentials or live procedures are being configured now.

### 18.9 Verification and incident exercises

Required scenario tests:
- strategy crash with working orders and an open position;
- risk supervisor failure while market data continues;
- market-data stale/divergent while account state is current;
- exchange outage with unknown cancellation state;
- partial acknowledgement, duplicated message and delayed fill;
- compromised API key with active working orders;
- compromised agent attempting tool/permission escalation;
- malicious dependency or update with persistence;
- corrupted database/audit sequence and invalid backup;
- ransomware or host loss with restore from clean source;
- manual intervention while the system is offline;
- restore followed by duplicate-event/order detection;
- emergency control-plane dependency failure;
- false-positive emergency trigger and safe release;
- no automatic return to normal after process restart.

Exercise tabletop and technical scenarios with synthetic data first. Record detection time, containment time, recovery time, lost/uncertain data, control coverage, decision points, failed assumptions and corrective actions. Testing an emergency process must not involve real funds or exchange credentials without separate explicit authorisation.

### 18.10 Cross-foundation responsibility

- **Risk management** defines financial safe states, exposure restrictions and approved emergency action classes.
- **Data integrity** preserves authoritative evidence, sequence, provenance and reconciliation.
- **System health** detects loss of control, degraded dependencies, heartbeat failures and recovery readiness.
- **Security** investigates compromise, isolates affected trust boundaries, manages credentials and validates clean recovery.

One pillar cannot certify another. A health monitor can report that a service is responsive but cannot certify that its data is authentic. A risk engine can block new exposure but cannot prove credentials are uncompromised. A security scan cannot prove the portfolio is reconciled. Release requires all relevant foundations to provide their own evidence.

### 18.11 Conclusions and boundaries

- Emergency control must be independent of strategy/AI and designed across failure domains, not just as a UI button.
- Cancel-on-disconnect is best-effort and venue/session-specific; it is not a guaranteed global cancellation mechanism.
- Containment actions can create new risk; cancel-all and flatten are not universal safe defaults.
- Incident response requires evidence preservation, scope identification, eradication, isolated recovery, reconciliation and explicit release.
- Restart or a green health signal cannot clear a financial or security incident.
- Manual fallback and recovery procedures are necessary for external account state that IDEAL cannot observe during outages.

No emergency action, credential operation, exchange integration, backup service, external scan or runtime change is approved. Phase 02 remains active; Phases 03–19 remain locked.


## 19. Research tranche 8 — independent risk assurance and architecture acceptance evidence (17 November 2026)

**Status:** Provisional assurance design. No test suite, validator, implementation or deployment is approved by this research.

### 19.1 Evidence reviewed

- FIA's July 2024 best-practices paper says trading software and infrastructure should be tested before new systems, versions or updates enter production, and identifies exchange conformance testing as an important practice. It also covers pre-trade controls, post-trade drop-copy reconciliation and operational safeguards. https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf
- CFTC's 2013 automated trading concept release discussed pre-trade controls, post-trade reports, system safeguards, development/testing/supervision and testing under stressed conditions. It is a historical concept release, not a statement that every discussed proposal became binding law or applies to IDEAL. https://www.cftc.gov/PressRoom/PressReleases/6683-13
- Federal Reserve model-risk guidance describes effective challenge, conceptual soundness, outcome analysis and ongoing monitoring; these provide useful independent assurance patterns for IDEAL's risk and quantitative models, without implying banking regulatory applicability. https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm
- NIST SP 800-61 Rev. 3 integrates incident response and continuous improvement into cybersecurity risk management; it supports testing incident and recovery controls, not just normal operations. https://csrc.nist.gov/pubs/sp/800/61/r3/final

### 19.2 Assurance objective

Every material risk control should have a demonstrable assurance case:
- **Claim:** what safety property the control is intended to guarantee.
- **Context:** scope, operating assumptions, dependencies and failure conditions.
- **Argument:** why the design and implementation should achieve the claim.
- **Evidence:** tests, source review, independent calculation, replay, fault injection, operational telemetry and approval records.
- **Residual risk:** what remains unproven, unobservable or outside the test boundary.

A green test summary is not sufficient without traceability to the control, requirement, exact code/configuration version, test data and expected property. Evidence must be reproducible and attributable.

### 19.3 Independence and effective challenge

Independent review must challenge:
- the requirement and risk assumption, not merely whether the code matches the author's interpretation;
- the mathematical model and implementation separately;
- the source data and its point-in-time correctness;
- the strategy/backtest selection process;
- venue adapter semantics and undocumented assumptions;
- control failure and recovery behaviour;
- the tests themselves, including whether they would detect a plausible defect.

The same implementation must not be the sole oracle for its own correctness. Use independent reference calculations, hand-checked examples, alternative implementations, invariants and external primary documentation. Where independent reviewers are unavailable, record the limitation and require a higher level of conservative restriction; do not describe self-review as independent assurance.

### 19.4 Requirements-to-control-to-test traceability

Maintain a traceability matrix linking:
- owner-approved requirement and decision;
- hazard/threat/failure mode;
- risk-control owner and authority boundary;
- inputs, freshness and provenance contract;
- deterministic calculation/policy version;
- expected safe state and action;
- test case and test data fixture;
- evidence artifact and result;
- reviewer/approval and residual risk.

Every hard limit and every fail-closed condition must map to at least one positive test, one boundary test, one negative/adversarial test and one relevant failure/recovery test. Critical controls require independent recomputation or a second verification path where feasible.

### 19.5 Testing layers

A complete verification strategy should combine:

1. **Static analysis and source review:** type/contract checks, dependency/security checks, policy immutability and code review.
2. **Unit and mathematical tests:** exact formula, decimal precision, boundary and rounding correctness.
3. **Property-based/metamorphic tests:** invariants across broad generated inputs and transformations.
4. **Contract tests:** adapters, data schemas, order/account semantics and version compatibility.
5. **Integration tests:** risk, data, health and security interactions using deterministic synthetic services.
6. **Historical replay:** point-in-time market/account data replay with event ordering and realistic costs.
7. **Scenario and stress tests:** market gaps, correlated shocks, collateral depeg, funding, liquidity and margin changes.
8. **Fault injection:** stale data, partial failures, disconnects, delayed acknowledgements, duplicate messages, clock drift, corrupted state and dependency outages.
9. **Recovery/restore tests:** clean rebuild, backup integrity, account-state reconciliation and no automatic resumption.
10. **Independent review and adversarial challenge:** challenge assumptions, bypasses, shared dependencies and test blind spots.

Testing levels are complementary. Passing unit tests does not prove venue semantics; passing a backtest does not prove execution; passing a security scan does not prove risk controls; passing an exchange conformance test does not prove IDEAL's portfolio risk model.

### 19.6 Critical safety invariants

The following are candidate invariants to formalise and test; they do not create new numeric policy:

- No risk-increasing action is approved when critical input, account state, instrument metadata, policy version or required risk service is missing, stale, contradictory or unauthenticated.
- An approval is bound to the exact action parameters, account/instrument scope, policy version, evidence snapshot, validity interval and idempotency key; a changed order requires a new approval.
- Total reserved plus filled exposure cannot exceed the applicable allocation; partial fills transfer reservation to position exposure exactly once.
- Unknown order/cancel state retains conservative reservation; a timeout cannot release risk.
- No strategy, model or AI agent can change hard limits, permission scope, approval state or risk policy.
- A risk-control or security incident cannot be cleared by process restart, clock reset, UTC rollover, account switch or model identifier change.
- A daily loss reset cannot clear rolling loss or peak-to-trough drawdown.
- A risk-reducing action must be verified against current position and venue semantics; labels such as reduce-only are not trusted without validation.
- Missing or stale collateral/FX/margin data cannot be interpreted as additional free capital.
- All material risk decisions and control transitions produce durable, ordered, attributable audit evidence.
- A failure in one foundation cannot be silently certified by another foundation's health state.

### 19.7 Test quality and mutation resistance

Tests must prove that controls fail when they should. For critical logic:
- introduce deliberate mutations such as removing a limit check, reversing a comparison, using stale data, dropping a fee, rounding quantity up, releasing reservation on cancel request, or allowing an AI permission change;
- confirm that tests detect these mutations;
- test both the expected rejection and the reason code/evidence;
- ensure test fixtures cover values immediately below, at and above boundaries;
- use randomized/property-based inputs with recorded seeds and reproducible failing examples;
- avoid brittle tests that merely repeat the implementation's own formula line-for-line.

Coverage percentage alone is not a safety metric. Prioritise hazard/control coverage, mutation detection, independent calculation and fault-path coverage.

### 19.8 Quantitative model assurance

For each model/strategy, assurance evidence should include:
- exact experiment population and selection count;
- immutable data/code/environment manifest;
- point-in-time dataset and universe validation;
- leakage and survivorship checks;
- baseline and no-trade comparisons;
- out-of-sample, walk-forward and regime-specific results;
- realistic fee/funding/slippage/latency/liquidity assumptions;
- uncertainty intervals and sensitivity to assumptions;
- drawdown, tail loss, exposure and capital usage;
- independent reimplementation or cross-check of critical metrics;
- performance monitoring and suspension criteria;
- known limitations and conditions under which the model must not be used.

Performance metrics must be recalculated from raw or canonical return series independently. A strategy report generated by the same pipeline being evaluated is not sufficient evidence on its own.

### 19.9 Control effectiveness monitoring

After any future approval, monitor control operation and not just market outcomes:
- risk checks invoked, passed, rejected and bypass attempts;
- stale/missing input rejection counts;
- policy/configuration changes and approvals;
- order reservation and reconciliation mismatches;
- venue margin and shadow model disagreement;
- kill-switch activation, acknowledgement and recovery;
- model drift and validation exceptions;
- audit pipeline completeness and clock/sequence integrity;
- backup/restore test results;
- security control and access anomalies.

A control that has never triggered may be functioning—or may be disconnected, misconfigured or untested. Use synthetic canary tests and periodic controlled exercises where safe and authorised.

### 19.10 Release and change-control gates

A material change to risk code, policy, data contract, instrument metadata, venue adapter, execution logic, model, dependency or permission requires impact assessment and appropriate regression/revalidation.

A release evidence package should contain:
- exact source commit and build artefact hash;
- dependency lock and security scan results;
- requirement/decision/test traceability;
- full test results and reproducibility instructions;
- independent review findings and resolution;
- risk-control and model validation evidence;
- known issues, residual risk and rollback plan;
- owner approval and scope of authorised capability.

No test or review process may be weakened to obtain a pass. A failed critical test blocks the affected capability. A waiver must not conceal a failed hard safety invariant.

### 19.11 Architecture assurance gaps still open

- Define the independent risk service boundary and failure-domain separation.
- Formalise exact D-006 equity denominator and D-008 reset/valuation semantics.
- Define account/venue state source-of-truth hierarchy and reconciliation tolerances.
- Define critical input freshness/clock rules and risk-service availability policy.
- Define risk decision/approval record schema and idempotency contract.
- Define exact emergency control authority and owner recovery workflow.
- Complete cross-foundation interface contracts and traceability.
- Independently challenge every provisional assumption, including whether the proposed architecture is proportionate and implementable.

### 19.12 Conclusions and boundaries

Risk assurance is an ongoing evidence system, not a one-time sign-off. The architecture must prove both normal operation and safe failure, use independent challenge, and preserve the exact evidence that justifies each approval.

No implementation, validator invocation, test environment, exchange integration, deployment or phase advancement is authorised. Phase 02 remains active; Phases 03–19 remain locked.
