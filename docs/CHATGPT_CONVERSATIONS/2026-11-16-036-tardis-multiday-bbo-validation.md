# 036 — Tardis OKX multi-day BBO agreement validation

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Phase state:** IN PROGRESS; Phase 02 remains LOCKED  
**Workflow:** [#43804760777](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43804760777)

## Result

<badge color="success">Multi-day comparison completed</badge>

The workflow retrieved first-of-month BTC-USDT-SWAP Tardis OKX Swap incremental-L2 samples and matching official OKX module-4 400-level archives for 1 September and 1 October 2026. It ran the complete research unit suite, reconstructed both books, produced BBO series, stable-sorted by exchange timestamp, compared strict-preceding/no-lookahead BBOs, removed raw archives and intermediate BBO CSVs, and uploaded summary-only artifact.

- Workflow conclusion: success.
- Unit tests passed.
- Archive retrieval and integrity checks passed.
- Both days reconstructed with zero exchange timestamp backsteps.
- All Tardis BBO samples had a preceding official state.
- Inclusive same-timestamp exact BBO match: 100% for both dates.
- Strict-preceding exact BBO match: 99.35174% September; 99.31758% October.
- Cleanup and summary-only upload passed.
- Artifact [14198581255](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43804760777/artifacts/14198581255), 4,753 bytes; artifact ZIP SHA-256 `970e09322fea56fb3fa8ce17120d6cbf1b5ab1409c36e865cdb4cd2b492dd15c`.

## 1 September 2026

Tardis:
- 854,293 messages; 48,055,501 level rows.
- 65 snapshots and 854,227 updates.
- 74 buffered rows skipped before the first snapshot.
- 854,292 valid reconstructed book states; zero exchange timestamp backsteps.
- Maximum exchange message gap 16,500 ms; maximum local message gap 16,501.192 ms.

Official OKX module-4 archive:
- 5,858,458 records; 82,790,279 level rows; 96 snapshots.
- 400 bid and 400 ask levels in every snapshot.
- No negative/invalid records and no duplicate snapshot levels.
- Maximum exchange timestamp interval in the day: 537 ms.

Strict preceding BBO comparison:
- 854,292 compared samples; zero without a preceding official state.
- Exact BBO match 99.3517439%; bid match 99.3561920%; ask match 99.3572455%.
- Preceding official state age: median 10 ms, p95 50 ms, max 510 ms.
- Inclusive same-timestamp exact match 100%.

Official archive had approximately **6.86x** as many records as Tardis.

## 1 October 2026

Tardis:
- 855,187 messages; 42,194,739 level rows.
- 49 snapshots and 855,137 updates.
- 55 buffered rows skipped before the first snapshot.
- 855,186 valid reconstructed book states; zero exchange timestamp backsteps.
- Maximum exchange message gap 2,400 ms; maximum local message gap 2,399.725 ms.

Official OKX module-4 archive:
- 7,217,446 records; 82,544,414 level rows; 96 snapshots.
- 400 bid and 400 ask levels in every snapshot.
- No negative/invalid records and no duplicate snapshot levels.
- Maximum exchange timestamp interval in the day: 508 ms.

Strict preceding BBO comparison:
- 855,186 compared samples; zero without a preceding official state.
- Exact BBO match 99.3175754%; bid match 99.3221358%; ask match 99.3213172%.
- Preceding official state age: median 10 ms, p95 40 ms, max 500 ms.
- Inclusive same-timestamp exact match 100%.

Official archive had approximately **8.44x** as many records as Tardis.

## Combined with 1 November baseline

The prior 1 November 2026 comparison (workflow #43778824863) reported:
- 844,982 Tardis samples, 13 Tardis snapshots vs 96 official snapshots.
- Strict preceding exact BBO match 99.85065%; inclusive same-timestamp 100%.
- Official preceding BBO age median 10 ms, p95 60 ms, max 529 ms.
- Tardis maximum exchange-time gap 3,800 ms vs 584 ms in official archive.
- Approximately 6.90x fewer Tardis messages.

Across all three first-of-month dates, Tardis sampled BBO values agree very closely with the preceding official BBO state (>99.3% exact match on each date), with no sample lacking a preceding official state and 100% inclusive same-timestamp matches.

## Interpretation and limitations

1. **BBO price fidelity:** strong evidence that the Tardis normalized stream is an accurate sampled BBO reference on these three dates.
2. **Sampling density:** Tardis has approximately 6.9x fewer messages on 1 Nov, 6.86x fewer on 1 Sep and 8.44x fewer on 1 Oct. Snapshot counts are 13/65/49 vs 96 official. Exchange-time gaps reach 3.8 seconds, 16.5 seconds and 2.4 seconds respectively.
3. **Not 10 ms equivalent:** the sparse message cadence and larger gaps mean Tardis must not substitute for the official 10 ms VIP4+ feed in latency, queue, event-order or execution-calibration work.
4. **Channel provenance:** the normalized CSV does not expose raw source channel ID. Provider coverage documentation lists OKX books-l2-tbt through 21 May 2026 and books from that date onward; this is documentation-based context, not packet-level proof of the exact channel used for each sample.
5. **No sequence/fill proof:** no historical sequence IDs or FIFO queue position are available. High BBO match rates do not prove lossless sequence continuity, L3 depth, RPI/non-RPI composition, passive-fill fidelity or exchange-equivalent execution.

## Disposition

**Accept Tardis OKX normalized history as a secondary sampled BBO/reference source for historical market-structure research. Do not select it as the primary 10 ms execution-calibration source.** This multi-day comparison gate is complete. Exact raw channel provenance remains unavailable and is a documented limitation rather than an unresolved reason to reject the secondary-reference use case.

No runtime integration, account access, exchange credentials, paid data or execution is authorised.
