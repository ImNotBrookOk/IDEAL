# Conversation 028 — OKX consecutive-day 400-level reconstruction

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Scope:** Research-only public historical data validation. No exchange credentials, accounts, paid infrastructure, runtime integration, paper trading or live trading.

## Owner direction

The owner instructed us to continue until Phase 01 is fully confirmed, saving, documenting and auditing each checkpoint. Existing governance and market scope remain unchanged.

## Checkpoint 1 — consecutive-day reconstruction

Workflow [#43774295757](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43774295757) completed successfully. It retrieved and reconstructed:
- BTC-USDT-SWAP module-4 400-level L2 for 11 November 2026;
- BTC-USDT-SWAP module-4 400-level L2 for 12 November 2026;
- BTC-USDT-SWAP module-5 5,000-level L2 for 11 November 2026.

Both 400-level days had 96 snapshots, 400 levels per side, approximately 6.6 million records, median six combined level changes per update and zero empty/crossed/locked/invalid reconstructed states. Exact 10 ms intervals were 85.929% on 11 November and 85.957% on 12 November. The module-5 5,000-level reference had 86,400 records and 99.947% exact one-second intervals.

Archive SHA-256:
- 11 Nov 400-level: e4a315e221c106fb59da079632ce4d4605e7e8e22cab810f350959a8950c7426
- 12 Nov 400-level: 6dd55534ddd376c6995bfac584f1e1a19ed64083b76b542da61ee488cacbdfce
- 11 Nov 5,000-level: b7a2e597f7e286d6b14c9fd50abe92a067af76b0129e99a04726a795ed44829f

The workflow passed the archive reconstruction unit tests, archive integrity checks and full state reconstruction. Artifact ID 14185851827, SHA-256 db78a9d5611552974f9bc581cf8c3cc1328dfdad7112e4e28dce20034e31e2e6, contains only manifests and summaries, expires 18 November 2026 23:28 UTC. Raw archives were deleted before artifact upload and were not committed.

## Third tuple field — evidence refinement

Official OKX API documentation states that GET /api/v5/market/books-full uses three-element order-book arrays [price, quantity, number of orders at the price] (https://app.okx.com/docs-v5/en/, GET / Full order book). This strongly corroborates interpreting the archive's three-element tuple third integer as an order count. However, the downloadable module-4/module-5 archive format is not explicitly specified in the retrieved official documentation. The current 400-level books/books-l2-tbt WebSocket arrays are four-element tuples containing a deprecated zero field followed by order count. Therefore the archive field remains raw and optional pending archive-specific confirmation. It is not a FIFO/queue-position indicator.

## Checkpoint 2 — adjacent-day trade alignment

A second workflow [#43776264061](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43776264061) was configured to:
- retrieve both 11 and 12 November 400-level archives;
- retrieve the adjacent UTC+8 trade files needed to cover both UTC days;
- run the existing six focused alignment tests;
- align each trade only to a strictly preceding book state;
- apply the initial quality gates independently to each day: nonzero aligned trades, zero missing preceding books, zero invalid book matches, p95 book age <=20 ms and side consistency >=98%.

Workflow #43776264061 completed successfully. Both days passed independently: 2,597,825 aligned trades on 11 November and 3,224,415 on 12 November; zero trades without a preceding book; zero invalid-book matches; median age 6 ms on each day; p95 age 18 ms / 10 ms; maximum age 497 ms / 509 ms; directional side consistency 99.118% / 98.542%. Same-timestamp trades were conservatively assigned to the preceding book (9.400% / 9.646%). Outside-spread prints were 64.445% / 62.584%; outside-distance p95 was 1.35 / 1.40 bps. Both days passed the initial gates (nonzero aligned trades, no missing preceding book, no invalid matches, p95 <=20 ms, side consistency >=98%). The outside-spread percentage is not a direct defect measure; 10 ms sampled states can miss intermediate updates. The stale tail and missing sequence IDs remain material limitations.

Artifact ID 14186960490, SHA-256 4e1e7cd7dece1882b72a07c85140aec39c95faa859e845de8be7eb09673ba55c, contains only summaries/manifests and expires 18 November 2026 23:47 UTC. Raw L2/trade archives were deleted before upload.

**Checkpoint 2 disposition:** two-day no-lookahead alignment is provisionally passed for sampled market-quality and conservative taker-impact research. It is not FIFO queue-position or exact passive-fill grade.

## Documentation updated and read-back required

- docs/HISTORICAL_L2_SAMPLE_VALIDATION.md, section 12.10
- docs/EXCHANGE_AND_DATA_SHORTLIST.md, section 13.8
- ROADMAP.md
- this conversation audit and its index

## Disposition

Two-day structural repeatability is provisionally passed. Trade alignment across both days is still pending. No venue is selected and no runtime integration is approved. Phase 01 remains IN PROGRESS; Phase 02 and implementation phases remain LOCKED.


## Additional deployment constraint — live feed entitlement

OKX's official WebSocket documentation states that 400-level 10 ms books-l2-tbt requires VIP4+; standard 400-level books updates at 100 ms; bbo-tbt is one-level/10 ms. Public historical 10 ms archives therefore do not establish equivalent live feed availability. Any 100 ms or BBO fallback requires separate calibration and must not inherit the 10 ms full-depth strategy assumptions. No account or VIP entitlement was checked or connected.

Official source: https://app.okx.com/docs-v5/en/, “WS / Order book channel”.


## New Zealand derivatives eligibility — hard gate

The FMA states that anyone offering derivatives to retail investors in New Zealand must hold a derivatives issuer licence; its crypto guidance specifically requires crypto CFD providers to hold an FMA derivatives issuer licence and directs users to verify providers of other crypto derivatives. This creates a hard gate before any NZ retail venue selection or account/API connection.

Public-source review:
- Binance NZ official entity-services list does not list derivatives issuance; NZ futures pages currently show no records. This does not prove the global futures product is unavailable or available to NZ users.
- Bybit's NZ addendum names Kono Group Limited as the contracting party and limits NZ users to “NZ Supported Services”, but does not enumerate the products.
- OKX's 14 November 2026 disclosure does not name NZ in its open-ended restricted/limited jurisdiction lists; this does not establish product-level derivatives availability or local licensing.

Sources: FMA derivatives guidance https://www.fma.govt.nz/consumer/investing/types-of-investments/derivatives ; FMA crypto guidance https://www.fma.govt.nz/consumer/investing/types-of-investments/cryptocurrencies/ ; Binance entity/services https://www.binance.com/en-GB/legal/licenses ; Bybit NZ addendum https://www.bybit.global/common-static/compliance/legal/BYBIT/700f3662d5d08a2d6cc9e75b47e381f0.pdf ; OKX disclosure https://www.okx.com/help/risk-compliance-disclosure .

No venue is confirmed eligible. This is not a legal conclusion that all are prohibited; exact entity, product, retail/wholesale classification and any licence/exemption require authoritative confirmation and independent legal advice. No exchange account, API key or trading action is authorised.


### Staleness sensitivity follow-up

The age histogram was converted into retained-trade coverage for explicit cutoffs. At <=50 ms, 99.229% of 11 Nov trades and 99.492% of 12 Nov trades remain; at <=20 ms, 96.273% and 97.628%; at <=10 ms, 92.503% and 95.001%. This is a research sensitivity analysis, not an approved runtime threshold. Keep sample age as an explicit field and never interpolate stale book depth. Full table in historical validation section 12.12.
