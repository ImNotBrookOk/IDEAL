# IDEAL Architecture-First Research and Design Plan

**Status:** Owner-confirmed Phase 02 planning direction — research and documentation only  
**Recorded:** 17 November 2026  
**Authority:** D-022  
**Scope:** Complete integrated architecture before implementation research is converted into adoption or build decisions  
**Implementation status:** Not authorised. Phase 02 remains active; Phases 03–19 remain locked.

## 1. Objective

IDEAL's first major development objective is to produce a complete, internally consistent, evidence-led architecture before writing or integrating runtime code. The project must not begin by collecting repositories and forcing them into an incomplete design. First establish what the system must do, why each component exists, who owns each responsibility, how components interact, what authority they possess, what can fail, and how failures are detected, contained and recovered.

Once the architecture has been defined and independently challenged, conduct a separate implementation-ecosystem research stage. Investigate existing code, libraries, frameworks, models, datasets and engineering approaches across GitHub, official documentation, Hugging Face, academic literature and other credible open-source sources. Reuse is preferred where a candidate demonstrably fits the architecture and passes due diligence; otherwise adapt, isolate, defer or build only the missing capability.

This plan establishes a process and acceptance criteria. It does not approve implementation, dependency adoption, runtime integration, external services, exchange connectivity, paper/live trading or phase advancement.

## 2. Architecture-first sequence

1. **System definition:** establish system purpose, active and deferred domains, responsibilities, bounded contexts, authority hierarchy, trust boundaries, external actors, assumptions and non-goals.
2. **Four foundation designs:** research and specify risk management, data integrity, system health and security in depth. Each receives explicit responsibilities, inputs/outputs, dependencies, states, policies, failure modes, recovery behaviour and verification criteria.
3. **Cross-pillar integration:** define contracts and control flows between foundations and all future engines. Specify ownership, permissions, data semantics, validity/freshness, failure propagation, safe states, escalation, audit evidence and recovery.
4. **System-wide architecture:** map domain boundaries, services/modules, storage, event/data flows, identity boundaries, trust zones, deployment-neutral interfaces and operational responsibilities. Do not select technology merely to fill a diagram.
5. **Adversarial and failure review:** threat-model the design; conduct failure-mode analysis, abuse-case review, dependency/blast-radius analysis, recovery exercises on paper, edge-case review and independent architecture challenge.
6. **Architecture acceptance:** trace requirements to components, contracts, owners and verification methods. Record unresolved questions and residual risks. Obtain explicit owner approval of the architecture baseline before moving to implementation research as an adoption/build plan.
7. **Implementation-ecosystem research:** research candidate repositories, libraries, services, models and datasets against the approved architecture. No candidate is adopted by default.
8. **Implementation blueprint:** map each approved architectural capability to a recommended implementation, alternatives, licence, maintenance evidence, security posture, dependencies, costs, limitations, adaptation needs and test strategy. Identify what to reuse, adapt, isolate, defer or build.
9. **Independent implementation-plan review and approval:** verify that the proposed technology stack still satisfies the architecture, budget and safety requirements. Obtain separate explicit approval before implementation or runtime changes.

The order is intentional: architecture determines what code is needed; available code must not dictate the system's safety model.

## 3. Four foundational pillars

The four pillars are distinct but mutually reinforcing. No pillar may certify itself as sufficient, and no component may silently assume another pillar is healthy.

### 3.1 Risk management

Design the capital-protection and permission layer, including capital/equity semantics; position and portfolio exposure; leverage, margin, collateral and settlement currencies; liquidation mechanics and buffers; volatility, correlation and concentration; liquidity, spread, market impact, slippage, fees and funding; drawdown and loss boundaries; venue/counterparty risk; strategy/model risk; operational risk; authority hierarchy; pre-action validation; ongoing monitoring; kill switches; fail-closed behaviour; and recovery/reconciliation.

Architectural principle to formalise and verify: strategy components propose; the risk authority evaluates and authorises or rejects actions within owner-approved policy. Strategy or AI components cannot alter risk limits, grant themselves permissions, disable safeguards or bypass deterministic checks. Risk controls themselves require security protection and independent health/assurance.

### 3.2 Data integrity

Design source identity and permitted-use records; acquisition and ingestion contracts; event/source time versus receive/ingest/process time; schema and instrument identity; sequence/continuity; completeness and freshness; validation and quality states; raw-evidence preservation where lawful/licensed; canonical observations; correction/cancellation/replacement history; reconciliation; lineage; derived features and labels; point-in-time datasets; reproducible research artefacts; retention tiers; privacy/deletion constraints; backup and restoration; and evidence hashes/versioning.

