# IDEAL Conversation Audit — 2026-11-16 — 025 — OKX Tardis historical data investigation

## User-visible transcript

**User:** I love it! Lets keep building and testing!

**Assistant:** We’ll continue Phase 01, with the same evidence standard: research and test until the data and execution assumptions are defensible; do not advance phases or introduce runtime trading.

The next priority is obtaining and independently validating real crypto perpetual-futures order-book and trade data. A dataset is not accepted just because its documentation looks promising. We need actual bytes, verified contract identity, reconstructable books, sequence continuity, timestamp integrity and paired trade data before using it for execution research.

**Assistant:** A useful new lead has emerged: Tardis documents historical OKX perpetual-swap L2 data, not just spot data. Its OKX Swap coverage page lists BTC swap trades and incremental L2, and records multiple feed generations. The important caveat is that the most granular `books-l2-tbt` feed is listed only through 21 May 2026; the `books` 100 ms feed is listed for 24 February 2023–19 July 2024 and again from 21 May 2026 onward. That makes feed continuity and granularity a first-class acceptance test, not an assumption.

## Scope and authority

- Work remained within Phase 01 research under D-012.
- No Phase 02 work, runtime integration, exchange/account access, credentials, testnet, paper/live execution, paid service, billing or risk-control changes were performed or authorised.
- D-001 remains unchanged: crypto perpetual futures are the sole active initial market.
- No venue or data vendor was selected.

## Operational research log

1. Read the installed Acumen research guidance and queried recent OKX historical-data changes. The brief did not return directly useful OKX data-access facts; it did surface unrelated market changes, which were not used.
2. Searched official and vendor documentation for OKX historical order-book and trade coverage.
3. Re-fetched the Tardis OKX Swap documentation. It states historical perpetual-swap coverage since 2019-03-30; first-of-month CSV samples are available without a Data API key; the exchange-native channels include trades, trades-all, books-l2-tbt, books, BBO, mark price, funding, open interest and instrument updates.
4. Confirmed the documented channel-generation boundary: books-l2-tbt (10 ms) ends 2026-05-21; books (100 ms) is listed 2023-02-24–2024-07-19 and again from 2026-05-21. Tardis also records a collector-region and WebSocket endpoint change on 2026-05-21. This is a material stratification boundary for future execution research.
5. Retrieved Tardis exchange metadata through the research fetch path. The JSON identifies `okex-swap`, `enabled=true`, coverage since 2019-03-30 and the listed channels.
6. Queried the 2026-11-01 `BTC-USDT-SWAP` trade CSV gzip URL. The fetch service returned binary content beginning with gzip magic bytes `1f 8b`, but did not provide a saved file, response headers, byte count or hash. Matching L2 URLs for `BTC-USDT-SWAP` and `BTC-USD-SWAP` were not parsed by the fetch service (`CRAWL_UNEXPECTED_CONTENT_TYPE`). This is not evidence of a 404 or source outage.
7. Retried HTTP HEAD from the execution container for the trade and L2 URLs. All three failed DNS resolution with `[Errno -3] Temporary failure in name resolution`. This remains an environment access limitation. No file bytes were saved locally and no gzip/CSV/reconstruction tests were possible.
8. Re-fetched CryptoHFTData's current Known Gaps & Corrections page. It still states that the October 2026 quality release is not deployed. The provider's own register continues to identify empty-book snapshot defects affecting OKX Futures and planned, unpublished OKX funding/ticker/trade-history repairs. CryptoHFTData remains on hold for empirical calibration.

## Evidence and disposition

- Tardis is a stronger no-key sample-evaluation candidate for OKX perpetual swaps than previously established, but has not passed actual-file validation.
- The 2026-05-21 feed transition is material: pre-boundary 10 ms tick-by-tick L2 and post-boundary 100 ms L2 must not be pooled without explicit treatment.
- The trade endpoint's gzip response is a retrieval-path observation only. It is not a locally available artifact or validated dataset.
- CryptoHFTData remains on hold while its own correction register says the release is not deployed.
- No test suite or code was run; this was documentation/source research and bounded network-access probing only.

## Sources

