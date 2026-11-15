# Exchange-specific liquidation and recovery gap matrix

- **Research date:** 2026-11-15
- **Scope:** Official public documentation for Binance Futures, Bybit UTA derivatives, and OKX derivatives
- **Purpose:** Determine whether the current NautilusTrader research POC can represent exchange liquidation and recovery semantics, and define the minimum venue-specific test contract.
- **Decision:** No exchange selected. No adapter, account, API key, testnet account, or live connection created.

This is a source-based comparison, not a guarantee of exchange behaviour in every jurisdiction, product, account type, or future rule revision. Product-specific contract specifications and account-specific terms prevail.

## 1. Executive findings

1. **The three venues do not share one liquidation state machine.** They all use mark-price/risk-based triggers, but partial reduction, takeover, bankruptcy-price treatment, insurance-fund allocation, ADL triggers, and event observability differ materially.
2. **NautilusTrader 2.0.0rc9's simulated liquidation path is not an exchange liquidation model.** Its matching engine cancels open orders when configured, checks for an executable bid/ask, then submits a single reduce-only IOC market close for the full open position quantity. It does not implement the venue-specific tier-reduction, bankruptcy takeover, insurance-fund or ADL workflows described below. Source: [pinned matching-engine liquidation path](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L2939-L3025).
3. **Liquidation trigger price, bankruptcy price, and actual execution price must remain separate fields.** A trigger can occur on mark price; the exchange can take over at a bankruptcy reference; actual execution can be better or worse; the fund/ADL ledger handles the difference.
4. **Public liquidation feeds are not sufficient as an account ledger.** They are market snapshots or risk indicators. Account state must be reconstructed from authenticated private events plus REST history/backfill and position/balance reconciliation.
5. **No engine adoption decision is justified yet.** The POC remains research-only. A selected venue will require a venue-specific adapter and a deterministic reference model with fixtures for every liquidation stage.

## 2. Venue comparison

| Dimension | Binance Futures | Bybit UTA derivatives | OKX derivatives |
|---|---|---|---|
| Trigger | Maintenance-margin breach using mark-price risk valuation | Mark Price; isolated position liquidation price; cross/portfolio account MMR | Mark Price; MMR at or below 100%; warning threshold documented at 300% |
| Initial response | Cancel relevant open orders; submit one large IOC liquidation order | Cancel orders that increase exposure; isolated position or account risk evaluated according to margin mode | Risk warning; cancel relevant unfilled orders at trigger |
| Partial reduction | One IOC can partially fill; if remaining margin is adequate, liquidation stops | Risk-tier ladder: IOC reduce from current tier to lower tier; re-evaluate maintenance margin; repeat/takeover if still unsafe | Futures reduced by two risk tiers per step; margin/options by one tier; recalculate MMR after each step |
| Full takeover | Unfilled bankrupt remainder is taken over by the Futures Insurance Fund at bankruptcy price | Liquidation engine takes over at bankruptcy price if tier reduction cannot restore margin | FAQ describes full close after reaching the lowest applicable tier, at mark price; separate ADL docs describe bankruptcy-price matching when fund is nearly depleted |
| Insurance fund | Multiple pools by contract groups/collateral; covers bankruptcy-price vs execution-price difference | Separate pools by product and some project risk profiles; surplus credited, deficit covered | Security funds can cover negative assets; one or more funds may apply per product line |
| ADL trigger | Relevant insurance fund cannot accept/cover further bankrupt positions | 8-hour contract PnL drawdown reaches the pool's trigger line, or combined balance of independent pools falls to/below zero | Security fund falls significantly below a preset threshold; special pre-market futures volume/time trigger also documented |
| ADL ranking | Symbol PnL percentage and effective leverage; account equity affects effective leverage | Leveraged return; different isolated vs cross/portfolio formulas | Leverage PnL%; account-level MMR modifies the ranking formula |
| Negative-balance handling | Automated clearance every 10 minutes only under stated eligibility conditions; otherwise support process | Insurance fund covers deficits; ADL if insufficient; no general automatic-clearing schedule identified in reviewed docs | Security fund covers negative assets; ADL is the last-resort mechanism |
| Important observability caveat | Public liquidation stream is a 1-second snapshot, only latest/largest event per symbol in interval; use private account stream for own account | Public all-liquidation snapshot every 500ms; private position stream exposes Liq/Adl status and ADL rank | Security-fund telemetry changed in June 2026; position/order/bill reconciliation must handle system events and tradeId=0 |

