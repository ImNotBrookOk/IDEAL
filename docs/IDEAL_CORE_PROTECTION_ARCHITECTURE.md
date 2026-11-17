# IDEAL Core Protection Architecture

**Status:** Phase 02 architecture baseline — design and research only  
**Recorded:** 17 November 2026  
**Authority:** Owner-approved architectural direction, recorded as D-020  
**Implementation status:** Not authorised. Phase 02 remains active; Phases 03–19 remain locked.

## 1. Purpose and system vision

IDEAL is one integrated personal financial intelligence system composed of specialised, separately bounded domains and engines. It is not a collection of independent trading bots. Its components may have distinct responsibilities, data stores and interfaces, but they must operate within shared protection, evidence and accountability rules.

The system's foundational objective is to make every consequential decision evidence-based, risk-bounded, observable, reproducible and recoverable. The integrity of the whole system takes precedence over the performance or autonomy of any individual engine.

The four foundational pillars are:

1. **Risk management — the protection and permission layer.** It evaluates capital exposure and constrains what the system may do.
2. **Data integrity — the evidence layer.** It establishes whether the information used by the system is authentic, complete, timely, correctly interpreted and traceable.
3. **System health — the oversight layer.** It independently observes whether the system, its components and dependencies are functioning within declared contracts.
4. **Security — the trust and defence layer.** It protects identities, permissions, data, code, infrastructure, integrations and audit evidence against unauthorised access, leakage, tampering and abuse.

These pillars reinforce one another. None is sufficient alone. Risk decisions depend on trustworthy data; data pipelines depend on observable and recoverable infrastructure; system health must detect when data, risk or security controls cannot be trusted. Security is designed into every layer and its telemetry is monitored by system health, but operational health is not proof of security. See [IDEAL Security Architecture and Assurance](IDEAL_SECURITY_ARCHITECTURE.md).

## 2. Architectural invariants

The following are cross-domain requirements, not optional features:

- No consequential engine may bypass the shared risk, data-trust or health requirements applicable to its activity.
- No decision-critical calculation may silently consume stale, missing, malformed, incomplete, contradictory or untraceable inputs.
- Unknown is a valid state. When evidence is insufficient, the system must preserve uncertainty rather than fabricate confidence.
- Critical controls fail closed. A failed dependency must restrict only the activities that depend on it, unless the failure is genuinely system-wide.
- No component may be the sole authority for certifying its own correctness or health.
- Strategy and AI components may analyse and propose; deterministic controls retain authority over risk limits, permissions and consequential state transitions.
- Risk limits and control policies cannot be changed by a strategy, model, agent or ordinary runtime output.
- Every consequential decision and control transition must be reproducible from versioned inputs, rules, code and recorded evidence to the extent the source rights permit.
- Historical evidence is preserved as an asset. Corrections and reinterpretations are recorded as new versions/events, not silent destructive overwrites.
- Failure, degradation, override, recovery and restoration must be visible and auditable.
- Domain boundaries must prevent a fault or permission in one financial domain from silently propagating into another.
- User authority remains explicit. Recommendations and warnings do not create unauthorised financial actions, mandatory tax withholding, payment initiation or capital restrictions.

## 3. The shared protection model

### 3.1 Risk management

Risk management is a first-class system capability and a mandatory independent decision gate for any activity that can create, increase or materially alter financial exposure.

Its future design must cover, as applicable to each authorised domain:

- trade and position sizing;
- leverage, margin, collateral, liquidation distance and settlement-currency risk;
- instrument, venue, strategy, counterparty and operational exposure;
- correlated positions, concentration, portfolio drawdown and aggregate risk;
- fees, spread, funding, slippage, liquidity and execution uncertainty;
- daily and rolling loss limits, warnings, cooldowns and recovery conditions;
- portfolio-level exposure across domains when those domains are separately authorised;
- capital allocation and user-approved permissions;
- pre-action validation, ongoing exposure monitoring and post-event reconciliation.

Risk is not merely a calculator attached to the trading engine. It is a shared policy and control capability with domain-specific adapters and explicit authority boundaries. Individual engines may calculate specialist metrics, but they cannot weaken or bypass central policies. Risk decisions must include the policy/version, input evidence, result, reason codes, validity period and any restrictions.

The architecture must distinguish:
- **hard invariants** that cannot be overridden by strategy or AI;
- **owner-approved policy parameters** that can change only through explicit change control;
- **contextual risk assessments** that may vary by instrument, strategy, regime or domain;
- **operational interlocks** triggered when required data, risk services or system-health dependencies are unavailable.

No numerical limits beyond already accepted decisions are introduced by this document. Existing risk parameters remain subject to their recorded scope and approval boundaries.

