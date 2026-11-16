# Conversation 056 — Risk management research, Stage 3: portfolio stress and liquidity

**Date:** 17 November 2026  
**Phase:** 02 — Architecture and contracts  
**Status:** Research/documentation checkpoint only; findings provisional

## Owner direction

The owner approved continuing Phase 02 risk-management research. This tranche does not alter accepted risk policy or authorise implementation, exchange access, venue selection or phase advancement.

## Work completed

Expanded `docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md` with:
- portfolio-level risk stack combining deterministic exposure, historical risk, tail statistics, hypothetical stress, liquidity and concentration;
- dynamic dependence, downside correlation, common-factor, liquidity, venue and strategy dependency analysis;
- conservative hedge-credit requirements and gross-exposure preservation;
- overlapping concentration taxonomy across assets, strategies, venues, collateral, settlement, funding and infrastructure;
- coherent market, correlation, liquidity, funding, collateral, margin and operational stress families;
- liquidity-adjusted close-out and time-to-liquidate requirements;
- VaR/Expected Shortfall limitations and point-in-time data requirements;
- auditable portfolio outputs and independent verification cases.

## Key sources

- CME SPAN methodology: https://www.cmegroup.com/solutions/risk-management/performance-bonds-margins/span-methodology.html
- CME SPAN 2 historical/stress/liquidity/concentration framework: https://www.cmegroup.com/clearing/risk-management/span-overview/span-2-methodology.html
- CME SPAN reference materials: https://www.cmegroup.com/solutions/risk-management/performance-bonds-margins/span-reference-documents.html
- 2026 Hyperliquid liquidation-cascade liquidity working paper: https://papers.ssrn.com/sol3/Delivery.cfm/6636998.pdf?abstractid=6636998&mirid=1&type=2
- 2026 Bybit hidden/displayed liquidity working paper: https://papers.ssrn.com/sol3/Delivery.cfm/6891658.pdf?abstractid=6891658&mirid=1&type=2
- 2026 October 2025 liquidation-cascade working paper: https://papers.ssrn.com/sol3/Delivery.cfm/6579278.pdf?abstractid=6579278&mirid=1&type=2
- 2026 cross-exchange perpetual market integration study: https://www.mdpi.com/2227-7072/14/5/103
- 2026 cross-exchange funding market study: https://www.mdpi.com/2227-7390/14/2/346

## Important conclusions

1. Portfolio risk cannot be inferred by summing isolated trade-risk estimates.
2. Static correlation and recent diversification can fail under stress; hedge credit must be evidence-backed and conservative.
3. Gross exposure, common factors, venue, collateral, settlement, strategy and liquidity dependencies must remain visible.
4. Stress scenarios must shock prices, correlation, basis, funding, liquidity, margin and operational conditions coherently.
5. Displayed depth and quoted spread do not guarantee executable exit capacity; liquidity horizon and market impact matter.
6. VaR/Expected Shortfall are supplementary estimates, never substitutes for hard limits, scenario tests or fail-closed controls.
7. Some recent crypto evidence is from working papers and narrow samples; it is used to identify scenarios, not to set numerical haircuts or limits.

## Decisions and boundaries

- No new accepted decision added.
- D-006 remains 0.5% per trade; equity denominator unresolved.
- D-008 remains 10% of UTC day-start equity including realised and unrealised P&L, followed by a 24-hour cooldown.
- No venue, account mode, margin methodology, numerical concentration/liquidity threshold or implementation selected.
- Phase 02 remains active; Phases 03–19 remain locked.
- No paper/live execution, exchange credentials, paid service, external scan or runtime change authorised.

## Verification

The updated architecture and roadmap were committed to GitHub. Read-back verification is required before checkpoint completion.
