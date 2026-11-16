# IDEAL

IDEAL is an integrated, evidence-driven personal financial intelligence system. Its initial active scope is crypto perpetuals research and paper trading; future financial domains remain separately gated. Specialised engines operate under four shared foundations: deterministic risk management, trustworthy data, independent system-health oversight and security by design. AI may research and propose; deterministic controls govern evidence quality, risk, permissions and authorised actions.

## Status
Planning baseline. Implementation is not yet authorised. This repository is the source of truth for scope, decisions, architecture, testing, trading knowledge and project accountability.

## Initial scope
- Crypto perpetual futures only.
- Timeframes: 1W/1D macro; 4H/1H structure; 30M intermediate; 15M entry evaluation; optional 5M refinement.
- Autonomous strategy discovery and regime-specific selection.
- Paper trading only; live trading requires separate explicit approval.
- Initial risk: 0.5% equity per trade; 1:3 reward/risk objective.
- Hard daily loss boundary: 10% of UTC day-start equity including realised and unrealised PnL, followed by 24-hour cooldown.
- $0 operating-cost target; free tiers/open source only. No billing activation without approval.
- Deterministic risk and execution controls; AI cannot modify limits, gates or permissions.

## Source of truth
- ROADMAP.md — gated implementation plan; Phase 02 prioritises the integrated risk, data-integrity and system-health foundation.
- docs/IDEAL_CORE_PROTECTION_ARCHITECTURE.md — owner-approved integrated system vision, protection pillars, authority boundaries, failure model and Phase 02 design requirements.
- docs/IDEAL_SECURITY_ARCHITECTURE.md — security threat model, defensive controls, security-health integration, vulnerability assurance and incident recovery requirements.
- RULES.md — mandatory engineering, accountability and trading constraints.
- REQUIREMENTS.md — product and quantitative requirements.
- ARCHITECTURE.md — provisional system boundaries and data flow.
- TESTING.md — verification and evidence requirements.
- SKILLS.md — persistent trading and research knowledge framework.
- DECISIONS.md — append-only decisions and rationale.
- docs/REPO_RESEARCH.md — open-source candidate shortlist, licence notes and Phase 01 due-diligence backlog.
- docs/CHATGPT_CONVERSATIONS/ — dated conversation transcripts and operational audit evidence; see its [index](docs/CHATGPT_CONVERSATIONS/README.md).

## Delivery and accountability
One approved task at a time: implement, test in isolation, integration-test with completed modules, run regression tests, audit, document evidence, then ask the owner to approve the next named task. Each IDEAL work conversation is recorded in `docs/CHATGPT_CONVERSATIONS/`; the assistant must stop at the closeout gate and wait for the owner's response. No task is complete without recorded proof.
