# IDEAL Conversation Audit 022 — Historical L2 Sample Validation

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Status:** Research gate attempted; sample retrieval remains blocked.  
**Transcript completeness:** Complete for the user-visible messages in this conversation to this point.

## 1. Available user-visible transcript

**User:**  
> Ok lets keep going and testing what we need in order to have a great engine that is right the first time so its safe to build on and correct. Do what you need to do please

**Assistant:**  
> I’ll continue with the next Phase 01 gate: **prove that we can obtain, reconstruct and validate real historical order-book data before choosing or building around an engine.**
>
> The standard is not simply “the tests pass”. We need evidence that the data and execution assumptions are realistic enough to support reliable backtesting later. I’ll keep the work exchange-neutral, use public/free data only, preserve failures as evidence, and update the repository’s roadmap and audit trail. No engine adoption, runtime integration, exchange account access, or trading is authorised at this stage.
>
> The research has exposed an important practical issue: a “free sample” is not necessarily a small file. The HftBacktest data-preparation guide documents a Tardis Binance Futures L2 sample download of approximately **238 MB compressed for one day**, alongside roughly 2.9 MB of trades. Its example reconstructs a dataset of about **27.5 million events**. That is useful evidence for planning storage and processing, but it is an older 2020 sample and cannot establish current-market execution quality.
>
> It also confirms two issues our validation must explicitly handle: event timestamps may not represent matching-engine time, and trades/depth updates sharing timestamps require a deterministic ordering policy. We must not treat a syntactically valid dataset as automatically suitable for fill calibration.

## 2. Operational audit log

### 2.1 Repository state inspected

Read from `main`:
- `ROADMAP.md`
- `RULES.md`
- `DECISIONS.md`
- `docs/EXCHANGE_AND_DATA_SHORTLIST.md`
- `docs/CHATGPT_CONVERSATIONS/README.md`
- `docs/CHATGPT_CONVERSATIONS/2026-11-16-021-multi-currency-collateral-liquidation.md`

Confirmed:
- Phase 01 remains IN PROGRESS.
- Phase 02 remains LOCKED.
- D-012 authorises bounded Phase 01 research only.
- No venue, data vendor, account mode or product is selected.
- No account/API key, testnet, paid service, runtime integration or trading is authorised.

### 2.2 Current documentation research