### 3.2 Data integrity

Every engine must consume data through explicit contracts. A value is not trustworthy merely because it exists or is the latest value received.

The data-trust plane must establish source identity, permitted use, instrument/entity identity, timestamps, sequence/continuity, schema, completeness, freshness, quality state, lineage, correction history and reconciliation status. It must retain separate source/event time and local receive/ingest/process time.

The information lifecycle has distinct layers:
1. **Original evidence:** source payloads or the most faithful legally permitted representation.
2. **Canonical observations:** validated, normalised, versioned records.
3. **Derived intelligence:** calculations, features, indicators, labels, valuations and aggregates with code/version lineage.
4. **Research artefacts:** point-in-time datasets, experiments, model artefacts, backtests and evaluation outputs.
5. **Decision evidence:** the exact data, quality states, rules, versions and outcomes supporting a consequential decision.

Derived data never replaces original evidence. Corrections, late arrivals, cancellations and reinterpretations are appended or versioned. Retention is tiered by value, cost, volume, privacy and licence; preservation does not override legal deletion or provider-use restrictions.

### 3.3 System health and independent oversight

A deterministic supervisor must observe the system from outside the components it monitors wherever practical. It must not accept a component's own green status as sufficient evidence.

It should monitor source health, data freshness and gaps, event backlogs, clock drift, process and worker liveness, scheduler status, storage and journal integrity, reconciliation, dependency/configuration drift, backup age and restore evidence, alert delivery and audit continuity.

Health must be explicit at source, component, domain and whole-system levels. At minimum, distinguish HEALTHY, DEGRADED, STALE, UNAVAILABLE and UNKNOWN. A green global state is valid only when all critical dependencies satisfy their declared contracts.

The supervisor may trigger predefined restrictive interlocks for affected consumers, but it must not invent or alter financial risk limits, approve trades, move funds or silently change permissions. Its own failure must be detectable through an independent watchdog or external heartbeat appropriate to the eventual deployment.

### 3.4 Security

Security is a distinct foundational pillar and a cross-cutting constraint on every component. It protects confidentiality, integrity, availability, authenticity and accountability through threat modelling, least privilege, strong authentication, scoped authorisation, secrets/key management, encryption, secure development and supply-chain controls, network/application/host hardening, privacy controls, tamper-evident audit and incident response. AI/agent permissions are enforced outside the model; prompts and outputs are untrusted. Security monitoring is integrated into system health, while security assurance remains a separate assessment with scope, evidence and freshness. A healthy process may still be compromised. No scan or architecture can guarantee that every vulnerability will be discovered.

## 4. How the pillars reinforce one another

The control relationship is cyclical rather than a one-way pipeline:

1. Data integrity establishes the evidence and its quality state.
2. System health observes ingestion, validation, storage, processing and downstream consumption.
3. Intelligence and specialist engines derive context from evidence that satisfies their contracts.
4. A strategy or domain engine proposes an action with its evidence and expected consequences.
5. Risk management independently evaluates the proposed action against current exposure, limits, policy and uncertainty.
6. A health/interlock check confirms that required dependencies remain valid at the point of action.
7. An authorised adapter may carry out only the permitted action and records the result.
8. Reconciliation compares intended, observed and resulting state.
9. Audit and learning stores preserve the evidence, decision, execution outcome and subsequent corrections.
10. Health and risk monitoring continue after the action and can restrict further activity if conditions deteriorate.

Feedback works in every direction. A data-quality failure changes the health state; the health state changes the validity of dependent risk calculations; risk can restrict an engine; reconciliation can reveal data or execution defects; and incident evidence feeds engineering research and corrective action.

## 5. Dependency, permission and failure boundaries

Every engine must declare:
- required data contracts and acceptable quality/freshness states;
- required risk services and policies;
- required health dependencies;
- actions it may propose, calculate, approve or perform;
- state it owns and state it only observes;
- failure modes, timeout behaviour and recovery prerequisites;
- audit events and reconciliation evidence it must emit.

A dependency graph must identify criticality, blast radius and safe degraded modes. Failure of a market feed may stop strategies that depend on it without unnecessarily disabling unrelated personal-finance viewing. Failure of a portfolio-wide risk service may restrict all activities that require that service. No broad freeze should be applied without a declared dependency or safety reason.

No fallback source is interchangeable merely because it provides a value. Equivalence must be established for semantics, timing, precision, coverage, entitlement and quality. Recovery requires backfill or explicit gap disposition, replay where applicable, reconciliation and verified state continuity; reconnect alone is not recovery.

## 6. Authority model

The architecture must explicitly distinguish these authorities:

