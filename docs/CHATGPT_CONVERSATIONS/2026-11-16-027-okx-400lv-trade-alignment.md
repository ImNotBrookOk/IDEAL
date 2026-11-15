# Conversation 027 — OKX 400-level L2 reconstruction and trade alignment

**Date:** 16 November 2026  
**Project phase:** Phase 01 — Open-source and infrastructure research  
**Scope:** Research-only historical market-data validation. No runtime integration, exchange account, credentials, paper trading or live trading.

## Owner direction

The owner instructed us to continue Phase 01 research until a viable historical-data candidate is established. The existing scope and governance remain unchanged: crypto perpetual futures are the active initial market; Phase 02 and all implementation phases remain locked; no venue or data vendor is selected by this research.

## Work completed

### 1. Independent archive audit tooling

Added research-only files on branch `research/okx-l2-sample-2026-11-16`:

- `research/okx_archive_audit.py`
- `research/tests/test_okx_archive_audit.py`
- `research/okx_trade_book_alignment.py`
- `research/tests/test_okx_trade_book_alignment.py`
- `.github/workflows/okx-l2-400lv-comparison.yml`
- `.github/workflows/okx-l2-trade-alignment.yml`

The audit implementation uses a streaming TAR reader, pinned `orjson==3.11.3`, and keyed lazy heaps for BBO reconstruction. It is not an IDEAL runtime adapter. Unit tests specify snapshot replacement, absolute quantity updates, zero-quantity deletions, invalid quantities, crossed-book detection, timestamp accounting, strict no-lookahead trade alignment, same-timestamp handling, monotonicity and sample-age metrics.

