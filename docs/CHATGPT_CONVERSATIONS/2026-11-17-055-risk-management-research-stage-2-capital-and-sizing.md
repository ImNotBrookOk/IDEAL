# Conversation 055 — Risk management research, Stage 2: capital and contract sizing

**Date:** 17 November 2026  
**Phase:** 02 — Architecture and contracts  
**Status:** Research/documentation checkpoint only; findings provisional

## Owner direction

The owner agreed to continue the deep Phase 02 risk-management research. No new policy value, venue, account mode, implementation, exchange connection or phase transition was approved.

## Work completed

Expanded `docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md` with:
- current official OKX, Bybit and Binance documentation on equity, collateral haircuts, instrument metadata, risk tiers and linear/inverse contract P&L;
- explicit separation of economic equity, IDEAL risk-adjusted equity, venue margin equity and available margin;
- a provisional recommendation that D-006's 0.5% risk target should use a defined IDEAL risk-adjusted-equity denominator, pending owner clarification;
- preservation of D-008's existing UTC day-start equity basis and 10% hard daily-loss boundary without alteration;
- contract-aware linear/inverse sizing, settlement-currency and FX conversion requirements;
- inclusion of fees, funding, spread, slippage, impact, gap reserve and venue constraints;
- discrete quantity rounding, minimum-size rejection, non-linear search and exact decimal arithmetic;
- distinction between trade risk budgets and venue margin capacity;
- order-risk reservation transitions and new verification cases.

## Key sources

- OKX API v5 account equity and margin fields: https://www.okx.com/docs-v5/en/
- Bybit V5 instrument specifications: https://bybit-exchange.github.io/docs/v5/market/instrument
- Bybit V5 risk-limit tiers: https://bybit-exchange.github.io/docs/v5/market/risk-limit
- Binance Futures calculator, USDⓈ-M and COIN-M formulas: https://www.binance.com/en/support/faq/detail/360036498511
- Binance futures P&L and settlement-currency examples: https://www.binance.com/en-AU/support/faq/detail/3a55a23768cb416fb404f06ffedde4b2
- Bybit USDT-contract P&L (updated 12 August 2026): https://www.bybit.com/en/help-center/article/Profit-Loss-calculations-USDT-Contract
- Bybit inverse-contract P&L: https://www.bybit.com/en/help-center/article/Profit-Loss-calculations-Inverse-Contracts

## Important conclusions

1. Available margin is not wealth, economic equity or an adequate standalone risk budget.
2. Venue margin equity and IDEAL risk-adjusted equity serve different purposes and must not be conflated.
3. Linear and inverse contracts have different payoff/settlement semantics; a generic sizing formula is unsafe.
4. Position size must be solved against total scenario loss, not leverage or initial margin alone.
5. Fees, funding, conversion, liquidity, market impact and gap-through risk must be represented.
6. Quantity must be rounded down and recalculated; if the minimum executable size breaches budget, reject the trade.
7. Order reservations must remain conservative through unknown acknowledgement/cancel states and transition cleanly on partial fills.

## Decisions and boundaries

- No new accepted decision added.
- D-006 remains 0.5% per trade; its equity denominator remains unresolved.
- D-008 remains 10% of UTC day-start equity including realised and unrealised P&L, with a 24-hour cooldown.
- No venue, margin mode, account mode, instrument family, implementation or runtime dependency selected.
- Phase 02 remains active; Phases 03–19 remain locked.
- No live or paper execution, exchange credentials, external infrastructure, or policy changes authorised.

## Verification

The updated risk architecture and roadmap are committed to GitHub. Read-back verification is required and will be recorded before this checkpoint is treated as complete.
