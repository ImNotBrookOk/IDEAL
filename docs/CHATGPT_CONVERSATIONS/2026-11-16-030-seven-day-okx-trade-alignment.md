# Conversation 030 — Seven-day OKX trade/BBO alignment checkpoint

Date: 2026-11-16
Scope: Phase 01 research only. No runtime integration, exchange credentials, paper/live trading or paid infrastructure.

## Work performed

Extended the official OKX BTC-USDT-SWAP 400-level historical L2 and paired trade alignment from an earlier three-day test to seven consecutive UTC days (7–13 November 2026). The research workflow reconstructs books and aligns each trade only to the strictly preceding BBO state. This avoids look-ahead where same-timestamp event order is unavailable.

Workflow: https://github.com/ImNotBrookOk/IDEAL/actions/runs/43779725982
Result: alignment acceptance failed; unit tests, archive retrieval, schema inspection, raw archive cleanup and summary artifact upload completed.
Artifact: 14188696071, 6,856 bytes, SHA-256 9e2ea9806da6451b1b2df8008aeb45deb5c47a8a14001f46ef90a835b04405ff. Summary-only; raw archives removed before upload.

## Results

| Day | Aligned trades | Age median / p95 / max | Side consistency | Result |
|---|---:|---:|---:|---|
| 7 Nov | 497,187 | 6 / 32 / 519 ms | 99.4270% | Fail: missing preceding book; p95 age |
| 8 Nov | 1,521,255 | 6 / 15 / 506 ms | 96.4530% | Fail: side consistency |
| 9 Nov | 3,283,080 | 6 / 10 / 475 ms | 99.1492% | Pass |
| 10 Nov | 3,238,578 | 6 / 10 / 489 ms | 98.2971% | Pass |
| 11 Nov | 2,597,825 | 6 / 18 / 497 ms | 99.1181% | Pass |
| 12 Nov | 3,224,415 | 6 / 10 / 509 ms | 98.5424% | Pass |
| 13 Nov | 5,556,342 | 5 / 10 / 507 ms | 98.1102% | Pass |

Five of seven days passed the initial gates. The 7 Nov and 8 Nov failures remain open. The 98% side-consistency and p95-age thresholds have not been relaxed. No failing day is excluded.

## Required follow-up

1. Diagnose 7 Nov start-of-archive coverage and trade/book pairing; identify exactly which trades lack a preceding book and whether the archive starts late or the UTC/UTC+8 pairing boundary is wrong.
2. Diagnose 8 Nov side-consistency by trade side, timestamp equality, BBO age and price category. Verify aggressor-side field semantics against official OKX documentation; do not infer them from column labels alone.
3. Determine whether side consistency is a valid acceptance metric for the specific archive sampling and event-time semantics. Keep it as a diagnostic until the semantics are proven; do not lower the threshold to force a pass.
4. Characterize the approximately 0.5-second maximum book-age tails across all days. Passing p95 does not remove tail risk.
5. Repeat the seven-day test after fixes and retain the failed run for audit.

## Documentation updated

- docs/HISTORICAL_L2_SAMPLE_VALIDATION.md — section 12.19 with daily metrics and disposition.
- docs/COMPONENT_SELECTION_MATRIX.md — cross-cutting execution-quality gate and Phase 01 exit criterion updated.
- ROADMAP.md — seven-day checkpoint and remaining blockers added.
- TESTING.md — unconditional cleanup on failed acceptance run documented in earlier checkpoint.

Phase 01 remains IN PROGRESS. Phase 02 remains LOCKED.
