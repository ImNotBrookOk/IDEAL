# IDEAL — Historical L2 Sample Validation Report

**Research date:** 16 November 2026  
**Phase:** 01 — Open-source, venue and infrastructure research  
**Gate status:** BLOCKED — no dataset bytes were obtained in this execution environment.  
**Venue status:** None selected. No account, API key, testnet, paid service or trading connection used.

## 1. Objective

Establish whether a representative, no-cost historical perpetual-futures L2 dataset can be obtained and inspected before any venue or engine is selected. The acceptance target is a real file containing an initial book state and incremental depth updates, with enough provenance and timestamp information to reconstruct the book and quantify data defects.

This report distinguishes (a) facts documented by vendors or third-party tooling, (b) network retrieval attempts made in this environment, and (c) validation that remains unperformed.

## 2. Retrieval attempts and outcomes

### Tardis public sample endpoints

The Tardis documentation defines daily gzip CSV files at:

`https://datasets.tardis.dev/v1/:exchange/:dataType/:year/:month/:day/:symbol.csv.gz`

First-of-month datasets are documented as available without an API key. The following direct requests were attempted from the execution container:

| Dataset | Date | Outcome |
|---|---|---|
| `binance-futures/book_snapshot_5/BTCUSDT` | 2020-09-01 | DNS resolution failure: `[Errno -3] Temporary failure in name resolution` |
| `binance-futures/incremental_book_L2/BTCUSDT` | 2020-09-01 | DNS resolution failure: same environment error |
| `binance-futures/trades/BTCUSDT` | 2020-09-01 | DNS resolution failure: same environment error |
| Tardis exchange metadata API | current | DNS resolution failure: same environment error |

A previous attempt recorded in audit 021 timed out. The browser retrieval route also returned an inaccessible-file error for the gzip URL. These results establish only that this execution environment could not resolve/retrieve the host; they do not establish a Tardis outage or sample unavailability.

### Independent documented download evidence

The HftBacktest v2.2.0 data-preparation guide includes a reproducible Tardis Binance Futures sample download for 2020-02-01 and records successful HTTP 200 responses in its example:
- Trades gzip: 3,090,479 bytes.
- Incremental L2 gzip: 250,016,849 bytes (about 238.43 MiB).
- The example converts the combined trade/book files into 27,532,602 normalized events.

