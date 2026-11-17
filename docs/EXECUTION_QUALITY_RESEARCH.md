# IDEAL — Execution Quality and Order-Placement Research

**Status:** Phase 01 research only  
**Date:** 16 November 2026  
**Decision boundary:** No execution implementation, exchange selection, account access, or Phase 02 entry is authorised by this document.

## 1. Objective and governing principle

IDEAL is not being designed to win a microsecond race. Its primary execution objective is to make the best risk-adjusted order decision from reliable information, even when that decision takes somewhat longer to compute.

The system must optimise **expected net decision value**, not raw order-entry speed and not execution cost in isolation. A cheaper order can be a worse decision if the strategy's alpha decays while waiting; an aggressive order can be wasteful if the signal is weak or the book is poor. The policy must quantify that trade-off.

For a candidate execution policy \(\pi\), the research objective is to estimate:

\[
U(\pi)=E[\text{gross strategy value captured}]
- E[\text{fees + spread + temporary/permanent impact + adverse selection}]
- E[\text{opportunity cost of unfilled quantity}]
- E[\text{inventory/holding and operational risk}]
\]

subject to deterministic constraints: risk approval, exposure and leverage caps, price collar, order-size/participation limits, deadline, data freshness, market integrity, venue permissions and order-state invariants.

The system must be willing to **wait, reprice, slice, cross, reduce, cancel, or place no order**. No order is a valid outcome when expected net value is not positive with adequate evidence, or when required inputs are uncertain.

## 2. Decision pipeline to research

Keep the following concerns separate. They may later be implemented as modules, but this is a Phase 01 decomposition, not a Phase 02 contract.

1. **Trade intent:** strategy proposes side, desired exposure, target quantity, urgency/deadline, expected alpha horizon, invalidation and risk context.
2. **Market-quality gate:** verify book synchronisation, timestamps, spread/depth, volatility, market status, funding/mark/index consistency and feed health. UNKNOWN means no order.
3. **Pre-trade economics:** estimate gross alpha available over the execution horizon and compare with fees, spread, impact, adverse selection and opportunity cost. Use conservative uncertainty bounds.
4. **Scheduling policy:** decide when and how much to release (immediate, TWAP, VWAP, POV, adaptive schedule or no action).
5. **Placement policy:** decide how to express each child (marketable limit/IOC, passive post-only limit, reprice, cancel/replace, reduce-only risk exit), with venue-specific semantics only after venue selection.
6. **Deterministic risk and OMS:** independently validate every parent/child, state transition, price/quantity precision, reduce-only semantics, position effects and worst-case working-order exposure.
7. **Outcome measurement:** reconcile acknowledgements, rejects, partial fills, cancellations, fees, funding and position state; calculate implementation shortfall and markouts.
8. **Learning loop:** use measured outcomes to update bounded model estimates and policy rankings. AI may explain/propose; it must not self-authorise execution, alter risk limits or bypass deterministic validation.

## 3. Scheduling and placement are different problems

Scheduling determines **when/how much** of a parent order should be released. Placement determines **where/how** each released slice should rest or execute. A strong scheduler with a poor placement policy can still lose; a good placement policy can be misused by an inappropriate schedule.

Candidate baselines to benchmark on identical parent decisions:
- Immediate marketable limit/IOC: urgency benchmark, with explicit collar and residual handling.
- TWAP: simple time-slicing benchmark; not presumed optimal.
- VWAP: volume-profile schedule; forecast errors and causal availability must be modelled.
- POV: participate in observed volume with a hard participation cap; no future volume access.
- Adaptive/catch-up: re-plan only from information available at decision time; account for completion urgency and impact.
- Almgren–Chriss family: scheduling baseline balancing temporary impact and inventory risk; calibrate coefficients from representative data rather than copying textbook constants.
- Passive/post-only placement: evaluate fill probability, queue uncertainty, maker fees/rebates, adverse selection and opportunity cost. L2 market-by-price is not true individual queue identity; avoid claiming exact queue position without L3 or defensible exchange-specific inference.
- GLFT / Avellaneda–Stoikov-style placement: research references for inventory-aware quoting, not default entry/exit policies and not assumed profitable.

The first implementation, if later approved, should be a small, deterministic baseline portfolio. Adaptive or learned policies must beat those baselines on untouched out-of-sample data under the same risk, deadline, market path and cost assumptions.

## 4. Measurement standard

Every comparison must use the same parent intents and time windows, with paired outcomes. Report:
- Implementation shortfall from a predeclared arrival benchmark, with the benchmark's limitations stated.
- Filled fraction, completion probability, time-to-fill, partial-fill distribution and residual quantity.
- Explicit maker/taker fees, rebates, funding where relevant, spread, slippage, market impact and opportunity cost.
- Post-fill markouts at fixed horizons to detect adverse selection.
- Risk-adjusted strategy value captured, not only lower execution cost.
- Confidence intervals, independent parent/path count, regime coverage and worst-tail outcomes.
- Sensitivity to fee tiers, latency, feed delay, cancel/replace delay, queue assumptions, volatility, liquidity and market gaps.

Use paired bootstrap or other justified inference at the **parent-order / independent path** level, not bar-level pseudo-replication. Keep development, validation and untouched out-of-sample periods disjoint. Walk-forward calibration must use only prior observations. Freeze primary comparisons before looking at test results. Reject a policy when evidence is inconclusive; do not select a winner by point estimate alone.

## 5. Open-source research candidates

### 5.1 `eshaan2418/sorx` — OMS, SOR and TCA research reference

