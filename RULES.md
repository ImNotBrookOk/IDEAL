# IDEAL Rules

These rules are mandatory for every contributor and agent.

## Scope and delivery
- Follow ROADMAP.md in order. Do not skip, bundle, reorder or silently expand tasks.
- Inspect existing code before adding a module; do not duplicate completed work.
- No implementation before the planning baseline and next task are approved.
- A task is not complete without isolated, integration, regression and audit evidence.
- Record deviations and failures; never claim an unrun test passed.
- No paid service, subscription or billing activation without explicit owner approval.
- Work on one approved task at a time. Completing a task does not authorise the next task.

## Conversation accountability
- At the close of every IDEAL work conversation, create a dated record under `docs/CHATGPT_CONVERSATIONS/`.
- Preserve the complete available user-visible transcript verbatim and add a chronological operational audit log covering material research, repository changes, tests, CI, PRs, merges, failures, corrections and evidence links.
- Clearly distinguish owner decisions, assistant proposals, assumptions, failed attempts and unresolved questions. Never treat a recommendation or silence as approval.
- Do not invent missing transcript content. Mark incomplete historical transcripts as partial.
- Do not record hidden chain-of-thought, private system/developer instructions, credentials, tokens or unnecessary sensitive information. Record concise decision rationales and verifiable actions instead.
- Conversation records are append-only. Correct errors with a dated addendum; do not silently rewrite history.
- A standing owner authorisation may cover a bounded sequence of roadmap research tasks. Record its exact scope and limits in DECISIONS.md; proceed through that scope in roadmap order without requesting approval at every gate.
- Under the current standing authorisation, continue Phase 01 research gates in order. For each research change, complete isolated/integration/regression tests, a five-axis audit and documentation before merging its PR. Automatically squash-merge a research PR only when CI is green, the reviewed diff is within the authorised research scope, no material blocker remains, and the PR head SHA is unchanged at merge time. If any condition fails, do not merge; record and report the blocker.
- Commit each conversation audit record and its index update directly to main after the work is complete; do not create a separate PR solely for the transcript. Verify the saved record by reading it back.
- The standing authorisation does not approve Phase 02 or later, implementation, exchange/account connections, paper/live orders, risk changes, paid infrastructure or billing. Stop at the Phase 01 exit review and obtain explicit owner approval before Phase 02.
- If no substantive project work occurred, a brief closeout entry may record that fact rather than manufacture a transcript.

## Trading safety
- Paper trading only. No live orders or real-money credentials until separate explicit approval.
- Initial risk target is 0.5% of equity per trade; 1:3 is a research objective, not a guaranteed outcome.
- Daily hard loss boundary is 10% of UTC day-start equity, including realised and unrealised PnL; breach triggers a 24-hour trading cooldown.
- The 10% boundary is an emergency ceiling, not a normal risk budget. Earlier warning/suspension thresholds and portfolio limits must be researched, documented and approved before paper trading.
- Unknown regime, stale/incomplete data, failed reconciliation, unavailable risk service or ambiguous state means no new trade.
- Risk, permissions, progression gates and execution invariants are deterministic and independently enforced.
- AI cannot edit its own limits, gate thresholds, permissions, kill switches or execution rules.

## Research integrity
- Include fees, spread, slippage, funding, partial fills and realistic latency assumptions.
- Prevent look-ahead, survivorship and selection bias; separate training, validation and untouched out-of-sample data.
- Use walk-forward validation and report sample size, uncertainty, drawdown and regime coverage.
- Win rate alone is not evidence of edge. If absolute quality gates fail, reject the candidate.
- Apply relative cohort ranking only after absolute gates and only to sufficiently large, comparable cohorts. Retain the strongest 50% of that eligible cohort; select none if none qualify.
- Correlated indicators are not independent confirmations.
- Preserve strategy versions, datasets, parameters, code/config hashes and reproducible run metadata.

## AI boundaries
- Treat model output, market text, exchange payloads and external data as untrusted.
- AI may research, propose, explain and write bounded lessons; deterministic validators decide eligibility and enforce safety.
- AI unavailability must fail safely; routine ingestion, calculations, risk checks and state transitions must not depend on AI.
