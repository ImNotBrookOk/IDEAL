# Conversation 059 — Risk management research, Stage 6: strategy, model and AI risk

**Date:** 17 November 2026  
**Phase:** 02 — Architecture and contracts  
**Status:** Research/documentation only; findings provisional

## Work completed

Expanded `docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md` with:
- model/strategy inventory and immutable provenance requirements;
- distinct prediction, regime, strategy, portfolio allocator, risk authority and execution responsibilities;
- experiment-population tracking, selection-bias and backtest-overfitting controls;
- chronological/nested/walk-forward validation and untouched holdout requirements;
- conceptual soundness, outcome analysis, monitoring and independent challenge;
- calibration, uncertainty and no-trade handling for regime models;
- execution model validation under realistic costs, liquidity and latency;
- drift detection, restriction, suspension and retirement;
- AI-agent risks including hallucination, prompt injection, data exfiltration, tool misuse, non-determinism and self-modification;
- least-privilege agent boundaries and prohibition on AI authority over capital, policy or execution;
- model lifecycle/promotion gates and aggregate correlated model risk;
- adversarial, reproducibility and independent verification requirements.

## Key sources

- Federal Reserve SR 26-2, revised model-risk guidance (17 April 2026): https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm
- Federal Reserve supervisory guidance on model risk management: https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm
- NIST AI Risk Management Framework 1.0: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- NIST Generative AI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- Bailey et al., Probability of Backtest Overfitting: https://escholarship.org/uc/item/4w1110bb
- Bailey & López de Prado, Deflated Sharpe Ratio: https://doi.org/10.3905/jpm.2014.40.5.094

## Important conclusions

1. Strategy, predictive, risk, execution and AI components all create model risk and require declared purpose, scope, limitations and lifecycle governance.
2. Extensive strategy search creates selection bias; all trials and rejected experiments must be retained.
3. A good backtest is not sufficient for approval; validation requires point-in-time data, realistic execution, out-of-sample/walk-forward tests, baselines and independent challenge.
4. Prediction, strategy generation, portfolio allocation, risk authority and execution must remain separate.
5. Regime uncertainty must permit no-trade rather than force a confident label.
6. AI-generated strategies and code are untrusted proposals; AI cannot modify policy, approve itself, or receive unrestricted trading credentials/tools.
7. Drift, material changes and shared dependencies can invalidate previously approved models; revalidation, restriction or retirement must be controlled.

## Decisions and boundaries

- No new accepted decision added.
- D-006 remains 0.5% per trade; equity denominator unresolved.
- D-008 remains 10% of UTC day-start equity including realised and unrealised P&L, followed by 24-hour cooldown.
- No strategy/model/agent/framework selected or promoted.
- No online self-learning, self-modification, runtime integration, exchange credentials or execution authority authorised.
- Phase 02 remains active; Phases 03–19 remain locked.

## Verification

The risk architecture and roadmap were committed to GitHub. This audit record and conversation index were created. All changed paths must be fetched back from the default branch and content-checked before checkpoint completion.
