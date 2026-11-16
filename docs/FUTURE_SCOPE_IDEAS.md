# IDEAL — Deferred Future Scope Ideas

**Status:** Captured for future evaluation only; NOT part of the active build scope.  
**Recorded:** 16 November 2026  
**Current governing scope:** Crypto perpetual futures research and eventual paper-trading platform, subject to existing phase gates and owner approvals.

This document preserves ideas raised by the owner without changing the active roadmap sequence, initial market scope, risk rules or implementation permissions.

## F-001 — Macro-regime-aware spot accumulation

### Concept

At a later stage, IDEAL may include a separate spot-investment sleeve alongside its crypto-perpetual trading system. The sleeve would use macroeconomic, liquidity, market-structure and broader regime evidence to estimate whether the market is transitioning from a bear regime toward a bull regime.

When the evidence supports a sufficiently attractive long-term accumulation regime, the system could allocate a predefined, bounded amount of eligible realised profits or other explicitly approved capital to spot assets using staged dollar-cost averaging (DCA).

The intent is gradual accumulation through a cycle, not attempting to identify the exact bottom. A regime model must express uncertainty; it must never treat a bottom or bull-market transition as certain.

### Potential future design questions

- What macro inputs are admissible, how are they timestamped, and how do we prevent revised data, publication lags and look-ahead bias?
- Which regime features matter (rates, real yields, liquidity, credit conditions, dollar strength, volatility, breadth, flows and crypto-native indicators), and how are conflicting signals handled?
- What evidence threshold activates accumulation, and what evidence pauses or terminates it?
- What does “profits” mean: realised net trading profits after fees/funding, tax/reserve provisions, loss recovery and minimum operating capital?
- What fixed fraction or absolute cap can be allocated, over what cadence, with what maximum cumulative exposure?
- Which assets qualify, using what liquidity, custody, concentration and delisting criteria?
- How are staged purchases sized, paused during deteriorating liquidity or operational incidents, and reconciled?
- How is the spot sleeve accounted for separately from leveraged derivatives, including cost basis, realised/unrealised PnL, fees, transfers and portfolio concentration?
- What human approval, tax, custody, jurisdiction and platform requirements apply?

### Non-negotiable research principles

- Do not claim reliable prediction of exact market bottoms.
- Use probabilistic regime classification and staged accumulation, not a binary “bottom detected” switch.
- Fund only from an explicitly defined and approved capital budget; profits are not automatically available capital.
- Preserve derivatives risk capital, liquidity reserves and operating buffers before any allocation.
- Keep spot assets unleveraged by default unless a separate future decision explicitly approves otherwise.
- Enforce deterministic per-asset, total-sleeve, drawdown and concentration limits.
- Backtest with point-in-time macro data vintages, publication lags, fees, spreads, slippage, survivorship controls and genuinely out-of-sample cycles.
- Keep the spot sleeve's ledger and risk budget distinct while reporting consolidated portfolio exposure.

### Status

Deferred. No spot venue, asset universe, capital allocation, strategy, account or implementation is approved. Initial market scope remains crypto perpetual futures under D-001.

## F-002 — Reuse IDEAL's decision framework for equities

### Concept

The owner asked whether the same platform could eventually support stock trading. The answer is architecturally plausible: strategy research, regime classification, signal evaluation, portfolio construction, risk checks, order scheduling/placement, execution measurement, audit trails and learning workflows are reusable concepts.

However, an equities system is not simply a crypto adapter. It requires market-specific data, execution, accounting and regulatory semantics. It should be treated as a separate future market expansion with its own evidence gates and approval.

### Reusable platform capabilities

- Point-in-time data lineage, feature computation and regime classification.
- Strategy generation, deterministic validation, backtesting and walk-forward evaluation.
- Expected-net-value execution decisions and transaction-cost analysis.
- Portfolio/risk orchestration, policy gates, audit journaling, reproducible replay and model governance.
- Monitoring, operator controls, explainability and post-trade learning.

### Equities-specific work that cannot be assumed reusable

- Exchange calendars, sessions, auctions, halts, price bands and venue routing.
- Corporate actions (splits, dividends, mergers, symbol changes), adjusted/unadjusted price series and point-in-time constituent membership.
- NBBO/consolidated feeds, venue-specific depth, odd lots, auction data and order handling.
- Tick/lot sizes, settlement, buying power, cash accounts, margin, short locate/borrow availability and borrow costs.
- Equity commissions, regulatory fees, taxes, dividends and financing.
- Different liquidity, market-impact, volatility and execution models.
- Broker, exchange, data-licence, investor-classification and jurisdictional permissions.