Unknown, missing, stale, contradictory or invalid data must remain explicit. Consumers must not silently substitute fabricated confidence or use data outside its rights/retention conditions.

### 3.3 System health

Design independent supervision of processes, workers, schedulers, data sources and pipelines, storage, journals, queues, dependencies, clocks, reconciliation, backups, audit continuity and security-control operation. Define health states, thresholds, evidence freshness, alerting, dependency-aware degradation, bounded containment, watchdog independence, false-positive handling, incident lifecycle, runbooks and recovery verification.

A component's self-reported status is not sufficient evidence. Availability is not correctness, and a green operational status is not proof of security.

### 3.4 Security

Design threat models and trust boundaries; identity, authentication and authorisation; least privilege and deny-by-default; secrets and cryptographic key lifecycle; encryption and data classification; privacy and retention; network/application/host hardening; secure development and CI/CD; dependency and software supply-chain provenance; AI prompt-injection and tool isolation; audit protection; vulnerability discovery and remediation; incident response; credential revocation; evidence preservation; and verified recovery.

Security telemetry and control status integrate with health monitoring, but security assurance remains separately reported with scope, evidence and freshness. No scanner or test suite can guarantee discovery of every vulnerability. Testing must be authorised and scoped; this plan does not authorise external scans or penetration testing.

## 4. Cross-pillar integration contracts

Every interface between pillars, domains and engines must document:

- producer, consumer, ownership and authoritative source;
- purpose, schema, units, precision, identity and versioning;
- timestamps, ordering, idempotency and correction semantics;
- authentication, authorisation and least-privilege scope;
- provenance, integrity checks, quality state and freshness requirements;
- required/optional fields and explicit unknown/invalid states;
- timeout, retry, duplicate, partial-result and contradictory-input behaviour;
- safe response when the producer or consumer is unavailable;
- failure classification, blast radius, escalation and recovery;
- audit events, evidence retention and traceability;
- compatibility and migration policy;
- deterministic acceptance and negative tests.

Integration must be tested as a system, not inferred from individually healthy modules. Shared contracts must not create shared authority that allows one engine to approve its own consequential actions.

## 5. Research methodology and source hierarchy

Architecture research and implementation research are separate workstreams.

For architecture research, prioritise authoritative standards, official technical documentation, established engineering literature, peer-reviewed research and primary source code. Use credible case studies and community experience as supplementary evidence, not sole proof.

For implementation research, search GitHub, official project documentation, package registries, Hugging Face and academic sources where relevant. Verify candidate facts against the underlying repository, release, licence and documentation rather than relying on snippets, popularity or stale summaries.

Every candidate assessment must record:

| Dimension | Required evidence |
|---|---|
| Identity and provenance | Canonical repository/model, maintainer and release source |
| Licence and rights | Exact licence/version, model and dataset terms, transitive obligations and intended-use compatibility |
| Maintenance | Last meaningful commit/release, release cadence, maintainer activity, archived status and open issues |
| Engineering quality | Architecture, tests, CI, documentation, reproducibility and known limitations |
| Security | Permissions, attack surface, advisories/CVEs, dependency posture, build provenance and security response |
| Compatibility | Fit with IDEAL contracts, languages, platforms, portability and integration complexity |
| Dependencies | Direct/transitive dependency tree, licence compatibility and supply-chain risk |
| Cost and operations | Compute, storage, bandwidth, quotas, hosting, support, lock-in and migration cost |
| Evidence and suitability | What has actually been verified, what remains unknown, and reuse/adapt/isolate/defer/reject recommendation |

No candidate is approved by popularity, star count, benchmark headline or model-card claim alone. Record evaluation date and source links because maintenance, licences, vulnerabilities and capabilities change.

Prefer mature, narrowly scoped, well-maintained components with compatible licences and small attack surfaces. Prefer deterministic, testable software for accounting, risk calculations, validation, reconciliation, permissions and safety enforcement. AI may assist bounded research and analysis but is not the security boundary, policy authority or sole validator of its own work.

## 6. Architecture completion and acceptance criteria

Phase 02 architecture work is not complete merely because documents exist. The following evidence must be present and reviewed:

