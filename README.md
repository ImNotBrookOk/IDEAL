# IDEAL

**IDEAL is a private, integrated financial intelligence and decision-support platform being designed to help its owner understand, manage, protect and grow their overall financial position.**

It is not intended to be merely a cryptocurrency trading bot. The long-term vision is one coherent personal platform made up of specialised, independently governed domains and engines: market intelligence and quantitative research; systematic trading and investment analysis; portfolio and capital oversight; personal finance; and tax-aware financial information. These capabilities are intended to share trustworthy information and a consistent view of the owner's financial position without collapsing their separate permissions, risks, accounting rules or responsibilities.

The initial research domain is **crypto perpetual futures**. That is the starting point for proving the architecture, not the limit of IDEAL's purpose. Future domains may include spot digital assets, equities, commodities and broader personal-finance capabilities, but each remains separately researched, specified and explicitly gated before adoption.

## The overall goal

Build a dependable personal financial operating system that can:

- observe and explain relevant markets, macro conditions, portfolio exposures and personal financial information;
- research, test and compare investment and trading ideas using traceable evidence rather than unsupported claims;
- identify market regimes and evaluate which strategies, if any, are suitable for the current conditions;
- manage risk, capital, liquidity and exposure across the whole system rather than optimising isolated strategies;
- maintain a reliable, auditable view of income, expenses, assets, liabilities, investment activity and financial performance as future domains are approved;
- learn from historical outcomes through controlled, reproducible research without allowing models or agents to silently rewrite production rules;
- automate appropriate low-risk research and operational work while preserving owner control over consequential actions;
- explain what it knows, what it does not know, why it reached a conclusion, what evidence it used and what could go wrong.

The objective is not maximum automation or maximum trading frequency. It is **better-informed decisions, durable capital protection, trustworthy records, operational resilience and accountable autonomy**.

## Four foundations shared by every domain

Every specialised engine must operate under four integrated foundations:

1. **Risk management** — governs capital, exposure, authority, permitted actions, containment and recovery. It is independent of strategy logic.
2. **Data integrity** — governs provenance, quality, completeness, point-in-time correctness, reconciliation, retention and reproducibility.
3. **System health** — independently monitors whether components, data flows, controls, dependencies and recovery mechanisms are functioning as intended.
4. **Security** — protects identities, permissions, secrets, data, code, integrations, infrastructure and audit evidence against unauthorised access, leakage, tampering and abuse.

These foundations reinforce one another but remain independently assessed. A healthy service is not necessarily secure; valid data does not make a strategy safe; and a profitable strategy does not earn authority to bypass risk controls.

## Intelligence, automation and owner authority

IDEAL is intended to use deterministic software for calculations, accounting, validation, risk decisions, reconciliation and other tasks where correctness must be testable. AI agents and models may assist with research, interpretation, discovery, explanation and proposing work within explicit permissions.

AI is not the ultimate authority for capital, risk limits, security permissions, data acceptance or consequential actions. No agent may silently weaken a hard control, approve its own work, conceal uncertainty or promote an unvalidated strategy. Models and research outputs must be versioned, reproducible and independently evaluated.

The owner remains the final authority. Consequential actions require explicit permission and the appropriate verified controls. Separate domains must not assume they can share funds, collateral, credentials or execution permissions merely because they belong to the same platform.

## Scope and delivery philosophy

- **Private personal system first.** Any future release for other users is a separate product, legal, security and regulatory decision—not an assumed outcome.
- **Architecture before implementation.** Define and challenge the complete system, trust boundaries, authority model and contracts before selecting frameworks or writing runtime code.
- **Evidence before adoption.** Research official documentation, maintained open-source projects, licences, security posture, limitations, costs and alternatives.
- **Auditability by design.** Preserve decisions, source evidence, versions, test results, approvals and meaningful changes in the repository.
- **Minimal cost and portable foundations.** Prefer free/open-source and self-hostable options where they meet the quality bar; avoid paid commitments without approval. Design for mobile-first use with portability to PC/server environments.
- **Safety before speed.** Fail closed when critical evidence, controls, permissions or system state cannot be trusted.

## Current project status — 17 November 2026