| Capability | Permitted responsibility | Prohibited authority |
|---|---|---|
| Data adapters | Acquire and report source observations | Declare unverified data trustworthy |
| Data validation | Apply deterministic contracts and quality states | Fabricate missing evidence |
| Intelligence/strategy engines | Analyse, research and propose | Override risk, health or permissions |
| Risk framework | Evaluate exposure and enforce approved policy | Rewrite source evidence or user-owned financial records |
| Health supervisor | Detect incidents and trigger predefined interlocks | Change financial policy or initiate financial actions |
| Execution/account adapters | Perform explicitly authorised operations and report outcomes | Expand their own permissions |
| AI agents/models | Bounded analysis, explanation and research assistance | Solely validate data, approve risk, alter limits or self-deploy |
| User | Approve scope, policy changes and consequential permissions | Be silently overridden by software |

This is a design contract, not an implementation grant. The exact interfaces, threat model and enforcement mechanisms remain Phase 02 work.

## 7. Cross-domain application

The active initial trading scope remains crypto perpetual futures only (D-001). The shared protection architecture is designed to support future domains without authorising them.

Potential future domains include long-term crypto spot investing, equities, commodity exposure, cross-asset hedging, personal finance and tax intelligence. Each must retain its own accounting, source semantics, permissions and domain-specific risk rules. A future portfolio-level view may aggregate exposures for risk analysis, but it must not imply pooled collateral, shared cash, shared permissions or automatic transfers.

User autonomy remains a system invariant. For example, tax estimates and optional reserves are informational; they do not lock funds, force payments or automatically restrict otherwise permitted access (D-018).

## 8. Assurance and evidence requirements

The design must eventually support:
- deterministic unit, contract, integration, regression and property-based tests;
- fault injection for stale, missing, duplicate, out-of-order, malformed, contradictory and corrected data;
- risk-boundary tests, including limit edges, concurrent proposals, correlated exposures and unavailable controls;
- supervisor independence and supervisor-failure tests;
- replay/recovery and reconciliation tests;
- security, permission, secret-handling and dependency-boundary reviews;
- backup restoration and audit-integrity verification;
- reproducible evidence bundles linking requirements, design, code, test results and approvals.

Tests must prove not only normal operation but also that unsafe actions are rejected and that failures remain contained. No component is considered reliable solely because its happy-path tests pass.

## 9. Phase 02 design work still required

Before any runtime implementation, research and specify:

1. Risk policy hierarchy, authority boundaries, domain adapters and portfolio aggregation semantics.
2. Canonical data/source/observation/lineage and quality-state contracts.
3. Health-state model, independent supervisor/watchdog and failure-domain topology.
4. Dependency graph, criticality classification, blast radius and degraded-mode matrix.
5. Pre-action and ongoing interlock contracts between data, health, risk and action adapters.
6. Event, decision, incident, reconciliation and audit schemas.
7. Recovery, replay, backup and restore contracts.
8. Security, privacy, retention, licence and access-control boundaries.
9. Quantitative acceptance criteria, health objectives and risk-control verification metrics.
10. Portable deployment topology and operational runbooks.
11. Threat modelling and independent design review.
12. A traceability matrix connecting each requirement to design, tests and approval evidence.

The architecture should be challenged for simplicity and failure modes before contracts are frozen. Do not create extra services or abstractions without a demonstrated isolation, reliability, security or maintainability benefit. A modular monolith remains the current provisional direction.

## 10. Explicit non-authorisations

This document does not authorise:
- implementation, runtime integration or dependency changes;
- exchange selection, exchange/account connectivity or credentials;
- paper or live execution;
- changes to accepted risk parameters;
- spot, equities, commodities, hedging or other future-domain implementation;
- bank, broker or IRD connections;
- payments, transfers, tax filing or financial write operations;
- paid infrastructure, hosting, subscriptions, hardware purchases or billing;
- model downloads, training jobs, online learning or autonomous model/strategy promotion.

Security is a fourth foundational pillar under D-021. Its detailed architecture and assurance lifecycle are documented in `docs/IDEAL_SECURITY_ARCHITECTURE.md`.

Phase 02 remains active. Phases 03–19 remain LOCKED until the relevant exit criteria and explicit owner approvals are satisfied.

## 11. Architecture-first integration and acceptance

The four pillars must be designed as one integrated protection system before implementation. Each pillar has distinct responsibilities and authority, while critical interfaces are explicit contracts rather than informal assumptions.

For every cross-pillar or domain interface, document producer/consumer and ownership; schema, units, identity and version; timestamps and ordering; authentication and authorisation; provenance, integrity, quality and freshness; unknown/invalid states; timeout, retry, duplicate and partial-result semantics; safe response to dependency failure; blast radius and escalation; audit evidence; and recovery verification.