- complete system/domain map with active, deferred and excluded scope clearly distinguished;
- four detailed foundation architectures with responsibilities, authority, dependencies, states and failure behaviour;
- integration/interface contracts for all critical cross-pillar and domain boundaries;
- authority and permission hierarchy, including human approval points and prohibited self-authorisation;
- data-flow, trust-boundary, dependency and failure-propagation diagrams;
- threat model, security-control matrix and vulnerability/incident lifecycle;
- failure-mode analysis, safe-state definitions, containment and recovery procedures;
- requirements-to-component-to-test traceability matrix;
- documented assumptions, unresolved questions, residual risks and rejected alternatives;
- independent architecture review with findings resolved or explicitly accepted by the owner;
- test and verification strategy, including negative, fault-injection, replay, reconciliation and recovery cases where applicable;
- explicit owner acceptance of the architecture baseline.

Each material requirement must map to an owner/component, an interface or policy, a verification method, and an expected response when the requirement cannot be met. Unresolved items remain visible and cannot be described as completed.

## 7. Implementation blueprint acceptance criteria

After architecture acceptance, the implementation research register must map each architectural requirement to candidate technologies and record evidence, alternatives, licence, maintenance, security, dependencies, cost, portability, adaptation effort, operational risks and proposed tests. The blueprint must identify gaps where no suitable open-source component exists and explain whether to build a small purpose-specific component or defer the capability.

A proposed stack must be reviewed as a whole for dependency concentration, shared failure modes, upgrade strategy, data migration, backup/restore, security boundaries, offline operation, portability and total cost. A collection of individually attractive projects is not an acceptable architecture.

## 8. Governance and unchanged boundaries

- Active market scope remains crypto perpetual futures only (D-001).
- Phase 01 remains closed.
- Phase 02 remains active and is limited to architecture, contracts and research.
- Phases 03–19 remain locked.
- No runtime implementation, test/runtime integration, dependency adoption or deployment is authorised by this plan.
- No live trading, paper execution, exchange credentials/accounts, venue selection/connectivity or external financial action is authorised.
- No paid infrastructure, hosting, security product, external scan or penetration test is authorised.
- No bank connection, financial account integration, payment initiation or handling of real financial records is authorised.
- Future spot, equities, commodities, personal-finance and tax capabilities remain separately scoped/deferred and do not expand D-001.
- Meaningful findings, decisions, assumptions and audit evidence must be recorded in GitHub and fetched back for verification. Never claim an update or test succeeded without evidence.
- Any phase transition, implementation, external access or adoption requires its own explicit approval.

## 9. Research cadence

A weekly IDEAL research review has been scheduled for Mondays at approximately 10:00 New Zealand time. It is intended to identify material architecture, security, standards and open-source developments; assess implications; track unresolved evidence gaps; and recommend the next research steps. It does not grant authority to change project scope, adopt technology, modify code or advance phases.

## 10. Immediate next work

Begin the Phase 02 deep research sequence with the risk-management architecture, while explicitly designing its contracts with data integrity, system health and security. Continue through the other foundations and cross-pillar integration. Do not begin implementation or broad repository harvesting until the architecture work has reached its acceptance gate.


## 11. Checkpoint 077 — current progress and next architecture work

The initial risk architecture, bounded autonomy authority, integrated system/domain map, temporal evidence model, domain risk/capital model and reconciliation/recovery model have all been developed at provisional design level. An internal integrated consistency/adversarial review is recorded in [IDEAL Phase 02 Integrated Architecture Review](IDEAL_PHASE_02_INTEGRATED_ARCHITECTURE_REVIEW.md).

The remaining Phase 02 sequence is:
1. Build worked end-to-end examples for cross-domain accounting, FX, transfers, collateral, spot-plus-derivative exposure, tax estimates and reconciled cash.
2. Complete a single integrated data classification, retention, deletion, audit and backup policy.
3. Define provider/venue source-specific freshness, clock and point-in-time fidelity requirements without selecting integrations.
4. Complete host trust topology, recovery root, watchdog and failure-domain decision analysis against realistic low-cost host options.
5. Reconcile every state machine and exact contract across authority, risk, data, health, security, reconciliation and recovery.
6. Perform independent architecture reviews (security/operations, simplicity/pattern fit, maintainability/testability) and disposition every finding.
7. Consolidate owner decisions into one review pack. Do not interrupt the owner with interim questions.
8. Obtain explicit owner acceptance of the full Phase 02 architecture before Phase 03 can be considered.

The sequence remains research/design/documentation only. No runtime, implementation, dependency, account, credential, paper/live execution, paid service or phase transition is authorised.