### Status

Deferred. No equities broker, data vendor, market universe, account or implementation is approved. Crypto perpetual futures remain the only active initial market scope under D-001.


## F-003 — Multi-asset investment and portfolio domain research

### Owner direction captured 16 November 2026

The owner requests deep research into future crypto spot portfolio management and a separate equities investment engine, with the architecture also considering commodity-linked exposure and cross-asset hedging. This is a research and architecture-planning request only. It does not amend D-001 or authorise implementation, broker/venue selection, accounts, credentials, paper/live execution or paid data/services.

### Architectural principle

IDEAL should be designed as a modular, multi-domain investment platform, not as one universal strategy engine. Reusable platform capabilities may include identity, event contracts, point-in-time data lineage, audit, replay, portfolio-level exposure aggregation, risk reporting, notifications and orchestration. Market-specific engines and adapters retain their own semantics, state and controls.

Potential future domains:
- Crypto spot portfolio: strategic allocation, macro/regime-aware accumulation, DCA, rebalancing, custody/wallet and exchange reconciliation.
- Equities and ETFs: long-horizon investment and/or systematic strategies, broker integration, corporate actions, dividends, exchange calendars, settlement, tax-lot and FX accounting.
- Commodity exposure: gold, silver, copper and other instruments, distinguishing physical bullion, physically backed funds/ETFs, exchange-traded futures, options, CFDs and tokenised claims. These are not interchangeable products.
- Other future research candidates: FX, rates/fixed income, options, REITs and energy/agricultural commodities. These are candidates for screening, not commitments to build.

### Shared platform services versus domain-specific engines

Potential shared services:
- Canonical instrument/security master with immutable instrument IDs, venue, currency, contract multiplier, tick/lot sizes, expiry, settlement and trading calendar metadata.
- Point-in-time market/fundamental/macro data with source, publication time, revision vintage, licensing and quality metadata.
- Event journal, deterministic replay, idempotency, provenance and audit.
- Native-currency double-entry accounting primitives and controlled FX translation.
- Consolidated read-only portfolio exposure, factor, currency, liquidity and stress reporting.
- Capital allocation and transfer workflow with explicit authorisation, immutable references and reconciliation.

Domain-specific capabilities must remain separate where their semantics differ: perpetual funding and liquidation; spot custody and on-chain transfers; equity dividends, splits and corporate actions; commodity futures delivery, expiry, rolls, basis and margin. A common interface must not erase these differences.

### Cross-asset hedging — separate future capability

Research a portfolio-level hedge and exposure-management module rather than making hedging an implicit feature of every strategy engine. It may eventually:
- Measure exposures by underlying economic risk, not just ticker or instrument.
- Estimate hedge ratios using beta, covariance, factor sensitivities, duration/DV01, FX delta or commodity sensitivities as appropriate.
- Propose hedge instruments and sizes subject to liquidity, basis, margin, collateral, concentration and cost constraints.
- Track hedge effectiveness, residual risk, basis risk, carry/roll cost and hedge drift.
- Enforce independent limits and human approval boundaries.

Gold, silver or copper positions must not automatically be labelled hedges. Their effectiveness depends on the exposure being hedged, horizon, instrument structure, correlation stability, basis, currency and funding. Commodity futures can introduce expiry, delivery, roll yield, contango/backwardation and margin risks. Physical metal, ETF shares, futures, CFDs and tokenised claims carry materially different ownership, custody and counterparty risks.

### Additional design questions to investigate

