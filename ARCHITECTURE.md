# IDEAL Architecture (Provisional)

## Principles
Deterministic-first, modular, auditable, fail-closed and cost-constrained. AI is an untrusted bounded reasoning component, never the authority for risk or execution permissions.

## Logical components
1. **Market data** — exchange adapters, historical loader, live stream, normaliser, candle completeness and freshness checks.
2. **Knowledge registry** — versioned SKILLS.md knowledge, rules and indicator metadata.
3. **Market state** — multi-timeframe structure, regime classifier and explicit UNKNOWN state.
4. **Indicator library** — pure calculations with warm-up, missing-data and numerical-stability contracts.
5. **Intelligence/context** — evidence aggregation, source lineage and correlated-feature controls.
6. **Strategy lab** — bounded candidate generation, versioning and deterministic parameter schemas.
7. **Research engine** — event-driven backtester, cost/fill models, walk-forward and out-of-sample validation.
8. **Strategy registry/selector** — eligibility, regime scope, cohort ranking and selection history.
9. **Risk engine** — sizing, exposure, stop/exit validation, daily loss and cooldown state machine.
10. **Future paper-execution simulator (not authorised)** — a proposed isolated simulation capability for order lifecycle, fills, fees, funding, positions and reconciliation. It is not an active runtime component and must not be implemented or used without separate explicit owner approval.
11. **Learning store** — trade records, lessons, retrieval metadata and immutable history.
12. **Gate controller** — deterministic promotion/demotion and permission state.
13. **Orchestrator** — startup, scheduling, health checks, recovery and safe shutdown.
14. **Mobile dashboard** — Android-first status, controls, audit trail and alerts.

## Data flow
Research flow: authorised public/historical market evidence → validation/normalisation → market state and indicators → contextual evidence → candidate strategy research → backtest and statistical validation → versioned experiment evidence. A future execution flow is only conceptual: proposed action → independent risk decision and reservation → separately authorised execution adapter/simulator → authoritative reconciliation. No paper or live order flow is currently authorised or running. Gate controller consumes verified research evidence but cannot grant execution authority. Every future consequential transition must emit versioned, traceable evidence.

## Trust boundaries
- Exchange/API responses, external text, historical datasets and model outputs are untrusted.
- Secrets remain server-side.
- Strategy code runs in a constrained environment with resource/time limits.
- Risk and order validation are separate from strategy generation.
- Any future execution adapter must reject actions if required inputs, policy, approval, reservations or state are absent, stale, invalid or inconsistent. This is a design requirement, not current execution authority.

## Contracts to define in Phase 02
Instrument and candle schema; timestamp/timezone convention; market-state schema; indicator metadata; strategy manifest; backtest result; order/fill/position ledger; risk decision; gate state; trade lesson; event envelope; error taxonomy.

## Deployment
Deployment remains intentionally undecided. The owner has approved phone-first control/monitoring, with an existing Windows PC/laptop only as a fallback if a concrete requirement forces it. No cloud provider or host is selected; no PC/cloud provisioning, inbound ports, continuous feed or paid infrastructure is authorised. GitHub Actions remains research CI, not a persistent trading worker. The pinned NautilusTrader POC passes on x86_64 and ARM64 but remains a pre-release research candidate, not an adopted engine. See [Infrastructure Research](docs/INFRASTRUCTURE_RESEARCH.md). SQLite event journal remains an isolated research prototype and requires target-environment durability, external hash anchoring and backup/restore validation before any future runtime consideration.

## Cross-domain scope and user authority (Phase 02 design requirements)

IDEAL is intended to become one coherent personal system with independently governed domains, not one monolithic trading strategy. The initial active trading scope remains crypto perpetual futures under D-001. Future research scope includes long-term crypto spot accumulation, stock/ETF investing, commodity exposure and cross-asset hedging (D-014/D-016), plus Personal Finance and Tax Intelligence proposals (D-017/F-004 and F-005). These future domains must not be mistaken for active implementation approval.

**User authority is a system invariant.** IDEAL provides information, analysis, recommendations, alerts and explicitly authorised actions. It does not own the user's capital or silently impose financial choices. In particular, tax estimates and recommended tax reserves are informational/accounting views only: no mandatory segregation, escrow, lock, deduction, forced payment, trade block or investment block. The user may choose to deploy funds shown as a recommended reserve. IDEAL must explain and record the resulting estimated exposure and relevant due dates, without restricting access. Legal obligations remain distinct from software permissions.

## Shared data trust and system-health plane (proposed Phase 02 architecture)

All domains depend on a shared, deterministic data trust plane. It is more foundational than any individual strategy or execution engine. It must track source identity and permissions, raw observations, normalisation, provenance, event time and ingest time, sequence continuity, freshness, completeness, quality state, corrections, reconciliation and downstream consumption. Each datum used in a decision must be traceable to its source, retrieval time, transformation/version, validation outcome and applicable instrument/venue.

