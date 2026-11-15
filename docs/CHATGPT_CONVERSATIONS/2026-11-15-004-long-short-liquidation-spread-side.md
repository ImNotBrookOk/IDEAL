# IDEAL Conversation Record 2026-11-15-004

- **Date:** 2026-11-15 (New Zealand)
- **Topic:** Standing Phase 01 authorisation; long/short liquidation quote-side selection under spread
- **Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)
- **Record status:** Committed directly to `main`; PR #7 squash-merged
- **Owner authorisation:** Continue Phase 01 research gates in roadmap order; automatically merge qualifying research PRs after green CI, five-axis review, scope verification and unchanged-head confirmation. Conversation records are committed directly to main and read back. Phase 02 and all trading/runtime/cost permissions remain excluded.

## 1. User-visible transcript

This record preserves the complete user-visible transcript available for this conversation, including the prior pending-merge instruction and the current standing-authorisation instruction.

**User:**

> Do what you think is best

**Assistant:**

> ## PR #6 merged successfully
>
> **15 November 2026**
>
> I chose to merge rather than request revisions. The PR was narrowly scoped, the tests passed, and the research findings were documented accurately.
>
> **Merge details**
>
> - PR: [#6 — Test bar/trade liquidation fallback and empty-book close path](https://github.com/ImNotBrookOk/IDEAL/pull/6)
> - Merge method: Squash
> - Merge commit: `d04af3de4308b096590908dec16daf2dc55c726a`
> - CI: **27 tests passed**
> - Changed files: 3
> - No merge-blocking issues identified.
>
> **Audit record updated and verified**
>
> [2026-11-15 conversation and operational audit](https://github.com/ImNotBrookOk/IDEAL/blob/main/docs/CHATGPT_CONVERSATIONS/2026-11-15-003-liquidation-bar-trade-fallback.md)
>
> Audit commit: `dec2dcd512e5c932035a79301b2ce5c830d9948d`
>
> ## Current IDEAL status
>
> | Area | Status |
> |---|---|
> | Phase 01 — Research | IN PROGRESS |
> | Phase 02 | LOCKED |
> | NautilusTrader adoption | Not approved |
> | Exchange/account connection | Not authorised |
> | Paper/live execution | Not authorised |
> | Paid infrastructure | Not authorised |
>
> **My recommendation:** Keep working through Phase 01's remaining liquidation and execution research before selecting an engine or beginning implementation. The empty-order-book result is particularly important: a system must never assume that detecting a liquidation means it can actually execute the close.
>
> I'll stop here. No further project changes or research tasks until you give the next instruction.

**User:**

> Yes lets test it until we are fully satisfied. Keep doing what your doing. And always auto merge our conversation. I trust you are recording it all and merging automatically.

**Assistant:**

> Confirmed. I'll treat this as standing authorisation to continue the approved Phase 01 research programme without asking you to approve every individual research gate.
>
> I'll also automate the GitHub closeout: record each conversation and its operational evidence, run the relevant tests and review, then merge completed research PRs when the quality checks pass. If a change fails verification or exposes a material risk, I'll stop and report it rather than merge it.
>
> This does **not** authorise live trading, exchange-account connections, changes to risk limits, paid infrastructure, or runtime integration. Those remain separate decisions.

**Assistant:**

> ## Next liquidation gate: long/short spread handling
>
> The pinned NautilusTrader source confirms the valuation rule:
>
> - **Long positions:** use the bid.
> - **Short positions:** use the ask.
>
> I've added tests designed to catch the wrong-side bug, not merely confirm that a position can be closed. A position enters at 40,000; the next quote is 39,800 bid / 40,200 ask. The adverse side should trigger liquidation, while the opposite side would show a favourable result.
>
> The first CI attempt exposed a test-strategy constructor incompatibility. I corrected it rather than weakening the assertions. The corrected full suite passed **30 tests**; CI is now also running against the final documentation-updated PR head.

## 2. Owner direction and governance changes

The owner granted a standing, bounded authorisation for Phase 01 research work. The previous per-gate approval requirement was updated in the repository rather than silently ignored.

Direct-to-main governance commits:

- `RULES.md`: `516f1b74a389ad60311cd33fd05dd82779346b90`
- `DECISIONS.md` (D-012): `3d6f9188e45e84ed9a29a9eeeaeb88599f5f7c6f`
- `docs/CHATGPT_CONVERSATIONS/README.md`: `fadb4668bbe9ec25c23aa88f0d635c9ab9cb6e6b`

D-012 records:
- Continue Phase 01 gates in roadmap order without per-gate approval.
- Automatically squash-merge qualifying research PRs only after green CI, five-axis review, scope verification and unchanged-head confirmation.
- Commit each conversation record and index update directly to main; verify by reading back.
- Stop at Phase 01 completion for explicit owner approval before Phase 02.
- No runtime integration, exchange/account access, paper/live execution, risk changes, paid services or billing are authorised.

## 3. Research task and source audit

**Task:** Verify long/short liquidation valuation when the bid and ask differ, and confirm the executable close side.

The exact upstream source at NautilusTrader tag `v2.0.0rc9` was fetched and inspected. The `liquidation_unrealized_pnl` helper selects:
- `PriceType::Bid` for `PositionSide::Long`.
- `PriceType::Ask` for `PositionSide::Short`.

It then uses the selected quote side after checking for a valid mark price, and before falling back to last trade and bar close. Pinned source reference: [exchange.rs liquidation valuation helper](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/backtest/src/exchange.rs#L2381-L2458).

## 4. Implementation and test evidence

Branch: `research/liquidation-spread-side-selection`

The test fixture:
- Opens a position at 40,000 with an initially equal bid/ask.
- Supplies a later quote of bid 39,800 and ask 40,200.
- For a long, the bid is adverse and ask is favourable.
- For a short, the ask is adverse and bid is favourable.
- Asserts the long closes at 39,800 and the short closes at 40,200.
- Replays both cases and asserts identical results.

The fixture makes an incorrect quote-side choice observable: the wrong side is favourable and should not cause the maintenance breach.

**Failed test attempt and correction (recorded, not hidden):**
- Initial CI run [43694492024](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43694492024) failed 3 new tests, with 27 existing tests passing.
- Cause: NautilusTrader's Strategy `__new__` rejected a `side` keyword argument.
- Correction: instantiate the strategy with no arguments and set its directional side before registration. The strategy was also renamed from `BuyInverseOnce` to `DirectionalInversePosition` to reflect both directions.
- The assertions were retained; no test was skipped or weakened.

**Final-head CI:**
- [GitHub Actions run 43694663624](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43694663624)
- **30 passed in 0.13s**
- Ubuntu 24.04 x86_64, Python 3.14
- Exact package: `nautilus_trader==2.0.0rc9`
- Final tested PR head: `1938dc38c324327d9fc887ffba0ac814ad06d6ea`
- Workflow job and all steps completed successfully.

## 5. Review and merge

Five-axis review:
- **Correctness:** Long and short tests distinguish the adverse quote side from the favourable opposite side, assert close prices, and verify deterministic replay.
- **Readability:** Directional strategy name and test names express the behaviour; fixtures are deterministic.
- **Architecture:** Research-only tests; no runtime dependency or module boundary changes.
- **Security:** No credentials, secrets, exchange connection or external data input added.
- **Performance:** Three additional fast tests; full suite completed in 0.13s.

PR #7 changed exactly three files:
- `research/nautilus_poc/test_liquidation.py`
- `research/nautilus_poc/README.md`
- `ROADMAP.md`

[PR #7 — Verify long and short liquidation quote-side selection](https://github.com/ImNotBrookOk/IDEAL/pull/7)

- Pre-merge PR state: OPEN, mergeable.
- Final head SHA confirmed unchanged before merge: `1938dc38c324327d9fc887ffba0ac814ad06d6ea`.
- Merge method: squash.
- Merge result: successful.
- Merge commit: `85785eca0274d577a87ecb4f6f4b5457712dc1e9`.
- PR state verified after merge: CLOSED, merged=true.

After merge, the README and roadmap CI references were corrected to the final-head run [43694663624](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43694663624) in documentation commits:
- README: `2278c9e9059a3448cf432e2a5d0ea55d2478448e`
- Roadmap: `c617d5e06ac640dfb6689b3d8a2d20de62de9599`

## 6. Current project state

- Phase 01: IN PROGRESS.
- Phase 02: LOCKED.
- NautilusTrader adoption: not approved; current pin remains a pre-release research POC.
- No runtime integration, exchange account, API credentials, paper/live orders, risk changes, paid service or billing activation.
- Remaining Phase 01 research includes exchange-specific liquidation/recovery; partial fills, queue and liquidity consumption; slippage and stop/target ordering; funding missing-data and multi-position cases; canonical replay/restart; free-worker resource proof; stable pins/licence review; adapter assessment and final component selection.

## 7. Next step

Continue with the next Phase 01 research gate: exchange-specific liquidation mechanics and recovery behaviour, comparing candidate venues without selecting or connecting an exchange. The standing authorisation remains active for Phase 01 only. Stop for explicit owner approval before Phase 02 or any excluded activity.
