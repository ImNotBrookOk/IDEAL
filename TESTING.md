# IDEAL Testing and Verification

## Required task evidence
Every task must define acceptance criteria before implementation and record exact commands, environment, commit, test counts, failures and resolutions. Never infer success from a tool returning without error.

## Test layers
- Static analysis, formatting, type checks and dependency/security scans.
- Unit tests for pure calculations and state transitions.
- Property-based tests for invariants and boundary conditions.
- Component tests with deterministic fixtures.
- Contract tests between modules and exchange adapters.
- Integration tests across all previously verified dependencies.
- Regression tests for every previously discovered defect.
- Historical replay and deterministic reproducibility tests.
- End-to-end data → decision → risk → paper order → fill → ledger → lesson.
- Fault injection for stale/missing data, disconnects, rate limits, clock drift, partial fills, duplicate events, process restarts and storage failures.
- Security tests for secret exposure, untrusted payloads and strategy sandboxing.
- Long-duration paper soak tests before operational readiness.

## Trading-specific checks
- No look-ahead, survivorship or train/test leakage.
- Fees, spread, slippage, funding, latency and partial fills included.
- Correct candle boundaries, timezone handling and indicator warm-up.
- No duplicate orders from retries; idempotency and reconciliation required.
- Risk sizing and stop distance validated against equity, precision, tick/lot sizes and leverage.
- Daily loss includes realised and unrealised PnL and resets only at UTC day boundary.
- Cooldown persists across restarts.
- UNKNOWN regime or ineligible strategy produces no trade.
- Gate demotion revokes permissions while preserving history and lessons.
- AI failure or malformed output cannot bypass deterministic controls.

## Research artifact retention
- CI jobs must delete raw market-data files in a separate unconditional cleanup step before uploading artifacts.
- Cleanup must run even if retrieval, parsing, reconstruction or acceptance assertions fail.
- Upload only hashes, manifests and small audit summaries; do not upload raw market data.
- Use explicit short retention for temporary research artifacts and record artifact IDs/expiry in the audit log.
- Test the failure path: force an acceptance assertion to fail and verify that the resulting artifact contains no raw archives.

## Evidence standard
A test is VERIFIED only when its command was actually run and its output recorded. Report skipped tests explicitly. No paper/live readiness claim without full end-to-end evidence and an approved operational checklist.

### 16 November 2026 — cleanup failure-path verification

The three-day OKX alignment workflow [#43777626875](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43777626875) intentionally failed the original 98% side-consistency acceptance screen on 13 November, but its separate unconditional cleanup step completed before artifact upload. Resulting artifact 14187715114 was only 3,348 bytes and contained summaries/manifests, not raw archives. This verifies the corrected failure path. The earlier artifact 14187155843 remains a documented one-off cleanup defect and expires 18 November 2026 at 23:55 UTC.


## Risk-weighted acceptance policy (16 November 2026)

Classify evidence by failure consequence rather than applying one pass percentage to every test:

- **Hard correctness and safety invariants:** require 100% pass. Examples include valid/non-crossed book state, monotonic event ordering where required, deterministic risk limits, order validation, idempotency, ledger reconciliation and fail-closed behaviour. A percentage pass rate is not acceptable for these controls.
- **Strong component evidence:** quality diagnostics at or above 98% are preferred, but the exact metric and sample coverage still matter.
- **Conditional research evidence:** 95% to below 98% may be retained as a bounded research candidate when structural invariants pass and the residual error is measured.
- **Exploratory evidence:** 90% to below 95% may justify further research, but not production selection or execution claims.
- **Below 90%:** normally reject or isolate the component until the cause is understood.

These are evidence classifications, not universal pass/fail thresholds. Never average away a failing day or a critical subpopulation. Report per-day and per-regime results, denominators, missing observations and tail distributions. Do not silently discard failures.

For market-data freshness, preserve observation age and source-quality flags. A stale observation may remain useful for slower historical context, but it must be excluded or explicitly down-weighted for a model whose freshness budget it exceeds. A research-data classification does not establish queue position, fill fidelity, sequence continuity, live venue eligibility or paper/live readiness.

The 90% principle applies only to non-critical component-quality evidence. Risk controls, execution correctness, accounting and fail-closed behaviour remain hard gates.


## Seven-day OKX market-data freshness classification (16 November 2026)

The 7–13 November 2026 BTC-USDT-SWAP 400-level L2/trade alignment is classified as **conditional historical market-structure research data**, not execution-grade calibration data. The original strict screen passed 5/7 days and failed 7 Nov and 8 Nov; those results remain unchanged.

- 7 Nov's only unmatched trade timestamp is 2 ms before the first snapshot; exclude that one boundary row from BBO-dependent metrics, retain it in coverage diagnostics, and fail any later unmatched trade.
- 7 Nov p95 book age is 32 ms. 92.094% of aligned trades are <=20 ms old, 97.625% <=50 ms, 99.432% <=100 ms and 99.979% <=250 ms.
- 8 Nov has zero missing/invalid matches but 96.453% taker-side/preceding-BBO consistency; the mismatch is concentrated in <=10 ms book-age observations. This is a BBO sampling/event-order diagnostic, not proof of incorrect taker labels.
- Across 19,918,682 aligned trades, 97.726% are <=20 ms old, 99.525% <=50 ms, 99.924% <=100 ms and 99.995% <=250 ms. Daily maxima reach 475–519 ms.

Any downstream feature must declare its own maximum observation age, exclude or down-weight stale states, and preserve per-day source-quality flags. A 20 ms freshness budget excludes 7.906% of 7 Nov observations; it is not acceptable to silently use those stale states as current. The data does not establish exact cross-channel event ordering, FIFO queue position, passive-fill accuracy or exchange-equivalent execution. See `docs/HISTORICAL_L2_SAMPLE_VALIDATION.md` section 12.20 and audit checkpoint 034.


## Owner disposition — seven-day OKX research dataset (16 November 2026)

The owner accepts the 7–13 November 2026 OKX BTC-USDT-SWAP 400-level L2/trade sample for **conditional historical market-structure research** and directs that Phase 01 work continue without another rerun of the same seven-day test. The revalidation workflow [#43803546192](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43803546192) completed all calculations and unconditional cleanup, but the original strict screen remains 5/7 days passed and 2/7 failed. This owner disposition does not change those results or waive downstream freshness controls.

Retain 7 and 8 November as conditional-quality days, preserve the one 7 November initial-snapshot boundary trade, and enforce model-specific age budgets. The dataset is not execution-grade fill calibration and does not establish event ordering, queue position, passive-fill fidelity, sequence continuity or live readiness. Reopen this test only if a materially new source, schema, alignment method or requirement justifies it. See checkpoint 039.


## Scoped dependency and workflow security evidence (16 November 2026)

Workflow [#43807450930](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43807450930) generated universal hash-pinned Python 3.14 locks, installed the exact locked environments, generated CycloneDX SBOMs and ran pip-audit. The parser environment (orjson 3.11.6) and Nautilus POC environment (six packages) each returned zero known vulnerability records. The locks and SBOMs are retained on the research branch. Zizmor reported no findings across nine workflows in offline mode, with one suppressed finding; offline mode omits some checks. Treat this as scoped evidence, not full repository/product clearance. The parser pin is 3.11.6 because 3.11.3 is affected by CVE-2025-67221; 3.11.6 introduces MPL-2.0-covered source files, requiring licence review before external distribution. See checkpoint 041.