Data must never be labelled live merely because it was recently retrieved. Each feed has an explicit freshness contract appropriate to its market/session and use. A missing, delayed, stale, contradictory, malformed, out-of-order or incomplete critical input becomes a visible degraded/unknown state. No fabricated values, silent forward-fill, guessed timestamps or stale-as-live substitution are permitted. Critical risk/execution decisions fail closed when mandatory data contracts are not satisfied; non-critical reporting may show last-known values only when visibly marked with age and quality.

A separate deterministic health and audit supervisor should monitor the data plane and the rest of the system: source connectivity and rate limits, feed lag and gaps, clock drift, schema/contract violations, event backlog, scheduler/worker liveness, storage capacity and write failures, reconciliation mismatches, backup age/restore evidence, dependency and configuration drift, audit-chain integrity and component heartbeats. The supervisor must not rely on the component it is checking as its sole source of truth. Health state, incidents, acknowledgements, recovery and overrides are append-only and auditable. It must distinguish healthy, degraded, stale, unavailable and unknown; recovery requires verified conditions, not merely a successful reconnect.

Prefer deterministic scripts, rules, tests and scheduled jobs for ingestion, validation, monitoring, reconciliation, alerting, housekeeping and routine reporting. AI is optional and bounded to tasks where it adds material value (for example, summarising an already verified incident); it is not the data validator, source of truth, risk authority or continuous monitor. This is a token-cost and reproducibility requirement.

## Deployment portability

Phone-first is the current interaction preference, not a permanent compute constraint. Architecture must separate user interface/control plane from data ingestion, scheduled work, storage and compute. A mobile client must not need to stay awake or connected for reliable ingestion/monitoring. Keep deployment portable across a future Windows/Linux PC and a later private server, with explicit adapters/configuration rather than phone-specific business logic. No PC/server/cloud provisioning, paid service, always-on worker or hosting choice is authorised by this requirement.

See `docs/DATA_INTEGRITY_AND_HEALTH.md` for the proposed data contracts, health model, failure behaviour and research questions.


## Integrated core protection architecture

IDEAL is one integrated system of specialised bounded engines. The shared protection foundation consists of risk management (protection/permission), data integrity (evidence) and system health (independent oversight). These are mutually reinforcing requirements across domains, not three optional services or features attached to one trading engine.

Risk is a mandatory independent gate for any activity that creates or increases financial exposure. Strategy engines propose; risk evaluates against approved policy and current exposure; health/data interlocks establish whether the decision's dependencies remain trustworthy; authorised adapters enforce only permitted actions. Risk policies cannot be weakened by AI, strategy output or a component's self-reported state.

Data contracts must carry provenance, timestamps, completeness, freshness, quality and lineage. Raw evidence, canonical observations, derived intelligence, research artefacts and decision evidence remain distinct. Corrections are versioned rather than silently overwriting historical facts.

A deterministic health supervisor observes sources, data pipelines, components, dependencies, storage, reconciliation, backups and audit integrity independently wherever practical. It may trigger predefined restrictive interlocks but cannot change financial risk policy, approve trades or initiate financial actions. A component cannot solely certify its own health.

Each engine must declare dependencies, authority, state ownership, acceptable input quality, failure modes, degraded behaviour, recovery prerequisites and audit events. Failure is contained to dependent consumers where safe; a market-data outage must not automatically disable unrelated personal-finance functions. Critical unknown or invalid state fails closed. Recovery requires gap disposition/backfill, replay where appropriate, reconciliation and verified continuity.

The complete owner-approved direction, including the authority model, feedback loops, failure boundaries and Phase 02 design backlog, is in [docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md](docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md). This remains a design contract only; no runtime implementation is authorised.


## Security architecture constraint

Security is the fourth foundational pillar and a cross-cutting constraint across every domain and component. Identity, authorisation, secrets, sensitive data, network boundaries, dependencies, CI/CD, host/runtime, audit and AI tools must be threat-modelled and protected by least-privilege deterministic controls. AI instructions are not an authorisation boundary; tools and actions must be constrained outside the model.

Security telemetry and security-control status feed the independent health supervisor. However, security assurance remains separate from operational health: a process can be available while compromised, and a monitor can be disabled or deceived. The design must include independent evidence, tamper detection, vulnerability management, incident response and tested recovery. No scanner or test can guarantee that all vulnerabilities are found.

The detailed requirements and Phase 02 backlog are in [docs/IDEAL_SECURITY_ARCHITECTURE.md](docs/IDEAL_SECURITY_ARCHITECTURE.md). This is a design requirement only; no security tooling, dependency or runtime change is authorised.


