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

## Governance

These ideas are deliberately separate from active requirements. They must not expand Phase 01, alter current testing priorities, unlock Phase 02, or be treated as implied approval to build. Revisit them only at a future scope-review point after the initial platform's research and validation gates are complete, or earlier only if the owner explicitly requests a scope review.
