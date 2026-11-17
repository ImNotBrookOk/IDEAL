# IDEAL Integrated System and Bounded-Context Architecture

**Status:** Phase 02 architecture research draft; not owner-accepted or implementation-ready  
**Checkpoint:** 072 — 17 November 2026  
**Authority:** D-020, D-021, D-022, D-023; D-018 and D-019  
**Scope:** System/domain boundaries, state ownership, shared foundations, dependency isolation and cross-domain authority  
**Boundary:** Documentation and research only. No implementation, runtime integration, dependency adoption, external account access, credentials, paper/live execution, hosting or phase advancement is authorised.

## 1. Purpose and architecture rule

IDEAL is one private, integrated financial-intelligence and decision-support system composed of specialised bounded contexts. It is not one undifferentiated application, shared ledger or universal agent. Integration means controlled exchange of evidence and decisions through explicit contracts; it does not mean shared ownership of records, funds, credentials, policies or permissions.

The architecture must support a phone-first control and monitoring experience while keeping ingestion, compute, storage, supervision and recovery independent of a mobile device remaining awake. It must remain portable to a later PC/server topology without choosing or provisioning a host now.

The four foundations apply system-wide but retain distinct authority:
1. Risk management — financial exposure and risk permission.
2. Data integrity — source evidence, provenance, quality and lineage.
3. System health — independent operational observation and restrictive interlocks.
4. Security — identity, access, confidentiality, integrity, containment and security incident authority.

No domain may bypass a foundation. No foundation may silently take over another foundation's authority.

## 2. Scope classification

| Domain/capability | Status | Current authority |
|---|---|---|
| Crypto perpetual-futures research | Active initial domain (D-001) | Public/historical research only; no venue/account/credentials or execution |
| Strategy discovery, regime and indicator research | In-scope research capabilities | Candidate generation and evaluation only; deterministic gates remain design requirements |
| Paper execution simulator | Future proposed capability | Not authorised or active |
| Crypto spot accumulation/investment | Deferred proposal (D-014) | No strategy, allocation, venue or implementation |
| Equities and ETFs | Deferred proposal (D-014/D-016) | No broker, instrument universe, account or implementation |
| Commodity-linked exposure (including gold, silver, copper) | Deferred proposal (D-016) | No product, venue, allocation or implementation |
| Cross-asset portfolio and hedging | Deferred architecture requirement (D-016) | Research only; no hedge credit, netting or shared collateral assumed |
| Personal finance and banking | Proposed private single-user domain (D-017) | Manual/file-based design research; no bank connection, real records, credentials or payments |
| Tax intelligence and tax accounting | Proposed future domain (F-005) | Informational research only; no filing, payment or IRD integration |
| Historical data archive and controlled learning | Proposed (F-007) | Architecture research; no collection service, subscriptions or training jobs |
| Local AI runtime and agent framework | Proposed (F-008) | Candidate research only; no model downloads, execution or adoption |
| Dashboard and alerts | Future UI/control capability | Design only; phone-first preference does not authorise deployment |

**Scope precedence:** D-001 remains the sole active market domain. Future domains must not be represented as active merely because they appear in the long-term system map. Proposals F-004–F-008 and D-014/D-016/D-017 remain proposals unless the decision register says otherwise.

## 3. Bounded-context catalogue and state ownership

A bounded context owns its canonical state and rules. Other contexts receive versioned, purpose-limited projections or evidence; they do not write directly into another context's authoritative store.

