# 034 — OKX seven-day timestamp-boundary revalidation and risk classification

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Phase state:** IN PROGRESS; Phase 02 remains LOCKED  
**Research branch:** `research/okx-l2-sample-2026-11-16`

## Result

The original seven-day 400-level OKX trade/BBO alignment run [#43779725982](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43779725982) had five days pass its strict per-day screen and two fail. The follow-up [#43803546192](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43803546192) reran all seven days with timestamp-boundary diagnostics. It again **failed the original strict gates on 7 Nov and 8 Nov**, as expected. It did not relax the thresholds. It completed all calculations, removed raw archives, and uploaded only summary files.

- Run conclusion: failure of original quality gates, not parser/unit-test or cleanup failure.
- Unit tests passed before archive retrieval.
- All seven L2 and paired trade archives passed retrieval/integrity checks.
- All seven day-level calculations completed.
- Raw archives and intermediate files were deleted by the unconditional cleanup step.
- Summary artifact: [14198101057](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43803546192/artifacts/14198101057), 7,243 bytes; artifact ZIP SHA-256 `a289e133ff5d8284ca96d29260c3f54f12c347f9606e54ab9ad46bde92126f18`.

## 7 November — missing trade is an initial-snapshot boundary

- First trade timestamp: `1794009600006` ms.
- First L2 book snapshot timestamp: `1794009600008` ms.
- The first trade precedes the first available snapshot by exactly **2 ms**.
- Exactly one of 497,188 trade rows has no preceding book; 497,187 align.
- No invalid-book trades.
- p95 book age 32 ms; max 519 ms.
- Age counts: 39,315 >20 ms; 11,809 >50 ms; 2,824 >100 ms; 105 >250 ms.
- Side consistency 99.42698%; strict-preceding subset 99.44395%.

This is a known initial coverage boundary, not a mid-session sequence gap. Exclude the one unmatched trade from BBO-dependent calculations and preserve it in the coverage audit. Any unmatched trade after the initial snapshot remains a structural failure.

The age screen is independent: 92.094% of aligned observations are <=20 ms; 97.625% are <=50 ms; 99.432% are <=100 ms; 99.979% are <=250 ms. The day is therefore conditional-quality for fast research and must carry observation-age flags. A model requiring a 20 ms maximum freshness budget must exclude or explicitly handle the 7.906% of observations older than that budget.

## 8 November — side/BBO discrepancy concentrated in fresh observations

- 1,521,255 trades aligned; zero missing/invalid book matches.
- p95 age 15 ms; max 506 ms.
- Side consistency 96.45299%.
- Same-timestamp subset 94.93731%; strictly preceding subset 96.60610%.
- By book age: <=10 ms 96.23000%; 10–20 ms 99.79272%; 20–50 ms 99.84022%; >50 ms 99.88234%.
- Age counts: 53,299 >20 ms; 16,998 >50 ms; 4,214 >100 ms; 208 >250 ms.

Official OKX public trade documentation defines `side` as taker direction. The metric therefore measures whether the trade price is consistent with the opposite-side quote in the preceding sampled BBO; it does **not** directly test whether OKX's taker-side label is correct. The sharp improvement for observations older than 10 ms, plus the lower same-timestamp subset, is consistent with book/trade event-ordering and rapid BBO movement in a sampled historical stream. It does not prove that explanation. Keep the discrepancy visible and do not use this dataset to claim exact aggressor/BBO event ordering or execution-grade fills.

## Seven-day aggregate age-tail profile

Total aligned trades: **19,918,682**.

| Preceding-book age | Trades older than threshold | Share within threshold |
|---|---:|---:|
| 20 ms | 452,951 | 97.7260% |
| 50 ms | 94,657 | 99.5248% |
| 100 ms | 15,176 | 99.9238% |
| 250 ms | 1,034 | 99.9948% |

All seven days have zero invalid-book trades. Maximum per-day age is between 475 ms and 519 ms. This makes age flags mandatory: the dataset is not uniformly fresh merely because its aggregate median is 5–6 ms.

## Per-day strict result retained

| Day | Aligned trades | p95 age | Max age | Side consistency | Original strict result |
|---|---:|---:|---:|---:|---|
| 7 Nov | 497,187 | 32 ms | 519 ms | 99.4270% | FAIL: 1 initial-boundary unmatched trade; p95 age |
| 8 Nov | 1,521,255 | 15 ms | 506 ms | 96.4530% | FAIL: side/BBO diagnostic |
| 9 Nov | 3,283,080 | 10 ms | 475 ms | 99.1492% | PASS |
| 10 Nov | 3,238,578 | 10 ms | 489 ms | 98.2971% | PASS |
| 11 Nov | 2,597,825 | 18 ms | 497 ms | 99.1181% | PASS |
| 12 Nov | 3,224,415 | 10 ms | 509 ms | 98.5424% | PASS |
| 13 Nov | 5,556,342 | 10 ms | 507 ms | 98.1102% | PASS |

## Risk-weighted classification

Apply the policy approved in checkpoint 031 and documented in `TESTING.md`:

1. **Structural integrity:** all seven reconstructed books remain valid; zero invalid-book trades; no mid-session unmatched trade was found. The single 7 Nov unmatched trade is exactly 2 ms before the first snapshot and is excluded as an initial boundary row with a retained audit record.
2. **Research utility:** 9–13 Nov are preferred-quality under the original 98%/20ms screens. 7 Nov is conditional due to age-tail distribution. 8 Nov is conditional due to side/BBO consistency. These are not averaged away.
3. **Use constraints:** preserve raw source provenance and day-level flags; use model-specific freshness budgets; do not treat stale BBO as executable; do not claim queue position, passive-fill accuracy, exchange sequence continuity or exact execution fidelity.
4. **Disposition:** accept the seven-day OKX 400-level sample as a **conditional historical market-structure research candidate**. It is not accepted as an execution-grade fill-calibration dataset. The original 5/7 strict screen result remains recorded and unchanged.

This is a classification of research usefulness, not a retroactive pass of the strict test. No threshold was lowered.

## Phase 01 implications

The seven-day trade/BBO diagnosis gate is now sufficiently resolved for historical research classification. The following Phase 01 gates remain:
- September/October multi-day Tardis/official OKX BBO comparison workflow [#43804760777](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43804760777) still in progress at this checkpoint.
- $0 persistent worker feasibility remains open; Oracle A1 is not accepted as a reliable sole production host.
- IDEAL-specific transitive dependency lock, vulnerability scan, workflow security lint and SBOM/licence inventory remain open.
- Component selections/rejections still require owner review before Phase 01 can close.

No runtime integration, venue selection, exchange access, paper/live execution, spend or Phase 02 work is authorised.
