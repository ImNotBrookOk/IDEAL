# IDEAL Trading Knowledge and Skills

This file is a versioned knowledge framework, not a substitute for validated rules or tested code. Add knowledge with source, date, applicability, confidence and known limitations.

## Core domains
- Perpetual futures mechanics: contract specifications, mark/index/last price, funding, basis, margin modes, liquidation, precision and exchange failure modes.
- Market structure: trend, range, swing structure, breaks/retests, volatility expansion/contraction and liquidity.
- Regimes: bull, bear, range, transition and volatility/liquidity sub-regimes; unknown/low-confidence states must remain explicit.
- Liquidity and execution: spread, depth, order-book dynamics, market impact, slippage, stop execution and partial fills.
- Derivatives context: funding, open interest, basis, liquidations and positioning, with source-quality controls.
- Multi-timeframe analysis: 1W/1D macro; 4H/1H structure; 30M intermediate; 15M entry; optional 5M refinement.
- Indicators: trend, momentum, volatility, volume, market structure and derivatives features. Track formula, parameters, warm-up, data requirements, regime fit and feature correlation.
- Quantitative research: hypotheses, baselines, sample size, uncertainty, multiple-testing correction, walk-forward validation, out-of-sample testing and bias prevention.
- Risk: fractional sizing, portfolio exposure, correlated positions, leverage, liquidation distance, drawdown, daily loss and operational kill switches.
- Execution: order state machines, idempotency, exchange precision, fees, funding and reconciliation.
- Learning: outcome attribution and concise lessons linked to strategy/version, regime, timeframe, context and execution.

## Knowledge admission
Each addition must state: claim; evidence/source; observed period; instruments/regimes; confidence; limitations; validation status; date; version. Distinguish established mechanics, empirical findings, hypotheses and model-generated suggestions.

## Strategy lessons
Store one concise lesson per completed paper trade, but do not generalise from one trade. Aggregate lessons only with adequate samples and uncertainty estimates. Preserve all lessons and history through strategy demotion.

## Non-negotiable
Confluence is contextual evidence, not a standalone entry signal. Correlated indicators do not count as independent confirmations. No strategy is considered profitable from win rate alone.