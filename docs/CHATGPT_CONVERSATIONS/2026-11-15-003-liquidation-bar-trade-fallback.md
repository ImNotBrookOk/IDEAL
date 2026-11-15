# IDEAL Conversation Record 2026-11-15-003

- **Date:** 2026-11-15 (New Zealand)
- **Topic:** Bar-only and trade-only liquidation valuation; liquidation close behaviour with an empty order book
- **Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)
- **Record status:** Recorded on `main`; research change proposed in PR #6, not merged
- **Approved task:** Continue Phase 01 with deterministic tests for bar-only/trade-only liquidation valuation and the close path when no executable quote book exists
- **Scope:** Isolated NautilusTrader POC only. No IDEAL runtime integration or trading permission changes.

## 1. User-visible transcript

This is the complete user-visible transcript available for this conversation.

**User:**

> Yes lets do it

**Assistant (scope confirmation):**

> Approved task scope: **bar-only and trade-only liquidation valuation, plus whether the liquidation close path can execute without an order-book quote**.
>
> I’ll keep this inside `research/nautilus_poc/`, use deterministic synthetic fixtures, and test the pinned `2.0.0rc9` engine. No IDEAL runtime integration, exchange access, trading permissions or paid services are in scope.

**Assistant (conversation closeout):**

> ## Phase 01 liquidation fallback research — completed for this gate
>
> **Result:** [PR #6 — Test bar/trade liquidation fallback and empty-book close path](https://github.com/ImNotBrookOk/IDEAL/pull/6)
>
> ### Findings
>
> 1. **Bar-only data:** The engine uses the latest valid bar close as a liquidation valuation fallback. With L1 bar execution enabled, it also creates synthetic market updates from the bar, which can provide the bid needed to execute the close. This is simulated liquidity, not a real exchange quote.
> 2. **Trade-only data with an empty L2 book:** The latest trade price can trigger liquidation. However, when the L2 book has been cleared and no executable best bid exists, the engine skips the synthetic close. The position remains open despite a maintenance-margin breach.
> 3. **Configuration matters:** L1 trade execution can derive synthetic bid/ask state from trades. Trade-only data does not automatically mean the order book is empty.
>
> **Verification:** [GitHub Actions run 43693632643](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43693632643) — **27 passed in 0.19s**, using `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 and Python 3.14.
>
> The research notes and roadmap have been updated. The code remains isolated under `research/nautilus_poc/`.
>
> ### Current state
>
> - PR #6 is open and GitHub reports it is mergeable.
> - No merge has been performed.
> - Phase 01 remains IN PROGRESS; Phase 02 remains LOCKED.
> - No runtime dependency, exchange account, API credential, paper/live order, risk setting or paid service was introduced.
>
> **One proposed next step:** Review PR #6 and approve merging it or request revisions. I will not merge it or start the next research gate until you explicitly respond.

## 2. Operational audit log

1. Read the installed test-driven-development skill before changing behaviour/tests and the code-review-and-quality skill before preparing the PR.
2. Inspected the existing POC liquidation tests, engine integration tests, order lifecycle tests, funding tests, POC README, pinned requirements and GitHub Actions workflow.
3. Confirmed the exact POC pin remained `nautilus_trader==2.0.0rc9`; no dependency version was changed.
4. Created branch `research/liquidation-bar-trade-fallback` from main commit `4c3869f1ec2a961ac6097a7ac7be07e5248d5a23`.
5. Added `research/nautilus_poc/test_liquidation_bar_trade.py` with deterministic synthetic fixtures:
   - Bar-only LAST feed, L1 book, `bar_execution=True`.
   - L2 ask snapshot to open a long, explicit L2 book clear, then adverse LAST TradeTick with `trade_execution=False`.
   - Independent inverse PnL oracle, account/maintenance values, engine log assertions and deterministic replay.
6. Audited the exact upstream `v2.0.0rc9` source. Findings and line references are documented in the POC README and summarised in section 3 below.
7. Iterated on failed tests rather than masking them:
   - Initial L1 trade-only fixture unexpectedly generated synthetic L1 bid/ask state and allowed a close. This exposed a configuration distinction; the no-book case was redesigned using L2.
   - Initial L2 run failed because the engine requires order-book data for an L2 venue. The fixture now seeds an L2 ask, then explicitly clears the book.
   - An enum value could not be passed as an integer flags field; the fixture now passes the documented F_LAST wire value.
   - The first empty-book log assertion used `capsys`, which did not capture native Rust output. It was changed to pytest `capfd`, which captures file-descriptor output.
   - Bar execution initially supplied insufficient synthetic liquidity for the full close; the deterministic bar fixture volume was increased to cover the order.
8. Final exact-head CI run [43693632643](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43693632643), commit `1d1fc394e24e4f1a38cf9c6e420956a60b9eb0ca`: **27 passed in 0.19s**. The duplicate push/PR workflow run [43693637026](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43693637026) also completed successfully.
9. Updated `research/nautilus_poc/README.md` with coverage, source audit, limitations and verification evidence.
10. Updated `ROADMAP.md` with the new Phase 01 evidence and remaining gates. Phase 01 remains IN PROGRESS; Phase 02 remains LOCKED.
11. Opened [PR #6](https://github.com/ImNotBrookOk/IDEAL/pull/6), base `main`, head `research/liquidation-bar-trade-fallback`. GitHub reports PR state OPEN and mergeable TRUE. No merge was performed.
12. No IDEAL runtime code, live/paper trading permissions, risk limits, exchange adapters, credentials, accounts, billing or paid services were changed.

## 3. Source-level findings

Exact upstream sources pinned to NautilusTrader `v2.0.0rc9`:

- [SimulatedExchange::process_liquidations, account equity and trigger](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/backtest/src/exchange.rs#L1995-L2060).
- [liquidation_unrealized_pnl valuation precedence](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/backtest/src/exchange.rs#L2381-L2458): mark price → position-side quote → last trade → latest valid bar close. For a long, the quote side is bid; for a short, ask.
- [Matching engine bar processing](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L1922-L2070) and [trade-tick processing](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L2403-L2495).
- [best_bid_price accessor](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L1356-L1365) and [liquidate_open_positions executable-side pre-check](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs#L2939-L3025).

### Observed test outcomes

**Bar-only case**
- No QuoteTick or TradeTick is supplied.
- External LAST bars are used.
- The L1 bar execution path creates synthetic market updates from the bar.
- The bar close triggers liquidation and the bar-generated synthetic bid executes the close.
- This proves the simulated engine path works under its configured bar execution model; it does not establish real exchange liquidity.

**Trade-only, empty L2 case**
- An L2 ask snapshot opens the inverse long.
- An explicit CLEAR delta empties the L2 book.
- A subsequent adverse TradeTick updates LAST; trade execution is disabled so it does not rebuild the empty book.
- The independent inverse PnL oracle at 40,000 → 20,000 is -250 BTC.
- Account balance is 0.8125 BTC; maintenance margin is 0.0875 BTC. Equity is therefore deeply below maintenance.
- The test asserts the engine logs both the liquidation trigger and the no-executable-price skip.
- No liquidation fill occurs; the position remains open because there is no best bid.

**Configuration caveat**
- An initial L1 `trade_execution=True` experiment showed trade ticks can create synthetic L1 bid/ask state and allow the close.
- Therefore “trade-only” and “no executable order book” are not interchangeable without specifying book type and execution settings.

## 4. Changed files and evidence

PR #6 changes exactly three files:

- `research/nautilus_poc/test_liquidation_bar_trade.py` — new deterministic tests.
- `research/nautilus_poc/README.md` — research findings and exact source references.
- `ROADMAP.md` — Phase 01 evidence and remaining research gates.

PR: https://github.com/ImNotBrookOk/IDEAL/pull/6

Final test evidence: https://github.com/ImNotBrookOk/IDEAL/actions/runs/43693632643

PR head commit at the time of this record: `6c7e3591dca93d6384200864863e0eef6cdd0524`.

## 5. Approval boundary and current state

- **Research gate:** completed and documented in the proposed PR.
- **PR #6:** OPEN, mergeable; owner review required.
- **Merge:** not performed.
- **Phase 01:** IN PROGRESS.
- **Phase 02:** LOCKED.
- **Engine adoption:** not decided.
- **Exchange/account access:** not authorised.
- **Paper/live execution:** not authorised.
- **Paid infrastructure/billing:** not authorised.

**One proposed next step:** Owner reviews PR #6 and either approves merging it or requests revisions. Wait for explicit owner response; do not start another research task or merge the PR before that response.


## 6. Post-commit evidence addendum — 2026-11-15

This addendum records the audit-record publication and index update. It supplements the conversation record without rewriting the transcript.

- Conversation record creation commit: [`3ddec3fc9aefb93f1257276d00a665fa0bf5a0e1`](https://github.com/ImNotBrookOk/IDEAL/commit/3ddec3fc9aefb93f1257276d00a665fa0bf5a0e1).
- Audit index update commit: [`034452d3f3bcc3d9066752181b47c4d45a55e892`](https://github.com/ImNotBrookOk/IDEAL/commit/034452d3f3bcc3d9066752181b47c4d45a55e892).
- Final conversation record read-back verified after publication.
- PR #6 remains open and unmerged. No merge action was performed.
- No automated tests were required or run for these Markdown-only audit updates.


## 7. Owner direction and merge closeout — 2026-11-15

**User:**

> Do what you think is best

**Interpretation and decision:** This response delegated the pending choice between merging PR #6 and requesting revisions. After rechecking the PR head, successful CI job, mergeability and complete patch, no merge-blocking issue was identified. The change was limited to the approved research scope and its documentation. The PR was therefore squash-merged.

- Pre-merge PR state: OPEN; mergeable=true; head SHA 6c7e3591dca93d6384200864863e0eef6cdd0524.
- CI run [43693632643](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43693632643): successful; the research-poc job completed successfully.
- Review: three files only; isolated POC test, research README and roadmap. No runtime execution path, exchange connectivity, credentials, risk parameters, permissions, or billing changes.
- Merge method: squash.
- Merge result: successful; merge commit d04af3de4308b096590908dec16daf2dc55c726a.
- PR: [#6](https://github.com/ImNotBrookOk/IDEAL/pull/6).

**Post-merge governance state:** This merge closes only the approved research change. Phase 01 remains IN PROGRESS, Phase 02 remains LOCKED, and no subsequent research task or implementation work is authorised by this merge. Await the owner's next instruction before proceeding.
