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


## 8. Additional no-cost source and collector screening (16 November 2026)

### 8.1 Community Binance L2 dataset and collector

The Hugging Face dataset `MaximumLeverage/crypto-lob-stream` advertises Snappy Parquet depth diffs, trades and full-book snapshot anchors for BTCUSDT, ETHUSDT and SOLUSDT. Its dataset card reports 251,388,868 rows and 1.72 GB total, an MIT licence, reconstructable sequence IDs from 2026-06-03 onward, and a known 43-minute capture interruption on 5 July 2026 for all three symbols. A fresh snapshot follows the outage, so it must be treated as a hard reset, not a continuous sequence. The card does not unambiguously identify the published Binance market as spot or USDⓈ-M perpetual; therefore it is not yet accepted as target-market perpetual data.

A critical reconstruction issue is explicitly documented: Binance depth updates do not necessarily emit deletions for levels that drift outside the tracked snapshot depth. A replay that removes only explicit zero-quantity levels can accumulate stale “ghost” levels even when sequence IDs are continuous. The published reconstruction helper prunes to the intended depth after every update. IDEAL's independent validator must test this property rather than trust a third-party reconstruction helper.

Dataset source: [Hugging Face dataset card](https://huggingface.co/datasets/MaximumLeverage/crypto-lob-stream).

### 8.2 MIT collector candidate

The related `crypto-lob-stream` package/repository is a small alpha-stage collector, not a trading engine. Its repository declares MIT; PyPI 0.9.2 was released 30 August 2026 and requires Python 3.10+. The GitHub repository's latest inspected commit is 1 September 2026; the README documents Binance USDⓈ-M, OKX swaps and Bybit linear perpetual adapters, Parquet output, sequence-gap logging, and Kraken checksum verification. It also documents material limits: Binance depth files before 2026-06-03 14:38:49 UTC lack sequence IDs; Binance/OKX/Bybit do not have checksum verification in this package; OKX/Bybit resynchronisation requires reconnect; pre-0.9.2 files may contain overwritten flush intervals; and OKX swap mark-price data is absent unless a separate channel is added. No package installation, test execution, live connection or adoption occurred.

Sources: [GitHub repository](https://github.com/Goodie-Goody/crypto_lob_stream_pypi), [MIT licence](https://github.com/Goodie-Goody/crypto_lob_stream_pypi/blob/main/LICENSE), [PyPI 0.9.2 release](https://pypi.org/project/crypto-lob-stream/0.9.2/).

### 8.3 CryptoHFTData free API candidate — hold pending corrections

CryptoHFTData documents anonymous downloads at up to 60 files/minute, one Zstandard Parquet file per symbol/data type/UTC hour, with Binance Futures, Bybit, OKX and Hyperliquid coverage from 28 June 2025 (venue-specific start dates vary). The documented free path needs no API key, but the standard terms limit use to personal/internal research and prohibit raw-data redistribution, resale, repackaging or embedding it in a downstream product/dashboard/service without a separate licence.

Its own known-gaps register says its October 2026 data-quality release was **not yet deployed** when inspected. The register describes material issues including timestamp-unit/clock corrections, empty-book snapshot handling, incorrect REST snapshot resets for Bybit/Kraken/Lighter, stale or crossed reconstructed books, missing reconnect trades, duplicated snapshots, mark-price gaps and historical periods that cannot be recovered. Some corrections are planned or under review rather than published. A free download endpoint is not evidence of usable data. Do not use this provider for empirical calibration until the corrected release is deployed, affected historical partitions are identified, and a real sample passes independent reconstruction and reconciliation.

Sources: [CryptoHFTData API/free tier](https://www.cryptohftdata.com/), [terms and licensing](https://www.cryptohftdata.com/terms), [known gaps and corrections](https://www.cryptohftdata.com/docs/data-gaps-and-corrections).

### 8.4 Retrieval status

Direct unauthenticated download attempts against both Tardis and CryptoHFTData from this execution container failed at DNS resolution. The browser retrieval path could not retrieve the binary files. No data bytes were obtained from either provider or the Hugging Face dataset; no Parquet/CSV parsing, gzip/Parquet integrity, reconstruction, sequence, timestamp, depth or cross-channel tests were run. The alternatives above are source-level screens only, not data-quality passes.

### 8.5 Revised disposition

1. Keep Tardis as a no-key sample candidate; obtain actual L2 and paired trade bytes when a network path is available.
2. The Hugging Face community dataset has since been identified as Binance spot, not USDⓈ-M perpetual. Do not use it for perpetual calibration. It may be considered only as a generic parser/reconstruction fixture after an actual bounded file is obtained and independently validated.
3. Keep `crypto-lob-stream` as an MIT collector reference only; inspect source/tests before any future reuse and independently test ghost-level pruning, sequence gaps, resync and file-write durability.
4. Hold CryptoHFTData until its own corrections are deployed and licence scope is confirmed for the intended use.
5. No source is selected, no venue is selected, and the historical-data acceptance gate remains BLOCKED.


## 9. Hugging Face sample API and market-identity verification (16 November 2026)

### 9.1 Public metadata and bounded row previews

The Hugging Face dataset metadata and datasets-server endpoints were reachable through the research browser, even though direct binary downloads were not. The dataset is public, ungated and marked MIT. Its API reports:
- 251,388,868 total rows and 1,723,754,188 bytes (about 1.72 GB) across all configurations.
- Depth: 220,581,733 rows / 1,491,633,558 bytes.
- Snapshots: 224,000 rows / 1,659,329 bytes.
- Trades: 30,583,135 rows / 230,461,301 bytes.

The public row-preview API returned schema and records for the depth, snapshot and trade configurations. The observed fields were:
- Depth: `timestamp_ms`, `asset`, `side`, `price`, `quantity`, `first_update_id`, `last_update_id`, `exchange`.
- Snapshot: `timestamp_ms`, `asset`, `side`, `price`, `quantity`, `last_update_id`, `exchange`.
- Trades: `timestamp_ms`, `asset`, `trade_id`, `price`, `quantity`, `buyer_maker`, `exchange`.

The published dataset-server schemas do not expose a separate `exchange_ts` field. The collector source currently defines `timestamp_ms` as local receive time and keeps exchange event time separately as nullable `exchange_ts`; however, the exact collector version used to produce this dataset was not proven. Therefore feed-delay/event-time analysis cannot be assumed available from the published dataset.

### 9.2 Spot versus perpetual — resolved

The dataset rows use `exchange="binance"` and paths such as `depth/binance/BTCUSDT`. The inspected MIT collector source defines:
- `BinanceExchange` (name `binance`) using `wss://stream.binance.com:9443/stream` and REST snapshot endpoint `https://api.binance.com/api/v3/depth` — the spot adapter.
- A distinct `BinanceFuturesExchange` (name `binance_futures`) using `wss://fstream.binance.com/stream` and `https://fapi.binance.com/fapi/v1/depth` — the USDⓈ-M futures adapter.

The published dataset uses the spot adapter identity and does not contain `binance_futures` records. Its market type is therefore **spot**, not USDⓈ-M perpetual. This resolves the earlier ambiguity. It is rejected as direct perpetual execution-calibration data. It may still serve as a generic parser/reconstruction fixture if actual Parquet bytes are later obtained and validated.

### 9.3 Snapshot coverage warning

The first returned row in the snapshot configuration has timestamp `1780640988543` (2026-06-05 06:29:48.543 UTC). The first returned depth row has `1780534480378` (2026-06-04 00:54:40.378 UTC), and the first returned trade row has `1780534474149` (2026-06-04 00:54:34.149 UTC). Thus the first exposed snapshot anchor is about 29 hours 35 minutes later than the first exposed depth/trade records. The row API's first row is not a full inventory proof, but the earliest interval has no preceding snapshot anchor demonstrated by the returned data. Do not replay that interval until earlier anchors are found or the dataset publisher explains the discrepancy.

The dataset card also documents a roughly 43-minute capture interruption on 2026-07-05 affecting all three symbols, followed by a fresh snapshot; it must be treated as a hard reset, not a continuous sequence.

### 9.4 What was and was not tested

- **Performed:** retrieved public metadata; inspected all three dataset-server schemas and bounded row previews; checked representative timestamps, IDs, quantities, symbol and exchange fields; inspected collector source to resolve spot/perpetual adapter identity.
- **Not performed:** downloaded Parquet bytes; verified Parquet/Snappy integrity; parsed the actual monthly files locally; checked complete sequence continuity; reconstructed a full book; compared reconstructed levels with REST; checked the entire snapshot coverage; ran the collector's tests; or measured replay performance.
- One depth row-preview request returned HTTP 502, while metadata, snapshot/trade previews and a depth first-rows request returned data. This is an API preview failure, not a claim about the underlying Parquet file.

**Disposition:** source-level and bounded API inspection only. The dataset is spot-only and has an early snapshot-anchor warning. It is not accepted for perpetual calibration. The historical perpetual L2 acceptance gate remains BLOCKED.


## 10. OKX Swap / Tardis current-access investigation (16 November 2026)

### 10.1 Exchange metadata and instrument scope

The Tardis exchange metadata endpoint was reachable through the research fetch path:

- `https://api.tardis.dev/v1/exchanges/okex-swap`
- Response identifies `id=okex-swap`, `enabled=true`, historical coverage beginning `2019-03-30`, and available channels including `trades`, `trades-all`, `books-l2-tbt`, `books`, `bbo-tbt`, `mark-price`, `funding-rate`, `open-interest`, `instruments` and related statistics.
- The exchange-specific Tardis page identifies the market as OKX perpetual swaps and documents first-of-month CSV samples without a Data API key.
- A public first-of-month sample URL for a linear perpetual trade file was queried: `https://datasets.tardis.dev/v1/okex-swap/trades/2026/11/01/BTC-USDT-SWAP.csv.gz`. The research fetch path returned a binary body beginning with the gzip magic bytes (`1f 8b`), establishing that the URL resolves to a gzip response through that path. It did **not** provide a saved local file, HTTP headers, content length or a verifiable full-body hash.
- Matching L2 URLs were queried for `BTC-USDT-SWAP` and `BTC-USD-SWAP`. The fetch service reported `CRAWL_UNEXPECTED_CONTENT_TYPE` for both compressed L2 responses. This is a fetch/parser limitation, not evidence of HTTP 404, vendor outage or absent data.

The execution container was separately retried with HTTP HEAD against all three URLs; DNS resolution still failed with `[Errno -3] Temporary failure in name resolution`. The browser/fetch path and the container therefore have different network reachability. No actual file was placed in the working filesystem.

### 10.2 Feed-generation discontinuity — material

The current Tardis OKX Swap page (last updated 23 days before this research) lists API v5 channels as follows:

- `books-l2-tbt`: tick-by-tick L2 updates (10 ms), available until **2026-05-21**.
- `books`: incremental L2 depth updates (100 ms), available **2023-02-24 to 2024-07-19**, then again from **2026-05-21 onward**.
- `trades-all`: non-aggregated trade messages, available since 2023-10-19.
- `trades`: public swap trade execution stream.
- `bbo-tbt`: best bid/offer updates at 10 ms, available since 2022-05-05.
- `mark-price`, `funding-rate`, `open-interest`, `index-tickers` and `instruments` are also listed.

The 21 May 2026 boundary coincides with a documented change in Tardis collection infrastructure from AWS Hong Kong to GCP Tokyo and a change in the OKX public WebSocket endpoint. Do not assume a homogeneous L2 event process across this boundary. The 10 ms tick-by-tick channel is not documented as available after that date; the currently listed `books` channel is 100 ms. This affects observable event granularity, queue-depletion inference, timing and comparisons between historical periods.

Sources:
- [Tardis OKX Swap historical coverage and channel dates](https://docs.tardis.dev/historical-data-details/okex-swap)
- [Tardis OKX Swap exchange metadata](https://api.tardis.dev/v1/exchanges/okex-swap)
- [Tardis downloadable CSV rules and schema](https://docs.tardis.dev/downloadable-csv-files)
- [OKX official historical market data portal](https://www.okx.com/historical-data)

### 10.3 CryptoHFTData correction status rechecked

The current public [Known Gaps & Corrections](https://www.cryptohftdata.com/docs/data-gaps-and-corrections) page was re-fetched on 16 November 2026. It still states that the 2026-10 data-quality release is **not yet deployed**. Its own table continues to identify material order-book issues for `okx_futures` and other venues, including empty-book snapshots omitted from earlier files; the corrections are not recoverable for affected historical periods. It also lists planned, not yet published, OKX funding timestamp and ticker-volume history repairs, and planned OKX trade backfill from REST. These are explicit provider disclosures, not independent observations by IDEAL.

**Disposition remains HOLD.** Do not use CryptoHFTData for calibration until deployment status changes, corrected partition boundaries are explicit, and independently downloaded samples pass the same reconstruction and cross-check matrix. Confirm permitted use separately; the provider's standard terms remain restrictive for redistribution and downstream embedding.

### 10.4 Updated result

- **Improved:** Tardis exchange metadata is reachable through the research fetch path; a November 2026 OKX linear-perpetual trade sample URL returns a gzip response through that path; current OKX channel dates and the post-May-2026 100 ms L2 feed are documented.
- **Not achieved:** no L2 or trade artifact is saved locally; no response headers, byte counts, hashes, gzip integrity, CSV schema, row counts, timestamps, sequence continuity or reconstruction results are available.
- **No pass:** the historical perpetual L2 acceptance gate remains **BLOCKED**. The trade URL response alone is not a usable paired dataset and does not validate order-book quality.
- **No selection:** Tardis remains a no-key sample-evaluation candidate only. No venue, data vendor, exchange account, API key, paid service or runtime component is selected or authorised.
- **Next test:** obtain the matching 2026-11-01 `incremental_book_L2`, `trades` and `derivative_ticker` artifacts through a network path that can save exact bytes; hash and validate them before any replay. Preserve the 2026-05-21 feed-generation boundary as a separate stratum in all analysis.


## 11. OKX native public historical L2 archive — endpoint and matching-trade discovery (16 November 2026)

### 11.1 Public endpoint contract

The OKX public REST endpoint is:

`GET https://www.okx.com/api/v5/public/market-data-history`

A source-level inspection of the MIT `burakoner/OKX.Api` client at commit `1dd5dd09d04627eb27a6b0b15bac980287295b1b` confirms the client sends this request with `signed: false`. Its module enum maps:
- `4`: 400-level order book
- `5`: 5,000-level order book
- `6`: 50-level order book (being deprecated)
- `1`: tick-by-tick trade history

The library changelog records that it checked the endpoint against unsigned production requests, including the maximum 10-inclusive-day/month query boundary. The current documented contract states 5 requests per 2 seconds per IP, order-book files normally available T+3, and 10 inclusive calendar days for daily requests. Order-book modules 4/5/6 use UTC calendar dates; trade module 1 uses UTC+8 calendar dates. This timezone difference is important when pairing trades to an order-book UTC day.

Sources:
- [OKX API change log — historical market data endpoint introduced](https://www.okx.com/docs-v5/log_en/#2025-09-02)
- [OKX API change log — query window reduced to 10](https://www.okx.com/docs-v5/log_en/#2026-08-06)
- [OKX public historical-data endpoint implementation and tests (MIT reference client)](https://github.com/burakoner/OKX.Api)
- [OKX official historical market data portal](https://www.okx.com/historical-data)

### 11.2 Live metadata-query observations

The public endpoint was queried through the research fetch path. It returned JSON `code=0` with file metadata and direct CDN URLs. These are metadata responses only; the archive files themselves were not downloaded.

| Query | Response | File size reported by OKX | Direct archive |
|---|---|---:|---|
| Module 5, SWAP, BTC-USDT, 2026-11-12 UTC | `code=0` | 177.63 MB | [BTC 5,000-level L2, 12 Nov](https://static.okx.com/cdn/okx/match/orderbook/pro/L2/5000lv/daily/20261112/BTC-USDT-SWAP-L2orderbook-5000lv-2026-11-12.tar.gz) |
| Module 5, SWAP, BTC-USDT, 2026-11-11 UTC | `code=0` | 170.27 MB | [BTC 5,000-level L2, 11 Nov](https://static.okx.com/cdn/okx/match/orderbook/pro/L2/5000lv/daily/20261111/BTC-USDT-SWAP-L2orderbook-5000lv-2026-11-11.tar.gz) |
| Module 4, SWAP, BTC-USDT, 2026-11-12 UTC | `code=0` | 477.07 MB | [BTC 400-level L2, 12 Nov](https://static.okx.com/cdn/okx/match/orderbook/pro/L2/400lv/daily/20261112/BTC-USDT-SWAP-L2orderbook-400lv-2026-11-12.tar.gz) |
| Module 5, SWAP, ETH-USDT, 2026-11-12 UTC | `code=0` | 149.22 MB | [ETH 5,000-level L2, 12 Nov](https://static.okx.com/cdn/okx/match/orderbook/pro/L2/5000lv/daily/20261112/ETH-USDT-SWAP-L2orderbook-5000lv-2026-11-12.tar.gz) |

The endpoint response for BTC 5,000-level L2 on 12 November identifies filename `BTC-USDT-SWAP-L2orderbook-5000lv-2026-11-12.tar.gz`, instrument family `BTC-USDT`, instrument type `SWAP`, and a 177.63 MB file. The corresponding 400-level module is a distinct archive and reports 477.07 MB. File size alone does not establish update cadence, event completeness or which module is better for a given execution study; inspect both file formats and event densities before choosing.

### 11.3 Matching trade archive metadata and timezone alignment

A module 1 query for `BTC-USDT` SWAP, with begin `1794412800000` and end `1794499200000`, returned `code=0` and two trade ZIP files:

- [BTC-USDT-SWAP trades, 12 Nov 2026 (UTC+8 file date)](https://static.okx.com/cdn/okex/traderecords/trades/daily/20261112/BTC-USDT-SWAP-trades-2026-11-12.zip?v=1001), 17.85 MB.
- [BTC-USDT-SWAP trades, 13 Nov 2026 (UTC+8 file date)](https://static.okx.com/cdn/okex/traderecords/trades/daily/20261113/BTC-USDT-SWAP-trades-2026-11-13.zip?v=1001), 30.43 MB.

Together these two UTC+8 trade-date files cover the UTC book day 2026-11-12 from 00:00 to 24:00, with an 8-hour boundary inside the 13 November trade file. The matching interval must be filtered by actual trade timestamps after extraction; do not pair files by identical filename date alone. The two trade archives report 48.28 MB combined. Combined with the 177.63 MB 5,000-level L2 archive, the metadata-reported download total for the first paired sample is approximately 225.91 MB, before any additional derivative context or redundant day needed for boundary checks.

### 11.4 What is proven and what is not

**Proven at metadata/query level:**
- The unauthenticated public endpoint returned successful metadata for current-dated BTC and ETH SWAP order-book files and BTC SWAP trade files.
- OKX provides 5,000-level order-book archive links for dates after 1 November 2025.
- Matching trade archive links are available through the same endpoint.
- Order-book and trade files use different calendar-date conventions (UTC versus UTC+8); correct pairing requires timestamp-based filtering.
- The endpoint supplies filenames, direct URLs and provider-reported sizes.

**Not proven:**
- The direct CDN archive bytes have not been retrieved into the local working environment.
- No HTTP status, content length, archive SHA-256, tar/gzip integrity, member listing, JSONL schema or row count has been verified.
- No snapshot cadence, delta cadence, sequence identifiers, event ordering, timestamp units, empty-book representation, depth semantics or reconnect handling has been independently established from the actual archive.
- No L2 reconstruction, trade/book alignment, independent oracle comparison, stale/crossed/duplicate detection or replay benchmark has been run.
- Public endpoint availability does not itself settle data licensing, permitted downstream use, NZ venue eligibility or live trading eligibility.

The container still has DNS resolution failures for external hosts. The research fetch path can retrieve the JSON metadata but does not provide the large archive as a local file. The reported file size is substantial (170–477 MB per day for the queried examples), so download, storage and decompression costs must be measured before scaling beyond a bounded sample.

### 11.5 Revised next test and disposition

Prioritise the OKX 2026-11-12 BTC-USDT-SWAP module 5 archive and the two matching trade ZIPs. Retrieve them through a network path that can save exact bytes; capture headers, byte counts and SHA-256; inspect the compressed archive and schema; then build an independent parser/reconstructor. Keep module 4 as a comparison candidate, not a default selection. Add at least the 11 November module 5 day to test day-boundary snapshot continuity.

**The historical-data acceptance gate remains BLOCKED.** This is the first concrete public exchange-native L2 + trade archive lead with successful current-date metadata, not a data-quality pass or source selection. Phase 01 remains IN PROGRESS; Phase 02 remains LOCKED.