| Context | Owns | May consume | Must not own/do |
|---|---|---|---|
| Market Data & Source Registry | Provider/venue identities, instruments, raw observations, sequence/gap state, source entitlements and source-quality evidence | Public feeds, licensed files, adapter observations | Decide financial risk, claim source truth from a hash alone, or silently repair raw evidence |
| Canonical Data & Evidence Plane | Normalised observations, provenance graph, revisions, quality/freshness labels, point-in-time snapshots and evidence references | Source registry and domain submissions | Erase source history or grant domain permissions |
| Market Intelligence | Market structure, regimes, indicators, contextual features and confidence/UNKNOWN state | Canonical market evidence | Place orders, set portfolio limits or certify input quality |
| Strategy Research Lab | Strategy manifests, hypotheses, parameter sets, candidate lineage and experiment metadata | Market intelligence and approved research datasets | Grant execution permission, mutate hard policy or self-promote |
| Backtest & Statistical Validation | Simulation runs, cost/fill assumptions, metrics, OOS/walk-forward results and reproducibility manifests | Point-in-time datasets, strategy versions, instrument metadata | Treat synthetic fills as empirical calibration or approve deployment |
| Strategy Registry & Selection | Strategy eligibility, regime scope, cohort comparisons, promotion/demotion history | Validated research evidence and policy thresholds | Force selection or alter gates |
| Derivatives Risk Context | Derivatives exposure, sizing, leverage/margin/collateral model, loss/drawdown state, reservations and risk decisions | Trusted market/account evidence, security permissions, health interlocks | Delegate authority to venue liquidation logic or strategy/AI |
| Future Execution & Reconciliation Context | Future order intent, dispatch lifecycle, fills, positions, funding, fees, venue reconciliation and UNKNOWN state | Exact action permit, risk reservation, venue metadata and adapter observations | Become active absent separate approval; assume exactly-once external effects |
| Personal Finance Context | User-owned account register, double-entry journal, categorisation, budgets, bills, debts, cash flow, goals, net worth and reconciliation cases | Manual/file imports, future approved read-only provider observations, read-only investment projections | Initiate payments, trade, or silently treat imported bank rows as ledger truth |
| Tax Intelligence & Accounting Context | Tax classifications, source facts, tax-year rules, calculations, estimates, liabilities, filing evidence and uncertainty | Personal-finance journal projections, investment/trading facts, official tax rules | Control/lock capital, force reserves/payments, or infer tax treatment from an adjacent asset class |
| Portfolio & Capital View | Read-only consolidated positions/assets/liabilities/cash/exposure projections with explicit currency and ownership semantics | Domain-owned projections and valuation evidence | Merge legal ownership, assume collateral fungibility or write to source ledgers |
| Data Archive & Research Dataset Registry | Retention classes, immutable source archive references, dataset manifests, point-in-time snapshots and licence restrictions | Approved source/evidence streams | Assume unlimited retention or mix private finance and market data indiscriminately |
| Learning & Model Registry | Model/agent versions, training/evaluation manifests, maturity labels, monitoring and retirement history | Approved de-identified/permissioned datasets and workflow traces | Online self-modify production models or autonomously promote itself |
| Health Supervision | Independent observations, dependency graph, health states, alert state and restrictive interlock requests | Telemetry, probes, reconciliation and backup evidence | Grant permissions, alter risk policy, access secrets broadly or initiate financial actions |
| Security & Identity | Principals, roles, credentials/key metadata, policy integrity, security findings, incidents, revocations and attestations | Authentication events, host/runtime evidence and audit events | Approve financial risk or use security incident authority to initiate trades/transfers |
| Owner Authority & Policy Registry | Owner approvals, versioned envelopes, policy artefacts, authority generations and reserved-action catalogue | Owner ceremony evidence and security attestations | Be modified by AI/strategy workloads or infer owner consent |
| Audit & Evidence Registry | Ordered audit events, evidence references, retention class, checkpoints and export history | All consequential state transitions and approvals | Store raw secrets or become a substitute for source/domain ledgers |
| Orchestration & Operations | Schedules, task state, dependency readiness, safe startup/shutdown and recovery workflow | Health/security/authority states and domain task requests | Override domain authority, bypass gates or interpret a restarted process as recovered |
| Mobile Control & Presentation | User-facing views, notifications, approval ceremony presentation and command requests | Read-only projections and scoped requests | Hold authoritative ledgers, private keys, exchange credentials or sole safety interlocks |

The table is a logical decomposition, not a mandated process count, database count or deployment topology. A modular monolith may host multiple contexts initially, provided ownership and write boundaries are enforced. Physical separation is a threat-model and platform decision still open.

## 4. Authority hierarchy and action classes

Authority is not inferred from data access or component placement.