**Current status:** Phase 02 — active | Design and research only

- Phase 01 open-source and infrastructure research is closed.
- Phase 02 architecture and contract design is active. The current priority is completing and challenging the four shared foundations and their cross-pillar contracts, including risk management and bounded-autonomy authority.
- Phase 03 and all later phases remain locked.
- No runtime implementation, trading execution, exchange credentials, bank connections, paid infrastructure, hosting or external security scans are authorised.
- No live trading is authorised. The initial market scope remains crypto perpetual futures research; any later paper or live execution capability requires its own explicit approval and gates.
- The long-term domains described above are vision and research scope, not a claim that those engines are built or authorised.

## Initial quantitative research scope

The first market-research domain is crypto perpetual futures. Its current research specification includes:

- Timeframes: 1W/1D macro; 4H/1H structure; 30M intermediate; 15M entry evaluation; optional 5M refinement.
- Regime-aware strategy research and controlled strategy discovery.
- Initial per-trade risk target: 0.5% of equity (the precise equity denominator remains an open architecture question).
- Reward/risk research objective: 1:3; this is an objective to test, not a promised result.
- Hard daily-loss boundary: 10% of UTC day-start equity including realised and unrealised P&L, followed by a 24-hour cooldown. This is an existing outer policy boundary, not a normal loss target or complete risk system.
- Realistic evaluation must account for fees, funding, spread, slippage, liquidity, latency, position sizing, survivorship/look-ahead bias and out-of-sample validation.

These initial trading constraints do not define the risk policies for future domains. Each domain must have its own approved requirements and controls.

## Repository source of truth

- [ROADMAP.md](ROADMAP.md) — gated project plan, phases, milestones and approval boundaries.
- [docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md](docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md) — integrated system vision and four-foundation architecture.
- [docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md](docs/IDEAL_RISK_MANAGEMENT_ARCHITECTURE.md) — provisional Phase 02 risk research, evidence, controls and unresolved questions.
- [docs/IDEAL_SECURITY_ARCHITECTURE.md](docs/IDEAL_SECURITY_ARCHITECTURE.md) — security threat model, defensive controls, vulnerability assurance and recovery.
- [docs/IDEAL_ARCHITECTURE_FIRST_RESEARCH_PLAN.md](docs/IDEAL_ARCHITECTURE_FIRST_RESEARCH_PLAN.md) — architecture-first research sequence and acceptance criteria.
- [REQUIREMENTS.md](REQUIREMENTS.md) — product, system and quantitative requirements.
- [ARCHITECTURE.md](ARCHITECTURE.md) — provisional system boundaries and data flow.
- [RULES.md](RULES.md) — mandatory engineering, accountability and trading constraints.
- [TESTING.md](TESTING.md) — verification and evidence requirements.
- [DECISIONS.md](DECISIONS.md) — append-only decisions and rationale.
- [SKILLS.md](SKILLS.md) — persistent trading and research knowledge framework.
- [docs/REPO_RESEARCH.md](docs/REPO_RESEARCH.md) — open-source candidates, licence notes and due-diligence backlog.
- [docs/CHATGPT_CONVERSATIONS/](docs/CHATGPT_CONVERSATIONS/) — dated work records and operational audit evidence.

## How work is accepted

One explicitly authorised task at a time. Research and design findings are documented with sources, assumptions, alternatives, limitations and open questions. Repository changes are fetched back and checked. When implementation is eventually authorised, each task must be implemented and tested in isolation, integration-tested, regression-tested, audited and documented before the next task is proposed.

A research checkpoint does not itself approve a decision, change policy, unlock a phase or authorise execution. IDEAL advances only through explicit owner review and approval. No task is complete without recorded verification.


## Bounded autonomy authority design

The future owner-authorised autonomy model is being translated into enforceable architecture, including signed operating envelopes, workload identity, exact-action authorisation, independent risk reservations, revocation, audit and recovery. This remains Phase 02 research; no execution capability or technology has been adopted. See [Autonomy Authority and Permission Architecture](docs/IDEAL_AUTONOMY_AUTHORITY_AND_PERMISSION_ARCHITECTURE.md).