The architecture must be challenged as a whole through threat modelling, abuse cases, failure-mode analysis, dependency/blast-radius review, edge cases and independent design review. Requirements must trace to an owning component or policy, an interface, a verification method and an expected failure response. Unresolved questions and residual risks remain explicit.

The architecture-first process, implementation-candidate due-diligence standard and acceptance gate are specified in [IDEAL Architecture-First Research and Design Plan](IDEAL_ARCHITECTURE_FIRST_RESEARCH_PLAN.md). The first detailed research task is the risk-management architecture, with data integrity, system health and security integrated from the beginning. Implementation ecosystem research follows architecture acceptance; code availability must not dictate the protection model.

This section records design requirements only. It does not authorise runtime implementation, dependency adoption, deployment, external testing or phase advancement.


The working requirements-to-controls-to-components-to-tests matrix across governance, risk, data integrity, system health, security, audit and cross-pillar interfaces is maintained in [IDEAL Integrated Foundation Traceability Matrix](IDEAL_FOUNDATION_TRACEABILITY_MATRIX.md). It is a Phase 02 working design, not an implementation authorisation or frozen contract.
The integrated cross-pillar adversarial review, including STRIDE-style threat coverage, authority conflicts, common-mode failure and recovery gaps, is maintained in [IDEAL Integrated Adversarial Architecture Review](IDEAL_INTEGRATED_ADVERSARIAL_REVIEW.md). It remains a Phase 02 review draft; independent review and owner acceptance are pending.


## 8. Bounded owner-authorised autonomy

D-023 establishes bounded autonomy as the intended future operating model for any execution-capable IDEAL domain. Owner approval grants a versioned, revocable operating envelope, not unrestricted authority.

Inside that envelope, a future engine may act without per-action human approval only when exact-action security authorisation, trusted/reconciled data, required health interlocks, deterministic risk approval and reservation, and durable audit requirements all pass. Risk may further restrict the envelope but cannot expand it. Data, health and security foundations provide independent prerequisites; none may substitute for risk approval or owner policy.

The owner retains approval authority over capability activation, envelope/policy/permission changes, new account/venue/integration scope, credentials and privilege expansion, fund transfers/withdrawals/payments, safeguard disablement and designated irreversible or incident-recovery actions. Agents and strategies cannot modify the envelope, approve exceptions or self-grant authority.

Unknown, stale, revoked, expired, compromised or out-of-envelope state denies the affected risk-increasing action. Emergency restrictions can reduce authority; they cannot create financial authority or autonomously initiate liquidation.

This is a governance and architecture direction only. No execution capability, account, venue, credential, paper/live trading or implementation is authorised. See [Security Architecture §9](IDEAL_SECURITY_ARCHITECTURE.md#9-bounded-owner-authorised-autonomy-d-023) and [Decision D-023](../DECISIONS.md).


## Autonomy authority as a cross-foundation control

D-023's bounded autonomy model requires a separate owner-authority/security gate and deterministic risk gate. The action-enforcement boundary consumes trusted data evidence, independent health/security interlocks and durable audit preconditions before admitting an exact action. Risk approval reserves capacity; security/owner permission establishes authority; neither can replace the other. Emergency interlocks may restrict capability but cannot create financial authority or initiate liquidation. Full provisional design: [Autonomy Authority and Permission Architecture](IDEAL_AUTONOMY_AUTHORITY_AND_PERMISSION_ARCHITECTURE.md).


## Adversarial enforcement and recovery requirements — checkpoint 068

The four foundations must jointly support three hard requirements: (1) revocation/dispatch ordering is serialised and reports already in-flight external requests honestly; (2) untrusted AI/strategy workloads cannot reach gateway credentials, host control planes or venue egress; (3) recovery cannot resurrect revoked authority from an old backup. A compromised host root/kernel is a trust-boundary failure, not a condition that local process health can certify away. Independent host/gateway trust separation and an external/current revocation anchor are required where the threat model demands protection from host compromise. See autonomy architecture §§19–21.


## Supervisor, audit and policy-root contracts — checkpoint 069

- Health supervisor is a read-only observer with one-way restrictive interlock authority; it cannot grant authority or initiate financial side effects.
- Authority, risk reservation, audit event and outbox are durably committed before dispatch; dispatch-start is atomically recorded before external network write.
- Policy publication and activation are immutable, owner-approved, signed, versioned and serialised with revocation/dispatch.
- A shared host root/kernel compromise defeats local process-level independence; trust boundaries must state this limitation.
- Remote side effects are never claimed exactly-once; ambiguous outcomes remain UNKNOWN and require authoritative reconciliation.
