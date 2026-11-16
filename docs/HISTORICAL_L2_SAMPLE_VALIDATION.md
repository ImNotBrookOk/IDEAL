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


### 11.6 Direct archive retrieval attempt

The direct 177.63 MB OKX CDN archive URL was opened through the web retrieval interface, which returned an inaccessible-file error for the `.tar.gz` resource. The container download utility then refused the URL because it had not been successfully viewed through that interface. This is a tooling/access-path limitation; it is not evidence that the CDN returned an HTTP error or that the file is unavailable. No partial archive was written. The actual-file validation gate remains blocked.


## 12. OKX 2026-11-12 BTC-USDT-SWAP sample: byte-level and reconstruction validation (16 November 2026)

### 12.1 Retrieval and artifact provenance

The isolated GitHub Actions research run [#43766633587](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43766633587) completed successfully on branch `research/okx-l2-sample-2026-11-16`, head commit `8c3bfd549276637327be9c75c6113a03e79a4bf3`. All four job steps completed successfully. No secrets, exchange credentials or paid runner were used.

- Artifact ID: `14182173189`
- Artifact name: `okx-btc-usdt-swap-historical-sample`
- Artifact size: 236,127,656 bytes
- GitHub artifact SHA-256: `f4a664471e12a28314c726e3d51335b630361eb05d7ecf4330f539a58130b94d`
- Artifact expiry: 2026-11-18 21:58:54 UTC (3-day retention configured by the workflow)
- The artifact was downloaded again through the GitHub artifact API into the current analysis workspace. Its local SHA-256 exactly matched GitHub's recorded artifact digest. ZIP integrity test passed with no errors.

Source archives inside the artifact:

| File | Bytes | SHA-256 |
|---|---:|---|
| BTC 5,000-level L2, 2026-11-12 UTC | 186,255,630 | `bab7213b2944a8f8c9540064d8c5b217c84d82d41f17c2e30fa426800e42c99b` |
| BTC trades, 2026-11-12 UTC+8 date | 18,720,850 | `1da901d447e66aa9bd9b0e57c9711cec27720adc093352d6456ea453a114545e` |
| BTC trades, 2026-11-13 UTC+8 date | 31,904,876 | `cc3cbef246c1efb3c477eb05816a4d1f32843ae5a5996688a32ebab216d87eb8` |

The L2 HTTP response recorded status 200 and content-length 186,255,630. Both trade ZIP responses also returned HTTP 200 with content-lengths matching the downloaded byte counts. TAR/GZIP and both ZIP integrity tests passed. The L2 tar contains one NDJSON member, `BTC-USDT-SWAP-L2orderbook-5000lv-2026-11-12.data`, which expands to 891,030,123 bytes.

### 12.2 L2 schema, cadence and full-day reconstruction

An independent streaming parser processed all 86,400 NDJSON records:

- Instrument: `BTC-USDT-SWAP` for all records.
- 96 full snapshots and 86,304 incremental updates.
- Timestamps span 2026-11-12 00:00:00.002 UTC through 23:59:59.003 UTC.
- Every snapshot contains exactly 5,000 bid and 5,000 ask levels.
- Snapshot intervals are approximately 900,000 ms (15 minutes); observed intervals range from 899,994 to 900,008 ms.
- Update timestamps are predominantly 1,000 ms apart: 86,349 of 86,399 adjacent intervals are exactly 1,000 ms.
- There are 14 larger timestamp deviations outside the 900–1,100 ms band, arranged as seven adjacent long/short pairs. Long intervals range from 1,130 to 1,429 ms; the compensating short intervals range from 570 to 870 ms. The remaining deviations are small jitter around one second.
- Each update changes a median 143 ask levels and 143 bid levels (283 combined); per-side p95 is 586, with maxima of 3,619 asks and 3,986 bids in a single record. The maximum combined update contains 7,586 price-level entries.
- 7,504,519 zero-quantity level updates were interpreted as deletions, consistent with the documented L2 aggregation rule.
- Full state was rebuilt by replacing the book on each snapshot and applying absolute price-level quantity updates/deletions thereafter.
- Across all 86,400 reconstructed states: zero empty books, zero crossed books and zero locked books. No negative price/quantity values were observed by the parser.

The archive records are sampled at approximately one-second intervals; they are not a tick-by-tick exchange event stream. The file has no sequence IDs or per-record checksum fields. Consequently, the clean reconstruction and absence of crossed/empty states do **not** prove that no source updates were omitted between records. The 14 timestamp deviations need provider-level explanation or independent corroboration; the paired pattern may reflect timestamp scheduling/serialization, but that is not established.

Each archived price-level row contains three values. OKX's public WebSocket documentation illustrates four values for live order-book levels (price, size, liquidated-order count, order count). The historical archive's three-value representation therefore must not be assigned the same field semantics without a specific archive schema. Treat the third field as unresolved; do not use it as an order-count or liquidation feature yet. See [OKX WebSocket order-book format and aggregation rules](https://github.com/okx/exchain-docs-api/blob/main/_ws.md#checksum).

### 12.3 Trade-file validation and UTC pairing

Both trade ZIPs contain one CSV with columns:
`instrument_name, trade_id, side, price, size, created_time, source`.

All 8,703,176 rows across both files were parsed:

- 2026-11-12 UTC+8 file: 3,222,603 rows; timestamps span 2026-11-11 16:00:00.054 UTC to 2026-11-12 15:59:59.949 UTC.
- 2026-11-13 UTC+8 file: 5,480,573 rows; timestamps span 2026-11-12 16:00:00.045 UTC to 2026-11-13 15:59:59.999 UTC.
- Correctly filtered 2026-11-12 UTC book-day interval [00:00, 24:00): 3,224,415 trades (2,288,403 from the 12 November UTC+8 file and 936,012 from the 13 November UTC+8 file).
- The filtered target-day trade timestamps range from 00:00:00.639 UTC to 23:59:59.553 UTC.
- Trade IDs are strictly increasing across the concatenated files; no non-monotonic or adjacent duplicate IDs were observed.
- No malformed rows, invalid sides, non-positive prices or non-positive sizes were observed.
- Side counts across both files: 4,406,929 sell and 4,296,247 buy.

This confirms date-level pairing and basic CSV integrity, not event-level book/trade synchronization. A full trade-to-preceding-BBO alignment test has not yet completed. Since the book is sampled once per second and has no sequence IDs, tick-level trade timestamps cannot be assumed to align to the exact book state at execution time.

### 12.4 Revised suitability assessment

**Partial pass:** byte retrieval, digest verification, compressed archive integrity, complete parsing, one-day L2 reconstruction and basic trade-file validation all passed for this sample.

**Still blocked:** sequence continuity, lost-update detection, exact timestamp provenance, event-level trade/book alignment, independent cross-check against an exchange reference, and representativeness across multiple dates/instruments remain unproven.

The sample can potentially support coarse one-second spread, visible-depth and imbalance research, subject to further timestamp and sampling-bias checks. It is not sufficient by itself for true FIFO queue-position estimation, passive-fill calibration, or high-fidelity intrasecond market-impact modelling. The archive is L2 market-by-price, not L3 order identity.

**Disposition remains BLOCKED for execution calibration and historical-data acceptance.** This is a successful retrieval and a meaningful partial data-quality pass, not approval of OKX as the selected venue/vendor. Phase 01 remains IN PROGRESS; Phase 02 remains LOCKED.

### 12.5 Next tests

1. Re-run the reconstruction with independent implementation/golden fixtures and validate snapshot ordering, duplicate price keys, update semantics and book-depth truncation.
2. Investigate the seven long/short timestamp interval pairs; compare another day and the 400-level module.
3. Complete trade-to-sampled-BBO alignment, explicitly measuring sample age and the proportion of trades outside the preceding sampled spread. Treat this as a staleness diagnostic, not proof of bad trades.
4. Obtain the adjacent 2026-11-11 5,000-level archive and verify day-boundary behavior and repeated schema/cadence.
5. Preserve the source artifact beyond its current 3-day GitHub retention window only through an approved, licence-compatible research-storage method. Do not commit raw vendor archives to the public repository.


### 12.6 Follow-up structural and trade-ID audit (16 November 2026)

A second pass refined the update-volume and field-semantics assessment.

- The L2 stream contains 39,035,798 price-level rows across snapshots and updates.
- There are 7,504,519 zero-quantity update rows, interpreted as price-level deletions by the reconstruction logic.
- Across 86,304 update messages, changed price levels per message range from 47 to 7,586, with a median of **283 total levels across both sides** (not 283 per side).
- All 96 snapshots contain exactly 5,000 bid and 5,000 ask levels.
- Of 86,399 adjacent timestamp intervals, 86,349 are exactly 1,000 ms; 50 differ from 1,000 ms, of which 14 are outside the 900–1,100 ms tolerance. The 14 outliers form seven long/short pairs. Snapshot intervals are approximately 900,000 ms with small jitter.
- No negative quantities, empty books, crossed books or locked books were observed during full reconstruction.

Every historical price-level row has exactly three fields: price, quantity and a third integer. Current OKX live RPI documentation describes four-field book levels (price, total quantity, non-RPI quantity, order count); older general WebSocket documentation also describes four fields with liquidation count and order count. Neither schema proves the meaning of the third field in this historical archive. **Treat it as opaque; do not use it as order count, liquidation count or queue-size evidence until OKX confirms the historical module-5 schema.** Sources: [current OKX API documentation](https://app.okx.com/docs-v5/log_en/), [OKX WebSocket field description](https://github.com/okx/exchain-docs-api/blob/main/_ws.md).

The two UTC+8 trade files were independently scanned:
- 12 Nov file: 3,222,603 rows; trade IDs 3,064,471,065–3,067,693,667.
- 13 Nov file: 5,480,573 rows; trade IDs 3,067,693,668–3,073,174,240.
- IDs strictly increase within each file and continue exactly across the file boundary (next first ID = previous last ID + 1). No malformed rows, invalid sides, non-positive prices/sizes, adjacent duplicate IDs or ID backsteps were observed.
- The matching 2026-11-12 UTC book interval contains 3,224,415 trades after timestamp filtering.

This strengthens file-level integrity, but does not prove every exchange event is present in the L2 archive. Trade IDs establish ordering in trade files only; they do not substitute for missing L2 sequence IDs.

A second attempt to build a full per-record BBO alignment series exceeded the local analysis execution time limit and was interrupted. **No trade-vs-preceding-BBO alignment statistic is claimed.**

### 12.7 Corrected next-test order

1. Resolve historical third-field semantics from an authoritative module-5 archive schema; until then, preserve it as opaque.
2. Compare module 4 and module 5 for the same date.
3. Retrieve the adjacent 2026-11-11 module-5 archive to test boundary and schema consistency.
4. Complete trade-to-preceding-BBO alignment with a more efficient implementation; report sample age, outside-spread rate and sensitivity to one-second sampling.
5. Keep sequence continuity and loss detection blocked unless OKX supplies a sequence-bearing historical format or an independent reference validates event completeness.


### 12.8 400-level module 4 and no-lookahead trade alignment (16 November 2026)

This section supersedes the earlier statements in sections 12.3–12.7 that full trade-to-preceding-BBO alignment remained incomplete. The alignment has now been completed with a streaming implementation that applies a strict no-lookahead rule: trades at the same timestamp as a book update are evaluated against the preceding book state because the archive provides no event sequence to establish ordering.

Two additional OKX archives were retrieved and fully reconstructed through isolated research workflows:

| Archive | Compressed bytes | Uncompressed member | Records | Snapshots | Updates |
|---|---:|---:|---:|---:|---:|
| Module 4, BTC-USDT-SWAP 400-level, 12 Nov UTC | 500,244,886 | 3,048,526,067 | 6,604,203 | 96 | 6,604,107 |
| Module 5, BTC-USDT-SWAP 5,000-level, 11 Nov UTC | 178,537,085 | 857,560,394 | 86,400 | 96 | 86,304 |

The 400-level archive SHA-256 is `6dd55534ddd376c6995bfac584f1e1a19ed64083b76b542da61ee488cacbdfce`; the 11 November 5,000-level archive SHA-256 is `b7a2e597f7e286d6b14c9fd50abe92a067af76b0129e99a04726a795ed44829f`.

**Module 4 (400 levels):**
- Every snapshot contains exactly 400 bid and 400 ask levels; 96 snapshots are approximately 15 minutes apart.
- 109,286,945 price-level rows were processed, including 20,114,734 zero-quantity deletions. Update messages changed 1–1,183 levels, with a median of 6 combined bid/ask levels.
- All 6,604,203 reconstructed states were valid; no empty, crossed or locked books were observed.
- 85.957% of the 6,604,202 adjacent record intervals were exactly 10 ms; 7.291% were 20 ms, 3.154% were 30 ms, 1.416% were 40 ms and 0.817% were 50 ms. Longer intervals occur and must be treated as staleness, not interpolated away.

**Module 5 (5,000 levels, 11 November):**
- Every snapshot contains exactly 5,000 bid and 5,000 ask levels; 96 snapshots.
- 37,499,572 price-level rows, including 6,941,995 zero-quantity deletions; median 279 combined bid/ask level changes per update.
- All 86,400 reconstructed states were valid; no empty, crossed or locked books.
- 86,353 of 86,399 adjacent intervals (99.947%) were exactly 1,000 ms. This confirms the one-second cadence observed in the 12 November module-5 sample.

**Historical record schema:** the first five module-4 records contained only `action`, `asks`, `bids`, `instId` and `ts`. No `seqId`, `prevSeqId`, `checksum` or `local_timestamp` field was present. Every sampled level tuple had three fields. The third field is an integer, but its meaning remains unverified; do not interpret it as order count, liquidation count or queue size without an authoritative historical-module schema. No sequence IDs/checksums means lost-update detection remains unproven.

**No-lookahead alignment to module-4 BBO:** the two UTC+8 trade ZIPs were combined and filtered by actual timestamps to the 12 November UTC book day. All 3,224,415 matching trades were aligned to a preceding valid BBO. Zero trades lacked a preceding book state and zero matched invalid book states.

| Measurement | 400-level module 4 | 5,000-level module 5, 12 Nov |
|---|---:|---:|
| Median preceding-book age | 6 ms | 489 ms |
| 95th-percentile preceding-book age | 10 ms | 947 ms |
| Maximum preceding-book age | 509 ms | 999 ms |
| Trades outside preceding sampled spread | 62.584% | 76.71% |
| Outside-distance p95 | 1.40 bps | 4.86 bps |

For the 400-level alignment:
- 311,016 trades (9.646%) shared a timestamp with a book update and were conservatively evaluated against the prior book.
- 98.542% of trade sides were directionally consistent with the preceding BBO (buy at/above ask or sell at/below bid); side mismatch was 1.458%.
- Outside-spread distance was p50 0.35 bps, p90 1.01 bps, p95 1.40 bps, p99 2.82 bps and maximum 11.81 bps.
- Preceding-book ages exceeded 10 ms for 161,204 trades (4.999%), 20 ms for 76,469 (2.372%), 50 ms for 16,390 (0.508%), 100 ms for 2,139 (0.066%) and 250 ms for 67 (0.0021%).

The outside-spread percentage is not a direct measure of bad trades: even a 10 ms sampled book can miss intervening state changes. The 98.542% directional consistency and much lower sample age are encouraging, but neither proves event ordering or exact passive fills. The 509 ms maximum age demonstrates a non-zero stale-sample tail and must be accounted for explicitly.

**Updated disposition:** module 4 400-level data is a viable research candidate for 10 ms sampled spread, visible-depth, imbalance, liquidity-dynamics and conservative market-impact/slippage research. It is not sufficient for exact FIFO queue-position or passive-fill calibration: no L3 order identity, no sequence IDs/checksum, no authoritative third-field schema, and no exact event ordering. Module 5 is a deeper but one-second sampled liquidity reference.

The final no-lookahead alignment and initial research acceptance assertions passed in [workflow run #43773844334](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43773844334). The initial gates were: non-zero aligned trades, zero no-preceding-book trades, zero invalid-book matches, p95 sample age at most 20 ms, and side consistency at least 98%.

**Phase 01 remains IN PROGRESS; Phase 02 remains LOCKED.** No venue/vendor is selected and no runtime integration is approved.

### 12.9 Next validation gates

1. Retrieve and reconstruct a second 400-level day (11 or 13 November) to test cadence, snapshot behavior, schema and alignment stability.
2. Characterize the 509 ms sample-age maximum and all >50 ms gaps by time-of-day and clustered duration.
3. Obtain authoritative OKX historical archive documentation for the third level field; continue treating it as opaque.
4. Define conservative execution-model bounds. Taker impact and spread/slippage research may proceed with 10 ms samples and staleness controls; passive fills must not assume FIFO or exact queue position.
5. Continue independent-source, licensing and venue-eligibility checks before any venue selection or runtime integration.


### 12.10 Consecutive-day 400-level reconstruction and field-schema corroboration (16 November 2026)

The adjacent-day workflow [#43774295757](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43774295757) successfully retrieved and independently reconstructed both 11 and 12 November 2026 BTC-USDT-SWAP module-4 archives, alongside the 11 November module-5 reference.

| Measurement | 11 Nov 400-level | 12 Nov 400-level |
|---|---:|---:|
| Compressed archive bytes | 452,866,800 | 500,244,886 |
| Uncompressed NDJSON bytes | 2,818,674,224 | 3,048,526,067 |
| Records | 6,630,044 | 6,604,203 |
| Snapshots | 96 | 96 |
| Updates | 6,629,948 | 6,604,107 |
| Snapshot depth per side | exactly 400 | exactly 400 |
| Price-level rows | 99,009,762 | 109,286,945 |
| Zero-quantity deletions | 17,885,894 | 20,114,734 |
| Median combined levels changed/update | 6 | 6 |
| Minimum/maximum changed levels/update | 1 / 1,218 | 1 / 1,183 |
| Empty/crossed/locked/invalid reconstructed states | 0 | 0 |
| Exactly 10 ms intervals | 5,697,158 / 6,630,043 (85.929%) | 5,676,756 / 6,604,202 (85.957%) |

Both days have 96 full snapshots, consistent with roughly 15-minute snapshot spacing. The two consecutive days show closely matching record cadence and median update density, while total level rows and deletion counts vary with market activity. This supports repeatability of the archive's structure across the two sampled days; it does not establish lossless sequence continuity.

SHA-256:
- 11 Nov 400-level: `e4a315e221c106fb59da079632ce4d4605e7e8e22cab810f350959a8950c7426`
- 12 Nov 400-level: `6dd55534ddd376c6995bfac584f1e1a19ed64083b76b542da61ee488cacbdfce`
- 11 Nov 5,000-level: `b7a2e597f7e286d6b14c9fd50abe92a067af76b0129e99a04726a795ed44829f`

**Third tuple field — refined interpretation:** OKX's official API documentation defines the three-element order-book tuple in GET /api/v5/market/books-full as [price, quantity, number of orders at the price] (official docs: https://app.okx.com/docs-v5/en/, section “GET / Full order book”, response parameter examples). The historical archive records also have exactly three elements and their third value is a nonnegative integer, so “order count” is now the leading, strongly corroborated interpretation. In both reconstructed 400-level days, the number of third-field zero values exactly matched the number of zero-quantity deletion rows (17,885,894 on 11 Nov; 20,114,734 on 12 Nov), which is consistent with a zero order count on a deleted level. However, the official documentation retrieved does not explicitly state that the downloadable module-4/module-5 archive serializer uses the same tuple contract. The current books/books-l2-tbt WebSocket schema is a four-element tuple: price, quantity, deprecated always-zero field, order count. Consequently, preserve the raw third value, do not make it a required feature, and retain archive-specific semantic confirmation as an outstanding documentation question. It is not a liquidation count or a queue-position signal based on available evidence.

The adjacent-day workflow passed all six archive audit unit tests, full archive integrity checks, and complete reconstruction for all three files. Audit artifact ID `14185851827` (SHA-256 `db78a9d5611552974f9bc581cf8c3cc1328dfdad7112e4e28dce20034e31e2e6`) contains only small manifests and summaries, not raw archives. Artifact expires 18 November 2026 at 23:28 UTC.

**Disposition:** consecutive-day structural repeatability is provisionally passed. Trade-to-book alignment on both days is the next gate; the previous one-day 12 November alignment remains the only completed event-level comparison until workflow #43776264061 finishes.


### 12.11 Historical-versus-live feed entitlement boundary (16 November 2026)

Historical archive availability must not be conflated with live WebSocket entitlement. OKX's official API guide states that:
- `books-l2-tbt` provides 400 depth levels with incremental updates every 10 ms;
- subscription to the 400-depth `books-l2-tbt` channel is restricted to VIP4 and above;
- standard `books` provides 400 depth levels with incremental updates every 100 ms;
- `bbo-tbt` provides one depth level with snapshots every 10 ms when changes occur.

Official source: https://app.okx.com/docs-v5/en/, “WS / Order book channel” (the channel cadence and VIP restriction are stated in the channel description).

This creates a material live-parity constraint: public historical 10 ms 400-level archives do not prove that IDEAL can obtain the equivalent live feed on an ordinary account tier. A future deployment would need either confirmed VIP4 entitlement, a tested 100 ms full-depth feed, or a 10 ms BBO-only feed with explicitly reduced depth-dependent capabilities. Do not train/calibrate on 10 ms full-depth data and silently execute against 100 ms depth as if the data were equivalent. Any change in live feed granularity requires separate calibration, latency/staleness controls and strategy eligibility review.

No VIP status, account or live feed was requested or connected. This is a research constraint only.


### 12.12 Two-day no-lookahead trade-to-book alignment (16 November 2026)

The expanded adjacent-day alignment workflow [#43776264061](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43776264061) completed successfully. It retrieved 11 and 12 November 400-level L2 archives plus the UTC+8 trade archives covering both UTC days, ran the six focused alignment unit tests, inspected the historical schema, and aligned trades to the strictly preceding valid BBO. At equal timestamps, the trade is consumed before applying the book update; this avoids look-ahead when archive ordering cannot establish which event occurred first.

Both days passed the initial independent quality gates: non-zero aligned trades, zero trades without a preceding book, zero invalid-book matches, p95 preceding-book age <=20 ms and directional side consistency >=98%.

| Measurement | 11 Nov 2026 | 12 Nov 2026 |
|---|---:|---:|
| L2 book records | 6,630,044 | 6,604,203 |
| Aligned trades | 2,597,825 | 3,224,415 |
| Trades without preceding book | 0 | 0 |
| Trades on invalid book state | 0 | 0 |
| Median preceding-book age | 6 ms | 6 ms |
| p95 preceding-book age | 18 ms | 10 ms |
| Maximum preceding-book age | 497 ms | 509 ms |
| Same-timestamp trades (conservatively assigned to prior book) | 244,183 (9.400%) | 311,016 (9.646%) |
| Trade-side directional consistency | 99.118% | 98.542% |
| Outside preceding sampled spread | 64.445% | 62.584% |
| Outside-spread distance p95 | 1.35 bps | 1.40 bps |

Preceding-book age tail by day:
- 11 Nov: >10 ms 194,754 (7.497%); >20 ms 96,808 (3.727%); >50 ms 20,039 (0.771%); >100 ms 2,608 (0.100%); >250 ms 177 (0.0068%).
- 12 Nov: >10 ms 161,204 (4.999%); >20 ms 76,469 (2.372%); >50 ms 16,390 (0.508%); >100 ms 2,139 (0.066%); >250 ms 67 (0.0021%).

Outside-spread distance distributions:
- 11 Nov: p50 0.34 bps, p90 0.98 bps, p95 1.35 bps, p99 2.76 bps, maximum 10.38 bps.
- 12 Nov: p50 0.35 bps, p90 1.01 bps, p95 1.40 bps, p99 2.82 bps, maximum 11.81 bps.

The high outside-spread fraction does not mean 62–64% of trade rows are corrupt. A sampled 10 ms BBO may miss intermediate book states between updates; timestamp ties are conservatively compared with the preceding state; the archive has no sequence IDs to resolve exact ordering. High side consistency (98.54–99.12%) and low median/p95 ages are encouraging, but these are diagnostics, not proof of exact event synchronization or passive execution. The 497–509 ms maximum preceding-state ages demonstrate a small but real stale tail; a runtime consumer must fail closed or apply an explicit staleness policy rather than extrapolate or use stale depth for execution decisions.

The workflow's initial acceptance assertions passed separately for each day. Artifact ID `14186960490`, SHA-256 `4e1e7cd7dece1882b72a07c85140aec39c95faa859e845de8be7eb09673ba55c`, contains only the summaries and small manifests, expires 18 November 2026 23:47 UTC. Raw archives were deleted before upload and were not committed.

**Updated disposition:** two-day structural reconstruction and two-day no-lookahead trade/BBO alignment are provisionally passed for research. The 400-level historical data is viable for sampled spread/depth/imbalance and conservative taker-impact research, subject to staleness controls and the unresolved sequence-continuity limitation. It is not FIFO/queue-position or exact passive-fill grade. Live 10 ms full-depth feed entitlement and NZ derivatives-issuer eligibility remain separate hard gates. See sections 12.11 and the exchange shortlist section 13.10.


**Staleness sensitivity (trade coverage if a research analysis excludes older preceding books):**

| Maximum preceding-book age | 11 Nov retained trades | 12 Nov retained trades |
|---|---:|---:|
| <=10 ms | 2,403,071 (92.503%) | 3,063,211 (95.001%) |
| <=20 ms | 2,501,017 (96.273%) | 3,147,946 (97.628%) |
| <=50 ms | 2,577,786 (99.229%) | 3,208,025 (99.492%) |
| <=100 ms | 2,595,217 (99.900%) | 3,222,276 (99.934%) |
| <=250 ms | 2,597,648 (99.993%) | 3,224,348 (99.998%) |

This is a sensitivity table, not a validated production staleness threshold. It shows that a 50 ms analysis cutoff would retain over 99.2% of trade rows in these two samples while excluding the long stale tail. Any later execution model should report results across multiple age cutoffs and must not interpolate stale book depth. A strategy requiring a stricter 10 ms book-age bound would lose 5.0–7.5% of observations, depending on day.


### 12.13 Independent Tardis public normalized-L2 sample validation (16 November 2026)

The isolated Tardis workflow [#43777192211](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43777192211) successfully retrieved the first-of-month public sample for Binance USDⓈ-M Futures BTCUSDT, 1 November 2026, without an API key:
- L2: `https://datasets.tardis.dev/v1/binance-futures/incremental_book_L2/2026/11/01/BTCUSDT.csv.gz`
- Trades: `https://datasets.tardis.dev/v1/binance-futures/trades/2026/11/01/BTCUSDT.csv.gz`

File sizes:
| File | Compressed | Uncompressed |
|---|---:|---:|
| Incremental L2 | 429.9 MB | 6,461,142,795 bytes |
| Trades | 9.09 MB | 103,671,148 bytes |

SHA-256:
- L2: `8856e6e61b480976d9e1bc7ea49d4d18d25b281c56c6e6523bee6179d9558061`
- Trades: `635a750afca5659cf7848487a1a8105e9dd8a38ce57254689b77ee7ec596efc4`

The new independent CSV parser/reconstructor was tested with six focused unit tests, then used on the full 79,438,130-row L2 file:
- 3,242,436 local-timestamp message groups;
- one initial snapshot and 3,242,435 update messages;
- zero rows before the first snapshot;
- 7,260,093 zero-amount level deletions;
- all 3,242,436 reconstructed message states valid (no empty, crossed or locked BBO);
- maximum gap between processed message groups 276.101 ms;
- exchange timestamps covered 2026-11-01 UTC;
- final reconstructed BBO at end of file: 78,313.0 / 78,313.1.

The trade file contained 1,190,743 rows: 587,069 buy and 603,674 sell. All rows had the expected schema, positive finite prices/amounts, valid side values and nondecreasing local timestamps. Local timestamps ranged from 1793491200019430 to 1793577599972800 microseconds.

This validates that the documented Tardis normalized incremental-L2 CSV format can be parsed and reconstructed on a full first-of-month Binance Futures sample. It does not validate the same exchange-day's fills against BBO, prove source-side sequence continuity, provide L3/FIFO order identity, or establish the license rights for commercial use of the data. The 276 ms maximum message gap is a measured property of this one sample, not a general Tardis guarantee.

Tardis's official CSV specification states that messages are grouped by local_timestamp; pre-snapshot updates must be skipped; a new snapshot after updates resets the book; amount is absolute rather than a delta; and amount zero removes a level. Source: https://docs.tardis.dev/downloadable-csv-files (incremental_book_L2 schema).

Artifact ID `14187255879`, SHA-256 `e7ee6eac5ddaf65fd89c0c692690fe109861bc9cf110f370244803bf004735be`, contains only small audit summaries, hashes and manifests (1,521 bytes); expires 18 November 2026 at 23:58 UTC. Raw files were deleted before artifact upload and were not committed.

**Disposition:** Tardis is now a validated independent historical-L2 sample source and normalized CSV reference for parser/reconstruction research. It is not yet a selected data vendor or runtime dependency. Public sample access does not establish commercial redistribution rights; paid historical access and terms remain separate checks.


### 12.14 Same-day Tardis OKX Swap and official OKX archive reconstruction (16 November 2026)

Workflow [#43777769642](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43777769642) successfully downloaded and reconstructed both Tardis normalized L2 and the official OKX module-4 400-level archive for BTC-USDT-SWAP on 1 November 2026. The Tardis trade CSV also passed schema, side, positive price/amount and local-timestamp monotonicity checks.

| Measurement | Tardis normalized CSV | Official OKX module 4 |
|---|---:|---:|
| L2 rows / level changes | 28,215,014 | 54,547,769 |
| Message / book records | 844,983 | 5,827,935 |
| Snapshots | 13 | 96 |
| Update messages / records | 844,969 | 5,827,839 |
| Zero-amount deletions | 4,527,548 | 9,255,375 |
| Reconstructed states | 844,982 valid | 5,827,935 valid |
| Pre-snapshot rows skipped | 8 | n/a |
| Maximum observed gap (Tardis local receive time; official exchange time) | 3,803.897 ms | 584 ms |
| Exact 10 ms record intervals | not yet histogrammed | 4,927,293 (84.546%) |
| Exact 20 ms record intervals | not yet histogrammed | 329,079 (5.647%) |

Tardis trade sample: 781,943 rows, 387,478 buy and 394,465 sell; local timestamps ranged from 1793491200589194 to 1793577598702054 microseconds.

The two sources are both structurally reconstructable, but their observation density differs materially: the official archive has approximately 6.90 times as many book records and 96 snapshots versus 13. The listed gap values use different clocks (Tardis local receive time versus official exchange event time) and must not be compared as an apples-to-apples cadence metric. The Tardis normalized sample's source channel mapping is not explicit in the CSV, so do not assume it is equivalent to OKX's 10 ms VIP4+ books-l2-tbt channel. A direct timestamp-aligned BBO comparison is now available in section 12.18: inclusive same-timestamp match was 100%, while strict-preceding no-lookahead exact BBO match was 99.85065%. This validates sampled BBO agreement on this day, but the Tardis message stream remains much sparser and is not a substitute for the official 10 ms archive.

The Tardis sample's 13 snapshots and 3.804-second maximum gap are consistent with reconnect/snapshot behaviour documented by Tardis; the CSV omits explicit disconnect markers. The official archive has 96 periodic snapshots and a 584 ms maximum adjacent record interval. Both reconstructions had zero empty/crossed/locked states, but this does not prove lossless capture.

Artifact ID `14186673619`, 2,596 bytes, SHA-256 `33d6a8fc07b1360683a8ada3cca0db7030012b9a906953ab320c82ce197ab734`, contains only manifests, hashes and small summaries; expires 19 November 2026 at 00:03 UTC. The workflow's separate unconditional cleanup step completed before artifact upload.

**Disposition:** Tardis's OKX Swap normalized sample is validated as a parseable source, but not as a 10 ms-equivalent source. Keep it as an independent coarser/reference dataset until direct BBO matching and channel provenance are established. The official OKX archive remains the stronger high-frequency historical candidate. No runtime vendor is selected.


### 12.15 Third-day OKX alignment diagnostic — 13 November failed initial side gate (16 November 2026)

Expanded three-day workflow [#43777626875](https://github.com/ImNotBrookOk/IDEAL) reran the full no-lookahead alignment and added side-consistency splits by timestamp tie and preceding-book age. The 13 November aggregate remains below the predeclared 98.0% initial side-consistency screen; no threshold was lowered.

| Measurement | 13 Nov 2026 |
|---|---:|
| Aligned trades | 4,544,561 |
| Book records | 7,391,929 |
| Trades without preceding book | 0 |
| Invalid book matches | 0 |
| Median preceding-book age | 5 ms |
| p95 preceding-book age | 10 ms |
| Maximum preceding-book age | 507 ms |
| Same-timestamp trades | 449,173 (9.884%) |
| Aggregate side consistency | 97.8348% |
| Aggregate side mismatch | 2.1652% |
| Outside preceding sampled spread | 64.718% |
| Outside-distance p95 | 1.89 bps |
| Outside-distance max | 17.77 bps |

**Side consistency split:**

| Subset | Trades | Consistent | Mismatch | Consistency |
|---|---:|---:|---:|---:|
| Same timestamp as book update | 449,173 | 437,278 | 11,895 | 97.3518% |
| Strictly preceding timestamp | 4,095,388 | 4,008,883 | 86,505 | 97.8877% |
| Preceding-book age <=10 ms | 4,412,377 | 4,314,485 | 97,892 | 97.7814% |
| Age 10–20 ms | 83,650 | 83,380 | 270 | 99.6772% |
| Age 20–50 ms | 43,002 | 42,788 | 214 | 99.5023% |
| Age >50 ms | 5,532 | 5,508 | 24 | 99.5662% |

The same-timestamp subset is weaker, but only accounts for 11,895 of 98,400 mismatches (~12.1%). The strict-preceding subset also fails at 97.8877%. Mismatches are concentrated in the <=10 ms age bucket; older-age buckets are above 99.5%. Therefore this is not explained solely by same-timestamp ties or the long stale tail. Plausible explanations include sub-millisecond/millisecond event-order ambiguity, fast market movement between sampled updates, source-side sequencing gaps, or an unverified assumption about the meaning of the exchange trade-side field. The current evidence does not distinguish these causes.

**Disposition:** retain the failed 98% result as a quality warning. Do not lower the threshold or claim three-day alignment acceptance. The 10 ms feed remains usable for sampled market-quality research with uncertainty bounds, but its trade/BBO directional alignment is not consistently within the initial target across all three days. Sequence IDs/checksums and exact event ordering remain absent. Further work must verify trade-side semantics, test more days/market regimes, and quantify BBO agreement against an independent source before this gate can be closed.

The rerun artifact ID `14187715114` (3,348 bytes, SHA-256 `3bab0de9a9659691165d0339d851fe70ebd9fb60cd557c66de2ac4492683d53b`) contains summaries/manifests only and expires 19 November 2026 at 00:05 UTC. The separate unconditional cleanup step completed successfully before upload. The earlier failed-run artifact `14187155843` still temporarily contains raw archives and expires 18 November 2026 at 23:55 UTC; this was recorded in conversation audit 029 and the workflow cleanup defect is corrected.


### 12.16 Three consecutive OKX 400-level archives passed independent structural reconstruction (16 November 2026)

Workflow [#43777630729](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43777630729) retrieved and independently reconstructed 11, 12 and 13 November 2026 module-4 BTC-USDT-SWAP archives. All 20 focused archive-audit unit tests passed before retrieval; all records across all three days reconstructed to valid, non-empty, non-crossed and non-locked books. Every one of the 288 snapshots had exactly 400 bid and 400 ask levels.

| Measurement | 11 Nov | 12 Nov | 13 Nov |
|---|---:|---:|---:|
| Book records | 6,630,044 | 6,604,203 | 7,391,929 |
| Snapshots | 96 | 96 | 96 |
| Updates | 6,629,948 | 6,604,107 | 7,391,833 |
| Price-level rows | 99,009,762 | 109,286,945 | 152,568,681 |
| Zero-quantity deletions | 17,885,894 | 20,114,734 | 29,620,105 |
| Median changed levels/update | 6 | 6 | 8 |
| Exact 10 ms intervals | 85.929% | 85.957% | 91.069% |
| Exact 20 ms intervals | 7.356% | 7.291% | 5.182% |
| Exact 30 ms intervals | 3.187% | 3.154% | 1.954% |
| Maximum adjacent interval | 508 ms | 520 ms | 517 ms |
| Invalid/empty/crossed/locked states | 0 | 0 | 0 |

The 13 November day is materially more active in the L2 stream: 7.39m book records, 152.57m level rows, 29.62m deletions and median 8 changed levels/update, versus 6.60–6.63m records and median 6 levels/update on the prior days. Its exact-10ms interval share is also higher (91.069%). This increased activity is consistent with a more demanding market-data sample, but does not by itself prove the cause of the 97.835% trade-side alignment result in section 12.15.

All three archive structures pass. The separate trade/BBO directional quality screen still fails on 13 November and remains open. Structural reconstruction does not establish sequence continuity because the historical schema has no sequence IDs/checksums.

Artifact ID `14186803944`, 7,033 bytes, SHA-256 `90a39d1d5c042d970e899a391833dd6f6bba01a22c8fa155d23d685361cde13e`, contains summaries/manifests only and expires 19 November 2026 at 00:10 UTC. The unconditional cleanup step completed before upload.


### 12.17 Live OKX feed entitlement, sequence integrity and RPI liquidity (official documentation review, 16 November 2026)

Current OKX documentation changes the live-feed assumptions that must be carried into any venue decision:

1. **10 ms order-book channel entitlement:** the 7 April 2026 change log states that the JSON books-l2-tbt channel (400-level tick-by-tick) and books50-l2-tbt channel (50-level tick-by-tick) are both accessible from VIP4 and above. This is the current documented requirement; older VIP5/VIP6 references are superseded. Source: https://www.okx.com/docs-v5/log_en/ (7 April 2026 Trading Fee Tier Requirement Changes).
2. **Live continuity validation:** on 23 June 2026 OKX deprecated checksum validation for books, books-l2-tbt and books50-l2-tbt; the checksum field remains but is fixed at zero. Live consumers must validate seqId/prevSeqId continuity and fail closed on gaps/resynchronisation. Historical archive records inspected in this research do not contain these sequence fields, so the historical archive cannot prove lossless capture. Source: https://www.okx.com/docs-v5/log_en/ (23 June 2026 Deprecation of checksum field in order book channels).
3. **RPI liquidity is a separate data/execution dimension:** on 28 July 2026 OKX introduced books-rpi, a public WebSocket/REST consolidated book with 400 depth levels and 100 ms snapshots/updates, including organic plus RPI liquidity. Each level contains totalQty, nonRpiQty and count. Its WebSocket continuity uses seqId/prevSeqId; there is no checksum. The channel applies to SWAP/FUTURES as well as SPOT/MARGIN. Source: https://www.okx.com/docs-v5/log_en/ (28 July 2026 New consolidated order book: books-rpi).
4. **Account/order permission:** rpiTakerAccess defaults to false; when true, standard limit/market/FOK/IOC orders may access RPI liquidity. The instrument permission field rpi distinguishes not enabled (0), enabled but user lacks permission (1), and enabled/permitted (2). An enabled instrument does not prove RPI liquidity is present.

**Implication for IDEAL:** do not model the 10 ms books-l2-tbt historical archive as complete executable liquidity without separately establishing RPI coverage and the intended account's permission/order flags. If the selected account can access RPI, capture the organic 10 ms book and consolidated 100 ms RPI book as separate streams, preserve each sequence chain, and model the additional 100 ms observation lag. The historical three-field archive schema does not establish whether RPI is included or expose total/non-RPI quantity separately.

The 10 ms channel's VIP4+ requirement is documented, but no account entitlement is known or assumed. Venue eligibility in New Zealand remains a separate legal gate.


### 12.18 Direct Tardis-to-official OKX BBO comparison (1 November 2026)

The first direct same-day comparison completed in workflow [#43778824863](https://github.com/ImNotBrookOk/IDEAL). It compared 844,982 reconstructed Tardis BBO message states with the official OKX module-4 BBO series using exchange timestamps in microseconds and a strict no-lookahead merge.

| Metric | Result |
|---|---:|
| Tardis BBO samples compared | 844,982 |
| Samples with no preceding official state | 0 |
| Samples sharing an official timestamp | 597,102 (70.664%) |
| Strict-preceding official exact BBO match | 99.85065% |
| Strict-preceding bid match | 99.85159% |
| Strict-preceding ask match | 99.85136% |
| Strict-preceding official BBO age, median | 10 ms |
| Strict-preceding official BBO age, p95 | 60 ms |
| Strict-preceding official BBO age, maximum | 529 ms |
| Inclusive same-timestamp exact BBO match | 100.000% |

All 844,982 Tardis BBO samples matched the official BBO when the official update at the same exchange timestamp was included. Under the conservative strict-preceding rule, 0.14935% differed; 70.664% of Tardis samples had an official update at exactly the same timestamp. This indicates the normalized Tardis feed is a highly accurate sampled BBO representation of the official OKX feed on this day, with the small strict-preceding discrepancy consistent with same-timestamp event-order ambiguity.

**Important clock distinction:** the previously reported Tardis 3,803.897 ms gap is measured using Tardis local receive timestamps; the official 584 ms interval is measured using exchange timestamps. They are not directly comparable. The updated parser now reports both local receive gaps and exchange timestamp gaps separately. The lower Tardis message count (844,983 versus 5,827,935 official records) still establishes a substantially sparser observation set, but the exact source channel and effective cadence remain to be confirmed.

**Disposition:** Tardis OKX is validated as a high-BBO-agreement, lower-density reference feed for this sample, not as a substitute for the official 10 ms archive. The 100% inclusive result is an upper bound, not a no-lookahead result; use 99.85065% as the conservative strict-preceding match rate. Full audit artifact ID `14187915961`, 2,991 bytes, SHA-256 `74d5c38cee84ced1e398fc51ea81a2d6b06152482e99689dc21d0229b0b95e69`, expires 19 November 2026 at 00:16 UTC and contains summaries/manifests only.
