# IDEAL Phase 02 — Three-Lens Review and Assurance Limits

**Checkpoint:** 105 — 18 November 2026  
**Status:** Internal read-only review; NOT independent assurance  
**Scope:** Current Phase 02 architecture baseline on GitHub main  
**Authority boundary:** No implementation, runtime, dependency, credential, host, venue, account, financial action or phase advancement.

## 1. Review method and independence statement

The current architecture baseline was examined through three separately bounded review lenses:

1. Architecture simplicity, boundaries and maintainability.
2. Security, operations, revocation and recovery.
3. Contract testability, traceability and evidence.

These are three passes by the same IDEAL documentation workstream. They are not independent reviewers, a penetration test, formal verification, legal/accounting advice or external assurance. No separate human reviewer or independent reviewer service is available within this workstream. This limitation is recorded rather than concealed. The owner may commission an external review or explicitly consider the residual risk; this report does not waive the review requirement.

Evidence inspected includes ROADMAP current state, owner decision register, completion-readiness assessment, integrated architecture, final integrated challenge, security architecture, requirement/component/control/test traceability, architecture complexity review, critical contract schemas, state-machine architecture, autonomy authority, recovery, data trust and margin/collateral/liquidation architecture.

## 2. Lens A — architecture simplicity and maintainability

### Positive evidence

- Logical bounded contexts and separate authority ownership are not automatically mapped to separate services.
- The complexity review recommends a modular monolith, one authoritative transactional store, deterministic domain services and a narrow action boundary as a provisional smallest viable shape.
- Broker, service mesh, Kubernetes, distributed consensus, lakehouse and multi-agent orchestration are not default requirements.
- Future domains remain logical/deferred; current active scope remains crypto perpetual research.
- Canonical document ownership is defined and historical audit records are retained.

### Findings

| ID | Severity | Finding | Required disposition |
|---|---|---|---|
| ARC-105-01 | Medium | The modular-monolith direction is a provisional recommendation, while the final runtime, transactional store and physical trust boundaries remain unselected. Readers could mistake a preferred shape for an approved implementation architecture. | Keep every diagram and summary labelled logical/provisional until ODR-09/10/11 and implementation approval. No stack inference. |
| ARC-105-02 | Medium | Several canonical documents repeat phase status and authority boundaries. The document map helps, but repeated statements can drift as checkpoints accumulate. | Treat ROADMAP current-state and DECISIONS as status/authority precedence; summaries link to canonical sources. Add date/checkpoint and supersession markers when updating. |
| ARC-105-03 | Medium | The logical separation of security incident control, health supervision, authority, risk and action is sound, but physical deployment separation is unresolved. | Preserve logical separation now; require threat-tier and host-root decision before deployment. Do not prematurely split into services. |
| ARC-105-04 | Low | The architecture pack is large enough that review navigation and canonical ownership are themselves operational risks. | Keep document map, short owner summary and traceability; do not delete history or perform bulk consolidation without owner approval. |

### Lens A disposition

No evidence justifies adding more services or infrastructure. Retain the provisional modular-monolith recommendation as a hypothesis, not an adopted stack. No architecture simplification may merge authority owners or weaken controls.

## 3. Lens B — security, operations, revocation and recovery

### Positive evidence

- Strategy/AI workloads are untrusted and have no direct credentials or unrestricted venue egress.
- Owner authority, policy, identity, health, security, risk, reservation, action, reconciliation and recovery have distinct responsibilities.
- Health is restrictive-only; security containment can revoke/contain but cannot grant financial authority.
- Revocation and dispatch serialize against a monotonic generation; transmitted requests remain potentially in flight.
- Durable intent, reservation, audit and outbox precede dispatch; uncertain venue outcomes retain reservations pending authoritative reconciliation.
- Recovery quarantines restored state and does not resurrect revoked permissions.
- Host root/kernel compromise, local audit compromise, single-owner limitations and venue-side liquidation/ADL uncertainty are explicit residual risks.

### Findings

| ID | Severity | Finding | Required disposition |
|---|---|---|---|
| SEC-105-01 | High | Revocation effectiveness depends on a complete and current inventory of every dispatcher/worker capable of crossing the final dispatch boundary. The inventory and measurable propagation objective remain open. | ODR-11 must define worker registration, stale-worker handling, acknowledgement evidence, partition behaviour and a measurable objective before any execution-capable runtime. |
| SEC-105-02 | High | A local supervisor, authority store and action gateway may share a host or failure domain. Logical separation alone does not survive host-root/kernel compromise. | ODR-09/10/11 must explicitly accept a host-root threat tier and decide whether the action gateway/revocation anchor/watchdog require a separate physical trust domain. |
| SEC-105-03 | High | Recovery depends on current revocation truth and trustworthy key custody. Independent revocation anchor, owner root/recovery custody and device-loss ceremony remain undecided. | ODR-10/11 remain hard gates before owner-envelope activation; no backup-only recovery path. |
| SEC-105-04 | Medium | Audit integrity and external witnessing are correctly distinguished, but retention durations, legal holds, deletion propagation and witness outage policy are not numerically selected. | Preserve privacy and legal constraints; ODR-11 and data policy must resolve before runtime retention configuration. |
| SEC-105-05 | Medium | The security architecture is a requirements/design baseline, not evidence that IDEAL itself has passed penetration testing, dependency scanning, host inspection or incident drills. | State these as future verification gates; do not report security as tested or secure merely because controls are specified. |

