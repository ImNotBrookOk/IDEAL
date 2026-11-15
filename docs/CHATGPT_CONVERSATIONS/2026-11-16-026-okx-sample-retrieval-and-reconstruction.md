# Conversation 026 — OKX sample retrieval and reconstruction validation

Date: 16 November 2026  
Project: IDEAL  
Phase: 01 — Open-source and infrastructure research (IN PROGRESS)  
Status: Partial validation pass; historical-data acceptance remains BLOCKED.

## Scope and controls

The user asked to continue the bounded OKX historical-data validation. Work remained limited to public market-data archives and isolated research tooling. No exchange account, API credentials, paid infrastructure, runtime integration, paper orders or live orders were used. No phase transition was requested or performed.

## Retrieval evidence

- GitHub Actions run: [#43766633587](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43766633587)
- Research branch: `research/okx-l2-sample-2026-11-16`
- Run head: `8c3bfd549276637327be9c75c6113a03e79a4bf3`
- Artifact ID: `14182173189`
- Artifact size: 236,127,656 bytes
- Artifact SHA-256: `f4a664471e12a28314c726e3d51335b630361eb05d7ecf4330f539a58130b94d`
- GitHub reports artifact expiry at 2026-11-18 21:58:54 UTC (3-day retention).
- The artifact was independently downloaded using the GitHub artifact connector into the current analysis workspace. Local SHA-256 matched GitHub's digest. ZIP integrity passed.

Source archives:
- L2: 186,255,630 bytes; SHA-256 `bab7213b2944a8f8c9540064d8c5b217c84d82d41f17c2e30fa426800e42c99b`.
- Trade UTC+8 date 12 Nov: 18,720,850 bytes; SHA-256 `1da901d447e66aa9bd9b0e57c9711cec27720adc093352d6456ea453a114545e`.
- Trade UTC+8 date 13 Nov: 31,904,876 bytes; SHA-256 `cc3cbef246c1efb3c477eb05816a4d1f32843ae5a5996688a32ebab216d87eb8`.
- L2 response: HTTP 200, content-length 186,255,630. Both trade archives: HTTP 200, content-lengths match actual bytes.
- TAR/GZIP and both ZIP integrity checks passed. L2 tar contains one NDJSON member of 891,030,123 uncompressed bytes.

## L2 parse and reconstruction

An independent streaming parser processed all 86,400 records:
- 86,304 updates and 96 snapshots; all records identify BTC-USDT-SWAP.
- 5,000 bids and 5,000 asks in every snapshot.
- Snapshot cadence approximately 15 minutes: 95 intervals range 899,994–900,008 ms.
- Main update cadence approximately 1 second: 86,349 of 86,399 adjacent intervals are exactly 1,000 ms.
- 14 intervals outside 900–1,100 ms form seven long/short pairs (long 1,130–1,429 ms; short 570–870 ms).
- Per update median 143 ask and 143 bid level entries; per-side p95 586; maxima 3,619 asks and 3,986 bids. Maximum combined update 7,586 entries.
- 7,504,519 zero-quantity changes treated as level deletions.
- Snapshot replacement plus incremental absolute-quantity changes/deletions rebuilt the book through the entire day.
- Zero empty, crossed or locked states; no negative price/quantity values observed.
- No sequence IDs or per-record checksum fields are present. Thus reconstruction cannot prove no missing updates between sampled records.
- Each archived price level has three values. OKX's public live WebSocket documentation illustrates four values (price, size, liquidated-order count, order count); the third archive value's exact semantics remain unresolved. Do not use it as an order-count/liquidation feature.

## Trade parse and timezone pairing

Parsed all 8,703,176 trade rows:
- 12 Nov UTC+8 archive: 3,222,603 rows, timestamp span 2026-11-11 16:00:00.054 UTC to 2026-11-12 15:59:59.949 UTC.
- 13 Nov UTC+8 archive: 5,480,573 rows, timestamp span 2026-11-12 16:00:00.045 UTC to 2026-11-13 15:59:59.999 UTC.
- 2026-11-12 UTC target interval: 3,224,415 rows (2,288,403 from first file; 936,012 from second).
- Target-day trade timestamp range: 00:00:00.639–23:59:59.553 UTC.
- Trade IDs strictly increasing across concatenated files; no non-monotonic IDs or adjacent duplicates.
- No malformed rows, invalid sides, non-positive prices or non-positive sizes.
- Both trade files must be timestamp-filtered; filename date alone does not align with the UTC book day.

## Interpretation

Partial pass for byte retrieval, archive hashes/integrity, full parse and coarse one-second book reconstruction. This dataset may support coarse one-second spread, visible depth and imbalance analysis after further sampling/timestamp checks. It is not tick-by-tick and cannot independently support FIFO queue position, high-fidelity passive-fill calibration or intrasecond market-impact modelling.

Not yet passed:
- sequence continuity / lost-update detection;
- timestamp provenance and explanation of seven long/short pairs;
- exact trade-to-book/BBO event alignment;
- independent exchange-reference comparison;
- adjacent-day and alternate-depth module comparison;
- multi-day and multi-instrument representativeness.

A trade-to-sampled-BBO alignment attempt did not complete in the local analysis runtime; no result is claimed.

## Next actions

1. Validate snapshot ordering, duplicate price keys, level semantics and parser behavior with independent golden fixtures.
2. Investigate timestamp outlier pairs and compare 400-level module for the same day.
3. Complete trade-to-preceding-BBO staleness diagnostics; do not treat one-second sampled BBO as event-time truth.
4. Retrieve and validate 11 November 5,000-level archive for adjacent-day continuity.
5. Establish approved, licence-compatible retention for the raw research artifact before its 3-day GitHub retention expires. Do not commit raw vendor archives to the public repository.

## Governance outcome

Phase 01 remains IN PROGRESS. Historical-data acceptance remains BLOCKED for execution calibration. Phase 02 remains LOCKED. No vendor/venue selected, no runtime component adopted, no credentials/accounts connected, and no trading authorised.


## Follow-up audit addendum (16 November 2026)

A follow-up pass refined update density and independently rechecked both trade files.

- 39,035,798 total L2 price-level rows; 7,504,519 zero-quantity deletion rows.
- 86,304 update messages; 47–7,586 changed levels per message; median 283 combined bid+ask changes per message.
- 86,349 of 86,399 adjacent L2 timestamp intervals are exactly 1,000 ms; 50 differ, 14 outside 900–1,100 ms.
- All 96 snapshots contain exactly 5,000 levels per side.
- Historical price-level rows have exactly three fields. The third integer is opaque pending authoritative historical module-5 schema confirmation. Current live RPI and legacy WebSocket documentation show four-field schemas, so neither may be projected onto this archive.
- 12 Nov UTC+8 trade file: 3,222,603 rows, IDs 3,064,471,065–3,067,693,667.
- 13 Nov UTC+8 trade file: 5,480,573 rows, IDs 3,067,693,668–3,073,174,240.
- Trade IDs strictly increase and continue exactly across the file boundary; no malformed/invalid rows or adjacent duplicate IDs observed. Matching UTC-day trade count remains 3,224,415.

A second BBO alignment attempt exceeded the local analysis execution limit. No trade-to-BBO alignment statistic is claimed. Execution calibration remains blocked. Updated test priorities: authoritative historical field semantics, module 4 vs 5 comparison, adjacent-day continuity, efficient BBO alignment and independent completeness evidence.
