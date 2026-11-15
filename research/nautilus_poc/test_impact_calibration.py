"""Unit tests for the offline execution-impact calibration utility."""
import csv

import pytest

from impact_calibration import analyze, load_csv


FIELDS = [
    "venue", "instrument", "data_source", "timestamp_ns", "order_id", "side",
    "order_qty", "fill_qty", "fill_vwap", "decision_mid", "spread_bps",
    "volatility_bps", "depth_10bps", "latency_ms",
]


def write_dataset(path, count=10):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for i in range(count):
            side = "BUY" if i % 2 == 0 else "SELL"
            # Both directions incur 10 bps adverse implementation shortfall.
            fill_vwap = "100.100" if side == "BUY" else "99.900"
            fill_qty = "0.000" if i == 0 else "1.000"
            writer.writerow({
                "venue": "TEST",
                "instrument": "BTCUSDT-PERP",
                "data_source": "synthetic-test-fixture",
                "timestamp_ns": str(1_000_000_000 + i * 86_400_000_000_000),
                "order_id": f"order-{i}",
                "side": side,
                "order_qty": "1.000",
                "fill_qty": fill_qty,
                "fill_vwap": "" if i == 0 else fill_vwap,
                "decision_mid": "100.000",
                "spread_bps": "2.000",
                "volatility_bps": "8.000",
                "depth_10bps": "10.000",
                "latency_ms": "20.000",
            })


def test_calibration_uses_signed_side_aware_slippage_and_removes_half_spread(tmp_path):
    path = tmp_path / "fills.csv"
    write_dataset(path)
    rows, metadata = load_csv(path)
    report = analyze(rows, metadata)

    assert report["all_orders"]["filled_orders"] == 9
    assert report["all_orders"]["partial_or_unfilled_orders"] == 1
    assert report["all_orders"]["slippage_bps"]["p50"] == "10.0000"
    assert report["all_orders"]["residual_impact_bps_after_half_spread"]["p50"] == "9.0000"
    assert report["chronological_split"]["training_orders"] == 7
    assert report["chronological_split"]["out_of_sample_orders"] == 3
    assert report["dataset"]["sha256"] == metadata["sha256"]
    assert report["status"] == "INSUFFICIENT_SAMPLE"


def test_calibration_rejects_duplicate_order_ids(tmp_path):
    path = tmp_path / "duplicate.csv"
    write_dataset(path, count=2)
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    duplicate = lines[2].replace("order-1", "order-0")
    path.write_text("\n".join([*lines[:3], duplicate]) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="unique"):
        load_csv(path)


def test_calibration_rejects_partial_fill_without_vwap(tmp_path):
    path = tmp_path / "missing-vwap.csv"
    write_dataset(path, count=2)
    content = path.read_text(encoding="utf-8").replace("order-1,SELL,1.000,1.000,99.900", "order-1,SELL,1.000,1.000,")
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError, match="requires positive fill_vwap"):
        load_csv(path)


def test_calibration_requires_single_provenance_universe(tmp_path):
    path = tmp_path / "mixed-venue.csv"
    write_dataset(path, count=2)
    content = path.read_text(encoding="utf-8").replace("TEST,BTCUSDT-PERP,synthetic-test-fixture,86401000000000,order-1", "OTHER,BTCUSDT-PERP,synthetic-test-fixture,86401000000000,order-1")
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError, match="exactly one non-empty venue"):
        load_csv(path)
