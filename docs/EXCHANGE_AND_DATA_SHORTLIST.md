# IDEAL — Exchange and Historical Market-Data Shortlist

**Research date:** 16 November 2026  
**Phase:** 01 — Open-source, venue and infrastructure research  
**Status:** Preliminary shortlist only. No venue, account mode, product or data vendor selected. No API credentials or exchange accounts created. No trading access requested.

## 1. Decision boundary

This document compares public market-data access and historical-data availability. It does **not** approve an exchange for trading, recommend a derivatives venue, or establish that any product is legally available to an individual in New Zealand.

The project requirement remains exchange-neutral research using public unauthenticated data and deterministic fixtures. Venue-specific adapters, account access and testnet work stay blocked until the owner approves a venue/product/account mode and regional eligibility is verified.

## 2. Evaluation criteria

A candidate must be evaluated on all of the following, not just REST API availability:

1. **Regional/product eligibility:** exact contracting entity, country addendum, perpetual/futures availability, client classification and regulatory status.
2. **Live market data:** public L2 snapshot and delta channels, sequence/update IDs, timestamps, checksum/continuity rules, depth and rate limits.
3. **Historical market data:** raw trades, L2 deltas plus reconstructable snapshots, funding, mark/index prices, open interest and liquidation events.
4. **Execution calibration:** depth sufficient for the intended order sizes, realistic update cadence, reliable sequence recovery and representative volatility regimes.
5. **Data quality:** gaps, reconnects, channel ordering, symbol changes, contract metadata, timestamp precision and provenance.
6. **Cost and licence:** free public endpoints, historical sample availability, data-vendor subscription requirements, redistribution restrictions and storage cost.

OHLCV and trade history alone are not sufficient to calibrate queue depletion, market impact or passive fill behaviour. L2 market-by-price can calibrate spread, depth and execution cost; it does not reveal individual order identity or true queue position. L3 market-by-order data would be required for defensible queue-position modelling.

## 3. Candidate venue comparison

| Candidate | Public live market data | Native historical L2 | Third-party historical L2 | NZ derivatives eligibility |
|---|---|---|---|---|
| Binance USDⓈ-M / COIN-M | Public REST depth snapshots (up to 1,000 levels) and public WebSocket depth/trade streams | Public Data archive contains trades, aggTrades and klines, not L2. Futures historical orderbook download is a signed USER_DATA/VIP-gated path; current docs state no data after 2024-11-01 and a maximum request window under 7 days | Tardis documents multi-year Binance Futures L2 data; paid access/sample availability must be checked for the exact product and dates | **Unconfirmed.** Binance New Zealand's listed local services are virtual-asset purchase/trading, NFT and investment services; the entity states it is not licensed by a NZ regulator. Its public NZ service list does not establish Futures eligibility |
| Bybit linear / inverse | Public V5 REST orderbook snapshot up to 1,000 contract levels; public WebSocket orderbook streams expose snapshots/deltas and update/sequence metadata. RPI liquidity is not included in the REST response | No official native historical L2 archive confirmed in this review; public market endpoints cover current orderbook, recent trades, funding history and open interest | Tardis documents Bybit derivatives historical coverage; depth/channel availability varies by product and date and must be validated on a sample before use | **Unconfirmed.** NZ addendum identifies Kono as the provider and limits NZ users to the changing “NZ Supported Services” list. The addendum does not itself establish perpetuals are included |
| OKX swaps / futures | Public orderbook channels are available. Standard `books` remains public; higher-frequency `books50-l2-tbt` and `books-l2-tbt` have VIP4/VIP5 eligibility requirements. Current sequence integrity uses `seqId/prevSeqId`; the checksum field was deprecated in June 2026 | Official historical-data portal advertises high-resolution L2 from March 2023, tick trades from September 2021 and perpetual funding from March 2022. Download access, schema, depth and cost still require direct validation | Tardis documents OKX derivatives history and L2 replay; per-channel depth/frequency changes over time | **Unconfirmed.** Exact NZ contracting entity, product availability and derivatives issuer status have not been verified |
| Hyperliquid perpetuals | Public Info API exposes L2 snapshots up to 20 levels; WebSocket market-data subscriptions are public. This is materially shallower than a full-depth L2 tape | No public full historical L2 delta archive verified. The Info API exposes candle snapshots (most recent 5,000) and user-specific fills (not a market-wide public fill tape) | Tardis documents Hyperliquid orderbook snapshots, not the same full incremental L2 event history available for some centralised venues | **Unconfirmed.** No NZ-specific product/legal eligibility determination made |

### 3.1 Binance