1. **Owner:** final authority over scope, activation, policy/envelope changes, capital actions and reserved approvals.
2. **Owner Authority & Policy Registry:** verifies owner-approved, signed, versioned and current grants; it does not invent owner intent.
3. **Security:** authenticates principals/workloads, evaluates permission and controls security incident containment/revocation.
4. **Data Integrity:** determines whether evidence is authentic enough, complete, fresh, consistent and fit for a declared use.
5. **System Health:** observes independently and can request scoped restrictive interlocks only.
6. **Risk:** independently decides whether a specific exposure-increasing action fits current financial policy and reserves capacity.
7. **Domain engines:** calculate, analyse and propose within read/write scopes; they cannot grant themselves authority.
8. **Adapters/UI/AI tools:** transport or present scoped requests; they are not policy authorities.

For any future consequential action, all required authorities are conjunctive. A positive decision from one authority cannot compensate for a denial/unknown from another.

Action classes must be explicit and domain-specific:
- Read/observe.
- Calculate/derive.
- Propose/recommend.
- Change internal non-financial research state.
- Change owner policy/permissions.
- Increase financial exposure or create an external side effect.
- Reduce/restrict authority or exposure.
- Transfer, withdraw, pay, file, or perform another reserved/irreversible action.
- Recover/release from incident hold.

D-023 governs future execution-capable actions. D-018 additionally requires the tax/personal-finance design to remain user-directed: tax estimates and reserve designations are informational; they cannot lock or segregate user capital or force a payment.

## 5. Shared contracts and data products

The following are logical contract families; no wire format, database schema, API or event bus is selected.

| Contract family | Producer of authority | Required semantics | Consumer rule |
|---|---|---|---|
| Source Observation | Source adapter / source registry | Source ID, instrument/account scope, source event time, receive time, ingest time, sequence/cursor, raw payload hash/reference, schema/version, entitlement and correction identity | Preserve raw evidence; do not infer truth from integrity hash |
| Canonical Evidence | Data integrity plane | Canonical identity, units/currency, source lineage, transformation version, quality/freshness/completeness, revision and point-in-time availability | Reject/mark UNKNOWN when required evidence is missing, stale, conflicted or revised after decision time |
| Domain Projection | Owning domain | Owner context, source revision, projection time, valuation basis, currency, confidence and completeness | Read-only outside owner; projections are not accounting or legal truth |
| Risk Evaluation | Risk context | Exact proposed action, exposure set, policy version, evidence snapshot, reason codes, limits and validity window | Permission alone is insufficient; no action without independent risk approval |
| Health Interlock | Health supervisor | Affected dependency/scope, restrictive state, reason, evidence, generation and expiry/recovery criteria | Restrictive only; stale/unknown interlock status blocks affected risk increases |
| Security Decision | Security context | Principal, action/resource scope, policy/key versions, allow/deny, reason and expiry | Must be checked outside untrusted caller; cannot approve financial risk |
| Owner Grant | Owner ceremony + policy registry | Exact canonical artefact digest, scope, capability, hard limits, reserved actions, expiry, revocation generation and signer evidence | Immutable and non-transferable; no agent-created or widened grants |
| Reservation / Action Lifecycle | Risk + action boundary | Idempotency, exact action digest, reserve/consume/release, dispatch-start, venue outcome, partial fills and UNKNOWN reconciliation | Retain uncertain exposure; external side effect is not locally atomic |
| Ledger Import / Reconciliation | Personal Finance context | Original statement row, provider ID, pending/posted state, corrections/deletions, transfer match, currency/FX fields, duplicate status and journal posting reference | Import is observation; only reconciliation rules create/update authoritative journal entries |
| Tax Assessment | Tax context | Jurisdiction, tax year, taxpayer context, asset/instrument classification, source facts, rule version, calculation, confidence, due date and professional-review flags | Informational until reviewed; no automatic payment or capital restriction |
| Dataset Manifest | Archive/dataset registry | Source revisions, time range, point-in-time cutoff, schema, licence/retention, transformations, exclusions, quality report and reproducible digest | Training/backtests must use immutable versioned snapshots and avoid look-ahead leakage |
| Model/Agent Release | Model registry + owner release authority | Source/data manifest, code/model digest, evaluation/OOS evidence, known limits, monitoring and rollback version | No self-promotion; offline evaluation and explicit release gate |
| Audit Event | Each owning context; audit registry orders | Actor, action, target, prior/new version, reason, evidence references, correlation/idempotency, event ordering, sensitivity class | Minimise sensitive payload; never log secrets; preserve retention/deletion policy |

## 6. Dependency graph and containment

Logical dependency direction:

