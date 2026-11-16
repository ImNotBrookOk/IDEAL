import unittest
import csv
import io

from okx_archive_audit import BookState, audit_records


class BookStateTests(unittest.TestCase):
    def setUp(self):
        self.book = BookState()

    def test_snapshot_initializes_bid_ask_and_best_prices(self):
        self.book.apply({
            "action": "snapshot",
            "bids": [["100.0", "2", "7"], ["99.0", "3", "5"]],
            "asks": [["101.0", "4", "8"], ["102.0", "1", "2"]],
        })
        self.assertEqual(self.book.best_bid(), 100.0)
        self.assertEqual(self.book.best_ask(), 101.0)

    def test_update_replaces_quantity_and_zero_quantity_deletes_level(self):
        self.book.apply({
            "action": "snapshot",
            "bids": [["100.0", "2", "7"]],
            "asks": [["101.0", "4", "8"]],
        })
        self.book.apply({
            "action": "update",
            "bids": [["100.0", "5", "9"]],
            "asks": [["101.0", "0", "0"], ["102.0", "1", "2"]],
        })
        self.assertEqual(self.book.bids["100.0"][1], 5.0)
        self.assertNotIn("101.0", self.book.asks)
        self.assertEqual(self.book.best_ask(), 102.0)

    def test_new_snapshot_replaces_prior_state(self):
        self.book.apply({
            "action": "snapshot",
            "bids": [["100.0", "2", "7"]],
            "asks": [["101.0", "4", "8"]],
        })
        self.book.apply({
            "action": "snapshot",
            "bids": [["90.0", "1", "1"]],
            "asks": [["110.0", "1", "1"]],
        })
        self.assertEqual(set(self.book.bids), {"90.0"})
        self.assertEqual(set(self.book.asks), {"110.0"})

    def test_negative_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            self.book.apply({
                "action": "snapshot",
                "bids": [["100.0", "-1", "1"]],
                "asks": [["101.0", "1", "1"]],
            })

    def test_crossed_book_is_detected(self):
        self.book.apply({
            "action": "snapshot",
            "bids": [["102.0", "1", "1"]],
            "asks": [["101.0", "1", "1"]],
        })
        self.assertEqual(self.book.status(), "crossed")


class AuditTests(unittest.TestCase):
    def test_bbo_writer_emits_one_row_per_valid_record(self):
        records = [
            {"ts": "1000", "action": "snapshot", "bids": [["100", "1", "1"]], "asks": [["101", "1", "1"]]},
            {"ts": "2000", "action": "update", "bids": [["100", "2", "1"]], "asks": []},
        ]
        output = io.StringIO()
        writer = csv.writer(output)
        audit_records(records, bbo_writer=writer)
        parsed = list(csv.reader(io.StringIO(output.getvalue())))
        self.assertEqual(parsed, [
            ["1000000", "100.0", "101.0"],
            ["2000000", "100.0", "101.0"],
        ])

    def test_audit_counts_snapshots_updates_and_timestamp_gaps(self):
        records = [
            {"ts": "1000", "action": "snapshot", "bids": [["100", "1", "1"]], "asks": [["101", "1", "1"]]},
            {"ts": "2000", "action": "update", "bids": [["100", "2", "1"]], "asks": []},
            {"ts": "4000", "action": "update", "bids": [], "asks": [["101", "0", "0"], ["102", "1", "1"]]},
        ]
        result = audit_records(records)
        self.assertEqual(result["records"], 3)
        self.assertEqual(result["snapshots"], 1)
        self.assertEqual(result["updates"], 2)
        self.assertEqual(result["timestamp_deltas_ms"]["2000"], 1)
        self.assertEqual(result["book_status_counts"]["valid"], 3)


if __name__ == "__main__":
    unittest.main()
