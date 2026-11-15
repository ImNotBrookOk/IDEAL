#!/usr/bin/env python3
"""Research-only reconstruction audit for Tardis normalized incremental L2 CSV."""

from __future__ import annotations

import argparse
import collections
import csv
import gzip
import heapq
import json
import math
from decimal import Decimal, InvalidOperation
from itertools import groupby
from pathlib import Path


def _decimal(value: str, field: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"invalid {field}: {value!r}") from exc
    if not result.is_finite():
        raise ValueError(f"non-finite {field}: {value!r}")
    return result


def _snapshot_flag(value: str) -> bool:
    normalized = str(value).strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ValueError(f"invalid is_snapshot value: {value!r}")


class TardisBook:
    def __init__(self) -> None:
        self.bids: dict[Decimal, Decimal] = {}
        self.asks: dict[Decimal, Decimal] = {}
        self._bid_heap: list[Decimal] = []
        self._ask_heap: list[Decimal] = []
        self.deleted_levels = 0

    def reset(self) -> None:
        self.bids.clear()
        self.asks.clear()
        self._bid_heap.clear()
        self._ask_heap.clear()

    def apply(self, row: dict[str, str]) -> None:
        side = row.get("side", "").strip().lower()
        if side not in ("bid", "ask"):
            raise ValueError(f"invalid side: {side!r}")
        price = _decimal(row.get("price", ""), "price")
        amount = _decimal(row.get("amount", ""), "amount")
        if price <= 0:
            raise ValueError(f"price must be positive: {price}")
        if amount < 0:
            raise ValueError(f"amount must be non-negative: {amount}")

        book = self.bids if side == "bid" else self.asks
        heap = self._bid_heap if side == "bid" else self._ask_heap
        if amount == 0:
            if price in book:
                del book[price]
            self.deleted_levels += 1
            return

        if price not in book:
            heapq.heappush(heap, -price if side == "bid" else price)
        book[price] = amount

    @staticmethod
    def _best(book: dict[Decimal, Decimal], heap: list[Decimal], is_bid: bool):
        while heap:
            key = heap[0]
            price = -key if is_bid else key
            if price in book:
                return price
            heapq.heappop(heap)
        return None

    def best_bid(self):
        return self._best(self.bids, self._bid_heap, True)

    def best_ask(self):
        return self._best(self.asks, self._ask_heap, False)

    def status(self) -> str:
        bid = self.best_bid()
        ask = self.best_ask()
        if bid is None or ask is None:
            return "empty"
        if bid > ask:
            return "crossed"
        if bid == ask:
            return "locked"
        return "valid"


def audit_rows(rows) -> dict:
    book = TardisBook()
    row_count = message_count = snapshots = updates = skipped = 0
    status_counts = collections.Counter()
    previous_local_ts = None
    previous_snapshot = False
    have_snapshot = False
    last_processed_local_ts = None
    max_gap_us = 0
    first_exchange_ts = last_exchange_ts = None

    for local_ts_text, grouped_rows in groupby(rows, key=lambda row: str(row["local_timestamp"])):
        local_ts = int(local_ts_text)
        if previous_local_ts is not None and local_ts < previous_local_ts:
            raise ValueError(f"local_timestamp moved backwards: {local_ts} < {previous_local_ts}")
        previous_local_ts = local_ts
        message_rows = list(grouped_rows)
        if not message_rows:
            continue
        message_count += 1
        flags = {_snapshot_flag(row.get("is_snapshot", "")) for row in message_rows}
        if len(flags) != 1:
            raise ValueError("mixed is_snapshot flags within one local_timestamp message")
        is_snapshot = flags.pop()

        for row in message_rows:
            row_count += 1
            exchange_ts = int(row["timestamp"])
            first_exchange_ts = exchange_ts if first_exchange_ts is None else min(first_exchange_ts, exchange_ts)
            last_exchange_ts = exchange_ts if last_exchange_ts is None else max(last_exchange_ts, exchange_ts)

        if is_snapshot and (not have_snapshot or not previous_snapshot):
            book.reset()
            snapshots += 1
            have_snapshot = True
        elif not have_snapshot:
            skipped += len(message_rows)
            previous_snapshot = is_snapshot
            continue
        else:
            updates += 1

        for row in message_rows:
            book.apply(row)

        if last_processed_local_ts is not None:
            max_gap_us = max(max_gap_us, local_ts - last_processed_local_ts)
        last_processed_local_ts = local_ts
        status_counts[book.status()] += 1
        previous_snapshot = is_snapshot

    if row_count == 0:
        raise ValueError("Tardis CSV contains no data rows")
    if not have_snapshot:
        raise ValueError("Tardis CSV contains no initial snapshot")

    best_bid = book.best_bid()
    best_ask = book.best_ask()
    return {
        "rows": row_count,
        "messages": message_count,
        "snapshots": snapshots,
        "updates": updates,
        "rows_skipped_before_first_snapshot": skipped,
        "deleted_levels": book.deleted_levels,
        "book_status_counts": dict(status_counts),
        "max_message_gap_ms": max_gap_us / 1000.0,
        "first_exchange_timestamp_us": first_exchange_ts,
        "last_exchange_timestamp_us": last_exchange_ts,
        "final_best_bid": float(best_bid) if best_bid is not None else None,
        "final_best_ask": float(best_ask) if best_ask is not None else None,
        "final_bid_levels": len(book.bids),
        "final_ask_levels": len(book.asks),
        "final_bid_amount_at_best": float(book.bids[best_bid]) if best_bid is not None else None,
        "final_ask_amount_at_best": float(book.asks[best_ask]) if best_ask is not None else None,
    }


def audit_gzip_csv(path: str | Path) -> dict:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"exchange", "symbol", "timestamp", "local_timestamp", "is_snapshot", "side", "price", "amount"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing required CSV columns: {sorted(missing)}")
        return audit_rows(reader)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--l2", required=True, help="Tardis incremental_book_L2 .csv.gz file")
    args = parser.parse_args()
    print(json.dumps(audit_gzip_csv(args.l2), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
