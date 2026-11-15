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

At the time of this audit entry, the workflow was still running. Its result must be appended when complete; it is not marked as passed here.

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
