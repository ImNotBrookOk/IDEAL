# Conversation 057 — IDEAL overall vision and risk research Stage 4

**Date:** 17 November 2026  
**Phase:** 02 — Architecture and contracts  
**Status:** Documentation/research only; risk findings provisional

## Owner direction

The owner asked to continue the risk-management research and update the GitHub main page because it still presented crypto perpetual futures as if that were the entire project. The README has been rewritten to explain IDEAL's overall long-term purpose while clearly distinguishing the current initial research domain from future, gated capabilities.

## README changes

The GitHub front page now presents IDEAL as a private integrated financial intelligence and decision-support platform. It describes:
- the overall goal of understanding, managing, protecting and growing the owner's financial position;
- specialised future domains: market intelligence and quantitative research, systematic trading and investment analysis, portfolio/capital oversight, personal finance and tax-aware financial information;
- crypto perpetual futures as the initial research domain, not the full platform scope;
- the four integrated foundations: risk management, data integrity, system health and security;
- deterministic controls versus bounded AI research/proposal roles;
- owner authority, separate permissions/capital domains, auditability, minimal cost and portability;
- Phase 02 design/research-only status, later phases locked, and explicit approval boundaries;
- initial trading constraints as research specifications, not performance promises or policies for future domains.

The README uses GitHub-native Markdown only. Future domains are described as vision/research scope, not as completed or authorised capabilities.

## Risk research Stage 4

Expanded `docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md` with:
- isolated, cross and portfolio margin semantics and their distinct contagion scopes;
- separation of IM, MM, venue margin ratios, IDEAL risk budgets, available margin and liquidation buffers;
- collateral eligibility, tiered haircuts, wrong-way risk, liabilities and asset/venue dependencies;
- joint stress of collateral, market positions, stablecoins, FX, liquidity and margin changes;
- multi-dimensional liquidation buffer outputs rather than a single liquidation price;
- venue liquidation waterfalls, partial reductions, insurance funds and ADL limitations;
- proposed IDEAL-side shadow margin calculation and reconciliation against venue state;
- margin procyclicality and liquidity preparedness;
- adversarial and independent verification requirements.

## Key sources

- Bybit UTA liquidation process: https://www.bybit.com/en/help-center/article/UTA-Trading-Rules-Liquidation-Process
- Bybit collateral value ratios: https://www.bybit.com/en/help-center/article/Assets-Collateral-Value-Ratio-List-UTA
- Bybit UTA FAQ and margin/available-balance distinction: https://www.bybit.com/en/help-center/article/FAQ-Unified-Trading-Account
- OKX API v5 account and margin documentation: https://www.okx.com/docs-v5/en/
- Binance Futures liquidation protocol: https://www.binance.com/en/support/faq/detail/360033525271
- Bank of England near-final CCP margin supervisory statement (16 November 2026): https://www.bankofengland.co.uk/paper/2026/ss/near-final-supervisory-statement-on-ccp-margin
- CPSS-IOSCO Principles for Financial Market Infrastructures: https://www.federalreserve.gov/frrs/regulations/appendix-cpss-iosco-principles-for-financial-market-infrastructures.htm
- CME SPAN 2 methodology: https://www.cmegroup.com/clearing/risk-management/span-overview/span-2-methodology.html

## Important conclusions

1. Margin capacity is not IDEAL's risk budget.
2. Account mode changes the scope of collateral sharing and liquidation contagion; it must be discovered and versioned.
3. Collateral requires independent assessment of liquidity, concentration, eligibility, haircut, conversion and wrong-way risk.
4. Liquidation prices are estimates, not guaranteed exit prices; IDEAL must act before venue liquidation thresholds with approved stressed buffers.
5. Venue insurance funds and ADL are loss-allocation mechanisms, not guarantees to the account holder.
6. A shadow margin model is useful for independent monitoring and discrepancy detection but cannot claim exact reproduction of proprietary venue logic.
7. Margin increases and collateral haircuts must be stressed jointly with market losses and liquidity deterioration.

## Decisions and boundaries

- No new accepted decision added.
- D-006 remains 0.5% per trade; equity denominator unresolved.
- D-008 remains 10% of UTC day-start equity including realised and unrealised P&L, followed by 24-hour cooldown.
- No venue, account mode, collateral asset, haircut, liquidation-buffer threshold or emergency execution action selected.
- Phase 02 remains active; Phases 03–19 remain locked.
- No runtime implementation, exchange credentials, paper/live execution, bank connection, paid service, hosting or external security scan authorised.

## Verification

The README, risk architecture and roadmap changes were committed to GitHub. The audit record and conversation index were also created. All changed paths must be fetched back from the default branch and content-checked before checkpoint completion.
