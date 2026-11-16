#!/usr/bin/env python3
"""Compare Tardis and official OKX BBO series without look-ahead."""

from __future__ import annotations

import argparse
import collections
import csv
import json
from decimal import Decimal, InvalidOperation
from itertools import groupby
from pathlib import Path


def _validated_rows(rows, label):
    previous_ts = None
    for row in rows:
        try:
            ts = int(row[0])
            bid = Decimal(str(row[1]))
            ask = Decimal(str(row[2]))
        except (ValueError, TypeError, InvalidOperation, IndexError) as exc:
            raise ValueError(f"invalid {label} BBO row: {row!r}") from exc
        if previous_ts is not None and ts < previous_ts:
            raise ValueError(f"{label} timestamps moved backwards: {ts} < {previous_ts}")
        if not bid.is_finite() or not ask.is_finite() or bid <= 0 or ask <= bid:
            raise ValueError(f"invalid {label} BBO prices: bid={bid}, ask={ask}")
        previous_ts = ts
        yield ts, bid, ask


def _quantile(histogram, total, q):
    if not total:
        return None
    target = max(1, int(total * q + 0.999999999))
    cumulative = 0
    for age_us in sorted(histogram):
        cumulative += histogram[age_us]
        if cumulative >= target:
            return age_us / 1000.0
    return max(histogram) / 1000.0


def _metrics(counter, age_histogram):
    compared = counter["compared"]
    return {
        "compared": compared,
        "bid_matches": counter["bid_matches"],
        "ask_matches": counter["ask_matches"],
        "exact_bbo_matches": counter["exact_bbo_matches"],
        "bid_match_pct": counter["bid_matches"] / compared * 100.0 if compared else None,
        "ask_match_pct": counter["ask_matches"] / compared * 100.0 if compared else None,
        "exact_bbo_match_pct": counter["exact_bbo_matches"] / compared * 100.0 if compared else None,
        "age_ms": {
            "median": _quantile(age_histogram, compared, 0.50),
            "p95": _quantile(age_histogram, compared, 0.95),
            "max": max(age_histogram) / 1000.0 if age_histogram else None,
        },
    }


def compare_rows(tardis_rows, official_rows) -> dict:
    official = iter(_validated_rows(official_rows, "official"))
    next_official = next(official, None)
    previous_official = None
    last_tardis_ts = None
    samples = no_preceding = same_timestamp = inclusive_missing = 0
    strict_counts = collections.Counter()
    inclusive_counts = collections.Counter()
    strict_age_histogram = collections.Counter()
    inclusive_age_histogram = collections.Counter()

    for ts, group in groupby(_validated_rows(tardis_rows, "Tardis"), key=lambda row: row[0]):
        if last_tardis_ts is not None and ts < last_tardis_ts:
            raise ValueError("Tardis timestamps moved backwards")
        last_tardis_ts = ts

        while next_official is not None and next_official[0] < ts:
            previous_official = next_official
            next_official = next(official, None)

        same_timestamp_official = None
        while next_official is not None and next_official[0] == ts:
            same_timestamp_official = next_official
            next_official = next(official, None)

        for tardis_row in group:
            samples += 1
            _, tardis_bid, tardis_ask = tardis_row

            if same_timestamp_official is not None:
                same_timestamp += 1

            if previous_official is None:
                no_preceding += 1
            else:
                official_ts, official_bid, official_ask = previous_official
                strict_counts["compared"] += 1
                strict_counts["bid_matches"] += tardis_bid == official_bid
                strict_counts["ask_matches"] += tardis_ask == official_ask
                strict_counts["exact_bbo_matches"] += (
                    tardis_bid == official_bid and tardis_ask == official_ask
                )
                strict_age_histogram[ts - official_ts] += 1

            inclusive_official = same_timestamp_official or previous_official
            if inclusive_official is None:
                inclusive_missing += 1
            else:
                official_ts, official_bid, official_ask = inclusive_official
                inclusive_counts["compared"] += 1
                inclusive_counts["bid_matches"] += tardis_bid == official_bid
                inclusive_counts["ask_matches"] += tardis_ask == official_ask
                inclusive_counts["exact_bbo_matches"] += (
                    tardis_bid == official_bid and tardis_ask == official_ask
                )
                inclusive_age_histogram[ts - official_ts] += 1

        if same_timestamp_official is not None:
            previous_official = same_timestamp_official

    return {
        "tardis_samples": samples,
        "no_preceding_official": no_preceding,
        "same_timestamp_samples": same_timestamp,
        "inclusive_missing_official": inclusive_missing,
        "strict_preceding": _metrics(strict_counts, strict_age_histogram),
        "inclusive_same_timestamp": _metrics(inclusive_counts, inclusive_age_histogram),
    }


def read_bbo_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"timestamp_us", "bid", "ask"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing BBO columns: {sorted(missing)}")
        for row in reader:
            yield row["timestamp_us"], row["bid"], row["ask"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tardis-bbo", required=True)
    parser.add_argument("--official-bbo", required=True)
    args = parser.parse_args()
    result = compare_rows(
        read_bbo_csv(args.tardis_bbo),
        read_bbo_csv(args.official_bbo),
    )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
