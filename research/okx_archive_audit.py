#!/usr/bin/env python3
"""Independent, streaming audit of OKX historical L2 NDJSON archives.

The historical third level-tuple field is counted but deliberately not assigned
semantics. This tool is a research validator, not a production market-data adapter.
"""
from __future__ import annotations

import argparse
import collections
import heapq
import json
import math
import statistics
import tarfile
from pathlib import Path


class BookState:
    def __init__(self):
        self.bids: dict[str, tuple[float, float]] = {}
        self.asks: dict[str, tuple[float, float]] = {}
        self._bid_heap: list[float] = []
        self._ask_heap: list[float] = []
        self.duplicate_snapshot_levels = 0
        self.deleted_levels = 0

    @staticmethod
    def _number(value, field: str) -> float:
        try:
            result = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid {field}: {value!r}") from exc
        if not math.isfinite(result):
            raise ValueError(f"non-finite {field}: {value!r}")
        return result

    def _apply_side(self, rows, book, heap, is_bid: bool, snapshot: bool):
        for row in rows:
            if not isinstance(row, (list, tuple)) or len(row) < 2:
                raise ValueError("price level must contain at least price and quantity")
            price_text = str(row[0])
            price = self._number(row[0], "price")
            quantity = self._number(row[1], "quantity")
            if price <= 0:
                raise ValueError("price must be positive")
            if quantity < 0 or (snapshot and quantity == 0):
                raise ValueError("quantity must be positive in snapshots and non-negative in updates")
            if snapshot and price_text in book:
                self.duplicate_snapshot_levels += 1
            if quantity == 0:
                if price_text in book:
                    del book[price_text]
                self.deleted_levels += 1
                continue
            if price_text not in book:
                heapq.heappush(heap, (-price if is_bid else price, price_text))
            book[price_text] = (price, quantity)

    def apply(self, record):
        action = record.get("action")
        if action == "snapshot":
            self.bids = {}
            self.asks = {}
            self._bid_heap = []
            self._ask_heap = []
            self._apply_side(record.get("bids", []), self.bids, self._bid_heap, True, True)
            self._apply_side(record.get("asks", []), self.asks, self._ask_heap, False, True)
        elif action == "update":
            self._apply_side(record.get("bids", []), self.bids, self._bid_heap, True, False)
            self._apply_side(record.get("asks", []), self.asks, self._ask_heap, False, False)
        else:
            raise ValueError(f"unsupported action: {action!r}")

    def best_bid(self):
        while self._bid_heap:
            negative_price, price_text = self._bid_heap[0]
            current = self.bids.get(price_text)
            if current is not None and current[0] == -negative_price:
                return -negative_price
            heapq.heappop(self._bid_heap)
        return None

    def best_ask(self):
        while self._ask_heap:
            price, price_text = self._ask_heap[0]
            current = self.asks.get(price_text)
            if current is not None and current[0] == price:
                return price
            heapq.heappop(self._ask_heap)
        return None

    def status(self):
        bid = self.best_bid()
        ask = self.best_ask()
        if bid is None or ask is None:
            return "empty"
        if bid > ask:
            return "crossed"
        if bid == ask:
            return "locked"
        return "valid"


def audit_records(records):
    book = BookState()
    actions = collections.Counter()
    statuses = collections.Counter()
    deltas = collections.Counter()
    tuple_lengths = collections.Counter()
    third_values = collections.Counter()
    update_sizes = []
    snapshot_bid_depths = []
    snapshot_ask_depths = []
    records_count = 0
    first_ts = last_ts = previous_ts = None
    level_rows = 0
    negative_or_invalid = 0

    for record in records:
        records_count += 1
        action = record.get("action")
        actions[action] += 1
        ts = int(record["ts"])
        if first_ts is None:
            first_ts = ts
        if previous_ts is not None:
            deltas[str(ts - previous_ts)] += 1
        previous_ts = last_ts = ts

        level_count = 0
        for side in ("bids", "asks"):
            rows = record.get(side, [])
            level_count += len(rows)
            level_rows += len(rows)
            for row in rows:
                tuple_lengths[str(len(row))] += 1
                if len(row) > 2:
                    third_values[str(row[2])] += 1

        try:
            book.apply(record)
        except ValueError:
            negative_or_invalid += 1
            raise

        statuses[book.status()] += 1
        if action == "snapshot":
            snapshot_bid_depths.append(len(book.bids))
            snapshot_ask_depths.append(len(book.asks))
        elif action == "update":
            update_sizes.append(level_count)

    def minmax(values):
        return [min(values), max(values)] if values else [None, None]

    return {
        "records": records_count,
        "snapshots": actions["snapshot"],
        "updates": actions["update"],
        "first_timestamp_ms": first_ts,
        "last_timestamp_ms": last_ts,
        "timestamp_deltas_ms": dict(deltas),
        "snapshot_bid_depth_minmax": minmax(snapshot_bid_depths),
        "snapshot_ask_depth_minmax": minmax(snapshot_ask_depths),
        "update_levels_minmax": minmax(update_sizes),
        "update_levels_median": statistics.median(update_sizes) if update_sizes else None,
        "level_rows": level_rows,
        "level_tuple_lengths": dict(tuple_lengths),
        "third_field_values_top20": third_values.most_common(20),
        "book_status_counts": dict(statuses),
        "duplicate_snapshot_levels": book.duplicate_snapshot_levels,
        "deleted_levels": book.deleted_levels,
        "negative_or_invalid_records": negative_or_invalid,
    }


def audit_archive(path):
    path = Path(path)
    with tarfile.open(path, mode="r:gz") as archive:
        members = [member for member in archive.getmembers() if member.isfile()]
        data_members = [member for member in members if member.name.endswith((".data", ".jsonl", ".ndjson"))]
        if len(data_members) != 1:
            raise ValueError(f"expected exactly one NDJSON data member, found {len(data_members)}")
        stream = archive.extractfile(data_members[0])
        if stream is None:
            raise ValueError("unable to read archive data member")

        def records():
            for line_number, raw in enumerate(stream, start=1):
                try:
                    yield json.loads(raw)
                except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                    raise ValueError(f"invalid JSON at line {line_number}") from exc

        summary = audit_records(records())
        summary["archive"] = str(path)
        summary["archive_bytes"] = path.stat().st_size
        summary["member"] = data_members[0].name
        summary["member_uncompressed_bytes"] = data_members[0].size
        return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archives", nargs="+")
    args = parser.parse_args()
    for path in args.archives:
        print(json.dumps(audit_archive(path), sort_keys=True))


if __name__ == "__main__":
    main()
