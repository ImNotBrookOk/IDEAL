# IDEAL Requirements

## Product objective
Build an autonomous crypto-perpetuals intelligence system that researches strategies, validates them statistically, classifies them by market regime and operates eligible strategies in paper trading under deterministic controls.

## Scope
- Initial instruments: crypto perpetual futures. Exchange selection remains an open research decision.
- Context timeframes: 1W/1D macro; 4H/1H structure; 30M intermediate; 15M entry evaluation; optional 5M refinement.
- Android phone is the primary user control/monitoring device. Compute may run on a free-tier remote worker or local-compatible environment, subject to Phase 01 feasibility.
- Autonomous strategy discovery is a core requirement; users should not need to hand-author strategies.
- Paper trading is the only permitted execution mode at this stage.

## Strategy lifecycle
Generate candidates → validate code/data → backtest → cost-adjust → walk-forward/out-of-sample validation → classify by regime → apply absolute quality gates → rank comparable passing cohort → select eligible candidates. No eligible candidate means no trade.

## Execution quality objective
Execution must optimise conservative expected net decision value, not minimum order-placement latency or execution cost in isolation. The execution policy must balance strategy alpha decay and urgency against fees, spread, market impact, adverse selection, fill probability and opportunity cost. It must be able to wait, reprice, slice, cross, cancel, reduce or decline to place an order. Scheduling (when/how much) and placement (where/how) are separate decisions. Compare candidate policies on identical parent intents and market paths, with causal inputs, realistic costs, paired inference, uncertainty intervals and untouched out-of-sample validation. Latency must be bounded and measured, but is not the primary optimisation objective. See [Execution Quality Research](docs/EXECUTION_QUALITY_RESEARCH.md).

## Preliminary screening
The user's initial screen is more than 100 trades and win rate above 30%. This is necessary only as an initial filter and is not sufficient proof. Additional gates must include positive net expectancy, profit factor, drawdown, uncertainty, regime robustness, execution realism and untouched out-of-sample performance.

## Risk requirements
- Initial per-trade risk target: 0.5% equity.
- Research objective: 1:3 reward/risk, assessed using realised net R after costs.
- Daily hard loss boundary: 10% of UTC day-start equity, realised plus unrealised, then 24-hour cooldown.
- Define and approve earlier warning/suspension levels, portfolio exposure limits, leverage caps, correlated exposure controls, liquidation buffers and order-rate limits before paper execution.
- Position sizing, order validation, stop/exit logic and gate enforcement must be deterministic.

## Learning requirements
Store trade context, regime, timeframe, strategy/version, indicators, risk state, execution details, outcome and a concise AI-generated lesson. Lessons must be searchable and survive strategy demotion or gate rollback.

## Reliability and security
Fail closed on stale data, missing candles, malformed payloads, clock drift, reconciliation mismatch, unavailable risk controls and ambiguous position/order state. Keep exchange secrets server-side; never place secrets in client code or logs.

## Cost and deployment
Target $0 recurring cost. Prefer open source and free tiers. Record free-tier limits, sleep/quotas, data retention and migration constraints. No billing or paid plan without approval.

## Unresolved decisions
Exchange/data provider; deployment target; universe/liquidity filters; fee/slippage model; absolute statistical thresholds; minimum cohort size; portfolio and leverage limits; early loss warnings; progression gate thresholds; AI provider/token budget; retention/backup policy. Resolve through documented research and approval before dependent implementation.