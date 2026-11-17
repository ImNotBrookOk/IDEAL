# IDEAL Domain Risk and Capital Architecture

**Status:** Phase 02 research/design draft; provisional and not owner-accepted  
**Checkpoint:** 074 — 17 November 2026  
**Scope:** Domain-specific risk authority, capital semantics, exposure aggregation and cross-domain financial truth  
**Authority:** D-018, D-019, D-020, D-021, D-022, D-023; existing D-001/D-006/D-008 preserved  
**Boundary:** Documentation only. No new risk limit, allocation, capital restriction, financial action, execution, provider integration or implementation is authorised.

## 1. Objective and core principle

IDEAL needs one coherent view of the owner's financial position without pretending that every financial activity has the same risk model, ledger, legal treatment, liquidity, collateral or authority.

**Integration is visibility and controlled evidence exchange, not automatic fungibility.** Domain risk authorities remain specialised. A portfolio/capital view may aggregate exposure and highlight concentration, but it does not automatically acquire the right to transfer, net, hedge, lock, allocate or liquidate capital.

The architecture separates:
- economic position and valuation;
- accounting/journal truth;
- cash availability and commitments;
- risk capital and approved risk capacity;
- venue margin and collateral;
- tax estimates and assessed liabilities;
- owner-designated reserves;
- legal ownership and enforceable netting sets.

No single scalar named equity, balance, available or risk may substitute for these concepts.

## 2. Risk taxonomy

Risk is a vector of distinct dimensions. A strategy score, portfolio VaR or account balance is not a complete risk assessment.

| Risk class | Examples | Primary owner | Typical evidence |
|---|---|---|---|
| Market / price | Directional loss, gap, volatility, basis, commodity/FX movement | Relevant investment/trading domain risk | Prices, positions, scenarios, instrument specifications |
| Leverage / margin / liquidation | Initial/maintenance margin, liquidation buffer, collateral haircut | Derivatives risk domain and venue-specific shadow model | Venue/account mode, tiers, collateral, mark/index, liabilities |
| Liquidity / execution | Spread, depth, market impact, exit capacity, slippage, opportunity cost | Trading/investment domain risk | Order book, trades, volume, order size, execution model |
| Funding / carry | Perpetual funding, borrow costs, financing, roll and basis | Relevant domain risk | Funding schedules/events, borrow rates, basis and holding horizon |
| Concentration / dependence | Asset, issuer, venue, counterparty, factor, strategy, collateral and liquidity clusters | Domain risk; portfolio view aggregates | Underlying/issuer mappings, factor exposures, correlations and stress |
| Counterparty / custody | Venue failure, bank/provider failure, custodian, settlement and withdrawal restriction | Domain risk / security / owner | Legal entity, custody model, account terms, operational status |
| Operational / technology | Data outages, order-state uncertainty, software defects, key loss, reconciliation failure | System health and security; financial consequences assessed by risk | Telemetry, incidents, audit, recovery and external reconciliation |
| Model / strategy | Overfit, regime shift, estimation error, drift, execution-model error | Research/model risk and domain risk | OOS evidence, uncertainty, model lineage, drift and challenge |
| Cash-flow / liquidity-of-life | Bills, debt servicing, income variability, emergency cash needs | Personal Finance context; owner decides | Reconciled cash flows, due dates, liabilities and forecast assumptions |
| Tax / legal / compliance | Tax classification uncertainty, filing obligations, legal/contract restrictions | Tax Intelligence / owner / qualified adviser | Effective-dated rules, source facts, assessments and legal status |
| Data / information | Stale, incomplete, manipulated, conflicted or mislicensed evidence | Data Integrity; consumer decides fitness | Provenance, quality, source status, clock and licence |

Operational, security and data risks can create financial losses, but their control authorities remain distinct. Security may contain/revoke identities; health may restrict affected capabilities; neither approves financial exposure or initiates financial actions.

## 3. Domain risk authorities

