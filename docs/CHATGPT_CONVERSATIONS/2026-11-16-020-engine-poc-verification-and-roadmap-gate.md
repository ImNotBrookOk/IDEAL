# IDEAL Conversation Record 020 — Engine POC Verification and Roadmap Gate

**Date:** 16 November 2026  
**Scope:** Verify the latest multi-currency margin/funding test, confirm current engine POC status, preserve the Phase 01/02 implementation gate, and update the infrastructure audit.  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Branch:** `main`  
**Status:** Latest POC CI jobs verified successful; 79-test result is recorded on the roadmap and POC notes. Infrastructure audit synchronized. No engine adoption or runtime implementation approved by this record.

## Available user-visible transcript

### User
> Ok just test this last part. If it works lets start here and implement the engine built for our needs. And then well move on to testing the other parts of new sections because we have spent an entire day on just one engine. We have a lot to cover. Make sure to keep to the road map. Update all documents and audits. Lets go

### Assistant
We will continue from the existing IDEAL roadmap, not restart the research or revisit completed sections.

I have recovered the project state and verified that the GitHub repository is accessible:

- Repository: [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)
- Branch: `main`
- Current phase: Phase 01 — Open-source and infrastructure research.
- Next phase: Phase 02 — Architecture and contracts.
- Engine under investigation: NautilusTrader, pinned to `2.0.0rc9` for the proof of concept.

One important distinction: the engine has not yet been approved for adoption. We are testing whether it meets IDEAL's actual requirements before making that decision.

The existing roadmap contains substantial recorded research, including liquidation behaviour, execution realism, order amendments, funding, multi-currency accounts and deterministic recovery.

### Assistant
## Latest engine test — result

79 / 79 passed in the latest recorded CI verification.

The latest completed test specifically covers multi-currency margin funding:

- Inverse BTCJPY funding debited in BTC.
- Linear BTCUSDT funding debited in USDT.
- USD balance remained unchanged.
- Both positions remained open and correctly accounted for.
- Native-currency settlement succeeded without FX conversion instruments.
- Both x86_64 and ARM64 jobs completed successfully.

Exact funding debits: `0.00016667 BTC` and `0.60000000 USDT`.

The test is recorded in [CI run 43760637330](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43760637330).

This verifies the tested native-currency settlement scenario only. It does not prove unified cross-collateral accounting, currency haircuts, consolidated portfolio equity or exchange-equivalent liquidation.

### Assistant
## Roadmap decision

The implementation gate remains intact. The sequence is:

1. Finish remaining engine and account-model verification.
2. Complete Phase 01 infrastructure, licensing, empirical-data and engine-selection audits.
3. Complete Phase 02 architecture and interface contracts.
4. Obtain the implementation gate and begin the IDEAL-specific engine integration.
5. Test each component independently and in the integrated system.

The distinction is preserved between using NautilusTrader as a simulation foundation and building IDEAL's deterministic risk, accounting, strategy and execution-control layers around it.

## Operational audit log

### 1. Repository and state verification

- Retrieved the current GitHub repository metadata and confirmed the canonical repository is `ImNotBrookOk/IDEAL`, default branch `main`.
- Read `README.md`, `ROADMAP.md`, `RULES.md`, `REQUIREMENTS.md`, `ARCHITECTURE.md`, `TESTING.md`, `SKILLS.md`, `DECISIONS.md`, `docs/REPO_RESEARCH.md`, `docs/INFRASTRUCTURE_RESEARCH.md`, `research/nautilus_poc/README.md` and the execution-realism research notes.
- Confirmed Phase 01 remains IN PROGRESS and Phase 02 remains LOCKED.
- Confirmed D-012 permits continued Phase 01 research but does not authorize runtime integration, implementation, exchange/account access, paper/live execution, risk changes or paid infrastructure.
- Confirmed the POC remains isolated research code and NautilusTrader remains an unapproved candidate, not an adopted runtime dependency.

### 2. Latest CI verification

- Inspected GitHub Actions run [43760637330](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43760637330).
- Both jobs completed successfully: `POC (aarch64)` and `POC (x86_64)`.
- Both jobs completed dependency installation, exact engine-version verification, isolated POC tests and the informational SQLite benchmark step.
- The POC README and roadmap record 79 passing tests on both architectures using Ubuntu 24.04 / Python 3.14.10 and exact `nautilus_trader==2.0.0rc9`.
- Reviewed `test_multi_currency_funding.py`: the fixture compares a no-funding baseline with a funded run in a margin account configured with `base_currency=None`, pre-seeded USD/BTC/USDT balances, an inverse BTCJPY contract and a linear BTCUSDT contract. It asserts native-currency funding deltas and unchanged USD.
- This CI evidence is not an empirical venue calibration, actual Oracle A1 benchmark, production integration or exchange-equivalence proof.

### 3. Documentation update

- Found `docs/INFRASTRUCTURE_RESEARCH.md` still described the older 71-test result.
- Updated its POC compatibility statement to 79 tests on x86_64 and ARM64 and linked CI run 43760637330.
- Commit: [b3bae7f5c0224b2783c21ee89761afdf1cc41766](https://github.com/ImNotBrookOk/IDEAL/commit/b3bae7f5c0224b2783c21ee89761afdf1cc41766).
- The roadmap, POC README and execution-realism matrix already contained the 79-test result and multi-currency limitations; no duplicate edits were made.
- No code, dependency, runtime configuration, exchange adapter or risk control was changed.

### 4. Findings and limitations preserved

The test confirms that the pinned simulator can retain native-currency funding adjustments for the two tested contracts in a no-base-currency margin account. Portfolio equity is returned as a per-currency map. It does not establish a consolidated reporting-currency equity figure, unified cross-collateral offsets, collateral haircuts, exchange-specific margin tiers or liquidation behaviour.

Other Phase 01 blockers remain, including venue selection, representative historical L2/trade/fill data for empirical impact calibration, venue-specific amendment priority, multi-currency equity/collateral/liquidation analysis, journal runtime integration and backup/restore, actual free-worker capacity/performance, component pin/licence review and the final component selection matrix.

### 5. Approval boundary and next step

The user's conditional request to begin implementing the engine after this test is recorded. However, the current roadmap and D-012 still require Phase 01 completion, Phase 02 architecture/contracts and the corresponding approval gate before runtime implementation. This record does not silently supersede those controls.

**Current state:** Phase 01 remains IN PROGRESS; Phase 02 remains LOCKED; NautilusTrader remains a research candidate; no production engine adoption or runtime implementation has occurred.

**Proposed next task:** Continue the next unresolved Phase 01 account-model research item, focusing on multi-currency equity aggregation, collateral conversion and liquidation boundaries, while progressing the remaining Phase 01 blockers in roadmap order.

**Owner approval:** Required before Phase 02 and runtime implementation under the current decision register.
