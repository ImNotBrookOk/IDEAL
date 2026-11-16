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

### 4.2 Action classification

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

### 4.3 Pre-action decision contract

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
