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

## Evidence standard
A test is VERIFIED only when its command was actually run and its output recorded. Report skipped tests explicitly. No paper/live readiness claim without full end-to-end evidence and an approved operational checklist.