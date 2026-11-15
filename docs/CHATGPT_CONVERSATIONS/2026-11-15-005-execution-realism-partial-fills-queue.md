# IDEAL Conversation Record 005 — Execution Realism Research

**Date:** 15 November 2026  
**Scope:** Phase 01 research — partial fills, queue position, liquidity consumption, competing orders and slippage  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** PR #9 merged; the tested L1 sub-scenarios are evidenced. The wider L2/L3 execution-realism gate remains IN PROGRESS.

## Available user-visible transcript

### User
> Yes lets continue. But also im checking you are updating the Documents and roadmap with your finds? At least documenting this process so absolutely everything can be audited later on? If yes. Then lets continue

### Assistant
Yes. Documentation and auditability are part of the work, not an afterthought.

For each Phase 01 research gate, I will maintain:
- **Research evidence:** what was inspected, source versions/commits, findings and limitations.
- **Decision records:** what the evidence means for IDEAL, including decisions deferred and why.
- **Roadmap and research register:** gate status, remaining work, dependencies and next steps.
- **Tests and CI evidence:** exact environment, test results, failures, corrections and final passing run.
- **Conversation audit record:** scope, actions, review, PR/commit references and verification that the record was committed and can be read back.

The existing conversation-audit protocol and D-012 governance are intended to make this traceable. I’ll verify the current documents before extending them, rather than assume they are complete.

### Assistant
I verified the repository’s current `ROADMAP.md`, `RULES.md`, `DECISIONS.md` and POC research notes. The roadmap already lists partial fills, queue position and competing-order liquidity as the next unfinished gate. The audit rules also require evidence and commit references before a task is marked verified.

One documentation gap is worth tightening: the roadmap has a useful running history, but the next research gate should also have its own focused evidence record, with exact source locations, test scenarios, limitations and merge references. I’ll add that as part of this gate, not just update a status line.

### Assistant
The first CI run exposed a test-harness issue, not an engine defect: NautilusTrader’s `Strategy` wrapper does not accept those constructor arguments in this release. I recorded the failure and corrected the fixture to initialise its parameters after construction. The one-tick slippage test already passed in that first run; the corrected queue and competing-order tests are now being rechecked.

No production trading logic or dependencies have been changed.

