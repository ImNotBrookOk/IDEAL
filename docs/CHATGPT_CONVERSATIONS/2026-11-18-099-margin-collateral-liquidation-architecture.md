# IDEAL Work Audit — Checkpoint 099

**Date:** 18 November 2026  
**Phase:** 02 — Architecture and contracts  
**Workstream:** Margin, collateral, tiering and liquidation architecture  
**Status:** Research/documentation only.

## Sources reviewed
Official Binance USDⓈ-M margin, liquidation, tier and insurance-fund documentation; Bybit UTA liquidation process (last updated 15 October 2026); OKX Futures cross-margin article (updated 11 August 2026) and API v5 guide; Hyperliquid margin-tier documentation. Acumen current-state brief queried before research. Exa searches used to locate primary documentation and pages were fetched for review.

## Findings
- Mark price can trigger liquidation while last trade differs; liquidation threshold is not execution price.
- Tiered maintenance margin is piecewise, with tier-specific rate and deduction; venue/account-mode aggregation varies.
- Isolated, cross and portfolio margin have different loss-sharing boundaries and liquidation rules.
- Bybit documents cancellation of risk-increasing orders, partial reduction for higher tiers, then closure; Binance documents bankruptcy takeover, insurance-fund capacity and ADL.
- Insurance funds are not insurance for the trader and do not guarantee protection against losses or ADL.
- Collateral value requires asset eligibility, price freshness, haircuts, concentration, depeg, liquidity, transferability and currency conversion treatment.
- Risk-adjusted equity must remain distinct from venue-reported margin equity and available margin.
- Pending/uncertain orders reserve worst-case exposure until reconciled.
- No implicit hedge credit across venues/accounts/netting sets; portfolio offsets require enforceable netting and stress evidence.
- Liquidation must be represented as a lifecycle with uncertain outcomes, not a deterministic single price.
- Simulator synthetic liquidation close is not a live venue execution result.

## Repository changes
Created docs/IDEAL_MARGIN_COLLATERAL_AND_LIQUIDATION_ARCHITECTURE.md. Updated risk management architecture, Phase 02 document map, owner decision register, roadmap, README and audit index.

## Verification and boundaries
Every changed file is fetched back from GitHub and content-checked. No tests, code, dependencies, exchange access, credentials, venue selection, margin-mode selection, numerical policy changes, paper/live execution or external service deployment. D-006/D-008 unchanged; Phase 02 active; Phases 03–19 locked.
