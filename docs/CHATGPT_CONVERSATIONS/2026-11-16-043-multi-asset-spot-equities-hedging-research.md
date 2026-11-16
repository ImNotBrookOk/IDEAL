# Checkpoint 043 — Multi-asset future research: spot, equities, commodities and hedging

**Date:** 16 November 2026  
**Phase:** 02 — Architecture/contracts (only unlocked phase)  
**Status:** Research direction captured; preliminary repository screen completed; deeper audits remain open.  
**Decision:** D-016 proposed, not accepted as active asset-class scope.

## User-visible transcript (available portion)

**User:**  
"Yes well I think then we will also need to do a deep research like you have into spot trading engine/ portfolio system.. then we must then also think about adding later the Stock investment engine.... this is also just as important as crypto is not our only asset we will eventually trade. Without making it too complex is there anything else that is important to consider here... What about hedging? Using spot Gold, copper, silver etc etc... without making this too complex but if we are to do this right we might aswel think about all the right things well eventually need and make sure we do an indepth audit and search and find the right code or build it ourselves..."

**Assistant:**  
"Yes. I think we should broaden the architectural research now, before we settle the platform contracts. Otherwise, we risk designing a system that works well for crypto perpetuals but becomes unnecessarily difficult to extend into spot, equities and commodity exposure later.

There is an important distinction, though:

We should design IDEAL to support multiple asset classes, but we should not build all those trading engines at once.

The right approach is a shared investment platform with independently governed domain engines. Each engine gets the functionality it actually needs, while sharing common infrastructure, accounting principles, audit controls and portfolio-level risk visibility.

I would add three future research domains:
- Spot and digital-asset portfolio management — accumulation, DCA, strategic allocation, rebalancing and macro-aware capital deployment.
- Equities and investment portfolios — stocks, ETFs, corporate actions, dividends, cash management and longer-horizon investment strategies.
- Cross-asset hedging and macro allocation — precious metals, industrial metals, currency exposure, rates and other instruments where suitable access and legal structures exist.

We should also research how these domains interact. A collection of individually profitable engines can still create a badly concentrated overall portfolio."

**User:**  
"Yes well I think then we will also need to do a deep research like you have into spot trading engine/ portfolio system.. then we must then also think about adding later the Stock investment engine.... this is also just as important as crypto is not our only asset we will eventually trade. Without making it too complex is there anything else that is important to consider here... What about hedging? Using spot Gold, copper, silver etc etc... without making this too complex but if we are to do this right we might aswel think about all the right things well eventually need and make sure we do an indepth audit and search and find the right code or build it ourselves..."

Earlier conversation transcript is not reproduced here beyond the available messages; this checkpoint records the material request and resulting actions, not hidden reasoning.

## Scope and governance

- Existing D-001 remains unchanged: crypto perpetual futures are the sole active initial market scope.
- D-014 already preserves deferred crypto spot accumulation and equities evaluation.
- Proposed D-016 expands the deferred research agenda to include spot portfolio management, a separate equities engine, commodity-linked instruments and cross-asset hedging.
- No spot/equity/commodity implementation, strategy, asset universe, broker, venue, data vendor, account, credential, allocation, hedge policy, paid service or live/paper trading is approved.
- Phase 02 remains architecture/contracts only. Phases 03–19 remain LOCKED.
- Modular Monolith remains the approved core architecture direction, with Hexagonal Architecture and Idempotency as supporting patterns. Formal architecture artifact bundle still requires its prescribed validator before write/acceptance.

## Research performed

### Current source and repository screening