- Separate legal account, strategy sleeve, engine and portfolio hierarchy; capital transfer and attribution.
- Consolidated risk without pooling cash, collateral or permissions by assumption.
- Native currency versus reporting currency; FX source, timestamp, stale-rate handling and conservative valuation.
- Double-entry ledger, immutable transaction history, corrections/reversals, cost basis, realised/unrealised PnL and reconciliation.
- Dividends, withholding tax, splits, mergers, spin-offs, rights issues, symbol changes, delistings and other corporate actions.
- Crypto deposits/withdrawals, chain fees, forks, staking rewards, custody, wallet attribution and exchange insolvency risk.
- Commodity contract specifications, delivery notices, first/last notice dates, expiry, settlement type, contract rolls, forward curves and storage/financing effects.
- Market calendars, holidays, auctions, halts, price limits, daylight-saving changes, overnight/weekend gaps and cross-market asynchronous sessions.
- Shorting, borrow availability/cost, funding, margin, collateral haircuts, liquidation and counterparty exposure.
- Data entitlements, redistribution restrictions, survivorship bias, delisted securities, point-in-time fundamentals and revised macroeconomic data.
- NZ tax classification and recordkeeping across crypto, shares, FIF interests, derivatives and commodity-linked instruments; obtain professional advice before any real-money expansion.
- Broker/venue eligibility for a New Zealand resident, account type, custody, client-money protections, product disclosure, API terms and data costs.
- Portfolio-level stress scenarios: crypto crash, equity drawdown, USD/NZD shock, rates/inflation surprise, commodity supply shock, liquidity freeze, venue outage and correlated liquidation.

### Preliminary open-source research shortlist — not adopted

