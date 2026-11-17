# IDEAL Requirement → Component → Control → Test Traceability

**Status:** Phase 02 architecture traceability; proposed test catalogue, not executed test evidence  
**Checkpoint:** 089 — 17 November 2026  
**Source of requirements:** REQUIREMENTS.md, DECISIONS.md, RULES.md, ROADMAP.md  
**Authority:** D-001, D-006–D-008, D-018–D-023  
**Boundary:** Documentation only. No implementation, runtime tests, paper/live execution or phase advancement is authorised.

## 1. Purpose and interpretation

This matrix connects the owner-approved/current requirements to logical components, control owners and future deterministic verification. Requirement IDs below are stable traceability aliases for the named source section/bullet; they do not alter the source requirement or its approval status.

Status values:
- **Design specified:** architecture/control/test intent exists.
- **Open:** material semantics, owner decision, source guarantee or topology remains unresolved.
- **Not implemented/tested:** no runtime code or test evidence is claimed.

## 2. Traceability matrix

| Req ID / source anchor | Requirement summary | Owning component(s) | Control / contract | Future verification ID and expected result | Status |
|---|---|---|---|---|---|
| R-SCOPE-001 — REQUIREMENTS / Scope; D-001 | Crypto perpetual futures is the only active initial market domain | Domain Registry, Market Research | Owner scope register; D-001 | T-SCOPE-01: attempted activation of spot/equities/commodities is denied without owner decision | Design specified |
| R-SCOPE-002 — REQUIREMENTS / Scope; RULES | No paper or live execution currently authorised | Owner Authority, Action Boundary | D-015/D-022/D-023; explicit phase gate | T-SCOPE-02: no runtime/action path or credential can submit paper/live order | Design specified |
| R-STRAT-001 — REQUIREMENTS / Strategy lifecycle | Candidate → validation → backtest → cost-adjust → OOS/walk-forward → regime → quality gate → cohort ranking | Strategy Research, Backtest/Validation, Strategy Registry | CT-07/CT-08; dataset manifest | T-STRAT-01: invalid candidate cannot promote; no passing cohort means no eligible strategy | Design specified |
| R-STRAT-002 — REQUIREMENTS / Preliminary screening | >100 trades and >30% win rate are initial filters only, not proof | Backtest/Validation | Statistical gates and uncertainty | T-STRAT-02: pass screening but fail net expectancy/OOS remains rejected | Design specified |
| R-STRAT-003 — REQUIREMENTS / Strategy + Learning | Costs, uncertainty, regime robustness, reproducible lessons and version lineage | Backtest/Validation, Learning Registry | CT-05/CT-08/CT-20 | T-STRAT-03: fees/funding/slippage and OOS evidence required; demoted strategy history retained | Design specified |
| R-EXEC-001 — REQUIREMENTS / Execution quality objective | Future execution optimises net decision value, not raw latency or fee minimisation | Future Execution Research | Execution Quality Research; CT-14/15 | T-EXEC-01: paired policy comparison uses same parent intent/path, causal inputs and untouched OOS | Open; no execution authorised |
| R-RISK-001 — REQUIREMENTS / Risk; D-006 | Initial 0.5% per-trade target applies only to initial crypto-perpetual policy | Derivatives Risk | D-006; CT-09/10 | T-RISK-01: no other domain inherits this limit; denominator must be resolved before future execution | Open denominator |
| R-RISK-002 — REQUIREMENTS / Risk; D-008 | 10% UTC day-start equity loss boundary, realised + unrealised, 24-hour cooldown | Derivatives Risk | D-008; UTC day-start snapshot | T-RISK-02: exact boundary, deposits/withdrawals, multi-currency and valuation semantics | Open semantics |
| R-RISK-003 — Foundational protection / Risk | Independent deterministic risk gate; exact action/evidence binding; reservations and safe states | Risk Authority, Reservation Ledger | CT-09/10; version vector | T-RISK-03: stale/unknown policy/account/position denies; reservation conservation under partial fill | Design specified |
| R-DATA-001 — Foundational protection / Data Integrity | Provenance, timestamps, schema, completeness, freshness, quality, corrections and lineage | Source Registry, Evidence Plane | CT-01–06 | T-DATA-01: raw evidence immutable; correction creates revision; source identity mismatch quarantined | Design specified |
| R-DATA-002 — Data temporal architecture | Point-in-time availability, valid/known time and no look-ahead | Dataset Registry, Backtest/Validation | CT-03/05; bitemporal semantics | T-DATA-02: late correction does not rewrite as-known-then backtest | Design specified; source fidelity open |
| R-HEALTH-001 — Foundational protection / System Health | Independent health supervision and scoped restrictive-only interlocks | Health Supervisor | CT-11; health state machine | T-HEALTH-01: supervisor cannot grant authority or self-certify; missing heartbeat restricts affected scope | Design specified |
| R-SEC-001 — Security requirements 9 | Confidentiality, integrity, availability, authenticity and accountability | Security / Identity | SEC-01–14 | T-SEC-01: threat/control coverage and negative permission tests | Design specified |
| R-SEC-002 — Security requirements 10 | Least privilege, scoped identities, authentication ≠ authorisation | Security / Policy Enforcement | SEC-01/02/05 | T-SEC-02: cross-scope principal/resource request denied | Design specified |
| R-SEC-003 — Security requirements 11 | Secret/key lifecycle, encryption, minimisation, no secrets in logs/prompts | Security / Data Policy | SEC-03/04/09 | T-SEC-03: secret scan, log/prompt redaction and key rotation/revocation tests | Design specified |
| R-SEC-004 — Security requirements 12 | Secure supply chain, CI/CD, provenance and reproducible verification | Build/Release Security | SEC-07 | T-SEC-04: unpinned/unverified dependency or workflow token privilege denied | Design specified; future stack open |
| R-SEC-005 — Security requirements 13 | Security assurance reported separately from operational health | Security + Health | SEC-11 | T-SEC-05: healthy-but-compromised scenario does not produce SECURE status | Design specified |
| R-SEC-006 — Security requirements 14 | Vulnerability discovery, remediation, incident response and recovery | Security Incident Control Plane | SEC-12/13 | T-SEC-06: finding closure requires evidence/retest; recovery requires scoped attestation | Design specified |
| R-AUDIT-001 — Security requirements 15 | Tamper-evident audit with privacy/retention controls | Audit Registry, Data Policy | SEC-09/10; CT-21 | T-AUDIT-01: audit durability failure blocks side effect; deletion respects holds/retention | Design specified; durations open |
| R-ARCH-001 — Integrated objective/foundations | Bounded domains share four foundations without merging authority | Domain Registry, four foundations | Core Protection Architecture | T-ARCH-01: cross-context writes forbidden; all critical flows have named owner | Design specified |
| R-ARCH-002 — Integrated objective/foundations | Failure containment by dependency blast radius | Health, Security, domain owners | Dependency graph and interlock contract | T-ARCH-02: single provider/feed outage restricts only dependent capabilities | Design specified; runtime topology open |
| R-AUTH-001 — D-023 / bounded autonomy | Versioned, scoped, time-bounded, revocable owner envelope | Owner Authority / Policy Registry | CT-13; SEC-01/02/03 | T-AUTH-01: out-of-envelope, expired or altered action denied | Design specified |
| R-AUTH-002 — Autonomy requirements | Dedicated action boundary outside AI/strategy; exact action and one-use permit | Action Boundary | CT-14; SEC-14 | T-AUTH-02: direct agent adapter/network access impossible; digest mismatch rejected | Design specified |
| R-AUTH-003 — Checkpoint 068 | Monotonic revocation generation serialised with DISPATCH_STARTED | Authority Registry, Action Boundary | Revocation/fencing protocol | T-AUTH-03: revocation-first blocks; dispatch-start-first stays UNKNOWN/in-flight | Design specified; SLO open |
| R-AUTH-004 — Checkpoint 069 | Intent, risk reservation, audit and outbox committed before dispatch; dispatch-start/audit before network write | Action Boundary, Risk, Audit | Local ACID transactions A/B | T-AUTH-04: crash/fault injection at each boundary never dispatches without durable evidence | Design specified; store open |
| R-REC-001 — Checkpoint 076 | Restore/recovery requires quarantine, reconciliation, scoped attestations and owner release | Recovery Controller, four pillars | CT-16/22; SEC-13 | T-REC-01: old backup cannot resurrect revoked authority; missing attestation blocks release | Design specified; topology open |
| R-CAP-001 — Checkpoint 074 | Domain-specific risk and capital semantics | Domain Risk, Personal Finance, Tax, Portfolio View | CT-06/09/18/19 | T-CAP-01: ledger cash, margin, collateral, tax and net worth remain distinct | Design specified |
| R-CAP-002 — Checkpoint 074 | No implicit legal/account/venue netting or hedge credit | Portfolio & Capital View, Risk | Gross/net/factor exposure contract | T-CAP-02: cross-account/venue offsets not applied without approved netting set | Design specified; policy open |
| R-TAX-001 — D-018 | Tax estimates/reserves cannot lock, segregate or force payment of owner capital | Tax Intelligence, Personal Finance | CT-19; D-018 | T-TAX-01: attempted lock/payment side effect is impossible absent separate owner action | Design specified |
| R-PF-001 — D-017/F-004 proposal | Bank imports are observations; journal posting requires reconciliation | Personal Finance | CT-17/18; reconciliation state machine | T-PF-01: duplicate/pending/changed/deleted rows do not double-post or silently disappear | Design specified; domain proposed |
| R-RET-001 — Checkpoint 079 | Data class/purpose retention and deletion across all copies | Data Policy, Security, Operations | SEC-09/13; C0–C3 | T-RET-01: deletion/expiry covers primary, replica, cache, export, derived data and backup | Design specified; periods open |
| R-PRIV-001 — Privacy/processor design | Agent-only processing distinguished from provider own-purpose use | Security / Provider Governance | Section 11 processor assessment | T-PRIV-01: processor purpose/subprocessor and cross-border role review before connection | Design specified; no provider selected |
| R-DEP-001 — REQUIREMENTS / Cost and deployment | $0 recurring target; open-source/free tiers; no spend without approval | Architecture / Operations | Cost and hosting gates | T-DEP-01: every selected component has cost/limit/exit analysis; no unapproved billing | Design specified |
| R-UI-001 — REQUIREMENTS / Scope | Android phone is primary control/monitoring device; compute can be headless | Mobile UI / Host Operations | Phone-first topology principles | T-UI-01: device loss/stale UI does not change authority or stop independent safe state | Design specified; host open |
| R-AI-001 — Foundational protection / D-023 | AI proposes/analyses only; no self-authority, credentials or generic egress | AI Boundary, Security, Action Boundary | SEC-08; CT-07/13/14 | T-AI-01: prompt injection/compromised agent cannot access secrets or invoke action without gates | Design specified |
| R-CONTRACT-001 — Canonical Contract Catalogue / checkpoint 089 | Financial amounts preserve canonical fiat/crypto asset identity, denomination, precision and explicit valuation lineage | Asset Registry (logical), Canonical Evidence, Risk, Personal Finance, Portfolio View | CT-03/06/09/18; AssetAmount semantics | T-ASSET-01–06: ambiguous ticker rejected; fiat/native/token identities distinct; stablecoin parity not assumed; precision deterministic; historical mappings effective-dated; projections preserve denomination | Design specified; registry/schema open |
| R-ARCH-003 — Architecture-first completion | Complete architecture, contracts, diagrams, threat model, failure analysis, traceability, independent review and owner acceptance before implementation | Architecture Governance | Phase 02 exit gate | T-ARCH-03: all artefacts, review findings and owner approval recorded before Phase 03 consideration | Open: independent review and owner acceptance |

