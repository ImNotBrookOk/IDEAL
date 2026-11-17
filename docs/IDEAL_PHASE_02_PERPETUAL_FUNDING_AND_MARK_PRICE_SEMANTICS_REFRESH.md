# IDEAL Phase 02 — Perpetual Funding and Mark-Price Semantics Source Refresh

**Checkpoint:** 110 — 18 November 2026  
**Status:** Research only; no venue, account mode, data feed, formula or runtime selected  
**Scope:** Current official-source refinement of funding, mark/index/last price and liquidation decision contracts for crypto perpetual futures.

## 1. Purpose and disposition

The existing margin/collateral architecture correctly separates mark, index, last-trade and executable prices, and the data-freshness contract distinguishes funding forecasts from realised settlement. This refresh tightens the venue-neutral contract because official venue material demonstrates that funding intervals, caps/floors, mark-price construction and margin consequences are configurable and may change.

**Conclusion:** IDEAL must treat funding schedules and mark-price methodology as effective-dated, instrument- and venue-specific configuration/evidence, not global constants. A generic eight-hour schedule, static funding cap, or universal mark-price formula is unsafe. No current venue documentation is a substitute for the exact contract specification, applicable account mode, current rulebook and authenticated event stream.

## 2. Official-source observations

### 2.1 Binance

- Binance's Futures liquidation FAQ, updated 16 November 2026, distinguishes Last Price (latest execution; used for realised PnL) from Mark Price (reference used for unrealised PnL and liquidation). It describes Mark Price as a combination of funding data and a basket of spot-exchange prices. The same page says leverage and required margin vary with absolute exposure and maintenance-margin tiers. Source: https://www.binance.com/en-NZ/support/faq/detail/360033525271
- Binance's official contract Default Procedures describe a more specific perpetual mark-price calculation: the median of three values, including an index/funding-adjusted value, an index plus moving-average deviation, and the contract's last traded price. The document defines a moving average of best-bid/ask mid-market deviation and allows the funding interval to vary. This is a materially more detailed rule than a simplified FAQ description. Source: https://bin.bnbstatic.com/static/cms/cg08ou2ak0tn7mcplvfg/file/53197b612332da02c20b5b7d19b81ff53ee5f4938c6330c72a30a1ca4f91049f.pdf
- Binance's funding FAQ describes an interest-plus-premium mechanism, but also says funding caps/floors and intervals may be adjusted in extreme conditions; some contracts differ from the default interval. Funding deductions may come from available balance and, if insufficient, position margin, affecting liquidation risk. Sources: https://www.binance.com/en-NZ/support/faq/detail/360033525031 and https://www.binance.com/en/support/faq/detail/360033525031
- Binance's liquidation-price explanation uses cross-wallet balance and other positions' maintenance margin/unrealised PnL in cross margin, while isolated mode excludes those cross-position terms. Tier-specific maintenance rates and deduction amounts are required; the assumed tier may need recalculation if the resulting notional falls in another tier. Source: https://www.binance.com/en-AE/support/faq/detail/b3c689c1f50a44cabb3a84e663b81d93

### 2.2 Bybit

- Bybit's current educational page says funding intervals and limits can vary by contract and should not be assumed to be eight-hourly. Funding is exchanged between traders at the funding timestamp; a position must be held at that timestamp to pay or receive it. Positive funding means longs pay shorts and negative funding means shorts pay longs. Source: https://www.bybit.com/en/learn/trading/trade-usdt-perpetual-futures
- Bybit's contract rules page describes mark-price-triggered liquidation, funding timestamps and a funding calculation based on position value and rate. It is a useful explanation, but the live contract-specific funding schedule and current limits must take precedence over generic examples. Source: https://www.bybit.com/en/contract-rules
- Bybit's current learning material distinguishes isolated liquidation (position mark-price threshold) from cross/portfolio account-level maintenance risk. Other positions, collateral and liabilities can change the outcome. Source: https://www.bybit.com/en/learn/trading/trade-usdt-perpetual-futures

### 2.3 OKX

- OKX's perpetual swap guide describes mark-price reference use, tiered maintenance margin and periodic funding settlement. Its generic guide describes the familiar 8-hour UTC schedule, but it must not be promoted to a universal or permanent schedule. Contract-specific live parameters remain authoritative. Source: https://www.okx.com/help/i-perpetual-swaps

## 3. Required IDEAL contract refinements