### Lens B disposition

No security finding can be closed by documentation wording alone. The existing architecture is directionally conservative, but deployment topology, owner key custody, dispatcher inventory and revocation objectives are material open gates. No runtime or external security test was performed.

## 4. Lens C — contract testability and traceability

### Positive evidence

- Stable requirement aliases connect requirements to components, controls and future test IDs.
- Test catalogue distinguishes design specified, open and not implemented/tested.
- Critical contract schemas include typed logical fields and explicit unknown/partial states.
- Temporal architecture distinguishes event time, observation/availability time and correction history.
- Margin/collateral/liquidation additions are linked to reservation conservation and authoritative reconciliation.

### Findings

| ID | Severity | Finding | Required disposition |
|---|---|---|---|
| TST-105-01 | High | Canonical serialization, schema evolution/compatibility, decimal/asset encoding and error-code mapping remain unresolved. Without these, exact digests and cross-version replay cannot yet be implemented unambiguously. | Keep implementation blocked; define canonical encoding and version negotiation before Phase 03 contract implementation. |
| TST-105-02 | High | D-006 denominator and D-008 day-start/capital-flow/FX/valuation semantics remain open. They affect risk sizing and loss-control outputs, not just presentation. | Keep ODR-02/03 open; no sizing or loss-control runtime may infer defaults from illustrative examples. |
| TST-105-03 | Medium | Future test IDs are useful but no executable test suite, coverage report, mutation analysis or fault-injection evidence exists for the architecture contracts. | Phase 03 must translate every critical contract into deterministic positive, negative, replay, concurrency and crash-boundary tests before dependent work unlocks. |
| TST-105-04 | Medium | Source-specific freshness, correction availability and point-in-time guarantees vary by provider and cannot be established by generic contract fields alone. | Bind provider capability evidence and dated thresholds when a source is selected; missing guarantees remain explicit UNKNOWN/PARTIAL. |
| TST-105-05 | Medium | The traceability catalogue has to remain synchronized with the canonical requirements and schemas as new checkpoints add requirements. | Add a release-time traceability diff/check to future CI; do not claim the matrix is automatically enforced today. |

### Lens C disposition

The architecture is substantially traceable at design level, but the contract surface is not yet implementation-complete. ODR-02/03 and canonical serialization/version semantics are material blockers to the dependent future capabilities. Planned tests are not executed tests.

## 5. Consolidated finding register

| ID | Severity | Area | Status |
|---|---|---|---|
| ARC-105-01 | Medium | Provisional architecture direction | Open clarification |
| ARC-105-02 | Medium | Documentation ownership/drift | Controlled; ongoing |
| ARC-105-03 | Medium | Logical vs physical isolation | ODR-09/10/11 |
| ARC-105-04 | Low | Documentation scale/navigation | Controlled; ongoing |
| SEC-105-01 | High | Dispatcher inventory/revocation SLO | ODR-11 |
| SEC-105-02 | High | Host-root/failure-domain separation | ODR-09/10/11 |
| SEC-105-03 | High | Root/recovery custody and independent revocation | ODR-10/11 |
| SEC-105-04 | Medium | Audit retention/witness/deletion | ODR-11 + data policy |
| SEC-105-05 | Medium | No external security assurance | Explicit assurance limitation |
| TST-105-01 | High | Canonical serialization/schema evolution | Phase 03 contract gate |
| TST-105-02 | High | Risk denominator/daily loss semantics | ODR-02/03 |
| TST-105-03 | Medium | No executable contract/fault tests | Phase 03 verification gate |
| TST-105-04 | Medium | Provider-specific temporal guarantees | Source-selection gate |
| TST-105-05 | Medium | Traceability enforcement | Future CI gate |

No finding is marked independently verified. These are internal findings based on the documents inspected.

## 6. Phase 02 disposition

This review pass does not close Phase 02. It improves the evidence presented for the final decision pack and confirms that unresolved decisions remain explicit rather than silently selected.

The independent review prerequisite is **unavailable within this workstream**. The owner decision register permits this limitation to be explicitly recorded and presented with residual risks; it does not permit the workstream to claim independent assurance. The owner must decide whether to commission an independent reviewer or consider the documented residual risk as part of ODR-12.

Phase 02 remains ACTIVE. Phase 03–19 remain LOCKED. No implementation, runtime, credentials, venue/account access, financial action, external security test or paid service is authorised.
