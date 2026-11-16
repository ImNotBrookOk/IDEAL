# 039 — Owner acceptance of seven-day OKX research dataset

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Phase state:** IN PROGRESS; Phase 02 remains LOCKED  
**Decision scope:** Historical-data research classification only

## Owner decision

The owner explicitly accepts the seven-day OKX BTC-USDT-SWAP 400-level L2/trade dataset **as it currently stands**, with the risk-weighted, conditional historical market-structure research classification. The owner does not require another seven-day rerun or further attempts to force the original strict screen to pass before continuing the remaining Phase 01 work.

This is acceptance of the dataset's bounded research utility, **not** acceptance of the original strict test as passed and not an execution-grade approval.

## Evidence retained without alteration

The revalidation workflow [#43803546192](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43803546192) completed all seven daily calculations. Its overall conclusion was **failure of the original strict quality gates** on 7 and 8 November. It did not fail during retrieval, parsing, unit tests or cleanup:

- Research alignment unit tests passed.
- All seven L2 archives and paired trade archives downloaded and passed integrity checks.
- All seven daily calculations completed.
- The original strict result remains **5/7 days passed**; no threshold was relaxed.
- The 7 November unmatched trade is exactly 2 ms before the first available book snapshot (497,187 of 497,188 trades aligned); p95 BBO age is 32 ms and max age 519 ms.
- 8 November has zero missing/invalid matches but 96.45299% taker-side/preceding-BBO consistency, with the discrepancy concentrated in observations aged <=10 ms.
- Across 19,918,682 aligned trades, 97.7260% are <=20 ms old, 99.5248% <=50 ms, 99.9238% <=100 ms and 99.9948% <=250 ms. Daily maximum age ranges from 475 to 519 ms.
- The unconditional raw-archive cleanup step completed after the acceptance failure. Only summary files were uploaded.

Summary artifact: [14198101057](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43803546192/artifacts/14198101057), 7,243 bytes, ZIP SHA-256 `a289e133ff5d8284ca96d29260c3f54f12c347f9606e54ab9ad46bde92126f18`.

## Approved use boundary

1. Retain the seven-day sample as a conditional historical market-structure research candidate.
2. Preserve day-level quality flags, observation ages, denominators and the 7 November initial-boundary row.
3. Require downstream features and models to declare freshness budgets and exclude or explicitly down-weight stale observations.
4. Prefer 9–13 November for stricter historical analysis; 7 and 8 November remain conditional, not silently averaged into a pass.
5. Do not use this sample as execution-grade fill calibration or to claim exact event ordering, FIFO queue position, passive-fill fidelity, sequence continuity, live venue eligibility or operational readiness.
6. Do not rerun this same seven-day test solely to obtain a green workflow. Reopen only if a materially new source, schema, alignment method or research requirement justifies it.

## Progress decision

The seven-day dataset classification gate remains **closed — conditionally accepted by owner**. Work proceeds on the other Phase 01 exit items: dependency/security remediation and reproducible supply-chain evidence, the bounded $0 persistent-host decision, final component dispositions, and documentation/audit verification.

This checkpoint does not close Phase 01, unlock Phase 02, select a venue, authorise exchange connectivity, runtime integration, paper/live trading or paid infrastructure.
