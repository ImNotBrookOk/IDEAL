# IDEAL Conversation Record 014 — SQLite Event Journal and Durable Recovery Prototype

**Date:** 16 November 2026  
**Scope:** Phase 01 persistence research — NautilusTrader cache adapters, durable event journal, checkpoints and crash recovery  
**Repository:** [ImNotBrookOk/IDEAL](https://github.com/ImNotBrookOk/IDEAL)  
**Status:** PR #20 merged; 71 tests pass on final PR head. Research only.

## Available user-visible transcript

### User
> Ok keep going

### Assistant
The next investigation is durable process restart and checkpoint/restore. Pinned NautilusTrader source shows Redis and PostgreSQL cache adapters, but the Python BacktestEngine wrapper in this release does not expose database injection. A standalone SQLite event journal is therefore being prototyped as a $0, standard-library research option.

## Operational audit log

### 1. NautilusTrader v2.0.0rc9 source audit

Inspected:
- `crates/common/src/cache/config.rs`
- `crates/common/src/cache/database.rs`
- `crates/common/src/python/cache.rs`
- `crates/backtest/src/python/engine.rs`
- `crates/infrastructure/src/redis/cache.rs`
- `crates/infrastructure/src/sql/cache.rs`
- `crates/live/src/node/builder.rs`
- `crates/live/src/python/node.rs`
- `crates/live/src/node/config.rs`

Findings:
- `CacheConfig`: `persist_account_events=true`, `save_market_data=false`, `flush_on_start=false`; tick/bar capacities default to 10,000; `drop_instruments_on_reset=true`.
- Cache database interface supports accounts, orders, positions, order/position snapshots, actor/strategy state, account events and supported market data.
- Python `PyCache` constructs `Cache::try_new(config, None)`; no `set_database` API is exposed.
- Python `BacktestEngine` constructs `BacktestEngine::new(config)`; no cache database factory injection is exposed.
- Python `LiveNodeBuilder` exposes a cache database factory; `LiveNodeConfig.load_state/save_state` exist but default false. These component state persistence controls are not a full process checkpoint of scheduler/data-cursor/exchange-session state.
- Redis adapter requires Redis 6.2+. It does not support persisting quotes, trades, funding rates, bars or order books in this release. Its `flush()` calls `FLUSHDB`, clearing the entire logical Redis DB, including other traders and unrelated keys.
- PostgreSQL adapter supports quotes, trades, funding rates and bars, but not order-book persistence. Its flush operation is scoped to trader rows. Integration tests require a PostgreSQL service and are Linux-only.
- No SQLite cache adapter exists in the pinned repository.
- Therefore neither adapter is a complete replay/checkpoint system, and neither can be injected into the Python BacktestEngine in this pin.

### 2. SQLite event journal prototype

Added:
- `research/nautilus_poc/event_journal.py`
- `research/nautilus_poc/test_event_journal.py`

Design:
- Standard-library `sqlite3`; no extra dependency or database server.
- File-backed WAL mode, `synchronous=FULL`, foreign keys, configurable busy timeout.
- Append-only event table with monotonic sequence, unique event ID, type, timestamp, canonical payload, previous hash and SHA-256 event hash.
- Fixed genesis hash; `BEGIN IMMEDIATE` serializes writes.
- Exact duplicate event IDs are idempotent; same ID with different content raises conflict.
- Canonical decimal strings; floats are rejected.
- Checkpoints persist canonical state, state hash, event sequence and chain hash anchor.
- Restore validates the entire event chain, snapshot state hash and chain anchor, then reads events after the checkpoint sequence.
- SQLite schema version is stored in `PRAGMA user_version`; unsupported newer versions fail closed.

Ten tests cover:
1. Close/reopen durability.
2. Abrupt writer-process exit after commit, followed by WAL recovery from a new process/connection.
3. Idempotent duplicate and conflicting duplicate event IDs.
4. Event payload tampering.
5. Checkpoint restore and post-checkpoint event replay.
6. Snapshot chain-anchor tampering.
7. Float rejection.
8. Newer schema version rejection.
9. Event metadata-column tampering (event ID/type/timestamp must agree with canonical payload).
10. Snapshot state tampering.

### 3. Test debugging and corrections

- First CI attempt failed because the event and snapshot document schema identifiers differed from the default replay-audit schema. The canonical JSON helper was generalized to accept an explicit expected schema, and the event journal now validates its own `ideal-event/v1` and `ideal-state-snapshot/v1` documents.
- Additional integrity tests were added after review: DB metadata columns must agree with canonical event payload, and snapshot state must match its hash.
- A security review clarified that a hash chain stored in the same database detects accidental/partial corruption but cannot stop a malicious writer with full database access from recomputing the entire chain. Stronger tamper evidence requires an off-host signed checkpoint, external HMAC key or immutable external hash anchor.
- Final PR-head CI [run 43756674011](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43756674011): **71 passed in 0.40s**, exact NautilusTrader pin, Ubuntu 24.04 / Python 3.14.

### 4. Five-axis review and merge

- **Correctness:** event chain, idempotency, checkpoint anchor, state hash, metadata consistency, crash recovery and post-snapshot replay are tested.
- **Security:** parameterized SQL, canonical payload validation, no secrets; threat model documents limits of an in-database hash chain.
- **Cost:** Python standard library only; no server or paid service.
- **Maintainability:** versioned schema, explicit errors, focused API, migration version check and regression suite.
- **Scope:** isolated research module/tests/docs only; no production runtime or dependency changes.
- Final PR head `6cdf8306fefc022e6bacd86528436220a3ac6841` matched the branch ref before merge.
- [PR #20](https://github.com/ImNotBrookOk/IDEAL/pull/20) squash-merged under D-012.
- Merge commit: `d79ede3b00211e4576440b765bad59dff169db3d`.

## Documentation updated

- [Roadmap](https://github.com/ImNotBrookOk/IDEAL/blob/main/ROADMAP.md): SQLite event journal prototype completed; runtime integration, external hash anchoring, encrypted backup/restore, retention and benchmarks remain open.
- [POC README](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/README.md): event journal usage, coverage and threat-model caveat.
- [Execution realism report](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/execution_realism_matrix.md): upstream cache adapter limitations and SQLite design.

## Remaining work

- Integrate the journal with IDEAL's runtime event flow (not authorised yet; remains Phase 02/implementation locked).
- External signed hash anchoring, encryption at rest, key management and off-host backups.
- Restore verification, retention/compaction, schema migrations and disk-full/corruption recovery.
- Performance/capacity benchmark at realistic event rates and payload sizes.
- Multi-writer design; current prototype is a single-writer journal.
- Full Nautilus engine/exchange session checkpoint is not provided by this journal.
- Persistent local disk required; ephemeral worker storage is not acceptable.
- Candidate worker cost/availability and persistent-volume guarantees remain unverified.

## Current state

- Phase 01: IN PROGRESS.
- Phase 02: LOCKED.
- Implementation phases: LOCKED.
- Isolated POC suite: 71 passing tests.
- No production runtime integration, dependencies, exchange adapter, credentials, account, testnet, paper/live trading or paid service introduced.
