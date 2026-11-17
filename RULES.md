# IDEAL Rules

These rules are mandatory for every contributor and agent.

## Scope and delivery
- Follow ROADMAP.md in order. Do not skip, bundle, reorder or silently expand tasks.
- Inspect existing code before adding a module; do not duplicate completed work.
- No implementation before the planning baseline and next task are approved.
- A task is not complete without isolated, integration, regression and audit evidence.
- Record deviations and failures; never claim an unrun test passed.
- No paid service, subscription or billing activation without explicit owner approval.
- Work on one bounded roadmap task at a time; do not skip, bundle or reorder. D-022 authorises autonomous progression through the defined Phase 02 architecture/research sequence without interim approval at every task boundary. Do not exceed that standing scope.

## Conversation accountability
- At the close of every IDEAL work conversation, create a dated record under `docs/CHATGPT_CONVERSATIONS/`.
- Preserve the complete available user-visible transcript verbatim and add a chronological operational audit log covering material research, repository changes, tests, CI, PRs, merges, failures, corrections and evidence links.
- Clearly distinguish owner decisions, assistant proposals, assumptions, failed attempts and unresolved questions. Never treat a recommendation or silence as approval.
- Do not invent missing transcript content. Mark incomplete historical transcripts as partial.
- Do not record hidden chain-of-thought, private system/developer instructions, credentials, tokens or unnecessary sensitive information. Record concise decision rationales and verifiable actions instead.
- Conversation records are append-only. Correct errors with a dated addendum; do not silently rewrite history.
- A standing owner authorisation may cover a bounded sequence of roadmap research tasks. Record its exact scope and limits in DECISIONS.md; proceed through that scope in roadmap order without requesting approval at every gate.
- Current active authority is Phase 02 architecture/research/documentation only. For documentation-only work, update all affected source/traceability/roadmap/audit files, fetch changed files back from GitHub and verify required content; record any unverified result. No code/runtime tests are applicable to a documentation-only change. If a future owner decision separately authorises code work, the applicable isolated/integration/regression tests, five-axis audit, review, CI and PR/merge controls must be completed before merge; no such code authority currently exists.
- Commit each conversation audit record and its index update directly to main after the work is complete; do not create a separate PR solely for the transcript. Verify the saved record by reading it back.
- Current active authority: Phase 01 is closed under D-015. D-022 authorises the architecture-first Phase 02 research/design sequence; the owner has explicitly directed autonomous continuation without interim progress interruptions. Continue in roadmap order and document each material checkpoint. Phase 02 authority is limited to research, architecture, contracts, source review and documentation. It does not authorise runtime implementation, test/runtime integration, dependency adoption, exchange/bank/account connections, credentials, real financial records, paper/live execution, tax filing/payment, external security testing, hosting, paid infrastructure or risk-policy changes. Phases 03–19 remain locked.
- If no substantive project work occurred, a brief closeout entry may record that fact rather than manufacture a transcript.

## Trading safety
- No paper or live trading/execution is authorised. A paper simulator is a future proposed capability only. Any paper or live execution requires separate explicit owner approval and its own gates; no real-money credentials or exchange account access are authorised.
- D-006's initial 0.5% per-trade risk target and D-007's 1:3 net reward/risk research objective apply only to the initial crypto-perpetual policy. D-006's equity denominator remains unresolved; these values are not approved for other domains.
- D-008's 10% UTC day-start equity hard daily-loss boundary (realised plus unrealised) and 24-hour cooldown apply only to the initial crypto-perpetual policy. Preserve the accepted value; its capital-flow, valuation and multi-currency semantics remain open. It is an outer boundary, not a normal risk target or complete risk system.
- The 10% boundary is an emergency ceiling, not a normal risk budget. Earlier warning/suspension thresholds and portfolio limits remain research/design questions; no paper execution is authorised.
- Unknown regime, stale/incomplete data, failed reconciliation, unavailable risk service or ambiguous state means no new trade.
- Risk, permissions, progression gates and execution invariants are deterministic and independently enforced.
- AI cannot edit its own limits, gate thresholds, permissions, kill switches or execution rules.

## Research data handling
- Never commit raw market-data archives, private exchange/account data or secrets to the repository.
- Research workflows may retain only manifests, hashes, validation summaries and small reproducibility metadata as CI artifacts.
- Raw data cleanup must be a separate unconditional workflow step (for example, GitHub Actions if: always()) that executes before artifact upload, so a failed test/assertion cannot bypass cleanup.
- Keep artifact retention short and explicit (default maximum three days for temporary research evidence). Record any accidental raw-data artifact exposure, expiry and corrective action in the audit log; never claim deletion unless verified.

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
