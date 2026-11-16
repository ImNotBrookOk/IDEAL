# 031 — Risk-weighted acceptance and OKX alignment boundary diagnostics

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Phase state:** IN PROGRESS; Phase 02 remains LOCKED  
**Research branch:** `research/okx-l2-sample-2026-11-16`

## Owner direction

The owner agreed to continue using a risk-weighted acceptance approach rather than requiring every non-critical research diagnostic to reach 100%. A result above 90% can be useful evidence that a component is viable, but it is not a blanket safety guarantee.

The policy has been added to `TESTING.md`:

- Hard correctness and safety invariants require 100%.
- At least 98% is preferred for quality diagnostics.
- 95% to below 98% is conditional research evidence.
- 90% to below 95% is exploratory evidence only.
- Below 90% is normally rejected or isolated pending diagnosis.
- Report per-day/per-regime denominators and tails; do not average away failures.
- Preserve data freshness and quality flags. Stale observations cannot be silently treated as current.
- No research-data percentage establishes execution-grade fills, queue position, live continuity, venue eligibility or operational readiness.

This policy classifies evidence; it does not retroactively change the original 98% screen or rewrite the first seven-day result.

## Seven-day failure diagnostics

Source run: [GitHub Actions #43779725982](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43779725982), artifact 14188696071 (summary-only; SHA-256 `9e2ea9806da6451b1b2df8008aeb45deb5c47a8a14001f46ef90a835b04405ff`).

### 7 November 2026

- 497,188 trade rows; 497,187 aligned to a strictly preceding book.
- Exactly one trade had no preceding book state (one row, approximately 0.0002% of rows).
- p95 preceding-book age: 32 ms; maximum: 519 ms.
- 39,315 aligned observations were older than 20 ms; 11,809 older than 50 ms; 2,824 older than 100 ms; 105 older than 250 ms.
- Side consistency: 99.42698%.

The one unmatched row is not a broad coverage failure. The age distribution is a separate quality issue: approximately 92.1% of aligned trades had a preceding-book age of 20 ms or less, but the original p95 <=20 ms screen was not met. The first/last book and trade timestamps, and the timestamp of the unmatched trade, are being added to the audit output to determine whether the unmatched row is simply before the first snapshot.

### 8 November 2026

- 1,521,255 aligned trades; zero missing or invalid book matches.
- p95 preceding-book age: 15 ms; maximum: 506 ms.
- Side consistency: 96.45299%.
- Same-timestamp subset: 94.93731%; strict-preceding subset: 96.60610%.
- Age <=10 ms: 96.23000%; 10–20 ms: 99.79272%; 20–50 ms: 99.84022%; >50 ms: 99.88234%.

The mismatch is concentrated in the <=10 ms age bucket and is present even in the strict-preceding subset. This is a measured discrepancy, not a field-name ambiguity. It is consistent with sampled-book/event-timing limitations during fast movement, but the available historical archive does not prove that cause.

## Official OKX trade-side semantics

The official OKX API guide defines the public trade `side` field as `吃单方向` (taker direction), with `buy` and `sell` values. The WebSocket `trades` channel aggregates multiple maker matches by taker order and price/source; `count` records the number of matches. The `trades-all` channel instead emits one trade per message. Official documentation:
- https://app.okx.com/docs-v5/zh/ — public trades fields at lines 10092–10170; WebSocket trades semantics at lines 10618–10667.
- https://www.okx.com/docs-v5/en/ — English API reference.

Therefore the current directional screen is comparing the taker direction with the strictly preceding sampled BBO. A mismatch means the trade price is not beyond the preceding opposite-side quote in the expected direction. It does not, by itself, prove bad source data: the preceding quote may have changed before the trade, and historical archive timestamps do not provide a shared sequence ordering for all book/trade events.

## TDD diagnostic change

The alignment summary now records:
- first and last book timestamps;
- first and last filtered trade timestamps;
- timestamp of the first trade with no preceding book.

Test-first evidence:
- Commit `d2394bceb1eb09599ed65e77cd1c6417f86da627` added two tests first. The focused CI run [#43803484682](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43803484682) failed as expected because the new summary fields did not yet exist (RED).
- Commit `3f96cf0ff7a9670864cfe9d4fdb7841a6a23f626` implemented the metadata (GREEN).
- The focused alignment tests passed in workflow [#43803546192](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43803546192) before archive retrieval.
- A separate lightweight CI workflow was added at `.github/workflows/research-unit-tests.yml` (commit `10498e9fc5c61ab9ed522d933ee342df3cd91e78`). Full research suite: **29 tests passed**, compileall passed, workflow [#43803785850](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43803785850).

The Tardis/OKX integration workflow at commit `d2394b...` also failed during the intentional RED stage because it runs the shared test directory. It was not an independent data-quality failure. The full 29-test suite passed after the implementation commit.

## Revalidation status

A fresh seven-day run, [workflow #43803546192](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43803546192), is reprocessing the same 7–13 November archives with the new timestamp-coverage diagnostics. At the time of this audit entry:
- focused alignment unit tests passed;
- all seven L2 archives and paired trade archives downloaded and passed integrity checks;
- historical schema inspection completed;
- full seven-day alignment was still running;
- no new data result or acceptance decision is claimed yet.

The original seven-day result remains the authoritative completed run until the new run completes. Raw archives must still be removed in the unconditional cleanup step and only small audit summaries retained.

## Current disposition

- Keep OKX module-4 400-level history as the leading historical research candidate.
- Preserve the first seven-day gate failure and all original metrics.
- Use the risk-weighted policy only to distinguish research utility from execution-grade evidence.
- Do not claim passive-fill accuracy, FIFO queue position, lossless historical sequence continuity, full executable liquidity (including RPI), live venue eligibility or runtime readiness.
- Phase 01 remains IN PROGRESS. Phase 02 remains LOCKED. No runtime integration or trading permissions are authorised.