| Domain | Risk questions | Authority / control model | Explicit non-assumptions |
|---|---|---|---|
| Crypto perpetual futures | Planned loss, gross notional, leverage, funding, liquidation, margin, liquidity, venue and correlated exposure | Independent deterministic derivatives risk gate; exact-action approval and reservation for any future execution | No current execution authority; D-006/D-008 are the only accepted numerical boundaries and remain semantically incomplete |
| Crypto spot investment | Concentration, drawdown, custody, liquidity, market regime, accumulation schedule and capital allocation | Future owner-approved investment policy; domain risk evaluates proposals | No leverage/margin assumed; no strategy/allocation currently approved |
| Equities / ETFs | Issuer/sector/country concentration, market risk, liquidity, FX, custody, corporate actions and tax/FIF treatment | Future investment-domain risk and portfolio view | No broker, account, universe, tax treatment or investment permission approved |
| Commodity exposure | Contract/vehicle basis, roll, issuer/counterparty, currency, storage/custody, liquidity and tracking | Future product-specific risk adapter | Gold/silver/copper exposure may be physical, ETF, CFD, futures or other structures; do not equate them |
| Cross-asset hedge | Basis, beta instability, correlation breakdown, liquidity mismatch, expiry/roll, counterparty and margin mismatch | Explicitly approved portfolio risk model and hedge-credit policy | Opposite signs or historical correlation do not prove a hedge; no implicit risk offset |
| Personal finance | Cash runway, bills, debt service, income uncertainty, overdraft and account reconciliation | Deterministic visibility, forecasts, warnings and user-controlled planning | No forced budget, lock, payment, withdrawal block or investment restriction |
| Tax intelligence | Classification uncertainty, tax-year timing, income estimates, due dates, FX and assessed balance | Versioned rule/calculation engine with human review; outputs informational to Personal Finance | No automatic tax reserve, capital lock, filing or payment; D-018 |
| Portfolio / capital view | Aggregate exposures, liquidity, concentration, net worth and scenario sensitivity | Read-only projection and cross-domain diagnostics | Not an authority to reallocate, net, transfer, hedge, pledge collateral or override a domain gate |

The same underlying instrument can have different risk meaning across contexts. For example, a crypto wallet asset is spot property/custody exposure; a perpetual position is a derivative exposure with funding, margin and liquidation; a tax classification is a legal/accounting assessment. They must not be collapsed into one generic crypto risk field.

## 4. Capital ontology

Every capital amount must include currency, unit, owner/legal entity, account/custody scope, source, valuation method, valuation time, status, restrictions/encumbrance and reconciliation state.

| Concept | Meaning | Must not be confused with |
|---|---|---|
| Ledger cash/balance | Posted accounting balance in an owned account ledger | Available cash, market value or risk capacity |
| Pending cash flow | Initiated/authorised but not settled transaction | Posted balance or realised profit |
| Available cash | Amount the provider/bank reports as currently available under its rules | Economic wealth, collateral or approved investment budget |
| Invested market value | Current valuation of owned investment assets | Cash or guaranteed liquidation proceeds |
| Derivatives economic equity | Account-specific economic value including applicable P&L/liabilities | Venue available margin or household net worth |
| Risk-adjusted equity | Approved conservative risk-capital measure after explicit haircuts/uncertainty/liabilities | Venue margin equity or general net worth |
| Venue margin equity | Venue/account-mode-specific value for margin/liquidation | IDEAL's own risk capital or consolidated wealth |
| Available margin | Venue-reported capacity for additional margin | Wealth, withdrawable cash or independent risk permission |
| Collateral | Assets eligible under a particular venue/account/legal scope, with haircuts and settlement rules | Cash equivalence or cross-venue transferable collateral |
| Encumbered/committed capital | Cash/assets already committed to orders, margin, collateral, debt or other commitments | Free capital |
| Tax estimate | IDEAL's current estimate under specified assumptions and rule version | Assessed liability or money held by IDEAL |
| Assessed tax liability | Amount assessed/confirmed by the tax authority | Optional owner reserve or cash held |
| Owner-designated reserve | Informational designation the owner may choose to track | Locked, escrowed, segregated or unavailable funds |
| Economic net worth | Assets less liabilities under stated valuation and ownership assumptions | Risk budget, available cash or margin |

Do not double-count:
- a bank transfer as both income and a balance increase;
- a position's unrealised P&L in both the ledger and valuation projection;
- an investment holding and its cash settlement proceeds simultaneously;
- derivative notional as if it were the market value of an owned underlying asset;
- collateral as both free cash and committed margin;
- an inter-account transfer as profit/loss.

## 5. Exposure aggregation without false netting

Portfolio aggregation should report several parallel views:

