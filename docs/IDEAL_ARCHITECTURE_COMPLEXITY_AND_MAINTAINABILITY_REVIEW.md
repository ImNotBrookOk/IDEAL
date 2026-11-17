# IDEAL Architecture Complexity and Maintainability Review

**Status:** Internal design review; recommendation only; no source documents deleted or rewritten  
**Checkpoint:** 084 — 17 November 2026  
**Scope:** Architecture complexity, component necessity, documentation ownership and smallest maintainable implementation direction  
**Method:** Big-Model Smell — complexity-to-outcome review  
**Boundary:** Review/documentation only. No code, runtime, dependency, hosting, deletion, document consolidation or phase advancement is authorised.

## 1. Required outcome

IDEAL must remain a secure, auditable, private, integrated financial-intelligence system that:
- begins with crypto-perpetual research only;
- can add separately approved personal-finance, tax, investment and other domains later;
- preserves four independent protective foundations;
- supports reproducible research, financial accounting and recovery;
- has no untrusted AI/strategy path to authority or external side effects;
- is affordable and operable by one owner;
- remains understandable and maintainable without a large operations team.

Non-negotiable constraints: no authority simplification, no privacy/security/recovery shortcuts, no false data confidence, no automatic capital restriction, no hidden domain activation and no phase advancement.

## 2. Complexity smells and evidence

| Smell | Evidence | Cost / risk | Disposition |
|---|---|---|---|
| Future domains designed in detail before activation | 17+ logical contexts include multiple proposed domains while only derivatives research is active | High cognitive/document burden; risks accidentally treating proposals as active scope | Keep logical contracts, but implement only active domain after approval |
| Many state machines may become many services | Owner, policy, identity, health, security, data, risk, reservation, action, reconciliation and recovery states | Distributed systems add network failure, consensus, deployment and operations cost | Keep distinct state ownership; do not make each state machine a microservice |
| Duplicate architecture summaries across many documents | README, ARCHITECTURE, ROADMAP, foundation docs and checkpoint audits repeat status/constraints | Drift and contradictions; RULES and COMPONENT_SELECTION_MATRIX required corrections | Establish canonical source map; summaries link rather than restate full policy |
| Very large research documents | Risk architecture ~160 KB; personal finance research ~96 KB; autonomy architecture ~87 KB | Harder review, more duplicated context, slower change control | Preserve evidence/history, but create concise canonical decision summaries and section indexes |
| One universal event-sourcing assumption | Audit, replay, reconciliation and local action transactions need durable evidence, but not every domain needs event sourcing | Excess write amplification, complex projections, migration and retention | Use append-only evidence where required; do not force full event sourcing on every context |
| Outbox applied everywhere | Outbox is essential at external side-effect boundary | Unnecessary complexity for internal read-only calculations | Reserve transactional outbox for consequential external side effects |
| Technology candidate proliferation | SQLite, multiple VMs, Firecracker, Cedar/OPA, SPIFFE/SPIRE, several AI frameworks, data lake candidates | Evaluation cost and lock-in without proven workload | No adoption until a measured requirement exists; choose one candidate per job |
| Premature distributed data lake | Iceberg/MLflow and long-term market archive discussed before storage/licence volume known | Cost, operations, privacy and retention complexity | Start with immutable files + manifest/index only if later justified; benchmark before lakehouse |
| Always-on AI/agent architecture | Local agent frameworks and multi-agent research are proposed | Larger attack surface and maintenance than deterministic tasks need | Prefer deterministic scripts and scheduled jobs; AI optional and isolated |
| Overbuilt hosting/security options | Android, WSL2, Hyper-V, KVM/Firecracker, cloud and two-host topologies all considered | Decision fatigue and premature deployment work | Keep comparison as research; current best choice remains no deployment |
| Unclear canonical document ownership | Many files contain overlapping status, authority and policy statements | Stale text can contradict current decisions | Introduce document map and explicit canonical owner per concern |

## 3. Keep, simplify, defer