### Binance Futures

**Liquidation sequence**
- Binance describes Smart Liquidation: cancel open orders (all cross-margin orders, or same-token isolated orders), then send one large IOC to offload as much of the position as possible.
- If the remaining position satisfies maintenance margin after realized losses and liquidation-clearance fee, liquidation stops.
- If IOC remainder is still bankrupt, the Futures Insurance Fund takes over the remainder at bankruptcy price.
- If the fund cannot take the bankrupt exposure, ADL is engaged.
- The fund covers the difference between bankruptcy price and liquidation execution price; it is not a guarantee against user losses.
- Binance documents automated negative-balance clearance every ten minutes only if Multi-Assets Mode is off, the account has no open positions, and the user has not transferred funds into the deficit account after liquidation. Otherwise support may be required.

**Fund and ADL**
- Multiple funds are allocated to contract groups; COIN-M contracts using the same collateral asset share a fund.
- Binance says minimum fund sizing is calibrated to a 99.9% confidence interval over historical stressed scenarios and reviewed quarterly. This is a calibration statement, not a promise that ADL cannot occur.
- ADL ranking uses symbol-level PnL percentage and effective leverage, with account-level wallet balance plus unrealized profit in the leverage calculation.

**Telemetry**
- Public `@forceOrder` / `!forceOrder@arr` feeds are 1-second snapshots; only the latest liquidation order per symbol in the interval is pushed. Do not treat this as a complete event tape.
- Private `ORDER_TRADE_UPDATE` identifies liquidation and ADL order events (including `LIQUIDATION`, `autoclose-...`, and `adl_autoclose` markers); `ACCOUNT_UPDATE` carries balance/position changes and may include `INSURANCE_CLEAR`.
- The symbol ADL risk rating considers fund balance, concentration, depth, volatility, leverage, unrealized PnL and margin utilization, but is updated every 30 minutes. It is a coarse risk indicator, not a real-time trigger.
- The REST user force-order history supports filtering `LIQUIDATION` versus `ADL`; the 2026 API changelog limits force-order history queries to the previous 90 days.

