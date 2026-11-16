#!/usr/bin/env python3
"""Streaming, no-lookahead alignment of OKX trades to preceding sampled L2 BBO."""
from __future__ import annotations

import argparse
import collections
import csv
import io
import math
import tarfile
import zipfile
from pathlib import Path

import orjson

from okx_archive_audit import BookState, records_from_stream


def _hist_quantile(histogram, count, quantile):
    if not count:
        return None
    target = max(1, math.ceil(count * quantile))
    cumulative = 0
    for value in sorted(histogram):
        cumulative += histogram[value]
        if cumulative >= target:
            return value
    return max(histogram)


def align_records(book_records, trade_records):
    """Align each trade only to a book state strictly preceding its timestamp.

    A trade whose timestamp equals the next book update is consumed before that
    update is applied. This conservative tie rule avoids introducing look-ahead
    where archive timestamps do not provide an event sequence.
    """
    book = BookState()
    trades = iter(trade_records)
    current_trade = next(trades, None)
    previous_book_ts = None
    previous_trade_ts = None
    first_book_ts = None
    first_trade_ts = None
    first_no_preceding_book_trade_ts = None

    book_records_count = 0
    trade_rows = 0
    aligned = 0
    no_preceding_book = 0
    invalid_book_trades = 0
    same_timestamp_trades = 0
    age_histogram = collections.Counter()
    categories = collections.Counter()
    side_consistency = collections.Counter()
    side_consistency_by_timestamp = {
        "same_timestamp": collections.Counter(),
        "strict_preceding": collections.Counter(),
    }
    side_consistency_by_age = {
        "<=10ms": collections.Counter(),
        "10-20ms": collections.Counter(),
        "20-50ms": collections.Counter(),
        ">50ms": collections.Counter(),
    }
    outside_distance_histogram = collections.Counter()
    outside_distance_max_bps = 0.0
    outside_count = 0

    def consume(trade, boundary_ts=None):
        nonlocal previous_trade_ts, trade_rows, aligned
        nonlocal first_trade_ts, first_no_preceding_book_trade_ts
        nonlocal no_preceding_book, invalid_book_trades, same_timestamp_trades
        nonlocal outside_count, outside_distance_max_bps

        ts, price, side = trade
        ts = int(ts)
        price = float(price)
        if previous_trade_ts is not None and ts < previous_trade_ts:
            raise ValueError("trade timestamps are not monotonic")
        previous_trade_ts = ts
        if first_trade_ts is None:
            first_trade_ts = ts
        trade_rows += 1

        if not math.isfinite(price) or price <= 0:
            raise ValueError("trade price must be finite and positive")
        if side not in ("buy", "sell"):
            raise ValueError(f"invalid trade side: {side!r}")

        if previous_book_ts is None:
            no_preceding_book += 1
            if first_no_preceding_book_trade_ts is None:
                first_no_preceding_book_trade_ts = ts
            return
        if ts < previous_book_ts:
            raise ValueError("trade precedes the currently applied book state")
        is_same_timestamp = boundary_ts is not None and ts == boundary_ts
        if is_same_timestamp:
            same_timestamp_trades += 1

        bid = book.best_bid()
        ask = book.best_ask()
        if bid is None or ask is None or bid >= ask:
            invalid_book_trades += 1
            return

        aligned += 1
        age_histogram[ts - previous_book_ts] += 1

        if price < bid:
            category = "below_bid"
            distance_bps = (bid - price) / bid * 10000.0
        elif price > ask:
            category = "above_ask"
            distance_bps = (price - ask) / ask * 10000.0
        elif price == bid:
            category = "at_bid"
            distance_bps = 0.0
        elif price == ask:
            category = "at_ask"
            distance_bps = 0.0
        else:
            category = "inside"
            distance_bps = 0.0
        categories[category] += 1

        if side == "buy":
            is_consistent = price >= ask
            side_consistency["buy_at_or_above_ask" if is_consistent else "buy_below_ask"] += 1
        else:
            is_consistent = price <= bid
            side_consistency["sell_at_or_below_bid" if is_consistent else "sell_above_bid"] += 1

        outcome = "consistent" if is_consistent else "mismatch"
        timestamp_group = "same_timestamp" if is_same_timestamp else "strict_preceding"
        side_consistency_by_timestamp[timestamp_group][outcome] += 1
        age = ts - previous_book_ts
        if age <= 10:
            age_group = "<=10ms"
        elif age <= 20:
            age_group = "10-20ms"
        elif age <= 50:
            age_group = "20-50ms"
        else:
            age_group = ">50ms"
        side_consistency_by_age[age_group][outcome] += 1

        if distance_bps > 0:
            outside_count += 1
            bucket = int(round(distance_bps * 100.0))
            outside_distance_histogram[bucket] += 1
            outside_distance_max_bps = max(outside_distance_max_bps, distance_bps)

    for record in book_records:
        ts = int(record["ts"])
        if first_book_ts is None:
            first_book_ts = ts
        if previous_book_ts is not None and ts < previous_book_ts:
            raise ValueError("book timestamps are not monotonic")

        while current_trade is not None and int(current_trade[0]) <= ts:
            consume(current_trade, boundary_ts=ts)
            current_trade = next(trades, None)

        book.apply(record)
        previous_book_ts = ts
        book_records_count += 1

    while current_trade is not None:
        consume(current_trade)
        current_trade = next(trades, None)

    side_consistent = (
        side_consistency["buy_at_or_above_ask"]
        + side_consistency["sell_at_or_below_bid"]
    )
    age_threshold_counts = {
        f">{threshold}": sum(count for age, count in age_histogram.items() if age > threshold)
        for threshold in (10, 20, 50, 100, 250)
    }

    def summarize_consistency(counter):
        total = counter["consistent"] + counter["mismatch"]
        return {
            "consistent": counter["consistent"],
            "mismatch": counter["mismatch"],
            "consistency_pct": (counter["consistent"] / total * 100.0) if total else None,
        }

    return {
        "book_records": book_records_count,
        "book_timestamp_ms": {"first": first_book_ts, "last": previous_book_ts},
        "trade_timestamp_ms": {"first": first_trade_ts, "last": previous_trade_ts},
        "first_no_preceding_book_trade_ms": first_no_preceding_book_trade_ts,
        "trade_rows": trade_rows,
        "aligned_trades": aligned,
        "no_preceding_book": no_preceding_book,
        "invalid_book_trades": invalid_book_trades,
        "same_timestamp_trades": same_timestamp_trades,
        "same_timestamp_pct": (same_timestamp_trades / trade_rows * 100.0) if trade_rows else None,
        "sample_age_ms": {
            "min": min(age_histogram) if age_histogram else None,
            "median": _hist_quantile(age_histogram, aligned, 0.50),
            "p95": _hist_quantile(age_histogram, aligned, 0.95),
            "max": max(age_histogram) if age_histogram else None,
        },
        "sample_age_threshold_counts": age_threshold_counts,
        "price_vs_preceding_bbo": dict(categories),
        "outside_spread_trades": outside_count,
        "outside_spread_pct": (outside_count / aligned * 100.0) if aligned else None,
        "outside_distance_bps": {
            "p50": (_hist_quantile(outside_distance_histogram, outside_count, 0.50) or 0) / 100.0,
            "p90": (_hist_quantile(outside_distance_histogram, outside_count, 0.90) or 0) / 100.0,
            "p95": (_hist_quantile(outside_distance_histogram, outside_count, 0.95) or 0) / 100.0,
            "p99": (_hist_quantile(outside_distance_histogram, outside_count, 0.99) or 0) / 100.0,
            "max": outside_distance_max_bps,
        },
        "side_consistency": dict(side_consistency),
        "side_consistency_by_timestamp": {
            key: summarize_consistency(value)
            for key, value in side_consistency_by_timestamp.items()
        },
        "side_consistency_by_age": {
            key: summarize_consistency(value)
            for key, value in side_consistency_by_age.items()
        },
        "side_consistency_pct": (side_consistent / aligned * 100.0) if aligned else None,
        "side_mismatch_pct": ((aligned - side_consistent) / aligned * 100.0) if aligned else None,
    }