## 3. Coverage summary

- Requirements are mapped to a logical component owner, control/contract and future verification identifier.
- The matrix includes both current active scope and future proposed domains, with their authority status preserved.
- The current matrix contains 35 requirement groups; checkpoint 086's 34-group count remains a historical snapshot.
- Future test identifiers are planning labels only. No code/test suite has been created or run by this matrix.
- The D-006 denominator, D-008 semantics, host topology, data source fidelity, retention durations and future domain policies remain open.
- Independent architecture/security/operations review and explicit owner acceptance remain mandatory before Phase 02 closure.

## 4. Verification quality rules

A future test is valid only if:
- it has a deterministic setup and an independent expected-result oracle;
- it covers both allowed and denied/unknown paths;
- it includes failure injection at state boundaries;
- it asserts audit/provenance and no unintended side effect;
- it is reproducible against pinned code, data, configuration and environment;
- it does not use real financial accounts or credentials in CI;
- it cannot be weakened by changing thresholds or deleting test cases without review;
- its output is retained under the relevant audit/retention class.

Quantitative backtests additionally require fees, spread, funding, slippage, latency, liquidity, survivorship/look-ahead controls, walk-forward/OOS, uncertainty, multiple-testing and position sizing.

## 5. Disposition

This matrix closes the requirement-to-component-to-control-to-test mapping at design level. It does not demonstrate implementation or test passage. Phase 02 remains active; Phases 03–19 remain locked. No implementation, dependency, account, credentials, paper/live execution, paid infrastructure or phase advancement is authorised.