1. **Gross exposure:** sum of absolute exposures before offsets.
2. **Net directional exposure:** signed exposure under an explicitly defined mapping and conversion methodology.
3. **Factor exposure:** sensitivity to shared market, currency, rates, commodity, sector or crypto factors.
4. **Liquidity exposure:** estimated time/cost to reduce or exit positions under normal and stressed conditions.
5. **Counterparty/custody exposure:** assets and obligations by legal entity, venue, bank, custodian and settlement path.
6. **Collateral and margin exposure:** by account, venue, asset, haircut, legal netting set and settlement currency.
7. **Economic net worth:** assets and liabilities by ownership and valuation basis.
8. **Cash-flow capacity:** near-term obligations, income uncertainty and accessible liquidity.
9. **Tax exposure:** estimates and assessed liabilities separately from cash.

Rules:
- Gross exposure remains visible even where net exposure is small.
- Netting is allowed only where the economic relationship, instrument mapping, currency, legal/account scope and enforceable offset assumptions are documented.
- A hedge credit requires evidence of basis stability, stressed correlation, liquidity, expiry/roll alignment, counterparty continuity and executable hedge capacity.
- Margin offsets are venue-specific. IDEAL's portfolio view cannot assume the venue will recognise an offset or that collateral can move across accounts.
- A hedge that requires both legs to remain open may fail under one-sided liquidity, API, venue or margin disruption.
- Unknown or stale FX rates do not become zero or a neutral conversion; the affected aggregate is marked incomplete/unknown.
- Portfolio views must show both the total and the components, source timestamps, excluded items and confidence/quality.

## 6. Risk budget and owner capital autonomy

The derivatives risk research proposes a hierarchical risk budget (owner-approved total capacity → portfolio allocation → strategy allocation → trade → order reservation). This hierarchy is provisional for the derivatives execution domain and must not be universalised across personal finance or all asset classes.

For every future domain, distinguish:
- **Owner capital preference:** what the owner chooses to allocate or retain.
- **Domain eligibility:** whether a domain is approved to operate at all.
- **Risk capacity:** maximum risk the owner-approved policy permits.
- **Current exposure:** positions, working orders, liabilities and commitments.
- **Available risk capacity:** residual capacity after current and reserved exposure.
- **Cash availability:** provider-reported funds that may be accessible.
- **Execution permission:** authority to perform a specific external action.

These are not interchangeable. A positive cash balance does not create risk capacity. Unused risk capacity does not compel deployment. A successful strategy does not increase its own allocation.

D-018 is a hard user-autonomy invariant: tax reserve figures are informational. The owner may deploy funds shown as a reserve; IDEAL updates estimates, coverage and warnings but does not lock, deduct, segregate, escrow or force payment. Personal Finance may support user-chosen budgets and designations, but it cannot convert a planning category into a technical prohibition without a separate explicit owner decision and lawful basis.

## 7. D-006 and D-008 scope preservation

- D-006: initial per-trade risk target of 0.5% of equity. The denominator remains unresolved. It applies to the initial crypto-perpetual risk policy only; do not copy it to spot, equities, commodities, personal finance or tax.
- D-008: hard daily loss boundary of 10% of UTC day-start equity, realised plus unrealised, followed by 24-hour cooldown. Its current semantics are incomplete; it remains an outer boundary, not a normal loss target or complete risk system. Preserve the accepted UTC day-start baseline unless a superseding owner decision changes it.
- No numerical limits are proposed in this document. Intermediate warnings, portfolio limits, liquidity buffers, concentration caps, leverage ceilings and cross-asset hedge credit remain open.
- Risk-adjusted equity is a research recommendation for D-006, not an accepted denominator.
- Tax estimates and personal-finance cash-flow forecasts must not be used as a reason to change D-006/D-008 without explicit policy design and approval.

## 8. Risk decision and data-validity contract

A risk result is valid only for an exact domain/action and a defined evidence snapshot. It must bind:
- domain, account, legal owner, venue/instrument and action class;
- exact action parameters and canonical digest where an external action is proposed;
- policy, model, instrument and contract versions;
- position/order/reservation/account snapshot and reconciliation state;
- named capital/equity measure, currency and valuation method;
- market, FX, funding, collateral, liquidity and counterparty evidence references;
- quality/freshness, source/availability time and clock confidence;
- portfolio stress/concentration outputs and known model limitations;
- security permission, owner envelope and health interlock state where applicable;
- outcome, reason codes, validity window, invalidation triggers and audit reference.