1. **Effective-dated instrument rule snapshot:** venue, legal/product entity where relevant, instrument identity, contract type, settlement asset, multiplier, margin mode, position mode, risk tier table, funding interval, next funding time, funding cap/floor, mark-price method/version, index constituents/method, fee assumptions, source reference, observed time, effective-from/to and revision.
2. **Distinct price evidence:** index/reference, mark, last trade, executable bid/ask/depth and any venue liquidation trigger price must remain separate typed values. Each carries source, event/publication/receive timestamps, sequence/revision, quality and age.
3. **Funding forecast versus realised settlement:** forecast rate and projected payment are non-ledger estimates. Realised funding is an immutable, uniquely identified settlement event with signed amount, position/notional basis, rate, settlement asset, event time, effective time, venue transaction reference and correction linkage.
4. **Funding schedule as data:** store actual scheduled/observed settlement instants and interval changes. Do not derive future timestamps from a hard-coded 8-hour clock. Handle schedule changes, missed/late events, duplicate events and corrections.
5. **Funding amount is contract-specific:** do not universally assume position value multiplied by funding rate without a verified definition of position value, multiplier, settlement currency, contract denomination, rounding and position snapshot time.
6. **Funding-to-margin interaction:** model venue-reported balance/position-margin effects separately from IDEAL economic PnL and risk-adjusted equity. A funding debit can reduce available balance or position margin and alter liquidation proximity.
7. **Mark-price method is versioned:** a mark value without the applicable method/configuration revision and source provenance is insufficient for an auditable liquidation-risk decision.
8. **Tier transitions are discontinuities to test:** effective-dated tier tables, cumulative maintenance deductions, order exposure, position aggregation and mode-specific scope must be captured. A tier update can alter required margin and liquidation estimate without a market-price move.
9. **Venue documentation hierarchy:** applicable contract specification/rulebook and current authenticated instrument parameters outrank generic help pages. Conflicting summaries are recorded as a source discrepancy, not silently reconciled into one formula.
10. **Unknown state:** missing/stale mark, funding schedule, rate, position snapshot, margin mode, tier table or settlement evidence invalidates dependent calculations. Risk-increasing actions remain blocked; preserve reservations and reconcile rather than substitute last price or assume no funding.

## 4. Additional conformance and adversarial tests

- Funding interval changes immediately before a scheduled settlement; no stale eight-hour assumption.
- Funding cap/floor changes and contract-specific exceptions.
- Position opened/closed immediately around the funding timestamp; boundary inclusivity and venue event ordering.
- Partial close, hedge mode, one-way mode, linear and inverse contracts; verify exact funding basis and settlement asset.
- Duplicate funding settlement, delayed settlement, correction/reversal and replay idempotency.
- Funding debit consumes available balance, then position margin; verify the venue-state and IDEAL-ledger projections remain distinct.
- Mark-price methodology/configuration revision changes while the instrument is open; stale revision must invalidate the risk result.
- Index constituent outage, spot-source divergence, mark/index/last divergence and stale mark.
- Risk-tier change with unchanged position and price; recompute IM/MM and liquidation estimate from the effective tier schedule.
- Cross-margin account with other positions and liabilities; isolated position; portfolio-margin account; do not share one liquidation formula across modes.
- Missing schedule or ambiguous event time; fail closed and retain UNKNOWN until authoritative reconciliation.
- Property tests: no missing evidence is interpreted as zero funding, no stale mark is silently replaced by last price, and a forecast never creates a realised ledger posting.

## 5. Integration and decisions

- Extends [Margin, Collateral and Liquidation Architecture](IDEAL_MARGIN_COLLATERAL_AND_LIQUIDATION_ARCHITECTURE.md) and [Data Freshness, Clock Quality and Decision-Validity Requirements](IDEAL_DATA_FRESHNESS_AND_CLOCK_REQUIREMENTS.md).
- Logical contract fields must include effective-dated funding/mark configuration and settlement-event provenance. The canonical serialization profile must preserve exact signed amounts and timestamps.
- Traceability additions are required for funding schedule/configuration integrity, settlement accounting, mark methodology provenance and mode-specific tier/liquidation recalculation.
- D-006 and D-008 remain unchanged. ODR-02/03 remain OPEN. ODR-12 remains a Phase 02 GATE. No venue or margin mode is selected.
- No code, exchange connection, account, credential, paper/live execution or runtime permission is created. Phase 02 remains ACTIVE; Phases 03–19 remain LOCKED.

## 6. Source limitations

This is a focused official-document refresh, not a legal or contractual interpretation. Some official help pages are explanatory and may be generic, regional or stale relative to a specific contract. The Binance Default Procedures PDF is a formal rule document but its applicability must be confirmed for the eventual product/entity and contract. Bybit/OKX generic guides do not establish all current per-instrument exceptions. A later venue-specific review must fetch the then-current contract rules, instrument metadata, funding history, risk-limit schedule and account-mode documentation together and archive their effective versions.