## Bounded-autonomy authority model (D-023)

The future execution architecture uses an owner-approved capability envelope. The owner grants a bounded, versioned, scoped and revocable authority; the engine does not receive unrestricted trading authority. Individual in-envelope actions may proceed without per-action human approval only after exact security permission checks, trusted/reconciled data, health interlocks, deterministic risk approval and reservation, and required durable audit.

Owner approval remains mandatory for capability activation, envelope/policy/permission changes, new accounts/venues/integrations, credential/privilege expansion, fund transfers/withdrawals/payments, safeguard disablement and reserved irreversible or incident-recovery actions. AI/strategy components cannot change or approve the envelope.

The policy registry, signing/root-of-trust, identity enforcement, revocation propagation, reservation/action state machine and audit durability remain Phase 02 contract work. This architecture direction does not activate an envelope or authorise an execution adapter, exchange connection, credentials, paper/live trading or implementation.


## Autonomy authority and permission enforcement (D-023)

A future execution-capable domain must route all consequential operations through a dedicated, non-bypassable action-enforcement boundary outside strategy/AI processes. The boundary separates owner grant, workload authentication, policy authorisation, risk approval/reservation, data trust, health/security interlocks, revocation and audit. It canonicalises the exact action and binds all approvals to its digest, scope, versions, evidence and expiry. Any material change requires fresh decisions.

The action boundary is the only permitted route to a future execution adapter. Durable intent and risk reservation precede dispatch. Ambiguous external outcomes remain UNKNOWN and reserved until authoritative reconciliation; no blind retries or timeout-based reservation release. Policy evaluation, owner approval and risk approval remain separate authorities. Detailed provisional contracts and technology research are in [Autonomy Authority and Permission Architecture](docs/IDEAL_AUTONOMY_AUTHORITY_AND_PERMISSION_ARCHITECTURE.md). No runtime implementation or execution is authorised.


## Revocation, isolation and recovery boundary — checkpoint 068

The authority registry and dispatch boundary serialise revocation against the durable DISPATCH_STARTED transition using a monotonic generation. Revocation-first denies dispatch; dispatch-start-first is in-flight and cannot be recalled. A worker that cannot prove current generation cannot dispatch. Global EFFECTIVE requires acknowledgement from every registered boundary; partitions and uncertain external outcomes remain explicitly unresolved.

AI/strategy/generated-code processes are hostile workloads in a separate trust zone, with no credentials, direct venue egress or privileged host interfaces. Enforce least-privilege OS identities, syscall and filesystem restrictions, namespaces/cgroups, strict IPC and host-level egress controls. Disposable microVMs are a candidate for high-risk code. Shared host root/kernel compromise defeats local process separation and requires a separate trust domain.

Backups restore data, not authority. Recovery quarantines restored permissions, invalidates old capabilities, advances generation, verifies an independent revocation anchor, rebuilds/attests and reconciles external state. If current trust is uncertain, remain in RECOVERY_HOLD. See autonomy architecture §§19–21.


## Health supervisor, policy activation and audit transaction boundaries — checkpoint 069

The health supervisor is an independent observer with a one-way restrictive interlock channel; it cannot create authority or initiate financial actions. Its failure or untrusted status blocks affected risk-increasing actions. Process separation on a shared host does not protect against host root/kernel compromise.

Policy/envelope artefacts are immutable, owner-approved against exact digest, separately signed, versioned and anti-rollback protected. Activation, revocation and dispatch-start serialize against one authority generation.

Before any external side effect, IDEAL durably commits canonical intent, authority evidence, risk reservation, audit event and outbox. It commits DISPATCH_STARTED and its audit event before network write. Remote side effects are not atomic with local storage; ambiguous outcomes remain UNKNOWN and require authoritative reconciliation.


## Unified authority and reservation event ordering — checkpoint 069

Consequential actions bind all current authority, identity, policy, risk, health/security, data, account and instrument versions to the exact canonical action digest. The initial authority generation is monotonic and global for simplicity; it is serialized with policy activation, revocation and dispatch-start. Separate health, security, risk, data and venue metadata generations are also bound.

The authoritative local event/transaction order determines state transitions; wall-clock timestamps are not the sole ordering mechanism. Reservation states distinguish HELD, IN_FLIGHT, PARTIALLY_FILLED, TERMINAL_PENDING_RECONCILIATION, RELEASED and INCIDENT_HOLD. Fill transfer is idempotent; uncertain residual exposure remains reserved. See autonomy authority architecture §27.


## Integrated bounded-context architecture — checkpoint 072

