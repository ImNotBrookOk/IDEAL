"""Informational SQLite event-journal benchmark; no pass/fail throughput threshold."""
from __future__ import annotations

import argparse
import json
import os
import platform
from pathlib import Path
import resource
import sqlite3
import statistics
import sys
import tempfile
import time

from event_journal import EventJournal


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    index = round((len(ordered) - 1) * p)
    return ordered[index]


def run_case(directory: Path, event_count: int, payload_bytes: int) -> dict:
    path = directory / f"events-{event_count}-{payload_bytes}.sqlite"
    journal = EventJournal(path)
    latencies_ms: list[float] = []
    half = event_count // 2
    blob = "x" * payload_bytes

    write_start = time.perf_counter()
    for index in range(half):
        started = time.perf_counter()
        journal.append_event(
            event_id=f"evt-{index + 1:08d}",
            event_type="MarketEvent",
            event_ts_ns=index + 1,
            payload={
                "instrument_id": "BTCUSDT-PERP.BINANCE",
                "price": f"{40000 + index % 1000}.0",
                "quantity": "0.100",
                "blob": blob,
            },
        )
        latencies_ms.append((time.perf_counter() - started) * 1000)
    write_elapsed = time.perf_counter() - write_start

    snapshot_started = time.perf_counter()
    snapshot = journal.create_snapshot(
        snapshot_id="checkpoint-halfway",
        state={
            "cursor": half,
            "account": {"currency": "USDT", "balance": "10000.00"},
        },
        created_at_ns=half + 1,
    )
    snapshot_elapsed = time.perf_counter() - snapshot_started

    tail_started = time.perf_counter()
    for index in range(half, event_count):
        started = time.perf_counter()
        journal.append_event(
            event_id=f"evt-{index + 1:08d}",
            event_type="MarketEvent",
            event_ts_ns=index + 1,
            payload={
                "instrument_id": "BTCUSDT-PERP.BINANCE",
                "price": f"{40000 + index % 1000}.0",
                "quantity": "0.100",
                "blob": blob,
            },
        )
        latencies_ms.append((time.perf_counter() - started) * 1000)
    tail_write_elapsed = time.perf_counter() - tail_started

    verify_started = time.perf_counter()
    verification = journal.verify_chain()
    verify_elapsed = time.perf_counter() - verify_started

    restore_started = time.perf_counter()
    restored = journal.load_snapshot(snapshot.snapshot_id)
    replay_tail = journal.events_after(restored.through_seq)
    restore_elapsed = time.perf_counter() - restore_started
    assert len(replay_tail) == event_count - half
    assert verification["event_count"] == event_count

    wal_path = Path(str(path) + "-wal")
    wal_bytes_before_close = wal_path.stat().st_size if wal_path.exists() else 0
    journal.close()
    db_bytes_after_close = path.stat().st_size

    return {
        "events": event_count,
        "payload_bytes": payload_bytes,
        "write_events_per_second": round(event_count / (write_elapsed + tail_write_elapsed), 2),
        "write_latency_ms": {
            "p50": round(percentile(latencies_ms, 0.50), 4),
            "p95": round(percentile(latencies_ms, 0.95), 4),
            "p99": round(percentile(latencies_ms, 0.99), 4),
            "max": round(max(latencies_ms), 4),
        },
        "snapshot_seconds": round(snapshot_elapsed, 4),
        "verify_seconds": round(verify_elapsed, 4),
        "restore_and_tail_replay_seconds": round(restore_elapsed, 4),
        "wal_bytes_before_close": wal_bytes_before_close,
        "database_bytes_after_close": db_bytes_after_close,
        "verified_event_count": verification["event_count"],
        "replayed_tail_events": len(replay_tail),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", type=int, default=5000)
    parser.add_argument("--payload-sizes", type=int, nargs="+", default=[256, 1024])
    args = parser.parse_args()
    if args.events < 2 or args.events % 2:
        parser.error("--events must be an even integer >= 2")
    if any(size < 0 for size in args.payload_sizes):
        parser.error("payload sizes must be non-negative")

    with tempfile.TemporaryDirectory(prefix="ideal-journal-bench-") as temp:
        directory = Path(temp)
        cases = [
            run_case(directory, args.events, size)
            for size in args.payload_sizes
        ]
    print(json.dumps({
        "environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "sqlite": sqlite3.sqlite_version,
            "cpu_count": os.cpu_count(),
            "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
        "notes": [
            "GitHub-hosted runner measurement; not a target-worker benchmark.",
            "Informational only; no minimum throughput is asserted.",
            "Each append commits separately with SQLite WAL and synchronous=FULL.",
        ],
        "cases": cases,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