1. Loaded the Acumen research skill and queried recent developments separately for crypto spot/custody, equities/broker APIs, commodity exposure/hedging, multi-asset risk/collateral and New Zealand tax/regulatory context. Results were used as discovery prompts, not accepted as authoritative facts without primary-source checks.
2. Screened open-source project descriptions and official GitHub/docs for:
   - QuantConnect LEAN — Apache-2.0, modular event-driven multi-asset backtest/trading engine.
   - NautilusTrader — LGPL-3.0, deterministic event-driven engine; IDEAL's current POC remains pinned to 2.0.0rc9 and research-only.
   - Hummingbot — Apache-2.0, CEX/DEX spot and perpetual connectors and execution/market-making framework.
   - Freqtrade — GPL-3.0, crypto spot/futures bot, backtesting, dry-run and DCA/position-adjustment patterns.
   - rotki — AGPL-3.0, crypto portfolio tracking, accounting and PnL.
   - Portfolio Performance — EPL-1.0, investment portfolio tracking, performance, multi-account/currency, allocation and rebalancing.
   - Deltabadger — AGPL-3.0, DCA, rebalancing, direct indexing and portfolio tracking.
   - CCXT — MIT, unified crypto exchange API patterns.
3. Screened official New Zealand IRD/FMA and CME educational/contract references.

### Primary sources opened

- QuantConnect LEAN repository: https://github.com/QuantConnect/Lean
- LEAN engine docs: https://www.quantconnect.com/docs/v2/lean-engine/getting-started
- NautilusTrader repository: https://github.com/nautechsystems/nautilus_trader
- Hummingbot repository/docs: https://github.com/hummingbot/hummingbot
- Freqtrade repository/docs: https://github.com/freqtrade/freqtrade
- rotki repository: https://github.com/rotki/rotki
- Portfolio Performance repository: https://github.com/portfolio-performance/portfolio
- Portfolio Performance release history: https://github.com/portfolio-performance/portfolio/releases
- Deltabadger repository: https://github.com/deltabadger/deltabadger
- CCXT repository: https://github.com/ccxt/ccxt
- IRD crypto recordkeeping: https://www.ird.govt.nz/cryptoassets/taxing/record-keeping
- IRD crypto tax: https://www.ird.govt.nz/cryptoassets/taxing
- IRD share investment tax: https://www.ird.govt.nz/income-tax/income-tax-for-individuals/types-of-individual-income/share-investments
- IRD FIF: https://www.ird.govt.nz/fif
- FMA derivatives: https://www.fma.govt.nz/consumer/investing/types-of-investments/derivatives
- FMA derivatives issuer licensing: https://www.fma.govt.nz/business/services/derivatives-issuers/
- CME futures contract specifications: https://www.cmegroup.com/education/courses/introduction-to-futures/learn-about-contract-specifications
- CME contango/backwardation: https://www.cmegroup.com/education/courses/introduction-to-ferrous-metals/what-is-contango-and-backwardation
- CME gold/silver contract comparison: https://www.cmegroup.com/education/articles-and-reports/trading-comex-gold-and-silver
- CME micro metals contracts: https://www.cmegroup.com/markets/microsuite/metals

## Material findings and design implications

- No single candidate should be assumed to provide all portfolio accounting, multi-asset research, market data, broker integration and execution safely.
- LEAN is the strongest preliminary multi-asset engine reference, but its data/cloud costs are separate and simulation models require independent realism audits. Documentation highlights that modularity and broad asset support do not remove fill-model, slippage, market-impact, borrow/funding or live reconciliation limitations.
- Hummingbot is valuable for crypto connector/execution patterns, not a complete long-horizon portfolio accounting authority.
- Freqtrade provides crypto spot/futures bot and DCA examples, but a strategy callback for adding to positions is not equivalent to a separately governed capital-allocation system.
- rotki and Portfolio Performance are useful accounting/reporting references. Their copyleft licences (AGPL-3.0 and EPL-1.0 respectively) require legal review before reuse/embedding.
- Commodity exposures must distinguish physical bullion, physically backed funds/ETFs, futures, options, CFDs and tokenised claims. These products confer different ownership, custody, counterparty, liquidity, legal and tax characteristics.
- Futures contracts have contract-specific underlying, unit, delivery/settlement, tick, expiry and trading schedule. Futures are not spot holdings. Term structure, basis, contango/backwardation, carry and rolls can materially affect returns.
- A hedge is not automatically effective because it is labelled gold/silver/copper. Hedge effectiveness depends on the underlying exposure, horizon, beta/factor sensitivity, correlation stability, basis, currency, funding and liquidity.
- Proposed architecture: separate domain engines and ledgers; shared instrument identity, event/audit, data lineage, accounting primitives and read-only consolidated risk; explicit authorised capital-allocation events; portfolio-level hedge/exposure module as a future separate capability.
- Do not pool cash, margin, collateral, permissions or risk budgets across engines by assumption.