- Repository: [GitHub](https://github.com/eshaan2418/sorx); MIT licence declared in repository.
- Inspected: README, `docs/DESIGN.md`, `docs/MICROSTRUCTURE.md`, `go.mod`, initial repository commit and CI workflow.
- Useful ideas: exact fixed-point order accounting; explicit parent/child OMS invariants; journaled state changes; property/fuzz tests; deterministic time-ordered replay; per-venue book validation; liquidity consumption; latency-at-arrival simulation; paired parent-order comparisons; explicit opportunity cost for unfilled quantity.
- Reported evidence: 40-minute BTC-USD/ETH-USD capture across Kraken, Coinbase, Bitstamp and Gemini; 463,653 frames; 154 parent orders; CI runs race tests and fuzzing. Its own report says zero-latency reruns changed mean shortfall by at most 0.13 bp under its assumed 5–80 ms venue delays, while fee differences and patience materially changed results.
- Critical limits: the captured instruments are spot USD pairs, not crypto perpetuals; fees and latencies are illustrative; only about 25 parents per comparison bucket; consolidated best bid/ask was crossed in all 2,374 one-second samples, making midpoint benchmarks misleading; Kraken depth is truncated to 10; simulation has no hidden liquidity, passive queue, competing taker race or market impact beyond consumed levels. The authors disclose these limitations.
- Disposition: **reference only** for OMS invariants, deterministic replay, book validation and TCA design. Do not import as the IDEAL execution engine or treat its performance numbers as transferable evidence.

### 5.2 `moussoulijane/execution-cost-analytics` — experimental design and TCA reference

- Repository: [GitHub](https://github.com/moussoulijane/execution-cost-analytics); MIT licence declared.
- Inspected: README, licence and initial commit (16 October 2026).
- Useful ideas: compare TWAP, forecast VWAP, POV and causal catch-up under shared paths; keep forecasts causal; separate development/test seeds; pair outcomes; bootstrap at path level; test non-inferiority/completion rather than relying on mean cost; report negative or inconclusive results.
- Important result: its own published experiment reports a small adaptive-versus-VWAP mean saving with a confidence interval spanning zero, and worse adaptive mean implementation shortfall than VWAP on both highlighted historical BTC/ETH comparisons. It explicitly states that OHLCV/trade data do not identify causal market impact and that impact parameters are hypothetical.
- Maturity: one inspected initial commit; maintenance history is not yet established.
- Disposition: **research-method reference**, not a calibrated impact model or runtime dependency.

### 5.3 `AshJha0/electronic-trading` — quantitative model and cross-language test reference

- Repository: [GitHub](https://github.com/AshJha0/electronic-trading); MIT licence declared.
- Inspected: README, licence and release 2.0.1 commit dated 31 October 2026.
- Useful ideas: Almgren–Chriss scheduling, Avellaneda–Stoikov/GLFT market-making references, impact models, alpha-aware scheduling, queue-fill probability, pre-trade cost estimates, post-trade markouts and multi-language golden-value tests.
- Limits: much of its calibration example is equities/US large-cap data; the README labels several presets and volume curves illustrative rather than fitted; cross-language numerical equivalence does not establish crypto-perpetual market validity.
- Disposition: **mathematical and test-design reference**. Reuse concepts and golden-test patterns only after independent crypto-perpetual calibration; do not adopt the whole multi-language stack.

### 5.4 Existing IDEAL engine candidates

- NautilusTrader remains an isolated engine POC, not adopted. Its execution realism and simulator limitations are recorded in `research/nautilus_poc/execution_realism_matrix.md`; the existing 84-test POC is not evidence of real-market execution quality.
- HftBacktest remains relevant for L2 replay and queue-aware backtesting research, but it does not remove the need for validated venue data and realistic market-impact calibration.
- No repository above is selected as the IDEAL runtime or execution policy.

## 6. Required experiments before an execution design can be accepted

1. Obtain actual, correctly identified perpetual L2 + trade data and pass the separate historical-data acceptance matrix.
2. Reconstruct books independently and prove no stale/ghost levels, crossed own books, sequence holes or invalid snapshot resets are silently accepted.
3. Establish event-time and receive-time semantics; test delayed, duplicated, reordered and missing messages; distinguish feed delay from exchange execution delay.
4. Build a replay harness with deterministic parent intents and fixed market paths.
5. Benchmark immediate IOC, passive limit, TWAP, VWAP and POV under identical conditions. Add adaptive/optimal schedules only after baselines are reproducible.
6. Calibrate queue/fill probabilities and adverse selection only to the extent the available feed supports them; quantify uncertainty and conservative haircuts.
7. Calibrate impact and liquidity replenishment using parent-order/fill observations, not OHLCV alone. Avoid assuming the strategy's own market impact is zero.
8. Stress fees, maker/taker tier, funding, price collars, order rejections, partial fills, cancel/replace delays, volatility spikes, gaps, venue outages and rate limits.
9. Compare policies out-of-sample by market regime, order size, side, urgency and liquidity bucket. Include confidence intervals and tail costs.
10. Prove OMS/reconciliation correctness and fail-closed behaviour before any future paper execution proposal.

## 7. Current conclusion and gate

The evidence supports a **decision-quality-first, deterministic-first execution research direction**. It does not establish a winning algorithm, profitable edge, calibrated impact model or suitable venue. The smartest policy is not necessarily the cheapest or fastest one; it is the policy with the best conservative expected net outcome for the strategy's actual intent and risk constraints.

The historical L2 data gate remains BLOCKED for execution calibration and venue selection; the seven-day sample is accepted only as a conditional historical market-structure research candidate under the separate validation report. No engine or execution policy has been selected. Phase 01 is CLOSED; Phase 02 architecture/contracts research is ACTIVE; Phases 03–19 remain LOCKED. No code, dependency, exchange connection, account, paid service or order execution was introduced by this research.