TDD evidence:
- The archive-audit tests were run before implementation and failed because the module did not exist; after implementation, all six tests passed.
- The trade-alignment tests were run before implementation and failed because the module did not exist. A later metric extension produced the expected failing test for missing age-tail metrics; after implementation, all six tests passed.
- Final trade-alignment workflow [#43773844334](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43773844334) completed successfully, including unit tests, retrieval, schema inspection, alignment and acceptance assertions.

### 2. Actual OKX archive retrieval and structural reconstruction

The isolated workflow retrieved and validated two new archives:

| Archive | Compressed bytes | Uncompressed data member | Records | Snapshots | Updates |
|---|---:|---:|---:|---:|---:|
| BTC-USDT-SWAP module 4, 400 levels, 12 Nov UTC | 500,244,886 | 3,048,526,067 | 6,604,203 | 96 | 6,604,107 |
| BTC-USDT-SWAP module 5, 5,000 levels, 11 Nov UTC | 178,537,085 | 857,560,394 | 86,400 | 96 | 86,304 |

Both archives passed HTTP retrieval, SHA-256 recording, TAR/GZIP integrity and full record parsing. The 400-level archive SHA-256 is `6dd55534ddd376c6995bfac584f1e1a19ed64083b76b542da61ee488cacbdfce`; the 11 November 5,000-level archive SHA-256 is `b7a2e597f7e286d6b14c9fd50abe92a067af76b0129e99a04726a795ed44829f`.

**400-level module 4:**
- All 96 snapshots contained exactly 400 bid and 400 ask levels.
- 109,286,945 price-level rows were parsed; 20,114,734 zero-quantity rows were processed as deletions.
- Update message size: 1–1,183 changed levels; median 6 levels across both sides.
- 6,604,203 reconstructed states were valid; zero empty, crossed or locked states.
- Exactly 85.96% of the 6,604,202 adjacent record intervals were 10 ms. Further common intervals: 20 ms 7.29%, 30 ms 3.15%, 40 ms 1.42%, 50 ms 0.82%. There are rare longer intervals; the trade-alignment sample's maximum preceding-book age was 509 ms.
- There were 96 full snapshots, approximately 15 minutes apart.

**5,000-level module 5, 11 November:**
- All 96 snapshots contained exactly 5,000 bid and 5,000 ask levels.
- 37,499,572 price-level rows were parsed; 6,941,995 zero-quantity rows were processed as deletions.
- Update message size: 53–5,749 changed levels; median 279 across both sides.
- All 86,400 reconstructed states were valid; zero empty, crossed or locked states.
- 86,353 of 86,399 adjacent record intervals (99.947%) were exactly 1,000 ms.

This adjacent-day module-5 result is consistent with the previously tested 12 November 5,000-level sample. The two modules are materially different: module 4 is a high-frequency 400-level stream dominated by 10 ms intervals; module 5 is a deep 5,000-level stream sampled predominantly once per second.

### 3. Historical record schema and sequence continuity

The first five 400-level records had exactly these keys:

`action, asks, bids, instId, ts`

The instrument field was `BTC-USDT-SWAP`. No `seqId`, `prevSeqId`, `checksum` or `local_timestamp` field appeared. The first record was a snapshot; subsequent examples were updates.

Every sampled price-level tuple had three fields: price, quantity and a third integer. Example values included `["73979.9","754.88","42"]` and `["73980","122.51","14"]`. This is not sufficient to infer the third field's semantics. Keep it opaque; do not call it order count, liquidation count or queue size without an authoritative historical-module schema.

The absence of sequence IDs/checksums means the archive cannot independently prove that no incremental updates were lost. Timestamp regularity and successful book reconstruction are not substitutes for sequence continuity.

### 4. No-lookahead trade-to-book alignment

The 400-level archive was aligned to both matching UTC+8 trade ZIPs, filtered by actual timestamps to the UTC day 12 November 2026. The alignment implementation consumes trades before applying a book update with the same timestamp; this deliberately uses the strictly preceding book state when event order at equal timestamps is unknown.

Results for 3,224,415 target-day trades:

| Measurement | Result |
|---|---:|
| Trades aligned to a preceding valid BBO | 3,224,415 |
| Trades without a preceding book state | 0 |
| Trades aligned to invalid book states | 0 |
| Median preceding-book age | 6 ms |
| 95th-percentile preceding-book age | 10 ms |
| Maximum preceding-book age | 509 ms |
| Trades sharing the timestamp of a book update (conservatively assigned to prior state) | 311,016 (9.646%) |
| Trades outside the preceding sampled spread | 2,017,954 (62.584%) |
| Trade-side directional consistency | 98.542% |
| Side mismatches | 1.458% |

Price location relative to the preceding sampled BBO:
- below bid: 1,050,359
- above ask: 967,595
- at bid: 555,290
- at ask: 646,077
- inside: 5,094

For trades outside the sampled spread, distance from the nearest preceding BBO boundary was p50 0.35 bps, p90 1.01 bps, p95 1.40 bps, p99 2.82 bps, maximum 11.81 bps.

Sample-age tail counts:
- older than 10 ms: 161,204 (4.999%)
- older than 20 ms: 76,469 (2.372%)
- older than 50 ms: 16,390 (0.508%)
- older than 100 ms: 2,139 (0.066%)
- older than 250 ms: 67 (0.0021%)

The 62.58% outside-spread rate is not automatically a trade-data defect. Even with a 10 ms book stream, trades can occur after intervening book changes that are not represented by the sampled BBO. The strong 98.54% side consistency is encouraging, but it does not prove exact event ordering. The maximum-age tail must be measured and handled conservatively.

For comparison, the same-day 5,000-level one-second archive aligned to the same trades had median sample age 489 ms, p95 947 ms, and 76.71% of trades outside the preceding sampled spread. The 400-level stream materially improves temporal alignment, although it does not eliminate staleness.

The initial research quality gates passed: non-zero aligned trades, zero trades without a preceding book, zero invalid-book matches, p95 sample age no greater than 20 ms, and side consistency at least 98%.

## Assessment and disposition

**Viable research candidate:** OKX module 4 BTC-USDT-SWAP 400-level historical L2 is a credible candidate for 10 ms sampled short-horizon market-quality research, including spread, visible depth, imbalance, liquidity dynamics and conservative market-impact/slippage analysis.

**Still not execution-grade for passive-fill calibration:** the archive has no sequence IDs/checksums, no L3 order identity, no authoritative semantics for the third level field, and only 10 ms sampled book updates. It cannot establish FIFO queue position or exact passive fill order. Same-timestamp trades also lack an exchange sequence to establish whether a book update occurred before or after the trade.

The 5,000-level module 5 remains useful as a deeper but approximately one-second sampled liquidity reference; it is not a replacement for module 4 in short-horizon execution research.

No venue/vendor is selected. No runtime adapter or dependency was adopted. Raw archives were kept out of the public repository; the retained GitHub artifact contains only small audit summaries and expires after three days.

## Next work

1. Retrieve and reconstruct a second 400-level day (prefer 11 or 13 November) to test whether the 10 ms cadence, snapshot cadence, schema and quality metrics repeat.
2. Measure the longest-gap and sample-age tails by time-of-day; determine whether 509 ms is isolated or clustered.
3. Seek an authoritative OKX historical-module schema for the third field. Until confirmed, keep it opaque.
4. Establish a conservative execution-model protocol: no assumed FIFO; quantify latency sensitivity, adverse selection, spread crossing and uncertainty bounds; distinguish taker market-impact research from passive-fill simulation.
5. Preserve the data-license/terms review and independent-source comparison. Do not promote OKX from research candidate to selected venue without owner approval.

**Governance:** Phase 01 remains IN PROGRESS. Phase 02 and implementation phases remain LOCKED. D-001 initial perpetual scope and D-013 decision-quality-first execution priority remain unchanged.