## Checkpoint 092 — critical field-schema traceability

The field-level schemas for OwnerEnvelope, SecurityAuthorization, HealthInterlock, RiskEvaluation, RiskReservation, ActionIntent, AdmissionPermit, DispatchReceipt, ReconciliationCase, PersonalFinanceImport, JournalPosting, TaxWorkpaper, AuditEvent and RecoveryAttestation are defined in [IDEAL Critical Contract Field Schemas](IDEAL_CRITICAL_CONTRACT_FIELD_SCHEMAS.md). Future tests must assert exact digest binding, type/unit validity, version-vector consistency, idempotency and forbidden fields such as capital restriction in tax workpapers.

 
## Margin, collateral and liquidation traceability — checkpoint 100

| Req ID / source anchor | Requirement summary | Owning component(s) | Control / contract | Future verification ID and expected result | Status |
|---|---|---|---|---|---|
| R-MARGIN-001 — REQUIREMENTS / Margin | Distinguish risk-adjusted equity from venue margin equity and available margin | Derivatives Risk, Capital Ledger | Risk-adjusted equity contract; CT-RISK | T-MARGIN-01: venue margin fields cannot silently replace risk denominator | Design specified; denominator open |
| R-MARGIN-002 — REQUIREMENTS / Margin | Eligible collateral with source-bound valuation and separate IM/MM haircuts | Collateral Registry, Data Integrity, Risk | CollateralEligibilityRule / CollateralValuation | T-MARGIN-02: stale/ineligible/depegged collateral cannot increase risk capacity | Design specified; values open |
| R-MARGIN-003 — REQUIREMENTS / Margin | Effective-dated margin tiers and contract/account-mode semantics | Venue Rule Registry, Risk | VenueRuleSet / InstrumentRiskTier | T-MARGIN-03: tier boundary and stale-rule tests reject optimistic risk | Design specified; venue open |
| R-MARGIN-004 — REQUIREMENTS / Margin | Mark/index/last/executable prices remain separate | Market Data, Data Integrity, Risk | PositionRiskSnapshot | T-MARGIN-04: mark breach triggers risk restriction even if last price does not; stale mark blocks risk increases | Design specified |
| R-MARGIN-005 — REQUIREMENTS / Margin | Reserve active/conditional/uncertain orders until reconciled | Risk Reservation Ledger, Reconciliation | OpenOrderRiskReservation | T-MARGIN-05: timeout/cancel ambiguity never releases exposure; partial fills conserve reservation | Design specified |
| R-MARGIN-006 — REQUIREMENTS / Margin | Liquidation, insurance/ADL and partial fills are external events requiring reconciliation | Action Gateway, Risk, Reconciliation | LiquidationEvent; integrated state machine | T-MARGIN-06: trigger/ADL notice alone cannot release reservation or assert terminal position | Design specified |
| R-MARGIN-007 — REQUIREMENTS / Margin | No implicit cross-venue/account/collateral hedge credit | Portfolio Risk | D-001/D-020; ODR-04 | T-MARGIN-07: offset denied absent approved enforceable netting set | Design specified; future domain deferred |