The decision is invalidated by any material change to action, authority, policy, instrument metadata, account/position state, risk reservation, data evidence, health/security interlock or relevant source correction. A new evaluation is required.

Data integrity owns source evidence and quality labels; the risk consumer determines whether those labels meet its fitness contract. A stale balance can invalidate cash availability without necessarily invalidating a market-only research calculation. A missing venue position snapshot may invalidate all account-level risk-increasing actions while leaving unrelated personal-finance reporting available.

## 9. Failure states and containment

| Condition | Affected capability | Required response |
|---|---|---|
| Market feed stale/conflicted | Strategies/decisions using that feed | Mark unknown; block dependent risk increases; preserve unaffected domains |
| Account/position reconciliation unknown | Account-level risk and future dispatch | Retain conservative exposure/reservations; no conflicting new risk |
| FX conversion stale/missing | Aggregates requiring that conversion | Mark partial/unknown; no silent zero or last-known unlimited carry-forward |
| Venue margin tier/collateral rule changed | Affected derivatives account | Invalidate cached calculations; refresh authoritative metadata or restrict |
| Bank provider refresh delayed | Personal-finance cash freshness | Show source age; retain ledger history; no claim of current available cash |
| Tax classification unresolved | Tax estimate for affected event | Expose uncertainty; require review; do not default to zero or force a reserve |
| Cross-asset correlation/hedge model unstable | Hedge credit / portfolio stress | Remove or reduce modelled hedge credit under predefined conservative rules |
| Security incident | Affected identities/integrations/data | Security incident authority contains/revokes; no financial side effect |
| Health supervisor failure | Affected dependent capabilities | Scoped fail-closed interlock; supervisor cannot grant authority |
| Risk service unavailable | All dependent risk-increasing actions | Deny new risk; existing positions handled only under separately approved emergency/manual policy |
| Audit durability failure | Consequential actions requiring audit | No dispatch; preserve evidence and enter restricted state |
| Portfolio aggregation incomplete | Consolidated decision relying on missing scope | Mark incomplete; no false all-up risk number |

Containment must be dependency-aware. The architecture should not globally disable unrelated contexts where isolation and independent trust can be demonstrated.

## 10. Required verification

Future tests include:
- currency/unit/ownership/valuation semantics and double-counting;
- cash, pending, available, invested, collateral, margin and risk capacity separation;
- native-currency aggregation and stale/missing FX handling;
- no implicit cross-account/venue/legal-entity netting;
- hedge credit removal under correlation/basis/liquidity/counterparty stress;
- gross versus net exposure and working-order reservations;
- D-006 denominator and D-008 baseline/flow semantics after owner decision;
- domain-specific policy prevents D-006/D-008 propagation into future domains;
- tax estimate changes never lock capital or prevent otherwise permitted access;
- read-only portfolio projection cannot mutate domain ledgers or issue capital instructions;
- unknown/stale data invalidates only affected dependent decisions;
- concurrency, partial fills, cancel-unknown and reconciliation invariants from the risk/autonomy contracts.

These are proposed future tests, not executed results.

## 11. Open design items

- D-006 equity denominator and exact risk basis.
- D-008 deposits/withdrawals, multi-currency, valuation source/age, fees/funding and UTC boundary semantics.
- Owner-approved portfolio risk hierarchy and intermediate loss thresholds.
- Personal-finance cash runway and warning semantics; no mandatory restrictions.
- Separate risk budgets for future spot/equities/commodities and whether any cross-domain risk capacity is desired.
- Enforceable netting-set definitions and collateral portability, if any.
- Hedge-credit methodology and independent stress validation.
- Risk treatment for custody, counterparty, stablecoin, provider and jurisdiction concentration.
- Portfolio reporting valuation cut-offs and stale-value policy.
- Whether consolidated capital view includes all personal assets/liabilities or only explicitly connected domains.

## 12. Disposition

This architecture defines the risk taxonomy and capital semantics needed to avoid a misleading single-balance/single-risk model. It does not approve a unified risk budget, new numerical limits, portfolio allocation, hedge credit, domain activation or capital restriction.

Phase 02 remains active; Phases 03–19 remain locked. No implementation, execution, external account access, credentials, paid infrastructure or financial action is authorised.