Source: [HftBacktest Data Preparation — Getting started from Tardis.dev data](https://hftbacktest.readthedocs.io/en/py-v2.2.0/tutorials/Data%20Preparation.html).

This is useful independent evidence that the documented route has worked and that a single day can be substantial. It is a historical tutorial/example, not a current availability check. The 2020 sample is not representative evidence for current market conditions or contemporary venue microstructure.

## 3. Schema and reconstruction facts established from documentation

Tardis documents these normalized incremental L2 fields:

- `exchange`, `symbol`
- `timestamp`: exchange-provided timestamp, with local timestamp used as fallback when the exchange does not provide one
- `local_timestamp`: local message receive timestamp in microseconds
- `is_snapshot`: snapshot/delta discriminator
- `side`, `price`, `amount`

Documented reconstruction rules and caveats:

1. Apply a snapshot as a full state replacement; do not retain prior levels when a new snapshot begins.
2. Apply incremental price-level updates by side and price; zero amount removes a level.
3. Rows sharing `local_timestamp` can represent one exchange message containing multiple level changes. Preserve row order and message grouping.
4. Tardis documents an initial snapshot at the beginning of the day and additional snapshots after WebSocket reconnects.
5. Tardis documents reconnect gaps of approximately 300–3,000 ms depending on venue.
6. CSV datasets do not include disconnect event markers; raw replay can expose disconnect messages.
7. Cross-channel events are not guaranteed to be causally synchronized. Do not infer trade-before-book or book-before-trade solely from equal exchange timestamps.
8. The `book_snapshot_5` / `book_snapshot_25` datasets are pre-reconstructed top-N views, useful for quick inspection but not a substitute for full incremental depth where available.
9. L2 is market-by-price. It does not expose individual resting-order identities and cannot establish true FIFO queue position.

Sources:
- [Tardis downloadable CSV documentation](https://docs.tardis.dev/downloadable-csv-files)
- [Tardis data types and CSV schemas](https://docs.tardis.dev/downloadable-csv-files/data-types)
- [Tardis data FAQ](https://docs.tardis.dev/faq/data)
- [Tardis dataset API reference](https://docs.tardis.dev/downloadable-csv-files/api)

## 4. Validation matrix

| Acceptance item | Status | Evidence / limitation |
|---|---|---|
| Obtain real gzip dataset bytes | **NOT PASSED** | All direct attempts failed at DNS resolution in this environment |
| Verify HTTP status, content length and file hash | NOT RUN | No response body or file bytes |
| Verify gzip integrity and decompression | NOT RUN | No file |
| Parse actual CSV header and rows | NOT RUN | No file |
| Confirm symbol, venue and contract identity | DOCUMENTED ONLY | URL example identifies Binance Futures BTCUSDT; no file metadata inspected |
| Reconstruct from first snapshot and deltas | NOT RUN | No actual event stream |
| Verify snapshot reset/reconnect behavior | DOCUMENTED ONLY | Vendor docs describe snapshots; no observed transitions |
| Quantify sequence gaps / missing intervals | NOT RUN | Normalized schema does not itself provide exchange sequence IDs in the documented fields |
| Measure timestamp skew and ordering | NOT RUN | Requires real rows and paired channels |
| Quantify duplicates, crossed books, empty books and depth | NOT RUN | Requires real rows |
| Align trades and L2 updates | NOT RUN | Requires both actual files; equal-time causality remains a known caveat |
| Establish current-market representativeness | NOT PASSED | 2020 tutorial sample is too old for that claim |
| Establish L3 queue-position fidelity | **NOT SUPPORTED** | L2 market-by-price has no individual order identity |

**Result:** no data-quality pass is claimed. This is a retrieval blocker, not a dataset rejection.

## 5. Engineering and cost implications

- A one-day L2 file can be hundreds of megabytes compressed and expand materially when decompressed or normalized. Capacity planning must use measured compressed size, decompressed size, row count, peak memory and conversion time.
- Trade and book files should remain separate immutable source artifacts with hashes and provenance. Any normalized replay file must retain a manifest describing source files, converter version, timestamp units, event ordering policy and exclusions.
- Never silently interpolate across reconnect or sequence gaps. Mark affected intervals invalid for execution calibration unless a defensible recovery boundary is proven.
- Keep exchange event time and local receive time distinct. Record timestamp unit and origin explicitly; reject ambiguous or non-monotonic data rather than silently sorting away evidence.
- A normalized L2 file can support spread/depth/impact analysis, but it cannot justify exact passive queue-position or FIFO fill-probability claims.

## 6. Next validation procedure

When the public host is reachable from a normal network environment, retrieve one matching first-of-month date for the same venue/instrument and download, at minimum:
1. `incremental_book_L2`
2. `trades`
3. `derivative_ticker` (where supported, for funding/open-interest/mark/index context)

Then record:
- exact URL, retrieval time, HTTP status, response headers, compressed bytes and SHA-256;
- gzip integrity, decompressed bytes, CSV row count and schema;
- first/last local and exchange timestamps, timestamp units, duplicate and out-of-order counts;
- snapshot count, snapshot boundaries, delta counts, empty-book and crossed-book counts;
- reconstructed bid/ask monotonicity, spread validity, depth distribution and maximum staleness;
- trade/book timestamp offsets and ambiguous same-time groups;
- gaps and invalid intervals, with no interpolation;
- CPU time, peak RSS and storage expansion.

Run an independent second implementation or oracle on a bounded event slice and compare reconstructed top-of-book and depth checksums at deterministic checkpoints. Do not proceed to empirical calibration until this comparison passes.

## 7. Current disposition

- Tardis remains a viable **sample-evaluation candidate**, not an approved vendor or data source.
- OKX still advertises native historical L2 from March 2023, but the actual downloadable file format, instrument coverage, access requirements and price have not been verified.
- No venue is selected. New Zealand product eligibility remains unresolved.
- Phase 01 remains IN PROGRESS; Phase 02 remains LOCKED.
- No runtime integration, exchange/account access, testnet, paper/live orders, paid service or infrastructure was used.

**Next roadmap task:** obtain actual public historical L2 and paired trade bytes through a network path that can reach the dataset host, then execute the validation matrix above. If access remains unavailable, preserve the blocker and assess an alternate no-cost source without weakening the acceptance criteria.
