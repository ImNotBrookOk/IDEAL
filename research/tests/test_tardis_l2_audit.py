import unittest
import csv
import io

from tardis_l2_audit import audit_rows


def row(local_ts, snapshot, side, price, amount, ts=None):
    return {
        "exchange": "binance-futures",
        "symbol": "BTCUSDT",
        "timestamp": str(ts if ts is not None else local_ts),
        "local_timestamp": str(local_ts),
        "is_snapshot": "true" if snapshot else "false",
        "side": side,
        "price": str(price),
        "amount": str(amount),
    }


class TardisAuditTests(unittest.TestCase):
    def test_skips_buffered_updates_before_first_snapshot(self):
        rows = [
            row(900, False, "bid", 99, 1),
            row(1000, True, "bid", 100, 2),
            row(1000, True, "ask", 101, 3),
        ]
        result = audit_rows(rows)
        self.assertEqual(result["rows_skipped_before_first_snapshot"], 1)
        self.assertEqual(result["book_status_counts"], {"valid": 1})
        self.assertEqual(result["final_best_bid"], 100.0)
        self.assertEqual(result["final_best_ask"], 101.0)

    def test_snapshot_transition_replaces_prior_book_state(self):
        rows = [
            row(1000, True, "bid", 100, 2),
            row(1000, True, "ask", 101, 2),
            row(2000, False, "bid", 99, 4),
            row(3000, True, "bid", 90, 1),
            row(3000, True, "ask", 110, 1),
        ]
        result = audit_rows(rows)
        self.assertEqual(result["snapshots"], 2)
        self.assertEqual(result["final_best_bid"], 90.0)
        self.assertEqual(result["final_best_ask"], 110.0)
        self.assertEqual(result["final_bid_levels"], 1)
        self.assertEqual(result["final_ask_levels"], 1)

    def test_updates_replace_absolute_amount_and_zero_deletes(self):
        rows = [
            row(1000, True, "bid", 100, 2),
            row(1000, True, "ask", 101, 2),
            row(2000, False, "bid", 100, 5),
            row(2000, False, "ask", 101, 0),
            row(2000, False, "ask", 102, 3),
        ]
        result = audit_rows(rows)
        self.assertEqual(result["final_bid_amount_at_best"], 5.0)
        self.assertEqual(result["final_best_ask"], 102.0)
        self.assertEqual(result["deleted_levels"], 1)

    def test_rows_with_same_local_timestamp_are_one_message(self):
        rows = [
            row(1000, True, "bid", 100, 2),
            row(1000, True, "ask", 101, 2),
            row(2000, False, "bid", 100, 3),
            row(2000, False, "ask", 101, 4),
        ]
        result = audit_rows(rows)
        self.assertEqual(result["messages"], 2)
        self.assertEqual(result["rows"], 4)
        self.assertEqual(result["book_status_counts"], {"valid": 2})

    def test_out_of_order_local_timestamp_is_rejected(self):
        rows = [
            row(1000, True, "bid", 100, 2),
            row(1000, True, "ask", 101, 2),
            row(2000, False, "bid", 100, 3),
            row(1500, False, "ask", 102, 4),
        ]
        with self.assertRaises(ValueError):
            audit_rows(rows)

    def test_local_and_exchange_timestamp_gaps_are_reported_separately(self):
        rows = [
            row(1000, True, "bid", 100, 2, ts=10000),
            row(1000, True, "ask", 101, 2, ts=10000),
            row(2000, False, "bid", 100, 3, ts=10150),
            row(3000, False, "ask", 101, 3, ts=10050),
        ]
        result = audit_rows(rows)
        self.assertEqual(result["max_local_message_gap_ms"], 1.0)
        self.assertEqual(result["max_exchange_message_gap_ms"], 0.15)
        self.assertEqual(result["exchange_timestamp_backwards_messages"], 1)

    def test_bbo_writer_emits_one_state_per_processed_message(self):
        rows = [
            row(1000, True, "bid", 100, 2),
            row(1000, True, "ask", 101, 2),
            row(2000, False, "bid", 100, 3),
        ]
        output = io.StringIO()
        writer = csv.writer(output)
        audit_rows(rows, bbo_writer=writer)
        parsed = list(csv.reader(io.StringIO(output.getvalue())))
        self.assertEqual(parsed, [
            ["1000", "100", "101"],
            ["2000", "100", "101"],
        ])

    def test_invalid_side_and_negative_amount_are_rejected(self):
        with self.assertRaises(ValueError):
            audit_rows([
                row(1000, True, "bid", 100, 2),
                row(1000, True, "ask", 101, 2),
                row(2000, False, "middle", 100, 1),
            ])
        with self.assertRaises(ValueError):
            audit_rows([
                row(1000, True, "bid", 100, 2),
                row(1000, True, "ask", 101, 2),
                row(2000, False, "bid", 100, -1),
            ])


if __name__ == "__main__":
    unittest.main()