### Assistant
The research is now recorded in a dedicated [execution realism report](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/execution_realism_matrix.md), and I’ve updated both the [roadmap](https://github.com/ImNotBrookOk/IDEAL/blob/main/ROADMAP.md) and POC README.

The current evidence is **33 passing tests**, including the three new execution tests. I have deliberately not marked the whole execution-realism gate complete: L2 multi-level depth walking and L3 order-level queue tracking still need IDEAL-side reproduction. Upstream source tests are useful evidence, but they are not substitutes for our own tests.

## Operational audit log

### 1. Governance and repository inspection

- Re-read `RULES.md`, `DECISIONS.md`, `ROADMAP.md`, `docs/REPO_RESEARCH.md`, and `research/nautilus_poc/README.md` on main before making changes.
- Confirmed the Phase 01 standing authorization and automatic research-PR merge conditions under D-012: green CI, five-axis review, scope verification and unchanged-head confirmation. Phase 02, runtime integration, exchange/account access, trading, risk changes and paid services remain outside the authorization.
- Confirmed the roadmap's next unfinished task was execution realism under partial fills, queue position, liquidity consumption and competing orders.
- Read the installed test-driven-development skill before changing tests. The test plan was to reproduce observable behavior using the exact pinned package and keep changes inside the isolated POC.

### 2. Pinned upstream source inspection

Inspected NautilusTrader tag `v2.0.0rc9`, not the moving default branch.

| Upstream file | Blob SHA | Evidence inspected |
|---|---|---|
| `crates/execution/src/matching_engine/mod.rs` | `d917ed1185f885593ddbf3f0faba49457663ffe5` | Per-level liquidity consumption, trade-consumption seeding, queue snapshots, queue depletion, queue fill quantity, L2/L3 queue rebasing and L1 quote adjustments |
| `crates/execution/src/matching_engine/config.rs` | `2aad9a18dcfd4e36372e0fdaa51c6dc8d663a7dc` | Defaults: trade execution on; liquidity consumption and queue tracking off |
| `crates/execution/src/matching_engine/tests.rs` | `1bb906bcc57d119b165123a5346ea40798f80804` | Upstream L1 queue, shared trade-budget and L2 snapshot/depth queue tests |
| `docs/concepts/backtesting/fill-prices-and-matching.md` | `c817edd12b4efda701c55a88010febad58736c94` | L1 residual one-tick rule, L2/L3 depth walking, book immutability and liquidity consumption |
| `docs/concepts/backtesting/fill-models.md` | `c6f3742d0df0cc5da0c96488d6d53f04743bff44` | Fill-model defaults, probabilistic one-tick L1 slippage, synthetic books and model limitations |
| `docs/concepts/backtesting/trade-execution.md` | `3720cb4724170973f751e4b5753c6d6407b1b96c` | Queue lifecycle, aggressor-side behavior, L1/L2/L3 tracking limitations and modification policies |

Key source links:
- [Matching-engine consumption and queue implementation](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/crates/execution/src/matching_engine/mod.rs)
- [Queue/trade execution documentation](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/docs/concepts/backtesting/trade-execution.md)
- [Fill price and matching rules](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/docs/concepts/backtesting/fill-prices-and-matching.md)
- [Fill model documentation](https://github.com/nautechsystems/nautilus_trader/blob/v2.0.0rc9/docs/concepts/backtesting/fill-models.md)

A preliminary Acumen current-state query did not return relevant NautilusTrader-specific information and was not used as evidence.

### 3. Findings recorded

- L2/L3 market-style orders walk crossed depth and can partially fill when displayed liquidity is insufficient. L1 has a separate deterministic residual one-tick fill rule.
- Historical books are immutable. `liquidity_consumption=True` prevents simulated orders from reusing consumed displayed quantity; trade-driven fills share a trade-volume budget when enabled.
- `queue_position=True` with `trade_execution=True` estimates displayed quantity ahead for resting LIMIT orders. Correct-side aggressor trades reduce the queue; only excess trade volume can fill the order.
- L2 aggregate queue estimates are rebased on book updates/snapshots. L3 MBO can track displayed order IDs. Hidden orders and venue-specific priority are not knowable from historical data.
- `NO_AGGRESSOR` can reduce both sides' queues and may create optimistic fills.
- `prob_slippage` is a one-tick probabilistic adjustment for L1 fills. L2/L3 price impact is determined by depth. Synthetic competition-aware/tiered fill models are model constants, not empirical liquidity.
- The exact feature defaults matter: trade execution defaults on; liquidity consumption and queue position default off.
- These behaviors are simulator semantics, not proof of Binance, Bybit, OKX or any other venue's matching parity.

### 4. IDEAL POC test work and CI history

New test file: `research/nautilus_poc/test_execution.py`.

Three scenarios were added:
1. **Queue-ahead depletion:** 10 displayed units ahead; a 12-unit SELL trade clears the queue and fills 2 units, then a later 3-unit SELL trade fills the remaining 3.
2. **Competing-order trade budget:** two 2-unit resting BUY orders share one 3-unit SELL trade print; with liquidity consumption enabled and queue tracking disabled to isolate consumption, aggregate fills cannot exceed 3.
3. **L1 slippage:** a BUY market order at ask 40,001.0 with 0.1 tick size and `prob_slippage=1.0` fills at 40,001.1.

Test and CI chronology:
- Initial test file commit: `0bc8c5c51d601af3f88b9fb72354fe578deb32ac`.
- Initial push/PR CI runs [43696082287](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43696082287) and [43696109287](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43696109287) failed: **2 failed, 31 passed**. Both failures were test-fixture construction errors: `Strategy.__new__()` did not accept the two positional parameters.
- Corrected fixture commit: `ed8801018b5daa6da346b306d72ca2286ad74525`. Strategy instances are now constructed without positional parameters; scenario values are assigned afterwards.
- Corrected test-commit CI runs [43696169232](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43696169232) and [43696163846](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43696163846): both passed, **33 passed in 0.18s**.
- Final PR-head CI runs [43696581007](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43696581007) and [43696577494](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43696577494): both passed. The final push run reported **33 passed in 0.16s**.
- CI verified exact `nautilus_trader==2.0.0rc9`, Ubuntu 24.04 x86_64 and Python 3.14.
- The original failure was recorded and corrected; it was not misreported as a simulator defect.

### 5. Documentation and PR

The PR updated exactly four files:
- `research/nautilus_poc/test_execution.py`
- `research/nautilus_poc/execution_realism_matrix.md`
- `research/nautilus_poc/README.md`
- `ROADMAP.md`

The dedicated execution realism matrix records source references, behavior, test fixtures, CI evidence, limitations and current decisions. The roadmap and POC README now link the report and state explicitly that L2/L3 POC reproduction remains open.

PR #9: [Test partial fills, queue position and competing liquidity](https://github.com/ImNotBrookOk/IDEAL/pull/9)
- Final PR head SHA: `2537d1ab4e4ef24a2a92300a0d82d271205e52ee`.
- Changed files: 4; additions: 352; deletions: 4.
- Five-axis review:
  - **Correctness:** tests match the documented pinned L1 behaviors and pass against the exact wheel.
  - **Readability:** descriptive tests and isolated fixture helpers; no merge-blocking complexity.
  - **Architecture:** changes stay in the research POC and documentation; no production imports or runtime integration.
  - **Security:** synthetic local fixtures only; no secrets, credentials, external market-data calls or exchange connectivity.
  - **Performance:** 33 tests complete in 0.16s in final-head CI; no material resource concern.
- Scope review: no production behavior, dependency, exchange adapter, account access, paper/live trading, risk setting or paid service changed.
- Final head was checked immediately before merge and matched the reviewed SHA.
- Automatically squash-merged under D-012.
- Merge commit: `2d7994c56a34fe66eeafabd4fb9b539c184dfff9`.
- PR #9 subsequently verified closed with `merged=true`.
- Main-branch readback verified the roadmap, POC README, execution realism report and test file are present.

## Current project state

- Phase 01 remains **IN PROGRESS**.
- The IDEAL POC now reproduces selected L1 queue depletion, partial trade-driven fills, shared trade-size consumption across competing limit orders and one-tick probabilistic slippage.
- L2 multi-level depth walking, finite-depth competing market orders, L2 queue snapshot rebasing and L3 MBO order-ID queue tracking are source-audited but remain unverified in IDEAL's Python POC.
- Queue cancellation/amendment priority edge cases and empirical market-impact calibration remain open.
- Phase 02 remains LOCKED. No exchange is selected. No account, testnet, paper or live trading has been connected or authorised. No production runtime integration or new dependency was added.

## Next proposed step

Continue Phase 01 by building IDEAL-side L2 tests for multi-level depth walking, partial fills and competing orders against finite depth, followed by L2 snapshot rebasing and L3 MBO queue tracking. Then address cancellation/amendment priority and market-impact calibration.

**Owner approval:** Not required for this bounded Phase 01 research under D-012. Explicit owner approval remains required before Phase 02 or any separately restricted activity.