- Source adapters → Source Registry → Canonical Evidence Plane.
- Canonical Evidence Plane → Market Intelligence → Strategy Research → Backtest/Validation → Strategy Registry.
- Canonical Evidence + account/instrument evidence → Risk Context.
- Owner grant + Security decision + Data validity + Health interlock + Risk decision/reservation → future Action Boundary → Adapter → external venue; then reconciliation returns evidence to the owning execution context.
- Manual/file/provider observations → Personal Finance reconciliation → Personal Finance ledger.
- Domain-owned projections + valuation/FX evidence → Portfolio & Capital View.
- Personal Finance ledger + investment/trading facts + effective-dated tax rules → Tax Intelligence; Tax Intelligence returns estimates/liabilities to Personal Finance as informational projections.
- Approved immutable datasets → offline Learning/Model Research → Model Registry; model outputs remain proposals until independently validated and explicitly released.
- All domains → Audit/Evidence; telemetry and audit integrity → Health/Security oversight.
- Mobile UI ↔ scoped request/read-model boundary; never direct database or credential access.

Containment rules:
1. Failure of one market venue/feed disables only consumers that require that source, unless portfolio-level risk explicitly depends on the missing evidence.
2. A personal-bank import outage must not stop market research or corrupt the personal ledger; imported balances become stale/unknown.
3. Tax-rule uncertainty must not prevent the user from accessing or deploying capital; it changes estimate confidence and warnings only.
4. Portfolio aggregation must mark missing/stale domain projections and must not silently sum incompatible currencies, ownership, valuation bases or collateral.
5. Health/security incidents block affected capabilities according to blast radius; no blanket shutdown without an explicit dependency reason.
6. Cross-domain aggregation is read-only by default. A shared view never creates authority to transfer, net, hedge or reallocate capital.
7. If a shared foundation is compromised, isolate affected trust domains; preserve independent unaffected domains only when their data/identity boundaries remain demonstrably intact.

## 7. Cross-domain financial semantics

The system must not collapse unlike concepts into a single “balance”:
- cash/account ledger balance;
- pending/available bank balance;
- investment market value;
- derivatives economic equity;
- risk-adjusted equity;
- venue margin equity and available margin;
- collateral by asset and legal/account scope;
- tax estimate/provision/liability;
- unrealised and realised P&L;
- external valuation and FX conversion.

Every amount carries currency, unit, valuation timestamp, source, ownership/account scope, status and conversion methodology. FX conversion must preserve source rate, side, timestamp, spread/haircut and uncertainty. Native-currency ledgers remain authoritative; consolidated views are projections.

No implicit netting across legal entities, venues, accounts, products or tax treatments. No implicit collateral transferability or hedge credit. Any future cross-asset risk offset must be explicitly modelled, stress-tested, policy-approved and independently verified.

## 8. Archive, privacy and learning boundaries

Three data planes must remain logically separate:
1. **Market/research evidence:** source-licensed observations, derived market features and point-in-time research datasets.
2. **Private financial records:** bank statements, account balances, liabilities, tax facts and personal financial documents; highest privacy classification and least access.
3. **AI/agent traces:** prompts, tool calls, retrieved documents and outputs; redact/minimise and retain only where justified.

Link by opaque references and purpose-limited access rather than copying sensitive records into prompts, logs or general-purpose datasets. Training use requires explicit dataset eligibility, licence/rights, privacy review, point-in-time correctness, reproducibility and leakage controls. User financial records are not a default training corpus.

Market model research is offline, reproducible, walk-forward/out-of-sample and cost-aware. No online weight updates, self-modifying production strategies or autonomous promotion. Assistant workflow optimisation is distinct from quantitative model learning and must not gain financial authority.

## 9. System topology principles — not a deployment decision

- UI/control plane is separate from compute, ingestion, storage and security/authority services.
- Mobile device is not the sole always-on worker, trusted clock, policy root, audit store or health supervisor.
- Data ingestion, scheduled jobs and archive maintenance can run headlessly when a future host is approved.
- Risk and action enforcement are deterministic and outside AI/strategy process boundaries.
- Security keys and owner approval material are not stored in general application configuration or logs.
- Health supervision must have a failure domain independent enough for the threat it claims to detect; same-host process separation does not survive host-root compromise.
- Initial deployment may use a modular monolith and one authoritative writer if later evidence supports it; this remains provisional.
- Separate domain schemas/transactions and explicit ownership are required even if a single ACID database is eventually selected.
- No cloud, PC, Android runtime, database, queue, policy engine or identity framework is selected here.