## 7. API-level event semantics refinement — checkpoint 112

A further review of the official OKX V5 API guide and exchange mark/funding documentation exposed additional distinctions that should be preserved in the canonical evidence model:

- OKX funding-rate history returns `fundingRate` as a predicted rate and `realizedRate` as the actual rate, with `fundingTime`, `formulaType` (`noRate` / `withRate`) and `method` fields. The guide states that intervals for some volatile altcoin swaps may be adjusted from the nominal eight hours to six, four, two or one hour; it specifically directs consumers to compare `fundingTime` and `nextFundingTime` rather than assume a fixed interval.
- OKX public WebSocket funding-rate messages include current rate, funding time, next funding time, min/max rate, premium, formula type, method, settlement state and settled funding rate. `settState` distinguishes `processing` from `settled`; `settFundingRate` semantics differ according to that state. The API documentation also labels the former `next_period` method as no longer supported. Treat this as a versioned API contract, not a permanent schema guarantee.
- OKX historical funding-rate endpoint documents a maximum three-month lookback. Historical reconstruction therefore cannot assume indefinite availability from one public endpoint; archive permitted contemporaneous evidence or use other independently verified sources where long-history research requires it.
- OKX mark-price help (updated 5 August 2026) describes mark as index plus a moving-average basis, with basis derived from contract mid-price minus index. It provides different PnL formulae for crypto-margined reciprocal contracts versus USDT/USDC-margined linear contracts. The formula and denomination therefore require instrument identity, contract face value, multiplier and settlement asset; a single generic linear PnL formula is invalid.
- Binance's funding-rate documentation says funding interval may be adjusted dynamically; its 2025 update describes automatic transition to hourly settlement after a cap/floor event for affected USDⓈ-M perpetuals, and directs API consumers to `GET /fapi/v1/fundingInfo` for current funding information. Its documentation also says a funding debit may first reduce available balance and then position margin, affecting liquidation price.
- Bybit exposes mark-price klines as a distinct historical series from ordinary price klines. This is useful for point-in-time mark reconstruction but does not itself provide the full contemporaneous mark-method inputs or prove the series is complete for a given period.

### Additional contract requirements

1. Preserve predicted rate, realised rate, rate currently being assessed, prior settled rate and next-period estimate as distinct typed values; do not overload a single `funding_rate` field.
2. Preserve funding formula/method identifier and API/schema revision, plus the exact source payload digest.
3. Preserve `fundingTime`, `nextFundingTime`, settlement state, source event time, receive time and local observation time. Do not infer settlement completion from the clock alone.
4. Historical funding and mark datasets require explicit coverage bounds, retention/licence status, gaps, corrections and retrieval limits. Absence outside endpoint retention is UNKNOWN, not zero funding.
5. PnL/risk calculations must dispatch by verified contract denomination and settlement asset; linear and inverse formulae must not share an untyped amount path.
6. Funding-to-margin effects must be represented as ordered venue balance/position-margin events and reconciled against account/position snapshots. Never apply a predicted funding amount as if it were a settled debit or credit.

### Additional future tests

- Distinguish predicted, processing, settled and corrected rates across API revisions; reject unknown method/formula enums.
- Reconstruct interval from adjacent funding timestamps when metadata is incomplete; detect contradictory interval metadata and event times.
- Test the deprecated OKX `next_period` method as a compatibility rejection/normalisation case, not a current assumption.
- Simulate funding endpoint history truncation, missing pages, duplicated timestamps and corrections; preserve explicit coverage gaps.
- Verify linear and inverse PnL and funding amounts in native settlement assets using independent exact-decimal oracles.
- Verify mark-price series and ordinary trade series cannot be substituted for each other in liquidation replay.
- Verify funding debit order (available balance then position margin) only when the selected venue/account mode's current rule proves it; otherwise mark the projection UNKNOWN.

### Sources

- OKX API V5 documentation, public funding history and WebSocket funding-rate channel: https://app.okx.com/docs-v5/en/ (sections “Get funding rate history” and “Funding rate channel”; reviewed 18 November 2026)
- OKX mark price and Last price, updated 5 August 2026: https://www.okx.com/en-gb/help/ii-mark-price-and-last-price
- Binance Introduction to Futures Funding Rates: https://www.binance.com/en-AU/support/faq/detail/360033525031
- Bybit Get Mark Price Kline: https://bybit-exchange.github.io/docs/v5/market/mark-kline

This refinement remains research only. No API, venue, formula, dependency or runtime is selected.