Reviewed:
- [Tardis downloadable CSV documentation](https://docs.tardis.dev/downloadable-csv-files)
- [Tardis data types/schema](https://docs.tardis.dev/downloadable-csv-files/data-types)
- [Tardis dataset API reference](https://docs.tardis.dev/downloadable-csv-files/api)
- [Tardis data FAQ](https://docs.tardis.dev/faq/data)
- [HftBacktest v2.2.0 Data Preparation](https://hftbacktest.readthedocs.io/en/py-v2.2.0/tutorials/Data%20Preparation.html)
- [OKX historical data portal](https://www.okx.com/historical-data)

HftBacktest's documentation records a successful historical Tardis Binance Futures example for 2020-02-01: 3,090,479-byte trades gzip, 250,016,849-byte incremental-L2 gzip, and 27,532,602 converted events. This is a third-party tutorial's historical example, not a current live retrieval result.

### 2.3 Retrieval attempts

Direct requests from the execution container to the following Tardis endpoints all failed with DNS resolution error `[Errno -3] Temporary failure in name resolution`:
- `binance-futures/book_snapshot_5/2020/09/01/BTCUSDT`
- `binance-futures/incremental_book_L2/2020/09/01/BTCUSDT`
- `binance-futures/trades/2020/09/01/BTCUSDT`
- Tardis `/v1/exchanges/binance-futures` metadata

The browser retrieval route also could not access the gzip file. A prior timeout is recorded in audit 021. No bytes were downloaded. No gzip, CSV, schema, order-book reconstruction, sequence, depth, timestamp or trade-alignment test was run. No data-quality pass is claimed.

### 2.4 Technical findings added

- A Tardis incremental L2 CSV includes exchange, symbol, exchange timestamp, local receive timestamp, snapshot flag, side, price and amount.
- A new snapshot replaces prior book state; zero amount removes a price level.
- Rows with the same local timestamp may be one multi-level message; preserve row order and grouping.
- Tardis documents start-of-day and reconnect snapshots, reconnect gaps around 300–3,000 ms, disconnect markers omitted from downloadable CSV, and cross-channel timing without guaranteed causal synchronization.
- Tardis L2 is market-by-price, not market-by-order; it cannot establish exact FIFO queue position.
- HftBacktest's sample demonstrates meaningful storage and processing requirements: roughly 238 MiB compressed L2 for one day and 27.5 million converted events.
- Exchange timestamps may reflect server send time rather than matching-engine event time. Preserve local and exchange timestamps separately and test skew.

### 2.5 Documentation writes

Created:
- `docs/HISTORICAL_L2_SAMPLE_VALIDATION.md`

Updated:
- `ROADMAP.md`
- `docs/EXCHANGE_AND_DATA_SHORTLIST.md`

The report explicitly records the failed retrieval, documented historical sample sizes, schema/reconstruction facts, a pass/not-run matrix, capacity implications and the exact next validation procedure. The roadmap keeps the gate BLOCKED and does not mark it verified.

## 3. Test and audit status

- Isolated code tests: NOT APPLICABLE; no code was changed.
- Integration tests: NOT RUN; no dataset or runtime integration available.
- Regression tests: NOT RUN; no code changed.
- Data integrity and reconstruction tests: NOT RUN; no bytes obtained.
- Five-axis audit:
  1. Correctness: no unsupported data-quality claims; evidence and limitations separated.
  2. Scope: Phase 01 research only; no runtime or venue selection.
  3. Security: no secrets, credentials, accounts or authenticated requests.
  4. Maintainability: reproducible URLs, schema facts and acceptance matrix documented.
  5. Cost: no paid services or infrastructure; public documentation and local attempts only.

## 4. Current state and next step

- Phase 01: IN PROGRESS.
- Historical L2 sample validation: BLOCKED pending actual bytes.
- Phase 02: LOCKED.
- NautilusTrader: research candidate only; not adopted.
- Venue/product/data vendor: none selected.
- No account connection, API key, testnet, paper/live order, paid subscription or runtime integration.

**Next step:** obtain real incremental L2 and paired trade files from a reachable no-cost source, then run the full validation matrix in `docs/HISTORICAL_L2_SAMPLE_VALIDATION.md`.

**Owner approval:** not required for this bounded Phase 01 research continuation under D-012; approval remains required before Phase 02, implementation, venue/account connection, trading, risk changes or spending.


## 5. Publication and read-back verification addendum

The following documentation commits were created sequentially on `main` and all five target files were fetched again successfully:
- Validation report `docs/HISTORICAL_L2_SAMPLE_VALIDATION.md`: `cff215acedfc731581c692c02f3ef8dc32dd0174`.
- Roadmap `ROADMAP.md`: `184c57a27252273de4ac1a2f467a511bf73d0a3f`.
- Exchange/data shortlist `docs/EXCHANGE_AND_DATA_SHORTLIST.md`: `96e298a90e94ce9b31d10c48b3e1c7bd2f4b74e6`.
- This conversation record: `b26adbe552f6efbf40a4ec3339e3ac3ecf222aa1`.
- Audit index `docs/CHATGPT_CONVERSATIONS/README.md`: `0ea0288af9b46004cabe3203d648f0c3310cdeb9`.

Read-back verification confirmed the validation report contains the BLOCKED disposition and historical sample size evidence; ROADMAP links the report and keeps the gate open; the shortlist contains the follow-up findings; this record contains the retrieval failures; and the audit index contains record 022. The final audit-record update below records these commit references.