- https://docs.tardis.dev/historical-data-details/okex-swap
- https://api.tardis.dev/v1/exchanges/okex-swap
- https://docs.tardis.dev/downloadable-csv-files
- https://www.cryptohftdata.com/docs/data-gaps-and-corrections
- https://www.okx.com/historical-data

## Current state and next step

Phase 01 remains IN PROGRESS. Historical perpetual L2 acceptance remains BLOCKED. No vendor or venue is selected. The next test is to obtain matching 2026-11-01 OKX Swap incremental L2, trades and derivative-ticker files as actual local artifacts, then record hashes, schema, gzip integrity, row counts, sequence/timestamp checks and independent book reconstruction. If this environment cannot retrieve binary files, use an owner-controlled ordinary network path or a different permitted retrieval route without weakening the acceptance criteria.

Owner approval for Phase 02 remains pending and is not requested by this research update.


## Addendum — OKX native archive discovery (16 November 2026)

Subsequent to the initial Tardis-only update, the public OKX historical-market-data endpoint was queried successfully through the research fetch path. Exact metadata responses:

1. `module=5`, `instType=SWAP`, `dateAggrType=daily`, `instFamilyList=BTC-USDT`, 2026-11-12 UTC: `code=0`; `BTC-USDT-SWAP-L2orderbook-5000lv-2026-11-12.tar.gz`; 177.63 MB; URL `https://static.okx.com/cdn/okx/match/orderbook/pro/L2/5000lv/daily/20261112/BTC-USDT-SWAP-L2orderbook-5000lv-2026-11-12.tar.gz`.
2. Same module and family, 2026-11-11 UTC: `code=0`; 170.27 MB.
3. `module=4`, BTC-USDT SWAP, 2026-11-12 UTC: `code=0`; 400-level archive; 477.07 MB.
4. `module=5`, ETH-USDT SWAP, 2026-11-12 UTC: `code=0`; 149.22 MB.
5. `module=1`, BTC-USDT SWAP, daily dates 2026-11-12 and 2026-11-13 in UTC+8: `code=0`; two trade ZIPs of 17.85 MB and 30.43 MB. Both are required to cover the 2026-11-12 UTC order-book day, because the trade and order-book modules use different calendar timezones.

The MIT `burakoner/OKX.Api` source at commit `1dd5dd09d04627eb27a6b0b15bac980287295b1b` was inspected: the endpoint implementation uses `signed: false`; module 4/5/6 map to 400/5000/50 levels; response fields include `filename`, `sizeMB`, and direct `url`; the request requires inclusive begin/end, one-to-ten instrument families for SWAP, and a maximum ten-day/month range. Its changelog records unsigned production boundary tests, T+3 order-book availability and 5 requests per 2 seconds per IP. The repository declares MIT. It is used as a source/code reference only; no dependency is adopted.

Important pairing rule: order-book modules 4/5/6 use UTC calendar dates, whereas trade module 1 uses UTC+8. For the full 2026-11-12 UTC book day, retrieve both trade-date files (12 and 13 November UTC+8) and filter rows by actual timestamps. Do not pair by filename date alone.

The execution container still fails DNS resolution for external data hosts. The research fetch path returned JSON metadata and direct URLs, not the 170+ MB L2 archive or trade ZIP bytes. No archive download, checksum, tar/gzip verification, schema parsing, row count, event-cadence measurement, reconstruction, sequence-gap check, trade alignment or replay test has occurred. The OKX source is now the highest-priority bounded retrieval candidate, not an approved data source or venue.

Updated roadmap/docs were read back after commit. Phase 01 remains IN PROGRESS, historical-data gate BLOCKED, Phase 02 LOCKED. No code tests were run; documentation/research only.


## Retrieval attempt addendum — direct archive access

After the metadata query, attempted to open the exact 177.63 MB OKX CDN `.tar.gz` URL through the web retrieval interface; it returned an inaccessible-file error. Attempted the container download utility; it refused because the URL had not been successfully viewed through the web interface. No file or partial file was written. This is a retrieval-tool limitation, not a verified HTTP/CDN failure. The actual-file validation gate remains blocked.