IDEAL is one integrated personal financial intelligence system composed of bounded contexts with explicit state ownership. Integration exchanges versioned evidence and projections; it does not merge ledgers, capital, credentials, policies or permissions. The provisional context catalogue covers market/source data, canonical evidence, market intelligence, strategy research, backtesting, strategy registry, derivatives risk, future execution/reconciliation, personal finance, tax intelligence, portfolio/capital views, archive/datasets, learning/models, health, security/identity, owner authority/policy, audit, orchestration and mobile presentation.

Each context owns its canonical records. Cross-domain aggregation is read-only by default; all amounts retain currency, unit, ownership, account, valuation time and source. No implicit collateral fungibility, legal-entity netting, tax equivalence or hedge credit is assumed. Personal finance imports remain source observations until reconciled into its own journal. Tax outputs are informational and cannot lock capital or force payment (D-018).

The authority hierarchy remains owner → owner-approved policy/authority → security permission → data validity → health interlock → independent risk approval/reservation → domain/action boundary. These are conjunctive gates, not substitutes. Health can restrict only; security can contain/revoke identities but cannot approve financial risk or initiate financial actions; strategy/AI can propose but cannot grant authority.

The complete provisional domain/state ownership catalogue, shared contract families, dependency/containment rules, data-plane separation, open questions and required verification catalogue are in [IDEAL Integrated System and Bounded-Context Architecture](docs/IDEAL_INTEGRATED_SYSTEM_AND_DOMAIN_ARCHITECTURE.md). This does not freeze schemas, module/process topology, storage, deployment or deferred domains.


## Data trust and temporal evidence — checkpoint 073

All data flows preserve source identity, raw evidence, validation version, canonical revision, transformation lineage and point-in-time availability. Event time, publication time, receipt time, ingest time, processing time, valid/effective time, knowledge time and decision-as-of time are distinct. Corrections are new linked revisions; raw observations are not silently overwritten. A backtest may use only data knowable at its simulated decision time.

Data quality is a consumer-specific vector, not a global green flag. Market data, private financial records, security/audit evidence and AI traces are separate data planes with purpose-limited access and retention. Unknown, conflicted, stale, incomplete, unlicensed or unreconciled inputs cannot be silently promoted to valid evidence.

See [IDEAL Data Trust, Temporal Semantics and Point-in-Time Evidence Architecture](docs/IDEAL_DATA_TRUST_TEMPORAL_AND_POINT_IN_TIME_ARCHITECTURE.md). W3C PROV, Apache Iceberg and MLflow are conceptual/candidate references only; no data technology or schema is selected.


## Domain risk and capital semantics — checkpoint 074

Risk policy is domain-specific. The shared platform provides common governance, provenance, authority and audit contracts, but derivatives, future investments, commodities, hedges, personal cash flow and tax estimation retain separate risk meanings and decision authorities.

Portfolio/capital aggregation is read-only by default and preserves gross exposure, net exposure, factor risk, liquidity, counterparty/custody, margin/collateral, economic net worth, cash-flow capacity and tax exposure separately. It cannot infer netting, collateral transferability, hedge credit or permission to reallocate capital. D-006/D-008 remain initial crypto-perpetual policy only; D-018 prevents tax reserve estimates from restricting capital.

See [IDEAL Domain Risk and Capital Architecture](docs/IDEAL_DOMAIN_RISK_AND_CAPITAL_ARCHITECTURE.md).


## Reconciliation and verified recovery — checkpoint 076

Reconciliation is domain-owned, evidence-based and explicit; no universal last-write-wins source of truth exists. External venue state, bank observations, IDEAL ledgers, IRD assessments, raw market evidence, policy trust and operational health have distinct authorities. Mismatches remain visible and corrections are linked revisions.

Restored data and services remain quarantined until integrity, identity/revocation, audit continuity, external-state reconciliation, derived-state recomputation and scoped pillar attestations pass. A restart or reconnect does not prove recovery. See [IDEAL Reconciliation, Incident Containment and Verified Recovery Architecture](docs/IDEAL_RECONCILIATION_AND_VERIFIED_RECOVERY_ARCHITECTURE.md).


## Cross-domain accounting and valuation fixtures — checkpoint 078

Synthetic worked examples now test bank-to-exchange transfers, spot-plus-perpetual exposure, funding/fees versus unrealised P&L, collateral encumbrance, pending-to-posted bank transactions, tax estimates versus owner-designated reserves/assessments/payments, stale FX and late corrections. They enforce no double-counting, no notional-as-asset, no transfer-as-income and no tax-reserve capital lock.

See [IDEAL Cross-Domain Accounting and Valuation Worked Examples](docs/IDEAL_CROSS_DOMAIN_ACCOUNTING_AND_VALUATION_EXAMPLES.md). These are illustrative design fixtures, not accounting/tax advice or executed tests.