### New Zealand issue-spotting

- IRD crypto recordkeeping guidance specifies asset type, transaction date/type, units, NZD value, opening/closing units, exchange records and wallet addresses, retained for at least seven years.
- IRD guidance states foreign shareholdings may be subject to FIF rules; the commonly referenced NZ$50,000 threshold and exemptions/methods require case-specific confirmation.
- IRD share-sale taxation depends on circumstances including dominant purpose at acquisition, dealing activity and profit-making schemes; blanket assumptions about capital gains being tax-free are unsafe.
- FMA guidance says derivatives issuers making regulated offers to NZ retail investors must be licensed. This is not a determination of the user's personal legal position or the eligibility of any offshore product/provider.
- This is preliminary issue-spotting, not tax/legal advice. Independent NZ professional advice is required before any real-money product, provider or account decision.

## Repository changes made

1. `docs/FUTURE_SCOPE_IDEAS.md`
   - Added F-003 multi-asset investment and portfolio research scope, domain boundaries, shared services, hedging capability, additional risk/data/tax issues, preliminary code shortlist, findings and explicit deferred status.
   - Commit: `ba575cb898d6f696b6d7e8888e036a96894b3724`
   - Blob SHA returned: `1f1f42f14b0087d3803ad62790689dcbdd6b180d`

2. `DECISIONS.md`
   - Added D-016 as Proposed, not Accepted. It records only the owner's request to research future spot, equities, commodity exposure and cross-asset hedging; it explicitly preserves D-001.
   - Commit: `36b0da92f0c2093643284af65d0371c5254d1c2a`
   - Blob SHA returned: `ea9347427ffa6924f127a71aae5d96fc8c8b2552`

3. `ROADMAP.md`
   - Added a current dated Phase 02 research-input note linking the deferred scope and recording that no extra asset class, integration or execution authority is granted.
   - Commit: `fe77e61be0f54a0c73281f7251e3eb81c8a31601`
   - Blob SHA returned: `1e02cd2e2bfea3d45a94e0e236a65388deba1623`

Fetch-back verification and audit index update are still pending at the time this checkpoint was drafted.

## Open work

1. Fetch back all three changed files and verify exact text, D-001 preservation, D-016 Proposed status, phase lock and no implementation authority.
2. Commit this checkpoint and update the conversation index; fetch both back and verify.
3. Continue deep repository audit: exact licences, commit/release recency, issue backlog, test quality, architecture, data model, broker/venue coverage, security, dependencies and feasibility on a low-cost/phone-first workflow.
4. Compare LEAN and other candidate engines against IDEAL's domain boundaries without adopting a framework prematurely.
5. Design cross-asset instrument identity and risk aggregation, then separately design capital allocation, accounting, hedge contracts and domain-specific semantics.
6. Keep commodity and equities work as research inputs only. No expansion of active market scope.

## Current state

- D-001 remains accepted and unchanged.
- D-016 is proposed.
- Phase 02 remains the only unlocked phase.
- Phase 03–19 remain locked.
- No runtime code, broker, venue, account, credentials, paper/live execution, paid service or risk-policy change was authorised.
- **Next step:** verify repository writes and checkpoint/index readback, then continue the asset-class and repository deep audit.
- **Owner approval pending:** any later change to active asset-class scope, implementation or external connectivity.
