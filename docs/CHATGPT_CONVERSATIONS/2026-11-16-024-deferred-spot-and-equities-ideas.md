# IDEAL Conversation Audit 024 — Deferred Spot Accumulation and Equities Ideas

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research (IN PROGRESS)  
**Scope effect:** No change to active scope or phase permissions.

## 1. User-visible transcript

**User:**
> Well we can eventually build in an engine that also invest in spot judging by the macro outlook. Meaning it realize we are at the bottom of the bear market about to flip into a bull market based on macro information and it uses x amount of profits and dca into spot.... its something we can add to the roadmap to look into later on. But for now lets focus on our main objective. But do save this idea for later. That way we can not only trade futures but slowly accumulate on spot.. because this engine could be used to better decisions for stock trading also right...?

## 2. Response and technical clarification

The idea is feasible as a future platform expansion, but it must not be treated as a promise that a system can reliably identify exact market bottoms. A more defensible design would estimate macro/regime probabilities, define an approved capital budget, and stage spot purchases only when evidence and deterministic risk gates permit.

The underlying decision framework can be reused for equities: point-in-time data, regime classification, strategy validation, portfolio/risk controls, execution scheduling and placement, TCA, audit and learning. Equities are not merely another symbol adapter; corporate actions, exchange sessions/auctions, consolidated market data, settlement, borrow/short constraints, fees, liquidity models, broker permissions and jurisdictional requirements need their own evidence and domain-specific components.

## 3. Documentation changes

Created `docs/FUTURE_SCOPE_IDEAS.md` with two deferred proposals:

- **F-001 — Macro-regime-aware crypto spot accumulation:** a separately risk-budgeted spot sleeve, potentially funded by an explicitly approved fraction of eligible realised profits, using staged DCA rather than an assumed exact-bottom signal. The document identifies macro data-vintage/look-ahead controls, reserve and capital definitions, allocation caps, asset eligibility, custody, accounting, concentration and drawdown controls, and backtesting requirements.
- **F-002 — Equities expansion:** reuse of general platform capabilities while requiring equities-specific market data, execution, accounting, corporate-action, broker and regulatory work.

Updated:
- `DECISIONS.md`: added **D-014 — Proposed**, not accepted. D-001 remains unchanged: crypto perpetual futures are the sole active initial market scope.
- `ROADMAP.md`: added a clearly labelled deferred-future-scope section. It does not change Phase 01 priorities, unlock Phase 02 or authorise implementation.
- `docs/CHATGPT_CONVERSATIONS/README.md`: indexed this audit record.

## 4. Approval boundary

The owner explicitly asked to save these ideas for later and to keep the current main objective unchanged. Therefore:
- Current Phase 01 work continues on historical perpetual data and execution-quality evidence.
- No spot venue, asset universe, capital allocation, DCA strategy, broker, equities universe, account or implementation is approved.
- D-014 remains Proposed; it does not supersede or amend D-001.
- Phase 02 remains LOCKED. No implementation, exchange/account access, paper execution, live execution, paid service or risk-policy change is authorised.

## 5. Test status

Documentation-only change. No source code or runtime behaviour changed; no code tests were run or claimed.


## 6. Commit and read-back verification

Initial commits:
- `docs/FUTURE_SCOPE_IDEAS.md`: `1212b2c4698c3843714374faf485ca54cf78c506`.
- `DECISIONS.md`: `5f218d797e17d83df22f942aa7f1e7ec85df7b99`.
- `ROADMAP.md`: `5c5a6e28f5459ec2b38ebe44f93a1e14b11207c9`.
- Audit index: `2ea21fbd2deffc0076c30c8a3bb64b1156495495`.
- This conversation record: `420841062c432001204f1512c08f572352280e6c`.

All five files were fetched again from `main`. Content checks passed: both deferred ideas are present; D-014 is Proposed; D-001 remains the active initial-scope decision; ROADMAP labels future scope as not active; this audit record and index entry are present. Read-back blob SHAs: future ideas `4f162e4595838d6c6a969d221fb4262823c43689`; decisions `f26c5794544c684d3af91a0b1bd2d55a5d954026`; roadmap `04ad45f5f5913705c3e3ced06a66b0d124875c06`; audit record before this verification append `fac79ea694e6c72c161f9aca2cb93098f1454709`; audit index `0fe3ad1c695d2a60711fb29dec11577abd377ffd`.

No code tests were run because the change is documentation only. No phase transition occurred.