Official references:
- [Binance Futures Liquidation Protocols](https://www.binance.com/en/support/faq/detail/360033525271)
- [Binance Futures Insurance Funds — updated 2026-01-04](https://www.binance.com/en/support/faq/detail/360033525371)
- [Binance ADL](https://www.binance.com/en-AE/support/faq/detail/360033525471)
- [Binance USD-M User Data Streams](https://developers.binance.com/en/docs/products/derivatives-trading-usds-futures/user-data-streams)
- [Binance liquidation snapshot stream](https://developers.binance.info/docs/derivatives/usds-margined-futures/websocket-market-streams/All-Market-Mini-Tickers-Stream)
- [Binance USD-M REST market data: ADL risk and insurance-balance snapshot](https://developers.binance.me/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)

### Bybit UTA derivatives

**Liquidation sequence**
- Liquidation uses Mark Price, not last traded price.
- Isolated mode is position-scoped. Cross and Portfolio Margin modes are account/portfolio risk-scoped; the displayed liquidation price may be estimated or unavailable in Portfolio Margin.
- The UTA process cancels orders that increase exposure. Above the lowest risk tier, it submits an IOC reduction sized to move the position to the lower tier. It then re-evaluates maintenance margin. If the position remains unsafe, the liquidation engine takes over at bankruptcy price.
- At the lowest tier, the process cancels exposure-increasing orders and then takes over at bankruptcy price if the maintenance requirement remains breached.
- Bankruptcy price is a takeover/settlement reference. The engine does not send the takeover through the normal matching engine. Better-than-bankruptcy execution contributes surplus to the insurance fund; worse execution creates a deficit for the fund to cover.

**Fund and ADL**
- Insurance funds are separated by product class (inverse, USDT, USDC), with some USDT projects assigned distinct pools.
- Isolated-pool API data is updated every minute and its WebSocket push every second; shared-pool API data is daily and no shared-pool WebSocket push is documented.
- ADL is not merely “fund balance equals zero”: Bybit documents an 8-hour contract PnL drawdown trigger line based on the highest fund balance in the period, plus a separate trigger when the combined balance of multiple independent pools falls to/below zero. Stop thresholds differ from trigger thresholds.
- ADL ranks opposing positions by leveraged return, with distinct formulas for isolated and cross/portfolio margin. ADL can partially reduce a selected position; the remainder may stay open.

**Telemetry**
- Public `allLiquidation.{symbol}` snapshots are pushed every 500ms and include side, executed size and bankruptcy price.
- Private position stream includes `positionStatus` = `Normal`, `Liq`, or `Adl`, `adlRankIndicator`, mark price, maintenance margin and risk-tier fields.
- Execution/order enums distinguish `CreateByLiq`, `CreateByTakeOver_PassThrough`, `CreateByAdl_PassThrough`, `BustTrade` (takeover liquidation), and `AdlTrade`.

Official references:
- [UTA liquidation process](https://www.bybit.com/en/help-center/article/UTA-Trading-Rules-Liquidation-Process)
- [Bankruptcy price by margin mode](https://www.bybit.com/en/help-center/article/Bankruptcy-Price-Perpetual-and-Expiry-Contracts)
- [Insurance Fund — updated 2026-03-24](https://www.bybit.com/en/help-center/article/Insurance-Fund)
- [ADL mechanism — updated 2026-04-13](https://www.bybit.com/en/help-center/article/Auto-Deleveraging-ADL)
- [Public all-liquidation WebSocket](https://bybit-exchange.github.io/docs/v5/websocket/public/all-liquidation)
- [Private position WebSocket](https://bybit-exchange.github.io/docs/v5/websocket/private/position)
- [V5 event enums](https://bybit-exchange.github.io/docs/v5/enum)

### OKX derivatives

**Liquidation sequence**
- OKX's current forced-liquidation FAQ says the trigger is maintenance margin ratio at or below 100%, using mark price. A 300% threshold is described as a warning parameter, not the liquidation trigger.
- Relevant unfilled orders are canceled first. Cancellation scope differs by margin mode: cross cancels all unfilled orders (including bot orders); isolated cancels opening-direction orders while retaining close-direction TP/SL orders.
- Partial liquidation reduces futures by two tiers per step and margin/options by one tier per step, recalculating MMR after each step.
- If the position/account remains unsafe at the lowest applicable tier, the remaining position is fully closed. The FAQ describes futures full-close execution at mark price.
- Liquidation fees include the taker fee rate and a liquidation-clearance fee; the FAQ says the proceeds go to the security fund. If the account ends negative, the security fund covers the negative assets.
- ADL is the last resort when the applicable security fund cannot take over more bankrupt positions. OKX says normal ADL matching is at mark price; if the fund is nearly depleted, bankruptcy price may be used.

**Fund and ADL**
- Each product line may have one or more applicable security funds.
- ADL can be triggered when fund value falls significantly below a preset threshold; crypto pre-market futures have an additional liquidation-volume/time trigger.
- Ranking uses leverage PnL%, with account-level MMR in the formula. The highest positive leverage PnL% positions are offset first.

**Telemetry and 2026 API changes**
- OKX's API changelog documents liquidation/ADL order-channel fields `fillPx`, `fillSz`, `fillTime`, and `fillPnl`; it sets `tradeId=0` for affected position/order updates and populates the bill `ordId`. Normal trade-ID-only reconciliation is therefore insufficient.
- Effective 2026-06-09, the security-fund REST API removed `regular_update` granularity; balance history is daily after settlement. The `adl-warning` WebSocket no longer pushes in `normal` state; it continues in `warning`/ `adl` states, but several fund/threshold fields return empty strings. The monitoring design must tolerate missing telemetry and must not infer “no ADL risk” from no normal-state message.

Official references:
- [Forced liquidation FAQ — published 2026-09-03, updated 2026-10-05](https://www.okx.com/en-us/help/forced-liquidation-faq)
- [OKX ADL — updated 2026-08-05](https://www.okx.com/en-us/help/iv-introduction-to-auto-deleveraging-adl)
- [Security Fund API change notice — June 2026](https://www.okx.com/en-us/help/notice-security-fund-display-api-updatese-effective-june-9-11-2026)
- [OKX API changelog: liquidation and ADL data improvements](https://www.okx.com/docs-v5/log_en/)

## 3. What the current NautilusTrader POC does and does not model

The pinned `v2.0.0rc9` matching engine:
- Cancels open orders when the configured liquidation path requests it.
- Checks for an executable best bid (long close) or best ask (short close).
- Creates one reduce-only IOC market order for the **entire open position quantity**.
- Routes the close through the generic simulated market-order fill machinery.

It does not, in the audited path, implement the venue-specific tiered partial-reduction ladders, bankruptcy-price takeover, fund pool accounting, negative-balance recovery, ADL triggers/ranking, or exchange-private liquidation event reconciliation described above. The prior POC tests already show two material consequences: a liquidation valuation fallback can trigger while an empty L2 book prevents a close; a severe quote gap can leave a negative simulated account balance without an insurance-fund recovery layer.

**Conclusion:** Do not treat the generic simulator's liquidation result as an exchange liquidation outcome. It is suitable for testing generic position-risk and market-fill mechanics, not for claiming Binance/Bybit/OKX liquidation equivalence.

## 4. Required venue-specific test contract before adapter selection

Once a venue and exact product/account mode are selected, create deterministic fixtures for:

1. Mark-price trigger versus last-price/quote divergence; stale, missing and delayed mark/index inputs.
2. Isolated versus cross versus portfolio risk aggregation; multi-position and multi-currency collateral.
3. Risk-tier transitions, order-cancel scope, partial IOC reduction, partial fills, retries and MMR recalculation after every step.
4. Bankruptcy-price calculation by contract type, side, margin mode, fee rate, funding debit and tick rounding.
5. Actual execution better/worse than bankruptcy price; surplus/deficit fund ledger and pool allocation.
6. Fund depletion and ADL start/stop conditions, ranking, partial ADL fills, affected opposing positions and fees.
7. Negative balance recovery, automated clearing eligibility, timing and manual-review fallback.
8. Private event ordering, duplicate/replayed events, WebSocket disconnect/reconnect, REST backfill and idempotent reconciliation.
9. Public liquidation stream sampling limits and stale/missing fund telemetry.
10. Position/account state reconciliation after liquidation/ADL when normal order IDs or trade IDs are absent, zeroed or non-monotonic.
11. Audit trail fields: trigger source/time/price, bankruptcy reference, each reduction/takeover/ADL quantity, execution fills, fees, fund movements, balance adjustments, final position/account state.

**Fail-closed requirement:** If mark price, account equity, risk tier, collateral haircut, maintenance margin, position state, or system-event reconciliation is stale or inconsistent, do not increase exposure. Treat exchange-reported liquidation/ADL events as authoritative for account reconciliation; the local risk engine is a preventive control, not a substitute for the exchange's risk engine.

## 5. Gate status

- Source comparison: complete for the three candidate venues listed.
- Exchange selected: no.
- Exchange testnet validation: not performed; no account or credentials authorised.
- Venue-specific model tests: blocked until a venue, contract family, and margin mode are selected.
- NautilusTrader production adoption: not approved.
- Phase 01 remains IN PROGRESS. The next independent gate is partial fills, queue position, liquidity consumption and slippage under competing orders.