## 10. Open architecture questions and required evidence

| ID | Open item | Why unresolved | Evidence needed |
|---|---|---|---|
| SYS-01 | Exact domain/module decomposition | Logical boundaries do not determine process boundaries | Dependency and transaction analysis; smallest maintainable deployment comparison |
| SYS-02 | Shared versus domain-local storage | Cross-domain transactions and privacy isolation trade off | Data classification, consistency needs, recovery and threat model |
| SYS-03 | Portfolio aggregation semantics | Multi-currency, ownership, derivative equity and stale valuation | Explicit accounting/valuation contract and worked examples |
| SYS-04 | Domain-specific risk authority | Personal finance, tax, investing and derivatives have different risk meanings | Separate risk taxonomies and action classes; no universal scalar |
| SYS-05 | Tax treatment of derivatives and future assets | Instrument-specific NZ tax classification and taxpayer facts | Current official IRD law/guidance and qualified NZ tax advice where necessary |
| SYS-06 | Bank provider path | Akahu Personal App limitations and production integration approval unclear | Provider confirmation, correct access tier, terms, data corrections and security model |
| SYS-07 | Market-data retention/licence | Full-depth storage cost and contractual rights vary by source | Per-feed entitlement, retention and deletion terms plus storage sizing |
| SYS-08 | Independent health/security topology | Threat coverage depends on actual host and failure domains | Host options, root/kernel compromise analysis and independent alert path |
| SYS-09 | User approval and recovery device | Platform/authenticator not selected | Device-loss, offline recovery and phishing-resistant ceremony tests |
| SYS-10 | Archive and dataset lifecycle | Retention, privacy, licence and research reproducibility intersect | Classification matrix, deletion/hold policy, manifest and restore design |
| SYS-11 | Local AI/agent framework | Candidate security/compute burden not proven | Pinned-source audit, capability tests, hardware profile and offline operation |
| SYS-12 | Owner approval of future domains | Proposals are not active scope | Separate decision records; no implied activation from architecture inclusion |

## 11. Required verification catalogue

Before any implementation blueprint is accepted, convert each contract into testable properties, including:
- forbidden cross-domain writes and reads; negative permission tests;
- market feed gap, correction, replay, stale and conflicting-source propagation;
- point-in-time dataset reconstruction and look-ahead/leakage tests;
- currency/unit/contract multiplier and rounding invariants;
- native-currency ledger balance, duplicate import, changed/deleted source row, pending-to-posted and transfer reconciliation;
- tax-rule version change, uncertain classification and no-capital-control behaviour;
- aggregation with missing/stale projections, incompatible currencies and no implicit netting;
- risk reservation concurrency, partial fill, unknown cancel/ack and crash recovery;
- owner grant, policy revocation, security interlock and health interlock precedence;
- host/supervisor common-mode failure and external alert path;
- archive retention/licence expiry, privacy deletion, restore and provenance continuity;
- offline model reproducibility, mature labels, OOS validation and no self-promotion;
- UI/device loss, stale display, duplicate command and approval-digest mismatch.

These are required future tests, not tests executed or passed.

## 12. Disposition and next work

This checkpoint establishes a provisional logical map and state-ownership model. It does not freeze schemas, modules, databases, deployment topology, risk limits, provider integrations or domain scope.

Next Phase 02 work:
1. Reconcile this context map against the four foundation documents and the integrated traceability matrix.
2. Define canonical data/evidence lifecycle, time semantics and point-in-time dataset contracts across market, personal-finance and tax domains.
3. Define domain-specific risk taxonomy and portfolio aggregation without collapsing accounting, margin and tax concepts.
4. Complete failure propagation, recovery and independent health/security topology.
5. Conduct a whole-system adversarial review and close traceability gaps.
6. Only after the architecture is complete and independently challenged, prepare implementation-ecosystem research; seek explicit owner acceptance before any Phase 03 consideration.

Phase 02 remains active. Phase 03–19 remain locked. No implementation, runtime integration, dependencies, credentials, accounts, external actions, paid infrastructure or execution are authorised.
