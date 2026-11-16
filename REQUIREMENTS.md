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

## Integrated system objective and foundational requirements

IDEAL is one integrated personal financial intelligence system composed of specialised, bounded domains and engines. It is not a collection of independent trading bots. Every consequential capability must operate within shared risk, data-integrity, system-health and audit requirements. The integrity of the whole system takes precedence over the performance or autonomy of an individual engine.

### Foundational protection requirements

1. **Risk management:** a mandatory, deterministic and independently enforced gate for actions that create or increase financial exposure. It must account for position sizing, leverage/margin/collateral, liquidation, liquidity and execution costs, concentration, correlation, drawdown, portfolio exposure and operational risk as applicable to each authorised domain.
2. **Data integrity:** decision inputs must have source identity, provenance, timestamps, schema, completeness, freshness, quality state, correction history and lineage. Raw evidence, canonical observations, derived intelligence, research artefacts and decision evidence remain distinguishable and reproducible.
3. **System health:** a deterministic supervisor must independently monitor sources, data pipelines, engines, dependencies, storage, reconciliation, backups and audit integrity. A component's own health assertion is not sufficient proof.
4. **Mutual reinforcement:** data quality and health state are inputs to risk validity; risk restrictions and health interlocks constrain dependent engines; reconciliation and audit findings feed back into system health and engineering research.
5. **Failure containment:** critical missing, stale, invalid, contradictory or unknown inputs cause the affected consumer to enter a safe no-action state. Failures must be contained to their dependency blast radius; unrelated domains must not be disabled without a declared reason.
6. **Authority separation:** strategy/AI components may analyse and propose but cannot change risk limits, approve their own permissions, certify their own data or bypass health interlocks. Consequential actions require explicit authority and deterministic enforcement.
7. **Audit and recovery:** decisions, policy versions, inputs, quality states, incidents, overrides, reconciliation and recovery must be traceable. Recovery requires verified continuity and reconciliation, not merely a successful reconnect.
8. **Design quality:** architecture, contracts, threat models, research and test criteria must be sufficiently complete and independently challenged before implementation. Schedule pressure must not lower the correctness, security or auditability bar.

These requirements apply across the system, while domain-specific contracts and permissions remain separate. Future spot, equities, commodities, hedging, personal-finance and tax domains inherit the shared protections but remain proposals until separately authorised. See [Core Protection Architecture](docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md).

No new numerical risk limits or execution permissions are introduced here. Existing scope and phase approval boundaries remain in force.


### Security and assurance requirements

9. **Security by design:** IDEAL must protect confidentiality, integrity, availability, authenticity and accountability across applications, data, identities, infrastructure, development and integrations.
10. **Least privilege and explicit authority:** owner, service, agent and integration identities receive only scoped permissions. Authentication does not imply authorisation. AI prompts and model outputs are not security boundaries.
11. **Secrets and data protection:** credentials and encryption keys require dedicated lifecycle management, rotation and revocation; sensitive data must be encrypted, minimised, access-controlled and excluded from ordinary logs/prompts.
12. **Secure supply chain and development:** dependencies, build artefacts, CI/CD, configuration and source changes require provenance, scanning, review and reproducible verification.
13. **Independent security monitoring:** security telemetry and control status integrate with system health, but security assurance is reported separately. Operational availability must never be presented as proof of security.
14. **Vulnerability and incident lifecycle:** use threat modelling, static/dynamic analysis, dependency/secret scanning, fuzzing, authorised penetration testing, remediation tracking, incident response and verified recovery. No scan can guarantee discovery of every vulnerability.
15. **Audit and privacy:** sensitive access, permission changes, key lifecycle, configuration changes and security incidents must be auditable and tamper-evident. Retention must respect purpose, privacy and provider/legal constraints.

See [IDEAL Security Architecture and Assurance](docs/IDEAL_SECURITY_ARCHITECTURE.md). Security is a mandatory Phase 02 design workstream; this does not authorise implementation, external scanning or new integrations.

## Architecture-first completion requirements

IDEAL's first major development milestone is a complete, internally consistent and independently challenged architecture before implementation. The architecture must define the system and domain boundaries, authority hierarchy, trust boundaries, responsibilities, dependencies, interfaces, data flows, failure propagation, safe states, audit evidence and recovery behaviour.

The four foundations must each have a detailed design: risk management, data integrity, system health and security. Critical cross-pillar/domain interfaces must specify ownership, schemas and semantics, permissions, provenance, validity/freshness, error and timeout behaviour, idempotency/correction semantics, safe responses, escalation, audit and recovery verification.

Architecture completion requires a system/domain map; four foundation designs; critical interface contracts; data-flow/trust/dependency/failure diagrams; threat model and security-control matrix; failure-mode and recovery analysis; requirements-to-component-to-test traceability; recorded assumptions and residual risks; independent design review; verification strategy; and explicit owner acceptance.

Only after architecture acceptance may implementation-ecosystem research be converted into a proposed stack/blueprint. Each repository, library, model or dataset must be assessed for exact licence and use rights, maintenance, engineering quality, tests/documentation, security, dependencies, compatibility, portability, cost, limitations and evidence. Record reuse/adapt/isolate/defer/reject disposition. No technology is adopted by popularity alone.

Deterministic software remains authoritative for risk calculations, accounting, data validation, reconciliation, permissions and safety enforcement. AI may assist bounded research and analysis but cannot be the security boundary, policy authority or sole validator of its own output.

These requirements are Phase 02 design/research only. They do not authorise code, dependencies, runtime integration, deployment, external security testing, exchange access or phase advancement. See [Architecture-First Research and Design Plan](docs/IDEAL_ARCHITECTURE_FIRST_RESEARCH_PLAN.md).
