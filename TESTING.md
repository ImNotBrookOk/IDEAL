# IDEAL Testing and Verification

## Required task evidence
Every task must define acceptance criteria before implementation and record exact commands, environment, commit, test counts, failures and resolutions. Never infer success from a tool returning without error.

## Test layers
- Static analysis, formatting, type checks and dependency/security scans.
- Unit tests for pure calculations and state transitions.
- Property-based tests for invariants and boundary conditions.
- Component tests with deterministic fixtures.
- Contract tests between modules and exchange adapters.
- Integration tests across all previously verified dependencies.
- Regression tests for every previously discovered defect.
- Historical replay and deterministic reproducibility tests.
- End-to-end data → decision → risk → paper order → fill → ledger → lesson.
- Fault injection for stale/missing data, disconnects, rate limits, clock drift, partial fills, duplicate events, process restarts and storage failures.
- Security tests for secret exposure, untrusted payloads and strategy sandboxing.
- Long-duration paper soak tests before operational readiness.

## Trading-specific checks
- No look-ahead, survivorship or train/test leakage.
- Fees, spread, slippage, funding, latency and partial fills included.
- Correct candle boundaries, timezone handling and indicator warm-up.
- No duplicate orders from retries; idempotency and reconciliation required.
- Risk sizing and stop distance validated against equity, precision, tick/lot sizes and leverage.
- Daily loss includes realised and unrealised PnL and resets only at UTC day boundary.
- Cooldown persists across restarts.
- UNKNOWN regime or ineligible strategy produces no trade.
- Gate demotion revokes permissions while preserving history and lessons.
- AI failure or malformed output cannot bypass deterministic controls.

## Research artifact retention
- CI jobs must delete raw market-data files in a separate unconditional cleanup step before uploading artifacts.
- Cleanup must run even if retrieval, parsing, reconstruction or acceptance assertions fail.
- Upload only hashes, manifests and small audit summaries; do not upload raw market data.
- Use explicit short retention for temporary research artifacts and record artifact IDs/expiry in the audit log.
- Test the failure path: force an acceptance assertion to fail and verify that the resulting artifact contains no raw archives.

## Evidence standard
A test is VERIFIED only when its command was actually run and its output recorded. Report skipped tests explicitly. No paper/live readiness claim without full end-to-end evidence and an approved operational checklist.

### 16 November 2026 — cleanup failure-path verification

The three-day OKX alignment workflow [#43777626875](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43777626875) intentionally failed the original 98% side-consistency acceptance screen on 13 November, but its separate unconditional cleanup step completed before artifact upload. Resulting artifact 14187715114 was only 3,348 bytes and contained summaries/manifests, not raw archives. This verifies the corrected failure path. The earlier artifact 14187155843 remains a documented one-off cleanup defect and expires 18 November 2026 at 23:55 UTC.