| Area | Keep | Simplify | Defer / do not build |
|---|---|---|---|
| Four foundations | Independent authority and restrictive interlocks | One shared contract vocabulary and traceability | Separate standalone products/services for each pillar |
| Domain architecture | Bounded contexts and state ownership | Implement only active context; logical module boundaries | Microservices for every future domain |
| Risk | Independent deterministic gate, conservative reservation, stress and reconciliation | One initial domain risk policy; no universal scalar | Cross-asset netting/hedge credit and multi-domain budgets |
| Data integrity | Immutable raw evidence, provenance, temporal fields, point-in-time manifests | Small quality vector with consumer fitness rules | Distributed streaming/lakehouse until volume/latency proves need |
| Personal finance | Double-entry journal, staged imports, reconciliation and owner autonomy | Manual import first; provider connector only if justified | Bank API, payments and auto-categorisation before legal/provider review |
| Tax | Effective-dated rules, workpapers and informational estimates | Start with manual source facts and human review | Automated filing/payment and derivative tax conclusions without advice |
| Security | Least privilege, separate key roles, default-deny, egress controls, audit and recovery | Central threat/control matrix and a small number of trust zones | Multiple overlapping policy engines, service meshes or redundant monitoring stacks |
| Health | Independent probes and restrictive interlocks | Monitor only critical dependencies and controls | A complex observability platform before runtime exists |
| AI/learning | Offline reproducibility, model registry principles, prompt/tool isolation | Scripts/statistical baselines first | Multi-agent orchestration, online learning and self-modifying production models |
| Audit/recovery | Atomic local pre-dispatch evidence, UNKNOWN semantics, quarantine and scoped attestations | One ordered local audit authority initially | Distributed audit ledger/consensus/external witness unless threat model demands it |
| Deployment | Phone UI, no always-on worker now | GitHub Actions for research CI | Cloud/PC/server provisioning and two-host topology until owner decision |

## 4. Smallest viable architecture direction

The provisional simplest future implementation shape is:

1. **One modular monolith** with explicit bounded-context module ownership and typed interfaces.
2. **One authoritative transactional store** initially, if selected platform can prove ACID/WAL/fsync and restore semantics. Separate schemas/table ownership and access policies; do not create one database per context by default.
3. **Immutable raw evidence files plus a compact metadata/manifest index** only if data volume and source licences justify it. Do not adopt a distributed lakehouse by default.
4. **Deterministic domain services** for validation, accounting, risk, reconciliation and policy enforcement.
5. **One narrow action boundary** as a future separately approved capability; it is not built or activated now.
6. **One health supervisor and one security incident control plane**, logically separate. Physical separation depends on the accepted host threat tier.
7. **One mobile-first presentation layer** reading projections and issuing scoped requests; no authoritative state or credentials in the UI.
8. **Optional AI research assistant** with no credentials, no generic egress and no ability to alter policy or canonical ledgers.
9. **GitHub Actions for CI/research only**; no persistent worker assumption.
10. **No message broker, service mesh, Kubernetes, distributed consensus, lakehouse or multi-agent scheduler** unless a concrete measured requirement proves it necessary.

This is a provisional simplicity recommendation, not an adopted stack or implementation approval.

## 5. Canonical documentation ownership

The proposed document ownership map is:

