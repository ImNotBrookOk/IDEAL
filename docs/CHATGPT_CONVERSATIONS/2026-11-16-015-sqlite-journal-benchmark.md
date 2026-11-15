# IDEAL Conversation Record 015 — SQLite Event Journal Performance Baseline

**Date:** 16 November 2026  
**Scope:** Phase 01 persistence capacity research — SQLite WAL throughput, latency, storage and recovery measurements  
**Status:** PR #21 merged; 71 tests pass and the informational benchmark completes. Research only.

## Available user-visible transcript

### User
> Ok keep going

### Assistant
Continued with a small-scale SQLite event-journal benchmark. The objective is to quantify write throughput, append latency, database/WAL growth, checkpoint verification and replay time, while keeping the distinction clear between GitHub-hosted runner measurements and actual always-free worker capacity.

## Operational audit log

### 1. Benchmark implementation

Added `research/nautilus_poc/benchmark_event_journal.py` and an informational CI step:
- Standard-library only.
- 5,000 event commits per payload-size case.
- Payload sizes 256 bytes and 1,024 bytes.
- One transaction per event, SQLite WAL mode and `synchronous=FULL`.
- Midpoint checkpoint after 2,500 events, followed by 2,500 more events.
- Full hash-chain verification, checkpoint load and tail replay.
- Captures throughput, p50/p95/p99/max append latency, WAL/DB size, snapshot, verification, restore and peak RSS.
- No pass/fail throughput threshold.

### 2. Benchmark results

Initial benchmark [CI run 43756858418](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43756858418):

| Metric | 256B payload | 1,024B payload |
|---|---:|---:|
| Events | 5,000 | 5,000 |
| Throughput | 10,779 events/s | 10,813 events/s |
| p50 append latency | 0.0736 ms | 0.0756 ms |
| p95 append latency | 0.1976 ms | 0.1744 ms |
| p99 append latency | 0.3382 ms | 0.2982 ms |
| Maximum append latency | 1.4036 ms | 1.3900 ms |
| Database size after close | 4.04 MB | 10.85 MB |
| WAL size before close | 4.14 MB | 4.14 MB |
| Full chain verification | 0.0527 s | 0.0659 s |
| Snapshot + tail restore | 0.0658 s | 0.0791 s |

Environment: GitHub-hosted Ubuntu 24.04 x86_64, 4 vCPU, Python 3.14.10, SQLite 3.45.1; peak process RSS 36,964 KiB (~36.1 MiB).

Final PR-head confirmation [CI run 43756973411](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43756973411):
- **71 tests passed in 0.39s**.
- 256B: 11,040 events/s; p50 0.0711 ms; p95 0.1608 ms; p99 0.2805 ms.
- 1,024B: 11,136 events/s; p50 0.0756 ms; p95 0.1224 ms; p99 0.2588 ms.
- Peak RSS 36,228 KiB (~35.4 MiB).
- Snapshot verification and replay remained below 0.08 seconds per case.

The initial result set is used in the research report as the primary baseline; final PR-head CI confirms similar throughput with normal run-to-run variation.

### 3. Interpretation and limitations

- Synthetic microbenchmark on a GitHub-hosted runner, not the candidate always-free worker.
- Runner disk and CPU are not known to match Oracle Always Free or another target.
- Not a production SLO; event distribution, disk class, checkpoint frequency, concurrency, WAL checkpointing, backups and long-run growth materially affect results.
- Does not test disk-full behavior, power loss, network filesystem semantics, off-host backup, encryption overhead or concurrent multi-writer contention.
- No always-free VM, persistent volume or $0 deployment was activated or verified.
- SQLite still requires persistent local storage; ephemeral runner storage is not suitable for production durability.

### 4. CI, review and merge

- Final PR-head CI [run 43756973411](https://github.com/ImNotBrookOk/IDEAL/actions/runs/43756973411): 71 tests passed and benchmark completed successfully.
- Five-axis review:
  - Correctness: benchmark asserts event count, checkpoint sequence and tail replay count.
  - Security: synthetic payloads, no secrets or external service.
  - Cost: standard library; public-repo CI only.
  - Maintainability: reproducible CLI, JSON output and non-gating semantics.
  - Scope: benchmark, CI step and docs only.
- Final PR head `0bd7bdb67135b33dce81b34f90913828cad6c40d` matched branch ref before merge.
- [PR #21](https://github.com/ImNotBrookOk/IDEAL/pull/21) squash-merged under D-012.
- Merge commit: `b17c072f5b2babf4d5633710a79579909c677798`.

## Documentation updated

- [Roadmap](https://github.com/ImNotBrookOk/IDEAL/blob/main/ROADMAP.md): records baseline and leaves candidate-worker capacity/persistence verification open.
- [POC README](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/README.md): benchmark command and result.
- [Execution realism report](https://github.com/ImNotBrookOk/IDEAL/blob/main/research/nautilus_poc/execution_realism_matrix.md): detailed baseline and limitations.

## Next work

- Run the same benchmark on an actual candidate always-free worker after availability and persistent-volume guarantees are verified.
- Benchmark representative IDEAL event types and larger event counts (100k/1M), WAL checkpointing and restore time.
- Verify disk growth, backup/restore and encryption overhead.
- Continue component licence review, stable release pin review and final component selection.
- No production integration, exchange adapter, account, paper/live trading or paid service was introduced.

## Current state

- Phase 01: IN PROGRESS.
- Phase 02: LOCKED.
- Implementation phases: LOCKED.
- Isolated POC suite: 71 passing tests.
- SQLite event journal: prototype and synthetic benchmark only.
- Candidate always-free worker and persistent storage: NOT VERIFIED.
