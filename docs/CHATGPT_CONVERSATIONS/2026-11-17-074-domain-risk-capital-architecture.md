# IDEAL Conversation / Work Audit — Checkpoint 074

**Date:** 17 November 2026 (Pacific/Auckland)  
**Workstream:** Phase 02 — domain risk and capital architecture  
**Repository:** https://github.com/ImNotBrookOk/IDEAL  
**Authority:** D-018, D-019, D-020, D-021, D-022, D-023; D-001/D-006/D-008 preserved  
**Status:** Research/documentation only; Phase 02 active; Phases 03–19 locked.

## 1. Work completed

Reviewed the risk architecture's capital/equity semantics, portfolio aggregation, risk-budget hierarchy, cross-pillar interfaces and conceptual decision contracts, alongside the integrated domain map and data temporal/evidence contract.

Created:
- `docs/IDEAL_DOMAIN_RISK_AND_CAPITAL_ARCHITECTURE.md`

Updated:
- `docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md` §22;
- `docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md`;
- `REQUIREMENTS.md`;
- `ARCHITECTURE.md`;
- `docs/IDEAL_FOUNDATION_TRACEABILITY_MATRIX.md`;
- `ROADMAP.md`;
- `README.md`.

## 2. Key architecture conclusions

1. Risk is a vector of domain-specific dimensions, not one universal score. Derivatives, spot investments, equities, commodities, hedging, personal cash flow and tax intelligence need separate risk contracts.
2. The portfolio/capital view is read-only by default. It can aggregate evidence and highlight risk but cannot infer authority to transfer, allocate, net, hedge, lock or liquidate capital.
3. Gross exposure, net directional exposure, factor exposure, liquidity, counterparty/custody, margin/collateral, economic net worth, cash-flow capacity and tax exposure remain separate views.
4. Ledger cash, pending/available cash, investment market value, derivatives economic equity, risk-adjusted equity, venue margin equity, available margin, collateral, encumbered capital, tax estimate, assessed liability and owner-designated reserve are distinct concepts.
5. No implicit netting across legal entities/accounts/venues, no cross-venue collateral portability and no hedge credit without explicit policy and stress evidence.
6. D-006 and D-008 remain specific to the initial crypto-perpetual risk policy. D-006 denominator remains unresolved; D-008 semantics remain as accepted. No new numerical limits are introduced.
7. D-018 remains a hard user-autonomy invariant: tax reserves are informational and cannot lock, deduct, segregate or force payment of capital.
8. Missing/stale FX and valuations yield incomplete/unknown aggregates, not silent zero or unlimited stale carry-forward.

## 3. Governance boundaries preserved

No new numerical risk limit, capital allocation, unified risk budget, hedge-credit policy, netting set, domain activation, implementation, runtime integration, account access, credentials, external financial action, paid infrastructure or phase advancement. No tests were run; future verification cases are requirements only.

## 4. Next work

Reconcile risk/capital contracts with account and portfolio reconciliation, authority/action lifecycle, health/security incident containment and audit/retention. Then perform an integrated cross-document adversarial challenge and identify residual owner decisions for the complete architecture review.
