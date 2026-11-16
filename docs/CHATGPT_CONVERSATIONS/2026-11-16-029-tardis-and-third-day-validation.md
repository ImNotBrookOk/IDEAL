# Conversation 029 — Tardis sample validation and third-day OKX diagnostics

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Scope:** Public market-data research only. No account/API credentials, paid services, runtime integration, paper or live trading.

## Owner direction

Continue Phase 01 until its acceptance gates are evidenced. Save, document and audit each checkpoint. Existing scope and governance remain unchanged.

## 1. Tardis parser — TDD and sample validation

A research-only parser was added at `research/tardis_l2_audit.py` with six tests in `research/tests/test_tardis_l2_audit.py`. The test-first workflow initially failed because the parser module did not exist; after implementation all six tests passed. The full research suite initially exposed a missing pinned `orjson==3.11.3` dependency in the new workflow; that CI dependency was added, and the full suite passed.

Workflow [#43777192211](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43777192211) downloaded the public Tardis first-of-month Binance Futures BTCUSDT L2 and trade samples for 1 November 2026 without an API key.

- L2 file: 429.9 MB compressed / 6,461,142,795 bytes uncompressed; SHA-256 8856e6e61b480976d9e1bc7ea49d4d18d25b281c56c6e6523bee6179d9558061.
- Trade file: 9.09 MB compressed / 103,671,148 bytes uncompressed; SHA-256 635a750afca5659cf7848487a1a8105e9dd8a38ce57254689b77ee7ec596efc4.
- L2: 79,438,130 rows, 3,242,436 local-timestamp message groups, one initial snapshot, 3,242,435 updates, 7,260,093 zero-amount deletions, zero pre-snapshot rows, and all 3,242,436 reconstructed states valid.
- Maximum gap between processed message groups: 276.101 ms.
- Trades: 1,190,743 rows; 587,069 buy and 603,674 sell; positive prices/amounts, expected schema, valid sides and nondecreasing local timestamps.
- Artifact ID 14187255879, 1,521 bytes, SHA-256 e7ee6eac5ddaf65fd89c0c692690fe109861bc9cf110f370244803bf004735be; summaries/hashes only; expiry 18 November 2026 23:58 UTC.

This validates one public Tardis normalized-L2 sample and our CSV reconstruction implementation. It does not establish paid data economics, commercial data rights, L3/FIFO identity, sequence continuity or event-level trade/BBO alignment.

## 2. Tardis Machine repository assessment

The Tardis Machine repository was reviewed: 313 stars, 60 forks, zero open issues, latest push and release 18.9.0 on 10 November 2026, MPL-2.0, TypeScript/Node 24.22.1+. It offers replay, normalization, local cache and realtime APIs, but depends on Tardis.dev data services and adds a second runtime stack. It is a useful reference/sidecar candidate, not adopted. Data rights for public sample files and paid service terms remain separate. See `docs/REPO_RESEARCH.md`.

## 3. Third OKX day — initial aggregate side-consistency gate failed

The first 11–13 November alignment attempt [#43776866247](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43776866247) completed the reconstruction and alignment, but 13 November failed the predeclared 98.0% aggregate side-consistency gate:
- 4,544,561 trades aligned to 7,391,929 book records;
- zero trades without a preceding book and zero invalid-book matches;
- median preceding-book age 5 ms, p95 10 ms, maximum 507 ms;
- 449,173 same-timestamp trades (9.884%), conservatively evaluated against the preceding book;
- side consistency 97.8348% (2.1652% mismatch), below the 98.0% gate;
- 64.718% outside the preceding sampled spread; outside-distance p95 1.89 bps, maximum 17.77 bps.

This is a real failed initial gate and must not be hidden by lowering the threshold. It is not yet known whether the discrepancy is concentrated in same-timestamp ties, stale samples or strict-preceding trades. A TDD extension now reports side consistency separately by timestamp-tie status and sample-age bucket. The added test was first run red (missing metrics), then the implementation was added. Workflow [#43777626875](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43777626875) is rerunning all three days with the expanded diagnostics and strict original threshold.

## 4. Raw-artifact retention correction

The failed 13 November acceptance assertion caused the previous workflow's in-step cleanup command to be skipped. Its `if: always()` artifact upload therefore retained raw archives/trade ZIPs in artifact ID 14187155843 (1,739,958,772 bytes; SHA-256 42e7902681ad57bdcf831964989aaa623d2530afade40c0b9fb9c7e49a9cbb21). It expires 18 November 2026 at 23:55 UTC. This artifact is temporary and not committed to Git history. The available GitHub connector exposes no artifact-delete action; do not claim it was deleted.

Corrective change: both OKX workflows now place raw archive removal in a separate `if: always()` step before artifact upload. The next run must be inspected to verify that the artifact contains only summaries/manifests even when an acceptance assertion fails.

## 5. Additional validations in progress

- [#43777630729](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43777630729): three-day OKX 400-level structural reconstruction (11–13 Nov).
- [#43777626875](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43777626875): three-day trade/BBO alignment and mismatch diagnostics.
- [#43777769642](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43777769642): same-day 1 November Tardis OKX Swap normalized L2 and official OKX 400-level archive reconstruction, with Tardis trades schema validation.

## Documentation updated

- `docs/HISTORICAL_L2_SAMPLE_VALIDATION.md`, section 12.13 (Tardis public sample).
- `docs/EXCHANGE_AND_DATA_SHORTLIST.md`, section 13.12.
- `docs/REPO_RESEARCH.md` (Tardis Machine and NautilusTrader POC progression).
- `ROADMAP.md` (Tardis sample and repo assessment).
- This conversation audit and index to be updated with final workflow outcomes.

## Disposition

The Tardis Binance Futures public sample/parser subgate passed. The OKX 11–12 November aggregate alignment gates passed; 13 November failed the aggregate side-consistency threshold and remains under diagnosis. No venue is selected. Live 10 ms full-depth entitlement, NZ derivatives eligibility, sequence continuity, passive-fill fidelity, free worker capacity and final component selection remain open. Phase 01 remains IN PROGRESS; Phase 02 and implementation phases remain LOCKED.