| Project | Initial research value | Licence / boundary | Preliminary disposition |
|---|---|---|---|
| [QuantConnect LEAN](https://github.com/QuantConnect/Lean) | Modular event-driven multi-asset research/backtest engine; equities, futures, FX, options and crypto concepts | Apache-2.0; data and hosted cloud services are separate; fill/slippage/impact assumptions require independent audit | High-priority architecture and simulation reference; do not assume broker/data coverage or realism |
| [NautilusTrader](https://github.com/nautechsystems/nautilus_trader) | Deterministic event-driven execution/replay and portfolio mechanics | LGPL-3.0; existing IDEAL POC is pinned to 2.0.0rc9 and limited to isolated research | Continue existing scoped evaluation; separately assess asset-class coverage and licence obligations |
| [Hummingbot](https://github.com/hummingbot/hummingbot) | Exchange connector patterns and crypto spot/perpetual execution | Apache-2.0; strategy focus is automated trading/market making, not a complete long-term investment ledger | Reuse/reference connector and execution ideas only after connector-specific audit |
| [Freqtrade](https://github.com/freqtrade/freqtrade) | Crypto spot/futures bot, backtesting, dry-run, persistence and position adjustment/DCA patterns | GPL-3.0; crypto-focused bot, not general equities/commodities portfolio architecture | Research reference; GPL boundary and strategy/execution coupling require review |
| [rotki](https://github.com/rotki/rotki) | Crypto portfolio tracking, transaction decoding, accounting and PnL reporting | AGPL-3.0; commercial licensing available from project | Strong accounting-domain reference; do not embed before licence and accounting-method audit |
| [Portfolio Performance](https://github.com/portfolio-performance/portfolio) | Multi-account investment tracking, time-weighted/IRR performance, allocation and rebalancing, dividends/fees and multicurrency concepts | EPL-1.0; desktop portfolio-analysis application, not an automated execution engine | High-priority equities/portfolio accounting reference; inspect data model and import/export boundaries |
| [Deltabadger](https://github.com/deltabadger/deltabadger) | Crypto DCA, rebalancing, direct indexing, portfolio tracking and tax-reporting workflows | AGPL-3.0; verify current maintenance, exchange support and implementation depth | Focused DCA workflow reference; not a core platform dependency candidate yet |
| [CCXT](https://github.com/ccxt/ccxt) | Unified crypto exchange REST API patterns | MIT; exchange-specific support and semantic differences remain | Potential crypto adapter reference, not a multi-asset broker abstraction |

The shortlist is discovery-stage only. Before any selection, record current commit/release activity, licence and transitive obligations, open issues, test quality, supported instrument types, exchange/broker limitations, security posture, data rights and reproducible POC evidence. Stars are a discovery signal, not a quality gate.

### Preliminary research observations

- LEAN's own documentation describes a modular engine, but its simulation defaults are not automatically conservative: some default brokerage models use zero slippage, fill models may assume complete fills, and market impact is not modelled by default. IDEAL must independently validate fill, slippage, impact, fees, borrow, funding and corporate-action behaviour.
- Hummingbot's connector abstraction is useful for exchange integration patterns, but connector availability does not prove NZ eligibility, account suitability, data rights or execution quality.
- Freqtrade's DCA/position adjustment is a strategy callback and bot workflow; it is not a substitute for an independently governed profit-allocation and long-term portfolio ledger.
- rotki and Portfolio Performance are portfolio/accounting references, not evidence that one package should become IDEAL's source of financial truth.
- Commodity futures are not equivalent to holding spot metal. Contract size, tick value, expiry, delivery/settlement and roll schedule are essential instrument metadata. Futures curve structure and basis can materially change long-horizon returns.

### New Zealand research boundary

Initial source screening indicates:
- IRD requires crypto transaction records including asset type, date, transaction type, units, NZD value, opening/closing units, exchange records and wallet addresses, retained for at least seven years.
- IRD guidance says foreign shares may fall under FIF rules; the commonly referenced NZ$50,000 threshold and applicable exemptions/methods require current case-specific verification.
- IRD share-sale tax treatment can depend on acquisition purpose, dealing activity or a profit-making scheme; a simplistic assumption that all share-sale gains are tax-free is unsafe.
- FMA states derivatives issuers making regulated offers to NZ retail investors require an FMA licence. The FMA also describes derivatives as complex/high-risk products. Product, provider, account and territorial scope must be checked independently before any venue or broker selection.

Sources: [IRD crypto recordkeeping](https://www.ird.govt.nz/cryptoassets/taxing/record-keeping), [IRD crypto taxation](https://www.ird.govt.nz/cryptoassets/taxing), [IRD share investments](https://www.ird.govt.nz/income-tax/income-tax-for-individuals/types-of-individual-income/share-investments), [IRD FIF](https://www.ird.govt.nz/fif), [FMA derivatives](https://www.fma.govt.nz/consumer/investing/types-of-investments/derivatives), [FMA derivatives issuer licensing](https://www.fma.govt.nz/business/services/derivatives-issuers/). This is issue-spotting, not tax or legal advice.

### Status and approval boundary

Deferred future research. Owner has requested investigation and architectural consideration, not activation. D-001 remains unchanged: crypto perpetual futures are the only active initial market scope. F-001 spot accumulation, F-002 equities, commodity exposure and cross-asset hedging remain proposals. No instrument universe, broker, venue, data vendor, hedge policy, capital allocation, account, strategy or implementation is approved.

## Governance

These ideas are deliberately separate from active requirements. They must not expand Phase 01, alter current testing priorities, unlock Phase 02, or be treated as implied approval to build. Revisit them only at a future scope-review point after the initial platform's research and validation gates are complete, or earlier only if the owner explicitly requests a scope review.

## F-004 — Private personal finance and banking domain

### Owner direction captured 16 November 2026

The owner wants IDEAL to become a private, single-user platform for their own financial management: bank-account visibility where lawful and technically viable, manual and file-based account/transaction entry, budgeting, bills, subscriptions, debt, savings goals, cash-flow forecasting, net-worth tracking and a consolidated view of investments. This is initially for the owner's personal use only. A future multi-user/public product may be considered only if the private system proves valuable and a separate legal, security, privacy, licensing and operational review is approved. It is not a current product commitment.

### Architectural direction to research

- Treat personal finance as a separate domain alongside (not inside) trading/investment engines.
- Provide manual account/asset/liability entry and statement imports independently of bank connectivity.
- Model accounts, transactions, transfers, categories, budgets, recurring bills, debts, savings goals and valuations with traceable source/provenance and correction history.
- Keep a native-currency double-entry ledger and explicit reporting-currency conversion; do not silently overwrite source transactions or rates.
- Consolidate net worth and investment exposure through read-only projections; retain separate authoritative ledgers and permissions for each engine.
- Start with read-only bank-data access. Payment initiation, transfers, brokerage orders and trading remain separate capabilities requiring independent explicit approval and legal/security gates.
- Design for local/private use first. A later web deployment must include strong authentication, MFA, TLS, network isolation, encrypted secrets/backups, least privilege, monitoring, restore drills and an explicit threat model.
- Keep all financial records exportable and deletable under a documented retention policy. Never send credentials, tokens or raw financial records to GitHub or conversation transcripts.

### Preliminary New Zealand bank-data path

Akahu is a leading candidate for personal-use investigation, not yet selected. Its developer documentation describes a free Personal App restricted to one user's own Akahu account, with ongoing account-information access, daily scheduled refresh, manual refresh subject to a one-hour rest period, and no payments or webhooks. Akahu describes this as Tier 0; full ongoing personal-finance/budgeting apps are separately classified Tier 2 and require a full app review. The exact terms and applicability to a self-hosted IDEAL instance must be confirmed before use. Akahu says personal apps are unsuitable as a production-ready multi-user application. Official CDR access via an accredited intermediary is a different pathway; IDEAL itself must not claim accreditation.

MoneyMatter's v0.33.6 release (29 October 2026) added New Zealand bank sync through Akahu and specifically instructs users to create a Personal App and enter its App Token and User Token. This is a useful implementation reference for the single-user use case. Tokens are secrets and must be stored only in a protected local secret store or encrypted server-side configuration, never in source control, logs, prompts or audit transcripts.

### Initial feasibility assessment — research only

| Capability | Preliminary viability | Constraints / next evidence |
|---|---|---|
| Manual accounts, assets, liabilities and transactions | High | Define canonical ledger, import formats, correction/reversal semantics and reconciliation |
| CSV/OFX/QFX statement import | High | Test real export formats, duplicate detection, transfer matching and provenance |
| Budgets, bills, subscriptions, debt and cash-flow views | High | Define period/calendar rules, recurring transaction handling and forecast uncertainty |
| Net worth and investment aggregation | High | Native-currency ledger, point-in-time prices, stale-price flags, FX lineage and no assumed cash pooling |
| Akahu Personal App for owner's own bank data | Plausible / high-priority test candidate | One-user own-account restriction; daily sync and no payment initiation/webhooks; verify current supported banks, data fields, refresh behaviour, terms and token controls |
| Direct IDEAL accreditation for public open banking | Not justified for personal-only use | CDR accreditation includes organisational, security, insurance/liability and complaints requirements; no need to pursue unless product direction changes |
| Payment initiation or automatic transfers | Defer | Separate permission, provider tier, strong confirmation, limits, fraud controls and legal review |
| Public multi-user SaaS | Out of current scope | Would materially change privacy, CDR accreditation, security, support, incident response and legal obligations |
| Always-on public web hosting | Technically possible later, not currently justified | Requires threat model, hardened deployment, backups/restore, MFA, TLS, monitoring, patching and recurring-cost approval; phone-only/free hosting is not yet established as reliable |

### MoneyMatter reference assessment

[MoneyMatter](https://github.com/letehaha/moneymatter) is a strong reference for account aggregation, transactions, categories, transfers/refunds, budgets, bills, subscriptions, loans, investments, net worth, imports/exports, multi-currency reporting, mobile layout and self-hosting. Its current README describes Vue 3/Vite/TypeScript, Node/Express, Sequelize, PostgreSQL, Redis/BullMQ, better-auth and Docker. Its licence is AGPL-3.0; earlier pre-relicensing versions were under CC BY-NC-SA 4.0. Treat it as a reference or isolated trial, not an IDEAL dependency, until exact version provenance, licence obligations, security, data model, tests, dependency health, backups and migration behaviour are audited. Do not copy code or adopt containers by default.

### Non-goals and safeguards

- No public-user product, commercial launch, financial-advice service or regulatory accreditation programme is authorised.
- No bank credentials, API tokens or account access are to be created or connected as part of this research.
- No payment initiation, bank transfers, brokerage orders or automatic movement of capital.
- No reliance on browser scraping or storing online-banking passwords.
- No assumption that budgeting data is investment permission or available trading capital.
- AI may classify, explain and propose; it cannot alter ledger truth, approve payments, change permissions or execute trades.
- Every import, sync, classification, correction, valuation, forecast and proposed action must carry source/time/version metadata and be reconstructable. Corrections use reversals or superseding records, not silent mutation.

### Status

Proposed private-use domain; Phase 02 architecture research only. No implementation, account connection, credential use, provider selection, payment capability, hosting choice or public release is approved. D-001 remains unchanged. See docs/PERSONAL_FINANCE_RESEARCH.md for the focused research plan and current evidence.

### F-004 research update — comparative open-source screen (16 November 2026)

A first-pass comparison is now recorded in `docs/PERSONAL_FINANCE_RESEARCH.md`:
- Actual Budget (MIT) is the leading candidate for an isolated synthetic-data budgeting trial: local-first, mature, statement imports, server-based browser/mobile and documented Akahu support. Bank credentials are stored server-side outside budget E2E encryption, so self-hosting and secret controls matter.
- MoneyMatter (AGPL-3.0) remains the broadest feature/reference candidate and includes NZ Akahu support, but its heavier stack, licence history and unverified data/security implementation mean it is not selected.
- Firefly III (AGPL-3.0) is a serious alternative for personal-finance tracking and transaction workflows.
- Beancount (GPL-2.0-only) and hledger (GPL-3.0) are useful double-entry accounting/import design references, not turnkey user-facing budgeting apps.
- Akahu Personal App's own documentation confirms daily refresh, one-hour manual-refresh rest period, account data only, no payments/webhooks, one user/own account, and developer terms plus identity verification/MFA. Generic Akahu refresh defaults differ by app class; use Personal App-specific limits.

Disposition remains research-only: no installation, bank account, credentials, real statements, dependency, runtime integration or provider selection approved. Actual is only a candidate for an isolated synthetic-data evaluation after the relevant architecture/security gate.


### Comparative repository audit update — 16 November 2026

The detailed audit is in [docs/PERSONAL_FINANCE_RESEARCH.md](PERSONAL_FINANCE_RESEARCH.md), sections 11–16.

- **Firefly III v6.7.9 + Data Importer v2.3.5:** strongest double-entry/multi-currency personal ledger candidate; 2FA and REST API. Akahu provider code and tests are present in the v2.3.5 source tag, but current user-facing setup documentation omits Akahu and NZ transfer mapping has known gaps. No at-rest encryption; AGPL-3.0-or-later; no native securities holdings.
- **MoneyMatter v0.33.7:** broadest all-in-one feature reference with Akahu, investment holdings, multi-currency and transaction sync tests. Bank tokens encrypted at rest, but no E2EE, no native 2FA, no disclosed third-party security audit; cloud Plus/trial sends selected transaction details to AI for categorisation. AGPL-3.0-only. Self-hosted mode is the only version worth considering for synthetic-data evaluation, with AI/MCP disabled.
- **Actual Budget 26.11.0:** strong local-first envelope-budgeting UX, MIT, experimental Akahu support and optional E2EE for budget data; native multi-currency is explicitly unsupported, and bank-sync tokens are plaintext on the server.
- **Money Manager Ex v1.9.4:** encrypted local/mobile/manual finance option with investment accounts, budgets and multi-currency; no Akahu or web/API integration identified.
- **GnuCash 5.17, Beancount v3 and hledger 1.52.4:** accounting/investment/ledger-model references rather than integrated phone-first bank-connected products.

Revised recommendation: do not adopt a single external app as IDEAL's universal ledger. Keep Personal Finance as its own domain and use read-only consolidated projections from investment/trading engines. Firefly III is the leading external ledger candidate for isolated synthetic-data evaluation; MoneyMatter is the broadest feature/UX reference. No product, dependency, bank connection or implementation is selected. D-017 remains Proposed and Phase 02 remains architecture/contracts only.


### Pinned Akahu source audit update — 17 November 2026

Pinned source inspection of MoneyMatter v0.33.7 and Firefly III Data Importer v2.3.5 is recorded in `docs/PERSONAL_FINANCE_RESEARCH.md`, section 17. MoneyMatter has the stronger mocked Akahu E2E coverage (pagination, 14-day overlap, stable-ID idempotency, unlink/relink, outage/auth recovery and balance history), but its existing-ID path skips changed rows, it does not reconcile upstream deletions, does not fetch pending transactions, imports every row as `not_transfer`, and does not preserve Akahu's explicit foreign-currency conversion fields. Firefly stores Akahu IDs and defaults to identifier-based deduplication, but its inspected Akahu feature test is a TODO/mock skeleton; it also skips same-ID updates, does not reconcile upstream deletions or pending transactions, and rounds foreign amounts to two decimals.

Revised research disposition: neither connector meets IDEAL's required source reconciliation contract. MoneyMatter is the better Akahu integration/UX reference; Firefly remains the stronger external double-entry ledger reference, not an adopted dependency. Any future POC must be separately approved and synthetic-only. D-017 remains Proposed; no implementation, account connection, credential, runtime, provider or hosting is approved.


### Backup and credential-key audit follow-up — 17 November 2026

MoneyMatter's pinned v0.33.7 source uses AES-256-GCM for stored bank credentials, with a key derived from `APPLICATION_JWT_SECRET`; preserve that deployment secret because no rotation workflow was found in the inspected source. Its backup tests strip bank/AI secrets and restore bank connections as disabled until credentials are re-entered. Attachments are excluded and require separate backup. Firefly's Akahu importer path has no visible application-level encryption for its Akahu tokens. Full evidence is in research section 17.7. No app or backup/restore was executed; no implementation or real data is approved.
