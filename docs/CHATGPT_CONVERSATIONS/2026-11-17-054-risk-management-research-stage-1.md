# Checkpoint 054 — Risk management architecture research, Stage 1

**Date:** 17 November 2026  
**Project phase:** Phase 02 — architecture and contracts  
**Research scope:** Initial risk management architecture research for crypto perpetual futures  
**Status:** Working research draft; not owner-approved as final architecture  
**Authority:** Documentation/research only

## Owner instruction

The owner authorised beginning the risk-management architecture research and explicitly allowed substantial depth, asking to be consulted where material uncertainty requires owner input. This does not authorise implementation, exchange access, paper/live execution, policy changes or phase advancement.

## Research conducted

The initial research examined:
- perpetual-specific risk controls and supervisory principles;
- exchange margin modes, mark prices, risk tiers and liquidation mechanics;
- layered pre-trade and post-trade automated trading controls;
- portfolio-level risk and stress-margin methodologies;
- risk authority, order lifecycle, failure containment and cross-pillar integration requirements.

## Main evidence and sources

1. **Hong Kong Securities and Futures Commission — High-level framework for virtual asset perpetual contracts offering by virtual asset trading platforms.** Last update shown as 11 February 2026. Relevant points: independent and verifiable price inputs, multiple price sources, contingency/failover for disrupted inputs, pre-trade margin checks, concentration-sensitive margin, predefined liquidation/loss-allocation priorities, stress testing, mark/index divergence and abnormal funding/liquidation surveillance, business continuity, and disclosure of cascading liquidation, basis and liquidity risks. This is supervisory guidance for SFC-licensed platform operators, used here as an engineering reference only.  
   https://www.sfc.hk/en/News-and-announcements/Policy-statements-and-announcements/A-high-level-framework-for-virtual-asset-perpetual-contracts-offering-by-VATP

2. **FIA — Best Practices for Automated Trading Risk Controls and System Safeguards, July 2024.** Relevant points: layered pre-trade controls, maximum order size, maximum intraday positions, price tolerance, cancel-on-disconnect, kill switches, working-order inclusion, independent drop-copy reconciliation, post-trade monitoring and conformance testing. FIA is industry best-practice material, not a universal law applying to IDEAL.  
   https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf

3. **Binance Futures liquidation protocols.** Mark price is used for liquidation and unrealised P&L; actual liquidation outcomes can differ from an estimated liquidation price during rapid movement.  
   https://www.binance.com/en/support/faq/detail/360033525271

4. **Binance Futures insurance funds.** Insurance funds mitigate counterparty liquidation risk but are not insurance products and do not guarantee user losses.  
   https://www.binance.com/en/support/faq/detail/360033525371

5. **Bybit Unified Trading Account liquidation process.** Documents isolated/cross/portfolio margin modes, mark-price liquidation, risk-tier-dependent maintenance margin and staged liquidation actions including cancellation of increasing orders and partial reduction.  
   https://www.bybit.com/en/help-center/article/UTA-Trading-Rules-Liquidation-Process

6. **Bybit maintenance margin for USDT perpetual and expiry contracts.** Documents tier-dependent maintenance rates/deductions and changing requirements as position value changes.  
   https://www.bybit.com/en/help-center/article/Maintenance-Margin-USDT-Contract

7. **OKX cross-margin rules.** Shared collateral/equity can cause losses on one position to put other positions using the same collateral token at risk; isolated margin separates position collateral.  
   https://www.okx.com/help/iii-single-currency-margin-cross-margin-trading

8. **OKX API documentation.** Provides account/position margin and equity fields and warns that estimated liquidation prices can change with funding, other positions and rapid market moves.  
   https://www.okx.com/docs-v5/en/

9. **CME SPAN and SPAN 2.** Useful portfolio-risk references. SPAN uses hypothetical portfolio scenarios; SPAN 2 adds explicit historical risk, stress risk, liquidity and concentration components. Not adopted and not treated as a drop-in crypto-perpetual model.  
   https://www.cmegroup.com/solutions/risk-management/performance-bonds-margins/span-methodology.html  
   https://www.cmegroup.com/clearing/risk-management/span-overview/span-2-methodology.html

10. **CPMI-IOSCO Principles for Financial Market Infrastructures.** Reference material for comprehensive risk, collateral, margin, liquidity and operational risk. IDEAL is not being classified as an FMI.  
    https://www.federalreserve.gov/frrs/regulations/appendix-cpss-iosco-principles-for-financial-market-infrastructures.htm

11. **Financial Stability Board — Policy Recommendations for Crypto and Digital Asset Markets (16 November 2023).** Relevant broader risk areas include conflicts of interest, market integrity, custody, cross-border, operational and technological risk.  
    https://www.fsb.org/2023/11/policy-recommendations-for-crypto-and-digital-asset-markets/

## Principal architectural implications