## 12. Architecture diagram coverage — checkpoint 082

[IDEAL System Architecture Diagrams](IDEAL_SYSTEM_ARCHITECTURE_DIAGRAMS.md) now provides logical domain/evidence flow, trust zones and forbidden flows, action admission/dispatch, incident/recovery lifecycle and temporal evidence lineage. These satisfy the logical diagram deliverable at design level; physical deployment, network, storage and process diagrams remain deferred until topology and technology selection evidence exists.


## 13. Security control-to-threat matrix — checkpoint 083

[IDEAL Security Control and Threat Traceability Matrix](IDEAL_SECURITY_CONTROL_AND_THREAT_TRACEABILITY_MATRIX.md) now maps the security architecture's control families to protected assets, threat paths, owners, enforcement points, evidence status and future tests. It explicitly marks all future controls as design-level and preserves residual host-root, external-side-effect, single-owner and third-party risks.

Independent security/operations review and runtime assurance remain future acceptance gates; no external scan or implementation is authorised.


## 14. Complexity and maintainability gate — checkpoint 084

The [Architecture Complexity and Maintainability Review](IDEAL_ARCHITECTURE_COMPLEXITY_AND_MAINTAINABILITY_REVIEW.md) establishes a provisional simplicity constraint: logical bounded contexts and independent authorities must not automatically become separate microservices, databases, agents or infrastructure. The smallest viable future direction is a modular monolith, one authoritative transactional store if durability is proven, deterministic services/scripts, immutable evidence manifests and a phone-first read/control UI.

A canonical document ownership map is proposed. Historical evidence remains intact; any document consolidation/deletion requires explicit owner approval. This is a design recommendation, not a selected implementation stack.


## 15. Requirement-to-component-to-test coverage — checkpoint 086

[IDEAL Requirement → Component → Control → Test Traceability](IDEAL_REQUIREMENT_COMPONENT_CONTROL_TEST_TRACEABILITY.md) now provides stable requirement aliases, component owners, controls/contracts and future verification IDs. Coverage includes active perpetual research, strategy validation, four foundations, autonomy, reconciliation/recovery, personal finance, tax, retention, privacy, host/UI and cost constraints.

This closes the traceability artefact at design level; tests are not implemented or executed. D-006/D-008, source-specific fidelity, host topology, retention periods and independent review remain open.


## 16. Canonical architecture document ownership — checkpoint 088

[IDEAL Phase 02 Architecture Document Map](IDEAL_PHASE_02_ARCHITECTURE_DOCUMENT_MAP.md) formalises the canonical source for each governance, system, foundation, authority, contract, recovery, privacy and assurance concern. It defines conflict precedence and records unresolved owner decisions as an inventory, not an approval request. The map preserves historical evidence and does not authorise consolidation/deletion or implementation.


## 16. Critical contract field schemas — checkpoint 089

[IDEAL Critical Contract Field Schemas](IDEAL_CRITICAL_CONTRACT_FIELD_SCHEMAS.md) now defines logical field-level semantics and constraints for all critical cross-pillar/domain contracts. This closes the technology-neutral schema deliverable at design level. Serialization, database DDL, API and compatibility tooling remain deferred until platform selection.


## 17. Consolidated owner decision register — checkpoint 090

[IDEAL Phase 02 Owner Decision Register](IDEAL_PHASE_02_OWNER_DECISION_REGISTER.md) consolidates deferred decisions with evidence, recommended defaults, dependencies and readiness status. It is a draft and must not be presented for approval until the full architecture, independent review findings and final traceability pass are complete.


## 17. Final integrated challenge — checkpoint 089

The [Final Integrated Architecture Challenge](IDEAL_PHASE_02_FINAL_INTEGRATED_ARCHITECTURE_CHALLENGE.md) identified and corrected the missing canonical crypto asset-denomination semantics in the shared contract catalogue. It records cross-pillar consistency findings and residual blockers. The next required gate is independent read-only review across architecture simplicity, security/operations and maintainability/testability; no owner decision pack is final until those reviews are reconciled.


## 18. Official source reference revalidation — checkpoint 090

Primary New Zealand privacy/tax and core security/host-hardening references have been rechecked and summarised in [Official Source Reference Revalidation](IDEAL_PHASE_02_SOURCE_REFERENCE_REVALIDATION.md). Before implementation research is converted into a proposed stack, all relevant source versions, provider terms, licence conditions and legal interpretations must be revalidated against the chosen deployment and use case.
