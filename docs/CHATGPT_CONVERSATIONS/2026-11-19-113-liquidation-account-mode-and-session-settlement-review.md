# Checkpoint 113 — liquidation account-mode and session-settlement architecture review

**Date:** 19 November 2026  
**Phase:** 02 — Architecture and contracts  
**Status:** Source review and documentation only

## Scope

Re-examined the liquidation model in `IDEAL_MARGIN_COLLATERAL_AND_LIQUIDATION_ARCHITECTURE.md` against current official exchange material. This was a source-driven refinement of the generic liquidation lifecycle, not a venue selection or implementation decision.

## Evidence

1. Bybit UTA liquidation rules, updated 15 October 2026, distinguish isolated, cross and portfolio margin:
   - Isolated liquidation is position-scoped and mark-triggered; above the lowest risk tier, a partial IOC reduction may precede full closure.
   - Cross liquidation is account-scoped and can include risk-increasing order cancellation, auto repayment, broader order cancellation, fully hedged-position treatment and unhedged position reduction according to venue liquidity order.
   - Portfolio margin has a distinct portfolio liquidation process, including cancellation of all orders, staged asset/position liquidation, MMR reduction logic and a takeover threshold.
   - Cross/portfolio displayed liquidation estimates are dynamic and account-state dependent.
   Source: https://www.bybit.com/en/help-center/article/UTA-Trading-Rules-Liquidation-Process
2. Bybit's same official documentation describes a USDC perpetual session-settlement mechanism where average entry basis changes at settlement, session realised PnL and margin adjustments are reflected, and fee-to-close / maintenance calculations are recomputed. This creates a discontinuity that a fills-only replay cannot safely infer.
3. OKX API V5 exposes account-level IMR/MMR, adjusted equity and forced-liquidation risk fields for relevant margin modes, reinforcing that account risk state is not reducible to one isolated position formula. Source: https://www.okx.com/docs-v5/en/
4. Binance published a USDⓈ-M margin-tier update dated 12 September 2026, demonstrating that risk tiers can be revised and must be effective-dated. Source: https://www.binance.com/en/support/announcement/detail/2adc4f459022496db814a96b93215a1e

## Changes committed

- Margin/liquidation architecture: removed duplicated checkpoint-110 appendix and added §16 account-mode-specific liquidation pathways and §17 session-settlement discontinuities.
- Critical Contract Field Schemas: added §21 logical records LiquidationPolicySnapshot, LiquidationActionEvent, LiquidationEstimate and SessionSettlementEvent.
- Requirement traceability: added R-LIQ-001–004 / T-LIQ-01–04 and R-MARGIN-010 / T-MARGIN-10.
- Required distinction between request, acknowledgement, execution and reconciliation; uncertain actions retain exposure reservations.
- Generic liquidation states remain a common event vocabulary only. Actual transition graphs must be keyed by venue/product/account mode/position mode/risk tier/effective policy revision.
- Cross/portfolio estimates are explicitly dynamic and account-scoped; no fixed position stop assumption.
- Session settlement must be explicit and reconciled, not inferred from candles or funding timestamps.

## Verification status

- Documentation changes committed through GitHub contents API and fetched back from GitHub main.
- All six changed architecture/traceability/schema/map/readiness/roadmap files plus this audit were fetched back and their expected sections checked.
- The current architecture document map contains 45 unique local Markdown targets. All 45 were fetched successfully in four bounded batches; no missing targets were returned.
- No tests, runtime code, API clients or exchange connections were run or created.
- No venue, account mode, formula, risk tier, or liquidation policy selected.

## Open gates

ODR-02/03 remain OPEN; ODR-12 remains the Phase 02 owner acceptance gate; TST-105-01 remains open. Phase 02 ACTIVE / NOT COMPLETE; Phases 03–19 LOCKED. No credentials, paper/live trading, paid service or external action authorised.