def iter_l2_records(path):
    with tarfile.open(path, mode="r|gz") as archive:
        member = archive.next()
        while member is not None and not member.isfile():
            member = archive.next()
        if member is None or not member.name.endswith((".data", ".jsonl", ".ndjson")):
            raise ValueError("expected an NDJSON data member in the L2 archive")
        stream = archive.extractfile(member)
        if stream is None:
            raise ValueError("unable to read L2 data member")
        yield from records_from_stream(stream)


def iter_trade_records(paths, start_ms, end_ms):
    for path in paths:
        with zipfile.ZipFile(path) as archive:
            bad_member = archive.testzip()
            if bad_member is not None:
                raise ValueError(f"trade ZIP CRC failure: {bad_member}")
            names = [name for name in archive.namelist() if not name.endswith("/")]
            if len(names) != 1:
                raise ValueError(f"expected one CSV member in {path}, found {len(names)}")
            with archive.open(names[0]) as raw:
                reader = csv.reader(io.TextIOWrapper(raw, encoding="utf-8", newline=""))
                header = next(reader, None)
                if not header:
                    raise ValueError(f"empty trade CSV: {path}")
                required = ("side", "price", "created_time")
                indices = {}
                for field in required:
                    if field not in header:
                        raise ValueError(f"missing {field!r} column in {path}")
                    indices[field] = header.index(field)
                for row in reader:
                    ts = int(row[indices["created_time"]])
                    if start_ms <= ts < end_ms:
                        yield (ts, float(row[indices["price"]]), row[indices["side"]])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--l2", required=True)
    parser.add_argument("--trades", nargs="+", required=True)
    parser.add_argument("--start-ms", type=int, required=True)
    parser.add_argument("--end-ms", type=int, required=True)
    args = parser.parse_args()
    if args.end_ms <= args.start_ms:
        parser.error("--end-ms must be greater than --start-ms")
    summary = align_records(
        iter_l2_records(args.l2),
        iter_trade_records(args.trades, args.start_ms, args.end_ms),
    )
    print(orjson.dumps(summary, option=orjson.OPT_SORT_KEYS).decode())


if __name__ == "__main__":
    main()
