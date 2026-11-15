"""Offline, provenance-aware execution-impact calibration from parent-order fills.

Input is one row per parent order, with realized fill VWAP and a decision-time
midpoint. This module measures realized implementation shortfall; it does not
infer exchange queue priority or predict impact from synthetic data.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path


REQUIRED_COLUMNS = {
    "venue",
    "instrument",
    "data_source",
    "timestamp_ns",
    "order_id",
    "side",
    "order_qty",
    "fill_qty",
    "fill_vwap",
    "decision_mid",
    "spread_bps",
    "volatility_bps",
    "depth_10bps",
    "latency_ms",
}
MIN_DATASET_ORDERS_FOR_REVIEW = 200
MIN_BUCKET_ORDERS_FOR_REVIEW = 30


def _decimal(value: str, field: str, *, allow_empty: bool = False):
    if value is None or value.strip() == "":
        if allow_empty:
            return None
        raise ValueError(f"{field} is required")
    try:
        result = Decimal(value)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field} must be a decimal") from exc
    if not result.is_finite():
        raise ValueError(f"{field} must be finite")
    return result


def _quantile(values: list[Decimal], probability: Decimal):
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = probability * Decimal(len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - Decimal(lower)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction


def _bucket(value: Decimal | None, bounds: tuple[Decimal, ...], labels: tuple[str, ...]):
    if value is None:
        return "UNKNOWN"
    for bound, label in zip(bounds, labels):
        if value <= bound:
            return label
    return labels[-1]


def _summarize(rows: list[dict]):
    slippage = [row["slippage_bps"] for row in rows if row["slippage_bps"] is not None]
    impact = [row["impact_bps"] for row in rows if row["impact_bps"] is not None]
    fill_ratios = [row["fill_ratio"] for row in rows]
    filled = [row for row in rows if row["fill_qty"] > 0]
    return {
        "orders": len(rows),
        "filled_orders": len(filled),
        "partial_or_unfilled_orders": sum(row["fill_qty"] < row["order_qty"] for row in rows),
        "mean_fill_ratio": _format(sum(fill_ratios, Decimal("0")) / len(fill_ratios)) if fill_ratios else None,
        "slippage_bps": _distribution(slippage),
        "residual_impact_bps_after_half_spread": _distribution(impact),
        "volume_weighted_mean_slippage_bps": (
            _format(
                sum(row["slippage_bps"] * row["fill_qty"] for row in filled)
                / sum(row["fill_qty"] for row in filled)
            )
            if filled else None
        ),
    }


def _distribution(values: list[Decimal]):
    if not values:
        return {"count": 0, "p50": None, "p90": None, "p95": None, "mean": None}
    return {
        "count": len(values),
        "p50": _format(_quantile(values, Decimal("0.50"))),
        "p90": _format(_quantile(values, Decimal("0.90"))),
        "p95": _format(_quantile(values, Decimal("0.95"))),
        "mean": _format(sum(values, Decimal("0")) / len(values)),
    }


def _format(value: Decimal | None):
    return None if value is None else str(value.quantize(Decimal("0.0001")))


def load_csv(path: str | Path):
    path = Path(path)
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    rows = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing required columns: {', '.join(sorted(missing))}")
        seen_ids = set()
        for line_number, source in enumerate(reader, start=2):
            order_id = source["order_id"].strip()
            if not order_id or order_id in seen_ids:
                raise ValueError(f"line {line_number}: order_id must be non-empty and unique")
            seen_ids.add(order_id)
            side = source["side"].strip().upper()
            if side not in {"BUY", "SELL"}:
                raise ValueError(f"line {line_number}: side must be BUY or SELL")
            try:
                timestamp_ns = int(source["timestamp_ns"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"line {line_number}: timestamp_ns must be an integer") from exc
            order_qty = _decimal(source["order_qty"], "order_qty")
            fill_qty = _decimal(source["fill_qty"], "fill_qty")
            mid = _decimal(source["decision_mid"], "decision_mid")
            spread = _decimal(source["spread_bps"], "spread_bps")
            volatility = _decimal(source["volatility_bps"], "volatility_bps")
            depth = _decimal(source["depth_10bps"], "depth_10bps")
            latency = _decimal(source["latency_ms"], "latency_ms")
            fill_vwap = _decimal(source["fill_vwap"], "fill_vwap", allow_empty=True)
            if order_qty <= 0 or fill_qty < 0 or fill_qty > order_qty:
                raise ValueError(f"line {line_number}: require 0 <= fill_qty <= order_qty and order_qty > 0")
            if mid <= 0 or spread < 0 or volatility < 0 or depth < 0 or latency < 0:
                raise ValueError(f"line {line_number}: midpoint must be positive; other metrics non-negative")
            if fill_qty == 0 and fill_vwap is not None:
                raise ValueError(f"line {line_number}: unfilled order must have empty fill_vwap")
            if fill_qty > 0 and (fill_vwap is None or fill_vwap <= 0):
                raise ValueError(f"line {line_number}: filled order requires positive fill_vwap")
            sign = Decimal("1") if side == "BUY" else Decimal("-1")
            slippage = (
                (fill_vwap / mid - Decimal("1")) * Decimal("10000") * sign
                if fill_qty > 0 else None
            )
            rows.append({
                "venue": source["venue"].strip(),
                "instrument": source["instrument"].strip(),
                "data_source": source["data_source"].strip(),
                "timestamp_ns": timestamp_ns,
                "order_id": order_id,
                "side": side,
                "order_qty": order_qty,
                "fill_qty": fill_qty,
                "fill_vwap": fill_vwap,
                "decision_mid": mid,
                "spread_bps": spread,
                "volatility_bps": volatility,
                "depth_10bps": depth,
                "latency_ms": latency,
                "fill_ratio": fill_qty / order_qty,
                "slippage_bps": slippage,
                "impact_bps": slippage - spread / Decimal("2") if slippage is not None else None,
                "participation": order_qty / depth if depth > 0 else None,
            })
    if not rows:
        raise ValueError("dataset contains no parent-order observations")
    metadata_fields = ("venue", "instrument", "data_source")
    for field in metadata_fields:
        values = {row[field] for row in rows}
        if len(values) != 1 or not next(iter(values)):
            raise ValueError(f"dataset must contain exactly one non-empty {field}")
    rows.sort(key=lambda row: (row["timestamp_ns"], row["order_id"]))
    return rows, {
        "sha256": digest,
        "source_file": path.name,
        "venue": rows[0]["venue"],
        "instrument": rows[0]["instrument"],
        "data_source": rows[0]["data_source"],
        "rows": len(rows),
        "unique_utc_days": len({
            datetime.fromtimestamp(row["timestamp_ns"] / 1_000_000_000, timezone.utc).date()
            for row in rows
        }),
        "first_timestamp_ns": rows[0]["timestamp_ns"],
        "last_timestamp_ns": rows[-1]["timestamp_ns"],
    }


def analyze(rows: list[dict], metadata: dict):
    if len(rows) < 2:
        raise ValueError("at least two parent-order observations are required for a chronological split")
    split = max(1, int(len(rows) * 0.70))
    if split == len(rows):
        split = len(rows) - 1
    train, test = rows[:split], rows[split:]
    train_filled = [row for row in train if row["slippage_bps"] is not None]
    test_filled = [row for row in test if row["slippage_bps"] is not None]
    train_p90 = _quantile([row["slippage_bps"] for row in train_filled], Decimal("0.90"))
    coverage = (
        sum(row["slippage_bps"] <= train_p90 for row in test_filled) / len(test_filled)
        if train_p90 is not None and test_filled else None
    )

    dimensions = {
        "participation": (
            lambda row: row["participation"],
            (Decimal("0.10"), Decimal("0.25"), Decimal("0.50"), Decimal("1.00")),
            ("<=0.10", "0.10-0.25", "0.25-0.50", "0.50-1.00", ">1.00"),
        ),
        "spread_bps": (
            lambda row: row["spread_bps"],
            (Decimal("1"), Decimal("2"), Decimal("5")),
            ("<=1", "1-2", "2-5", ">5"),
        ),
        "volatility_bps": (
            lambda row: row["volatility_bps"],
            (Decimal("5"), Decimal("10"), Decimal("25")),
            ("<=5", "5-10", "10-25", ">25"),
        ),
        "latency_ms": (
            lambda row: row["latency_ms"],
            (Decimal("10"), Decimal("50"), Decimal("100")),
            ("<=10", "10-50", "50-100", ">100"),
        ),
    }
    buckets = {}
    for dimension, (getter, bounds, labels) in dimensions.items():
        grouped = defaultdict(list)
        for row in train_filled:
            grouped[_bucket(getter(row), bounds, labels)].append(row)
        buckets[dimension] = {
            label: {
                **_summarize(grouped[label]),
                "minimum_bucket_sample_met": len(grouped[label]) >= MIN_BUCKET_ORDERS_FOR_REVIEW,
            }
            for label in (*labels, "UNKNOWN")
            if grouped[label]
        }

    enough_rows = len(rows) >= MIN_DATASET_ORDERS_FOR_REVIEW
    enough_oos = len(test_filled) >= 30
    status = "ELIGIBLE_FOR_REVIEW" if enough_rows and enough_oos else "INSUFFICIENT_SAMPLE"
    return {
        "status": status,
        "notice": (
            "This is a diagnostic calibration report, not proof of predictive validity or venue parity. "
            "Review requires provenance, representative regimes, bucket sample sizes and independent OOS analysis."
        ),
        "dataset": metadata,
        "chronological_split": {
            "training_orders": len(train),
            "out_of_sample_orders": len(test),
            "training_filled_orders": len(train_filled),
            "out_of_sample_filled_orders": len(test_filled),
            "training_slippage_p90_bps": _format(train_p90),
            "oos_fraction_at_or_below_training_p90": (
                _format(Decimal(str(coverage))) if coverage is not None else None
            ),
            "p90_nominal_coverage": "0.9000",
        },
        "all_orders": _summarize(rows),
        "training_buckets": buckets,
        "minimums": {
            "total_orders_for_review": MIN_DATASET_ORDERS_FOR_REVIEW,
            "out_of_sample_filled_orders": 30,
            "per_bucket_orders": MIN_BUCKET_ORDERS_FOR_REVIEW,
            "note": "Provisional research screening minimums, not owner-approved trading gates.",
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv")
    parser.add_argument("--output", default="impact_calibration_report.json")
    args = parser.parse_args()
    rows, metadata = load_csv(args.input_csv)
    report = analyze(rows, metadata)
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{report['status']}: {len(rows)} parent orders; report={args.output}")


if __name__ == "__main__":
    main()