- Risk management is an independent authority/control system, not a strategy-owned calculator.
- Risk decisions should be layered: owner policy/system authority, portfolio risk, strategy/trade risk, order/execution risk and venue constraints.
- Venue margin/liquidation is not a substitute for IDEAL's own risk authority.
- Venue-specific contract/margin rules require adapters, provenance and versioning; no universal simplified margin formula is sufficient.
- Working orders and partial fills must count as potential exposure. A cancel request is not a confirmed cancellation.
- Portfolio risk requires gross/net exposure, concentration, collateral and funding risk, liquidity-aware close-out estimates, historical measures and coherent stress scenarios.
- Mark/index divergence, funding shocks, risk-tier changes, stablecoin depegs, liquidity collapse, API outages, correlated liquidation and ADL require explicit scenarios.
- A kill switch is a final backstop. Stop-new-risk, cancel increasing orders, permit defined risk-reducing actions and close positions are distinct actions requiring explicit policy.
- A risk approval should be bound to exact action parameters, policy version, portfolio and market evidence, validity conditions, idempotency and audit evidence.
- Risk-increasing actions should fail closed when critical inputs, policy, calculations, reconciliation or monitoring are unavailable or stale.
- The four foundations remain integrated: data integrity supplies trustworthy inputs; system health independently monitors controls; security protects policy, permissions and evidence.

## Existing policy constraints preserved

- D-001: crypto perpetual futures remain the sole active initial market scope.
- D-006: initial per-trade risk target remains 0.5% of equity.
- D-008: hard daily loss boundary remains 10% of UTC day-start equity, realised plus unrealised, followed by a 24-hour cooldown.

This research does not validate or change these numbers. The daily hard boundary must not be mistaken for the sole or desired operating risk limit. Earlier warnings, throttles, portfolio limits and intermediate containment controls remain unresolved and require further research.

## Provisional design hypotheses — not accepted decisions

The working draft proposes a versioned owner-approved policy registry; reconciled capital/portfolio state; market/instrument risk adapter; exposure/margin calculator; risk-budget allocator; pre-action decision authority; continuous risk monitor; emergency control/recovery manager; and independent audit.

It proposes risk states such as Normal, Restricted, Halted, Recovery Required and Unknown, with risk-increasing actions blocked when required evidence is untrusted. It proposes that the execution component receives only exact, current and narrowly scoped authorisation. These are hypotheses for further review, not final approved contracts.

## Repository changes

- Created `docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md` — initial research draft with evidence, provisional authority model, components, portfolio and position risk, controls, cross-pillar contracts, failure modes, verification requirements and open questions.
- Updated `ROADMAP.md` — risk management research workstream.
- Updated `README.md` — source-of-truth index.
- Created this checkpoint audit record.
- Updated conversation audit index.

No decision-register entry was added because this checkpoint records research and provisional design hypotheses, not a new owner-approved architectural decision.

## Governance

Phase 01 remains closed. Phase 02 remains active. Phases 03–19 remain locked. No code, tests, dependencies, runtime configuration, credentials, exchange integrations, external services, infrastructure or financial records were changed. No exchange or margin mode was selected. No numerical risk policy was changed.

## Verification

All created/updated paths must be fetched from `main` after writing and checked for expected content. Read-back evidence and blob SHAs will be appended after successful verification.

## Read-back verification

All five paths below were fetched from `main` after the writes. Expected checkpoint markers were present in each response.

| Path | Read-back blob SHA | Check |
|---|---|---|
| `docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md` | `c8c0faac3a57a6bfadb3503fef0e56d7cccc3d28` | PASS |
| `docs/CHATGPT_CONVERSATIONS/2026-11-17-054-risk-management-research-stage-1.md` | `9cd7f2f8c2c41d931bf694f1ec58afb23a3cc663` | PASS |
| `ROADMAP.md` | `0524a7954d8b7455bcbee030c2e980fab95bc67e` | PASS |
| `README.md` | `6721b17425f106fbcfcdc504a5025012179021b2` | PASS |
| `docs/CHATGPT_CONVERSATIONS/README.md` | `18270ab71bcb622c40838bb477646d6f82ddf62b` | PASS |

## Research extensions added to the working draft

After the initial checkpoint write, the risk research document was expanded to cover:
- distinct capital measures: economic equity, risk-adjusted equity, venue margin equity and available margin, with immutable financial events separated from time-varying valuations;
- leverage, gross/net notional, margin utilisation and liquidation buffer as distinct risk measures;
- isolated/cross/portfolio margin, collateral scope, netting and hedge assumptions;
- funding cash flows, contract-specific valuation, settlement timing and dynamic funding intervals;
- time-varying venue risk tiers, margin rates, leverage caps and position limits;
- risk-policy classes and owner-controlled policy change governance;
- hierarchical risk budgets and conservative reservations for working orders, partial fills and uncertain order states.

Additional primary sources:
- Binance Futures balance definitions: https://www.binance.com/en/blog/futures/457299340443288694
- Bybit V5 wallet balance API: https://bybit-exchange.github.io/docs/v5/account/wallet-balance
- Bybit Unified Trading Account glossary: https://www.bybit.com/en/help-center/article/Glossary-Unified-Trading-Account
- OKX account overview: https://www.okx.com/docs-v5
- Binance funding rates: https://www.binance.com/en/support/faq/detail/360033525031
- Bybit funding fee calculation: https://www.bybit.com/en/help-center/article/Funding-fee-calculation
- OKX perpetual funding mechanism: https://www.okx.com/help/perps-funding-fee-mechanism
- Bybit risk limits: https://www.bybit.com/en/help-center/article/Risk-Limit-Perpetual-and-Expiry-Contracts

The document remains a working research draft. No final risk architecture, venue, margin mode or new numerical policy has been approved.
