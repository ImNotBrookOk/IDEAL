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
