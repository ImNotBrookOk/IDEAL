#!/usr/bin/env python3
"""Independent, streaming audit of OKX historical L2 NDJSON archives.

The historical third level-tuple field is counted but deliberately not assigned
semantics. This tool is a research validator, not a production market-data adapter.
"""
from __future__ import annotations

import argparse
import collections
import csv
import heapq
import orjson
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


def audit_records(records, bbo_writer=None):
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

        book_status = book.status()
        statuses[book_status] += 1
        if bbo_writer is not None and book_status == "valid":
            bbo_writer.writerow([ts * 1000, str(book.best_bid()), str(book.best_ask())])
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


def audit_archive(path, bbo_output=None):
    path = Path(path)
    bbo_stream = None
    try:
        if bbo_output is not None:
            bbo_stream = Path(bbo_output).open("w", encoding="utf-8", newline="")
            bbo_writer = csv.writer(bbo_stream)
            bbo_writer.writerow(["timestamp_us", "bid", "ask"])
        else:
            bbo_writer = None
        with tarfile.open(path, mode="r|gz") as archive:
            member = archive.next()
            while member is not None and not member.isfile():
                member = archive.next()
            if member is None or not member.name.endswith((".data", ".jsonl", ".ndjson")):
                raise ValueError("expected one NDJSON data member in the tar archive")
            stream = archive.extractfile(member)
            if stream is None:
                raise ValueError("unable to read archive data member")

            summary = audit_records(records_from_stream(stream), bbo_writer=bbo_writer)
            extra = archive.next()
            while extra is not None:
                if extra.isfile() and extra.name.endswith((".data", ".jsonl", ".ndjson")):
                    raise ValueError("expected exactly one NDJSON data member")
                extra = archive.next()

            summary["archive"] = str(path)
            summary["archive_bytes"] = path.stat().st_size
            summary["member"] = member.name
            summary["member_uncompressed_bytes"] = member.size
            return summary
    finally:
        if bbo_stream is not None:
            bbo_stream.close()


def records_from_stream(stream):
    for line_number, raw in enumerate(stream, start=1):
        try:
            yield orjson.loads(raw)
        except (orjson.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError(f"invalid JSON at line {line_number}") from exc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archives", nargs="+")
    parser.add_argument("--bbo-output")
    args = parser.parse_args()
    if args.bbo_output and len(args.archives) != 1:
        parser.error("--bbo-output requires exactly one archive")
    for path in args.archives:
        print(orjson.dumps(audit_archive(path, args.bbo_output), option=orjson.OPT_SORT_KEYS).decode())


if __name__ == "__main__":
    main()