| Concern | Canonical design source | Supporting sources |
|---|---|---|
| Project scope, decisions and phase gates | DECISIONS.md + current-state block in ROADMAP.md | RULES.md, REQUIREMENTS.md |
| User-facing project identity | README.md | ARCHITECTURE.md |
| System/domain boundaries | IDEAL_INTEGRATED_SYSTEM_AND_DOMAIN_ARCHITECTURE.md | ARCHITECTURE.md, IDEAL_SYSTEM_ARCHITECTURE_DIAGRAMS.md |
| Four-pillar integration | IDEAL_CORE_PROTECTION_ARCHITECTURE.md | Foundation Traceability Matrix |
| Financial risk | IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md | Domain Risk and Capital Architecture |
| Security | IDEAL_SECURITY_ARCHITECTURE.md | Security Control and Threat Traceability Matrix |
| Data evidence/time | IDEAL_DATA_TRUST_TEMPORAL_AND_POINT_IN_TIME_ARCHITECTURE.md | DATA_INTEGRITY_AND_HEALTH.md |
| Data privacy/retention/audit | IDEAL_DATA_CLASSIFICATION_RETENTION_AND_AUDIT_POLICY.md | Security Architecture |
| Owner authority/autonomy | IDEAL_AUTONOMY_AUTHORITY_AND_PERMISSION_ARCHITECTURE.md | Autonomy Closure Assessment |
| Cross-authority state machines | IDEAL_INTEGRATED_STATE_MACHINE_AND_CONTRACT_ARCHITECTURE.md | Autonomy, risk, reconciliation documents |
| Reconciliation/recovery | IDEAL_RECONCILIATION_AND_VERIFIED_RECOVERY_ARCHITECTURE.md | Health, Security, Risk |
| Capital/accounting examples | IDEAL_CROSS_DOMAIN_ACCOUNTING_AND_VALUATION_EXAMPLES.md | Personal Finance Research |
| Host trust/deployment | IDEAL_HOST_TRUST_TOPOLOGY_AND_RECOVERY_OPTIONS.md | INFRASTRUCTURE_RESEARCH.md, COMPONENT_SELECTION_MATRIX.md |
| Whole-system review | IDEAL_PHASE_02_INTEGRATED_ARCHITECTURE_REVIEW.md | Integrated Adversarial Review |
| Requirement/control/test mapping | IDEAL_FOUNDATION_TRACEABILITY_MATRIX.md | Security Control Matrix |
| Historical conversation/audit | docs/CHATGPT_CONVERSATIONS/README.md and checkpoint records | Never authoritative over accepted decisions |

This map is proposed. Do not delete historical evidence or merge files until the owner approves a consolidation pass. Where a summary conflicts with a canonical decision, DECISIONS.md and the current-state roadmap govern.

## 6. Reversible simplification sequence

1. Freeze new technology candidates unless a documented requirement exposes a gap.
2. Use the canonical ownership map for all new changes; summaries should link to canonical sources.
3. Add a compact current-state index with active/deferred scope and phase gates.
4. Create a one-page architecture contract summary for owner review, retaining detailed research.
5. Mark repeated status statements as historical/superseded where needed; do not silently delete them.
6. When the owner approves documentation cleanup, consolidate duplicated summaries without deleting checkpoint evidence.
7. Only after architecture acceptance, compare a modular-monolith implementation blueprint against the requirements and actual host constraints.

Every step is reversible and preserves source history.

## 7. Verification criteria

- Every architecture component maps to a necessary outcome or explicit future requirement.
- No state machine is implemented as a separate service without a demonstrated need.
- No external dependency is adopted solely because it appears in a candidate list.
- No domain beyond D-001 is activated implicitly.
- All four foundations retain independent authority.
- Security, privacy, approval, audit and recovery controls remain intact after simplification.
- The canonical document map prevents contradictory active status.
- A reviewer can locate each authoritative policy in one place.
- The implementation blueprint has a bounded operational burden for one owner.
- No code or deployment is introduced during documentation simplification.

## 8. Review conclusion

The architecture's security and domain complexity is justified at the *logical design* level because the system spans multiple financial and privacy domains. It would be unjustified to mirror that logical complexity directly into dozens of services, agents, databases or always-on infrastructure.

The smallest viable future build is likely a modular monolith, one transactional authority store, deterministic scripts/services, immutable evidence manifests, one narrowly scoped action boundary (only if later approved), and a phone-first read/control UI. All other technologies remain candidates until requirements and measurements justify them.

No original documents were deleted or consolidated in this checkpoint. No implementation, dependencies, host provisioning, account integration, paper/live execution or phase advancement is authorised.
