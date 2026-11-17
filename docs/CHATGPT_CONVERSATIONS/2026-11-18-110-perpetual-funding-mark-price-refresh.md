# Checkpoint 110 — Perpetual Funding and Mark-Price Semantics Source Refresh

**Date:** 18 November 2026  
**Repository:** ImNotBrookOk/IDEAL, main  
**Status:** Completed research/documentation checkpoint; Phase 02 remains ACTIVE  
**Authority boundary:** No venue, account mode, formula, runtime, dependency, credential, connection, execution or phase transition is approved.

## Work completed

Created `docs/IDEAL_PHASE_02_PERPETUAL_FUNDING_AND_MARK_PRICE_SEMANTICS_REFRESH.md` using current official Binance, Bybit and OKX sources.

Key findings:
- Funding intervals and caps/floors can vary by contract and may be changed; a global eight-hour schedule is not safe.
- Mark-price methods require venue/product-specific rule versions; generic FAQs may simplify the operative calculation.
- Funding forecasts must remain separate from realised immutable settlement events.
- Funding debits can affect available balance or position margin and therefore liquidation proximity.
- Isolated, cross and portfolio margin modes cannot share an assumed universal liquidation formula.
- Effective-dated instrument configuration, source provenance and fail-closed handling are required.

## Source references

- Binance liquidation FAQ (updated 16 November 2026): https://www.binance.com/en-NZ/support/faq/detail/360033525271
- Binance Default Procedures: https://bin.bnbstatic.com/static/cms/cg08ou2ak0tn7mcplvfg/file/53197b612332da02c20b5b7d19b81ff53ee5f4938c6330c72a30a1ca4f91049f.pdf
- Binance funding FAQ: https://www.binance.com/en-NZ/support/faq/detail/360033525031
- Binance liquidation formula: https://www.binance.com/en-AE/support/faq/detail/b3c689c1f50a44cabb3a84e663b81d93
- Bybit perpetual futures guide: https://www.bybit.com/en/learn/trading/trade-usdt-perpetual-futures
- Bybit contract rules: https://www.bybit.com/en/contract-rules
- OKX perpetual swaps guide: https://www.okx.com/help/i-perpetual-swaps

## Repository changes

- Added: `docs/IDEAL_PHASE_02_PERPETUAL_FUNDING_AND_MARK_PRICE_SEMANTICS_REFRESH.md`
- Updated: `docs/IDEAL_MARGIN_COLLATERAL_AND_LIQUIDATION_ARCHITECTURE.md`
- Updated: `docs/IDEAL_DATA_FRESHNESS_AND_CLOCK_REQUIREMENTS.md`
- Updated: `docs/IDEAL_CRITICAL_CONTRACT_FIELD_SCHEMAS.md`
- Updated: `docs/IDEAL_PHASE_02_ARCHITECTURE_DOCUMENT_MAP.md`
- Updated: `docs/IDEAL_PHASE_02_COMPLETION_READINESS_ASSESSMENT.md`
- Updated: `ROADMAP.md`
- Updated: `docs/CHATGPT_CONVERSATIONS/README.md`

All eight changed/created content files were fetched back after their respective writes and matched the submitted content. This is content read-back, not a full semantic review or runtime test. The historical 38/38 document-map path audit at checkpoint 108 remains a historical result; this checkpoint did not complete a fresh full-map crawl after adding the new document.

## Test and decision disposition

Added future conformance requirements for interval/cap changes, funding timestamp boundaries, linear/inverse and position modes, duplicate/delayed/corrected settlements, margin deductions, mark-method revisions, index-source divergence, tier changes and unknown-state fail-closed behaviour. No runtime tests were run.

D-006 and D-008 remain unchanged. ODR-02/03 remain OPEN. ODR-12 remains a Phase 02 owner gate. Canonical serialization TST-105-01 remains open. No venue or account mode is selected.

**Phase status:** Phase 02 ACTIVE. Phases 03–19 LOCKED. No implementation or external integration authorised.