- The official [Binance Public Data repository](https://github.com/binance/binance-public-data) describes daily/monthly public files for Futures trades, aggregate trades and klines. It does not document a general public historical L2 orderbook archive.
- The Futures historical orderbook link endpoint is `GET /sapi/v1/futures/histDataLink`, classified as `USER_DATA`. The current developer documentation states VIP eligibility, a request window shorter than seven days, and no historical data after 1 November 2024. Treat this as unsuitable for obtaining recent historical L2 without a separately verified vendor source.
- Live public Futures depth streams remain useful for a future collector; they do not solve the historical calibration gap.
- Binance's current [licences and registrations page](https://www.binance.com/en/about-legal/licenses) states InvestbyBit Limited (Binance New Zealand) is registered on the NZ FSPR as FSP1003864, lists virtual-asset purchase/trading, NFT and investment services, and explicitly says it is not licensed by a NZ regulator. This is not proof that Binance Futures is available to NZ users.

### 3.2 Bybit

- Official [V5 Get Orderbook](https://bybit-exchange.github.io/docs/v5/market/orderbook) documents up to 1,000 levels for linear/inverse contracts, a snapshot response, update ID `u`, cross-sequence `seq`, and matching-engine timestamp `cts`. It also states RPI orders are not visible in this API response.
- Public WebSocket depth streams should be the live collection source if this venue is later approved; REST snapshots alone cannot reconstruct historical queue changes.
- The [New Zealand terms addendum](https://www.bybit.com/en/help-center/article/Addendum-to-Terms-of-Service-New-Zealand-Users) says NZ users may access only the NZ Supported Services, which can be a subset of the platform and may change. Do not infer that the global API or product catalogue is available to an NZ account.

### 3.3 OKX

- The [official historical-data portal](https://www.okx.com/historical-data) advertises tick-level trades from September 2021, funding history from March 2022 and high-resolution L2 from March 2023. The actual download format, exact instruments, update cadence, access conditions and whether downloads are free must be verified.
- The [OKX API changelog](https://www.okx.com/docs-v5/log_en/) records that from 23 June 2026 the order-book checksum field is deprecated for the relevant channels; continuity must be checked with `seqId/prevSeqId`.
- The same official changelog distinguishes public `books` from restricted higher-frequency channels: `books-l2-tbt` 400-depth requires VIP5 and `books50-l2-tbt` 50-depth requires VIP4. Do not assume tick-by-tick 400-level data is available on a basic account.
- OKX is currently the strongest **data-access candidate** in this preliminary review because it advertises a native historical L2 download portal. This is not a venue recommendation or eligibility decision.

### 3.4 Hyperliquid

- The [official Info API documentation](https://hyperliquid.gitbook.io/Hyperliquid-docs/for-developers/api/info-endpoint) states that `l2Book` returns at most 20 levels per side. `candleSnapshot` is limited to the most recent 5,000 candles. `userFillsByTime` is account-specific and limited to 10,000 recent fills, so it is not a substitute for a public market-wide trade/fill archive.
- Tardis documents Hyperliquid book snapshots rather than a full historical incremental L2 event tape. Treat Hyperliquid as a weaker fit for queue-sensitive historical execution calibration unless a separate raw event source is found.

## 4. Historical data providers and free-tier position

### Tardis.dev

- Tardis documents normalized tick-level trades, incremental L2 updates, top-25/top-5 book snapshots, quotes, derivative tickers (funding, open interest, mark/index prices) and liquidations. Its raw replay API is restricted to Pro/Business subscriptions.
- Historical CSV datasets for the first day of each month are available without an API key. This is a viable no-cost schema/sample evaluation path, but it is not a free full-history entitlement.
- The vendor documents daily initial book snapshots at 00:00 UTC and additional snapshots after WebSocket reconnects. Reconnects can create roughly 300–3,000 ms data gaps depending on venue. Cross-channel events are not guaranteed to be synchronized; the vendor preserves local receive order rather than claiming exchange-wide causal ordering.
- L2 is market-by-price, not market-by-order. The vendor states historical L3 is available only for a limited set of venues (Bitfinex, Coinbase Pro and Bitstamp), not the main perpetual candidates in this shortlist.
- No public price for the full required history has been verified. Do not purchase or create a paid subscription without owner approval.

### Exchange-native archives

- Binance Data Vision is useful for free trade/aggTrade/klines research, but it does not replace L2 deltas.
- OKX advertises historical L2 downloads from March 2023; download access, exact format/depth and cost need to be checked directly.
- No equivalent official Bybit or Hyperliquid full-depth historical delta archive was verified in this review.

### Self-capture

Public market-data endpoints and WebSocket channels can generally be consumed without trading credentials. A future collector can therefore begin with public feeds after a venue is approved. This is not zero-cost in operation: persistent storage, reconnect supervision, sequence validation, clock discipline, retention, backups and incident monitoring still consume compute and engineering time.

## 5. New Zealand eligibility and compliance gate

- The [FMA's derivatives-issuer guidance](https://www.fma.govt.nz/business/services/derivatives-issuers/) states that a derivatives issuer making a regulated offer of derivatives must be licensed by the FMA. Its definition includes products commonly referred to as futures, swaps, CFDs, margin contracts and rolling spot contracts. Whether a specific offshore venue/product/account arrangement constitutes a regulated offer is a legal question; this document does not decide it.
- Binance New Zealand's local entity is listed as registered on the FSPR but not licensed by a NZ regulator. The listed local services do not establish that derivatives/perpetuals are offered to NZ users.
- Bybit's NZ addendum limits NZ users to the changing NZ Supported Services list; the addendum itself does not identify perpetual futures as a supported NZ product.
- OKX and Hyperliquid NZ-specific product eligibility and the relevant contracting entities remain unverified.
- **Gate:** no exchange account, API key, testnet or trading connection until the exact legal entity, product, account mode, user classification and NZ eligibility are confirmed. Public read-only data research does not constitute approval to trade.

## 6. Data-quality acceptance checklist

Before any historical dataset is used for market-impact or fill calibration, verify:

- [ ] Exact venue, instrument, contract type, settlement currency, tick/lot size and listing/delisting dates.
- [ ] L2 snapshot plus incremental delta schema; sequence IDs and checksum/continuity semantics.
- [ ] Snapshot bootstrap, reconnect recovery and gap boundaries; never interpolate across missing book events.
- [ ] Exchange event timestamp and local receive timestamp preserved independently.
- [ ] Trade, book, funding, mark/index, open-interest and liquidation channels retained separately with source provenance.
- [ ] Cross-channel ordering assumptions documented; do not assume a trade timestamp proves whether a book update is pre- or post-trade.
- [ ] Duplicate, out-of-order, crossed-book, empty-book and stale-instrument cases quantified.
- [ ] L2 depth sufficiency for target order sizes measured; L2 fill assumptions explicitly separated from true L3 queue modelling.
- [ ] Contract metadata and funding schedule changes time-versioned.
- [ ] Data gaps, vendor corrections and excluded intervals recorded in a machine-readable quality report.

## 7. Preliminary disposition

1. **Do not select a venue yet.** Regional/product eligibility is unresolved and historical L2 quality has not been validated on actual files.
2. **First no-cost data experiment:** inspect one Tardis first-of-month CSV sample for a relevant perpetual, and inspect an OKX official historical L2 download if it is available without paid access or account approval.
3. Compare the sample's schema, snapshot bootstrap, sequence continuity, depth, timestamps and data gaps. A sample that contains only trades or OHLCV fails the L2 acceptance requirement.
4. If free historical L2 proves insufficient, begin collecting public live L2 only after venue/product eligibility is approved; accumulate a forward dataset rather than silently weakening the execution-realism standard.
5. Keep Hummingbot (Apache-2.0) and CCXT (MIT) as connector references already identified in `docs/REPO_RESEARCH.md`. Treat CCXT Pro as a separate paid WebSocket feature. Cryptofeed's AGPL licence and attribution condition require a separate legal review before direct reuse.

**Sample retrieval status:** the documentation confirms that first-of-month CSV samples are available without an API key, including the documented `binance-futures` dataset family. The current execution container could not resolve the external dataset host, and a separate live fetch attempt timed out, so no binary sample was downloaded or parsed in this pass. This is an environment/network limitation, not evidence that the vendor endpoint is unavailable. No sample-quality claim is made.

## 8. Historical L2 sample validation follow-up (16 November 2026)

- Added [the detailed validation report](HISTORICAL_L2_SAMPLE_VALIDATION.md). Direct Tardis sample requests for Binance Futures BTCUSDT top-5 snapshots, incremental L2 and trades (2020-09-01), plus exchange metadata, failed at DNS resolution in the execution environment. No bytes were obtained; no file integrity, CSV parsing or order-book reconstruction test was run. A previous attempt timed out. This is an environment retrieval failure, not evidence of vendor outage.
- Independent HftBacktest v2.2.0 documentation records successful HTTP 200 downloads for a Tardis Binance Futures 2020-02-01 example: 3,090,479-byte trades gzip and 250,016,849-byte incremental-L2 gzip, with 27,532,602 normalized events. Historical example evidence only, not proof of current reachability or current market representativeness.
- Data format facts: microsecond exchange/local timestamps, snapshot/delta flag, side/price/amount, same-local-timestamp row grouping, snapshot reset semantics, daily/reconnect snapshots, reconnect gaps, disconnect marker omission from CSV, asynchronous cross-channel ordering and L2 market-by-price limitations.
- No-cost alternative screening is in report section 8: the Hugging Face Binance L2 dataset has 251m rows/1.72 GB and a known 43-minute capture gap, but published market type is ambiguous; `crypto-lob-stream` is an MIT alpha collector reference with known sequence, resync, checksum and file-write limits; CryptoHFTData has anonymous free hourly downloads but its own October 2026 data-quality release was not yet deployed and its standard terms prohibit redistribution/downstream embedding.
- Disposition: sample validation remains BLOCKED; no data-quality pass, vendor/venue selection or account eligibility conclusion. No data vendor subscription, API key or download was used.

**Next task:** obtain actual L2 and paired trade file bytes from a reachable no-cost source, then execute the validation matrix. No venue selection or account connection is implied.

## 9. Alternative-source screening (16 November 2026)

See [Historical L2 Sample Validation](HISTORICAL_L2_SAMPLE_VALIDATION.md), section 8. The community Binance dataset is a potential parser/reconstruction fixture only until spot-versus-perpetual market identity is verified. CryptoHFTData is held pending deployment and independent verification of its documented corrections. The MIT `crypto-lob-stream` collector is a reference, not an adopted dependency. No candidate passed the actual-file validation gate.


## 10. Execution-quality and order-placement research (16 November 2026)

The owner has explicitly prioritised decision quality and execution correctness over minimum order-placement latency (D-013). See [Execution Quality Research](EXECUTION_QUALITY_RESEARCH.md) for the objective function, scheduling-vs-placement decomposition, evaluation protocol and repository review.

- `eshaan2418/sorx` (MIT): useful OMS invariants, deterministic replay, per-venue book validation, parent-level paired TCA and fill simulation. Its reported 5–80 ms latency sensitivity is small in its own 40-minute spot USD-pair capture, but this cannot be transferred to perps. The capture's consolidated book was crossed in every 1-second sample, sample size was small, fees/latencies illustrative, and passive queue/market impact beyond consumed depth were not modelled. Reference only.
- `moussoulijane/execution-cost-analytics` (MIT): useful causal scheduling comparisons, paired path-level inference, bootstrap uncertainty and explicit negative results. One inspected initial commit; historical results and impact parameters are not a calibrated crypto-perpetual model. Research-method reference only.
- `AshJha0/electronic-trading` (MIT, release 2.0.1 dated 2026-10-31): useful Almgren–Chriss, Avellaneda–Stoikov/GLFT, impact/markout and golden-value test concepts. Its illustrative/equity calibration is not directly transferable to crypto perps. Mathematical/test reference only.
- No repository or algorithm was selected. No dependency was installed. No code or execution tests were run in this documentation/research update.

The next execution-research sequence is: validate actual perpetual L2/trades first; then establish causal replay and identical parent intents; benchmark immediate IOC, passive limit, TWAP, VWAP and POV; calibrate fill probability, adverse selection, liquidity replenishment and impact; and only then evaluate adaptive or learned policies out-of-sample. Latency remains measured, not ignored, but it is not the primary optimisation objective.


## 11. Hugging Face Binance dataset — market identity resolved (16 November 2026)

The earlier “spot/perpetual unclear” note is superseded by source inspection. The public dataset rows identify `exchange=binance`; the associated MIT collector maps that adapter to spot endpoints (`stream.binance.com`, `api.binance.com/api/v3/depth`). The same source has a distinct `binance_futures` adapter using `fstream.binance.com` and `fapi.binance.com/fapi/v1/depth`. The published files are therefore **spot data**, not USDⓈ-M perpetual data.

The Hugging Face datasets-server API reports 220.6m depth rows (1.49 GB), 224k snapshot rows (1.66 MB), and 30.58m trade rows (230 MB), total 251.39m rows / 1.72 GB. Bounded row previews exposed depth/snapshot/trade schemas, but the published schemas omit separate `exchange_ts`. The first returned snapshot row is 2026-06-05 06:29:48 UTC, while first returned depth/trade rows are 2026-06-04 00:54 UTC, so an initial snapshot anchor is not demonstrated for the earliest ~29.6 hours. The dataset card also documents a 43-minute outage on 2026-07-05 requiring a hard snapshot reset.

No Parquet bytes were downloaded, parsed or reconstructed. This dataset is rejected for perpetual calibration; it may be considered only as a generic spot-data parser fixture after actual file validation. See [Historical L2 Sample Validation](HISTORICAL_L2_SAMPLE_VALIDATION.md), section 9.


## 12. OKX Swap / Tardis historical-data update (16 November 2026)

Tardis's current OKX Swap metadata endpoint is reachable through the research fetch path and reports the exchange enabled, historical coverage since 2019-03-30, and channels including trades, trades-all, books-l2-tbt, books, BBO, mark price, funding, open interest and instrument updates. Tardis documents first-of-month CSV files without a Data API key.

A 2026-11-01 `BTC-USDT-SWAP` trades sample URL returned a gzip-signature binary response through the research fetch service, but the response was not materialised as a local file and no HTTP headers, byte count or hash were captured. The matching L2 URLs for `BTC-USDT-SWAP` and `BTC-USD-SWAP` were not parsed by that service (`CRAWL_UNEXPECTED_CONTENT_TYPE`). The execution container still fails DNS resolution. This is an access-path improvement, **not** a data-quality validation or successful local download.

The current Tardis channel history is a material constraint: `books-l2-tbt` (10 ms) is listed only until 2026-05-21; `books` (100 ms) is listed from 2026-05-21 onward (with an earlier 2023-02-24 to 2024-07-19 interval). The 21 May 2026 boundary also coincides with a collector-region and WebSocket-endpoint change. Any replay or model calibration must stratify across this feed-generation boundary; do not treat pre/post data as one homogeneous microstructure sample.

CryptoHFTData's current correction register still says the 2026-10 data-quality release is **not yet deployed**. Its disclosures include omitted empty-book snapshots affecting OKX Futures and planned, not published, OKX funding/ticker/trade-history corrections. It remains on hold for calibration.

Sources: [Tardis OKX Swap](https://docs.tardis.dev/historical-data-details/okex-swap), [Tardis exchange metadata](https://api.tardis.dev/v1/exchanges/okex-swap), [Tardis CSV documentation](https://docs.tardis.dev/downloadable-csv-files), [CryptoHFTData correction register](https://www.cryptohftdata.com/docs/data-gaps-and-corrections), [OKX official historical data portal](https://www.okx.com/historical-data).

**Disposition:** no sample files were saved or validated; no provider or venue selected; the historical-data gate remains BLOCKED. See validation report section 10.


## 13. OKX public historical L2 endpoint — concrete archive metadata (16 November 2026)

OKX's public `GET /api/v5/public/market-data-history` endpoint provides an unsigned route to order-book archive metadata and direct CDN file URLs. The endpoint was successfully queried through the research fetch path with `module=5`, `instType=SWAP`, `dateAggrType=daily`, `instFamilyList=BTC-USDT`, and the UTC date range for 2026-11-12. It returned `code=0`, a 177.63 MB 5,000-level archive and a direct `.tar.gz` URL. Further successful metadata queries returned BTC 5,000-level data for 11 November (170.27 MB), BTC 400-level data for 12 November (477.07 MB), and ETH 5,000-level data for 12 November (149.22 MB).

A matching module 1 BTC-USDT SWAP trade query returned two UTC+8-dated ZIP archives for 12 and 13 November (17.85 MB and 30.43 MB). Because order-book modules use UTC dates while trade module 1 uses UTC+8 dates, both trade archives are needed to cover the full 12 November UTC book day; trim the combined trade rows by actual timestamps. The query contract and date behavior are corroborated by the MIT OKX client source and its 2026 changelog, which documents unsigned production verification, 10-day inclusive maximum windows, and a 5-requests-per-2-second IP limit.

The 400-level and 5,000-level archives have materially different reported sizes, but no cadence or quality inference is made from size alone. Actual archive bytes, headers, hashes, archive integrity, schema, event cadence, sequence continuity, snapshot behavior, trade alignment and reconstruction remain untested. The execution container still cannot resolve the external hosts, and the research fetch service has only returned JSON metadata, not the large archives.

Sources: [OKX API change log, endpoint introduced](https://www.okx.com/docs-v5/log_en/#2025-09-02), [OKX API change log, query limit](https://www.okx.com/docs-v5/log_en/#2026-08-06), [MIT OKX.Api implementation](https://github.com/burakoner/OKX.Api), [OKX historical-data portal](https://www.okx.com/historical-data).

**Disposition:** OKX is now the highest-priority direct-download candidate for the next bounded sample test. It is not a selected venue or data vendor; no file has been downloaded or validated. The acceptance gate remains BLOCKED. See [Historical L2 Sample Validation](HISTORICAL_L2_SAMPLE_VALIDATION.md), section 11.


### 13.5 Bounded OKX 2026-11-12 sample: actual bytes inspected

The isolated GitHub Actions retrieval run [#43766633587](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43766633587) retrieved the 5,000-level BTC-USDT-SWAP L2 archive and the two matching UTC+8 trade archives. The artifact was independently downloaded and its SHA-256 matched GitHub's artifact digest. HTTP 200/content-length, source SHA-256, TAR/GZIP and ZIP integrity checks passed.

The L2 archive expands to 891,030,123 bytes and contains 86,400 NDJSON records: 96 snapshots (5,000 levels per side each) and 86,304 updates. Reconstructing from snapshots and absolute quantity updates/deletions produced no empty, crossed or locked states. The archive is sampled at approximately one-second intervals, not tick-by-tick; it has no sequence IDs or per-record checksums. Fourteen timestamp intervals are outside 900–1,100 ms and occur as seven long/short pairs. The historical row has three fields per level; do not infer the third field's meaning from the four-field live WebSocket format.

Both trade archives contain 8,703,176 parsed rows in total. Correct timestamp filtering across UTC+8 files yields 3,224,415 trades for the 2026-11-12 UTC L2 day. IDs are strictly increasing across both files and no invalid trade rows were observed. This validates basic pairing, not exact event-level alignment.

**Disposition:** a partial data-quality pass for archive integrity and coarse one-second L2 reconstruction. Potentially useful for coarse spread/depth/imbalance analysis after further checks; insufficient on its own for FIFO queue-position or high-fidelity passive-fill/market-impact calibration. Sequence continuity, timestamp provenance, event-level trade/BBO alignment and multi-day representativeness remain blocked. No venue/vendor selection or runtime adoption. Full results: [Historical L2 Sample Validation](HISTORICAL_L2_SAMPLE_VALIDATION.md), section 12.


### 13.6 Follow-up audit: update density and unresolved level field

A second structural pass found 39,035,798 price-level rows, including 7,504,519 zero-quantity deletions. Across 86,304 update messages, changed levels range from 47 to 7,586, with a median of **283 total bid-plus-ask levels per message**. All 96 snapshots have exactly 5,000 levels per side. Of 86,399 adjacent timestamps, 86,349 intervals are exactly 1,000 ms; 50 differ, including the 14 outliers outside 900–1,100 ms.

Each historical price-level tuple has exactly three fields. The third is an integer but its meaning is not authoritatively established. Current live OKX RPI documentation uses a four-field schema and legacy general WS documentation also describes four fields; neither is sufficient to infer the historical archive's third field. Treat it as opaque until the historical module-5 schema is confirmed.

Trade-file recheck confirms 3,222,603 rows in the 12 Nov UTC+8 file and 5,480,573 in the 13 Nov file, with strictly increasing and continuous trade IDs across the file boundary. No malformed or invalid rows were observed. The 2026-11-12 UTC book-day filter yields 3,224,415 trades.

A second BBO alignment attempt exceeded the local execution limit; no alignment metric is claimed. The data remains a partial pass for archive integrity and coarse one-second visible-book analysis only. Execution calibration remains blocked.


## 13.7 OKX module-4 400-level high-frequency sample: updated candidate assessment (16 November 2026)

A follow-up research workflow downloaded and reconstructed the 2026-11-12 BTC-USDT-SWAP module-4 400-level archive (500,244,886 compressed bytes; SHA-256 `6dd55534ddd376c6995bfac584f1e1a19ed64083b76b542da61ee488cacbdfce`). It contains 6,604,203 records, 96 snapshots of 400 levels per side and 6,604,107 updates. All reconstructed states were valid. 85.957% of record intervals were exactly 10 ms. The corresponding module-5 5,000-level archive for 11 November was also retrieved and reconstructed: 86,400 records, 96 snapshots, 5,000 levels per side and 99.947% one-second intervals.

The 400-level stream's first records contain only `action`, `asks`, `bids`, `instId` and `ts`; no sequence IDs, previous-sequence IDs, checksums or local timestamps were present. Each level tuple has three fields, with the third integer still semantically unresolved. Do not use it as an order-count, liquidation-count or queue-size feature without authoritative historical-module documentation.

A no-lookahead alignment against the two matching UTC+8 trade files (timestamp-filtered to the 12 November UTC day) matched all 3,224,415 trades to a preceding valid BBO. Median preceding-book age was 6 ms, p95 10 ms, maximum 509 ms. 62.584% of trades printed outside the preceding sampled spread, but 98.542% were directionally consistent with the preceding BBO and outside-spread distance p95 was 1.40 bps. The same-day one-second module-5 sample had median age 489 ms, p95 947 ms and 76.71% outside-spread prints. This demonstrates materially better temporal resolution for module 4, not exact event synchronization.

**Updated shortlist status:** OKX module 4 400-level L2 is the leading research candidate for short-horizon, 10 ms sampled liquidity, spread, imbalance and conservative taker-impact/slippage analysis. It is not approved for exact FIFO queue position or passive-fill calibration because the historical archive has no sequence IDs/checksums or L3 order identity, and the third level field is unresolved. Module 5 remains a deep, one-second sampled reference. OKX is still a candidate only; no venue/vendor is selected and no runtime integration is approved.

Evidence: [final trade-alignment workflow #43773844334](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43773844334). Detailed reconstruction, alignment, limitations and next gates are in [Historical L2 Sample Validation](HISTORICAL_L2_SAMPLE_VALIDATION.md), sections 12.8–12.9.


## 13.8 Consecutive-day 400-level repeatability and order-count field evidence (16 November 2026)

The successful adjacent-day reconstruction workflow [#43774295757](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43774295757) establishes consistent archive structure on 11 and 12 November:
- 6.630m and 6.604m records respectively;
- exactly 96 snapshots each, each with 400 levels per side;
- 85.929% and 85.957% exact 10 ms adjacent intervals;
- median six combined price-level changes per update on both days;
- zero empty/crossed/locked/invalid reconstructed states.

This supports structural repeatability over two consecutive days. It is not proof of no dropped events because the archive records still have no sequence IDs/checksums.

The third tuple field is now **strongly corroborated as order count**, but not fully archive-spec-confirmed. OKX's official API guide defines the three-element array in GET /api/v5/market/books-full as price, quantity and number of orders at that price (https://app.okx.com/docs-v5/en/, “GET / Full order book”). Historical archive rows also contain three elements and the third is a nonnegative integer. However, OKX's currently documented 400-level WebSocket books/books-l2-tbt format has four elements, including a deprecated zero field followed by order count. We therefore retain the raw field and treat it as an optional, provisionally interpreted order-count feature until OKX confirms the downloadable archive schema. It cannot be used to infer FIFO position.

**Shortlist status remains:** OKX module 4 400-level L2 is the leading research candidate for short-horizon sampled market-quality and conservative taker-impact work; module 5 is the deeper one-second reference. No venue selected, no runtime adoption, Phase 01 remains open.


## 13.9 Historical/live OKX feed entitlement mismatch (16 November 2026)

OKX's official WebSocket guide distinguishes:
- `books-l2-tbt`: 400 levels, incremental updates every 10 ms, restricted to VIP4+;
- `books`: 400 levels, incremental updates every 100 ms;
- `bbo-tbt`: one level, 10 ms snapshots on change.

Source: https://app.okx.com/docs-v5/en/, “WS / Order book channel”.

Thus, the public historical 400-level 10 ms archive is a credible research-data source, but equivalent live full-depth data is not established for an ordinary account tier. Any venue shortlist must separately score historical data access and live feed entitlement. A 100 ms book or 10 ms BBO fallback changes the information set and requires separate calibration; it cannot be assumed execution-equivalent to 10 ms full depth. No VIP entitlement or live connection is assumed.


## 13.10 New Zealand derivatives-issuer eligibility gate (16 November 2026)

This is a hard venue-selection gate, not a minor onboarding check. The New Zealand FMA states that anyone offering derivatives to retail investors in New Zealand must hold a derivatives issuer licence and comply with the relevant disclosure and client-funds rules. The FMA's crypto guidance specifically states that providers offering crypto CFDs in New Zealand require a derivatives issuer licence and directs users considering other crypto derivatives to verify that the service provider is licensed. Official sources:
- https://www.fma.govt.nz/consumer/investing/types-of-investments/derivatives
- https://www.fma.govt.nz/consumer/investing/types-of-investments/cryptocurrencies/
- https://www.fma.govt.nz/business/services/derivatives-issuers/

Preliminary public-source screen:
- Binance New Zealand's official licensing page lists fiat purchase, virtual-asset trading, NFT trading and virtual-asset investment services; it does not list derivatives issuance. Its NZ futures market/fee pages exist but currently render “No records found”, which is not proof of eligibility.
- Bybit's NZ-specific terms identify Kono Group Limited as the contracting party and state that NZ users may access only the “NZ Supported Services”; the public addendum does not enumerate those services. Bybit's global excluded-jurisdiction list alone is insufficient to establish NZ perpetuals availability.
- OKX's 14 November 2026 Risk & Compliance Disclosure does not name New Zealand among the restricted locations or its separately named limited-service jurisdictions, but both lists are open-ended. OKX's terms list Aux Cayes FinTech Co. Ltd. for other eligible users; no NZ product-level derivatives entitlement is established by these pages.

Official source links:
- Binance NZ entity/services: https://www.binance.com/en-GB/legal/licenses
- Bybit NZ addendum: https://www.bybit.global/common-static/compliance/legal/BYBIT/700f3662d5d08a2d6cc9e75b47e381f0.pdf
- Bybit restricted jurisdictions: https://www.bybit.com/en/help-center/article/Service-Restricted-Countries/trade/spot
- OKX disclosure: https://www.okx.com/help/risk-compliance-disclosure
- OKX terms: https://www.okx.com/help/terms-of-service

**Disposition:** No venue is currently verified as legally/product-eligible for a New Zealand retail user to trade crypto perpetuals. This is not a legal conclusion that all are unavailable. Do not create an account, connect an exchange, obtain API keys or route orders based on generic availability pages. Before venue selection, obtain authoritative confirmation of the exact contracting entity, product, customer classification (retail/wholesale), and applicable FMA licence or exemption. Obtain independent New Zealand legal advice where necessary. The public market-data research can continue without this gate being cleared.


## 13.11 Two-day trade/BBO alignment gate passed for research (16 November 2026)

The expanded no-lookahead workflow [#43776264061](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43776264061) aligned 2,597,825 trades on 11 November and 3,224,415 on 12 November to strictly preceding valid 400-level BBO states. Both days had zero trades without a preceding book and zero invalid-book matches. Median age was 6 ms on both days; p95 was 18 ms and 10 ms; maximum age 497 ms and 509 ms. Directional side consistency was 99.118% and 98.542%, respectively. Initial acceptance gates passed independently on each day.

Outside-spread rates were 64.445% and 62.584%; this is not automatically a data defect because 10 ms sampling can miss intervening states and same-timestamp ordering is unknown. It does mean the dataset cannot establish exact trade/book event ordering. The 497–509 ms stale tail requires explicit runtime staleness controls. Detailed metrics: [Historical L2 validation](HISTORICAL_L2_SAMPLE_VALIDATION.md), section 12.12.

**Status:** historical module-4 400-level data is provisionally viable for sampled market-quality and conservative taker-impact research on the two validated days. It remains unsuitable for FIFO queue-position or exact passive-fill calibration. This does not clear live feed entitlement (13.9), NZ derivatives eligibility (13.10), venue selection or runtime adoption.


Staleness sensitivity from the same two days: a preceding-book age cutoff of <=50 ms retains 99.229% of 11 Nov trades and 99.492% of 12 Nov trades; <=20 ms retains 96.273% and 97.628%; <=10 ms retains 92.503% and 95.001%. These are research coverage calculations, not a production policy. The data model must preserve sample age and exclude stale depth rather than interpolate it. Full counts: historical validation section 12.12.


Additional classification nuance: the FMA's official derivatives guidance defines derivatives to include recurrently traded contracts commonly referred to as futures, options, swaps, CFDs, margin contracts or rolling spot contracts, regardless of duration. It does not explicitly classify every crypto perpetual product by name. Do not assume that an exchange's “perpetual” or “swap” label removes the product from the FMC Act definition; obtain a product-specific New Zealand legal determination. Source: https://www.fma.govt.nz/business/services/derivatives-issuers/.


## 13.12 Tardis public historical sample validated (16 November 2026)

A no-API-key first-of-month Tardis Binance Futures BTCUSDT sample for 1 November 2026 was retrieved and reconstructed successfully in [workflow #43777192211](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43777192211). The normalized incremental L2 file was 429.9 MB compressed / 6.461 GB uncompressed and contained 79.44m level rows across 3.242m message groups. One initial snapshot, 3.242m update messages, 7.26m zero-amount deletions and all 3.242m reconstructed states valid; maximum message gap 276.101 ms. The matching trade file contained 1,190,743 rows with valid schema, positive price/amount and monotonic local timestamps.

This proves Tardis's public first-of-month sample can be acquired and the documented normalized L2 format can be reconstructed in our research pipeline. It does not prove paid historical API cost, commercial data rights, sequence continuity, L3 queue identity or event-level trade/BBO alignment. Tardis remains an independent data-source candidate/reference only; no vendor is selected. Full details and hashes: [Historical L2 validation](HISTORICAL_L2_SAMPLE_VALIDATION.md), section 12.13.


## 13.13 Same-day Tardis OKX sample is not equivalent to official 10 ms archive (16 November 2026)

The same-day 1 November 2026 Tardis normalized OKX Swap L2 and official module-4 archive were both reconstructed successfully in [workflow #43777769642](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43777769642). Both had zero invalid reconstructed states, but the data cadence differed materially:
- Tardis: 844,983 message groups, 28.22m level rows, 13 snapshots, maximum message gap 3,803.897 ms.
- Official OKX module 4: 5,827,935 records, 54.55m level rows, 96 snapshots, maximum record interval 584 ms; 84.546% of intervals were exactly 10 ms.

The Tardis sample therefore has ~6.90x fewer message groups and substantially longer gaps. The CSV does not expose the raw OKX WebSocket channel identifier, so it is not proven to be the 10 ms VIP4+ books-l2-tbt stream. Treat it as a validated normalized/coarser reference, not as a substitute for official 10 ms history. Direct timestamp-aligned BBO comparison and exact channel provenance remain open. Artifact 14186673619 (2,596 bytes) contains summaries only; unconditional cleanup passed before upload. Full details: [Historical L2 validation](HISTORICAL_L2_SAMPLE_VALIDATION.md), section 12.14.
