import unittest

from okx_trade_book_alignment import align_records


def snapshot(ts, bid="99", ask="101"):
    return {
        "ts": str(ts),
        "action": "snapshot",
        "bids": [[bid, "2", "1"]],
        "asks": [[ask, "3", "1"]],
    }


def update(ts, bid=None, ask=None):
    return {
        "ts": str(ts),
        "action": "update",
        "bids": [] if bid is None else [[bid, "2", "1"]],
        "asks": [] if ask is None else [[ask, "3", "1"]],
    }


class AlignmentTests(unittest.TestCase):
    def test_trade_uses_preceding_book_not_same_timestamp_update(self):
        books = [snapshot(100), update(200, ask="100")]
        trades = [(200, 100.5, "buy")]
        result = align_records(books, trades)
        self.assertEqual(result["aligned_trades"], 1)
        self.assertEqual(result["same_timestamp_trades"], 1)
        self.assertEqual(result["price_vs_preceding_bbo"]["inside"], 1)

    def test_trade_between_book_updates_uses_last_preceding_state(self):
        books = [snapshot(100), update(200, ask="100")]
        trades = [(150, 101.0, "buy")]
        result = align_records(books, trades)
        self.assertEqual(result["aligned_trades"], 1)
        self.assertEqual(result["price_vs_preceding_bbo"]["at_ask"], 1)

    def test_trade_before_first_snapshot_is_not_aligned(self):
        books = [snapshot(100)]
        trades = [(99, 101.0, "buy")]
        result = align_records(books, trades)
        self.assertEqual(result["aligned_trades"], 0)
        self.assertEqual(result["no_preceding_book"], 1)

    def test_trade_after_last_book_uses_last_available_state(self):
        books = [snapshot(100)]
        trades = [(125, 101.0, "buy")]
        result = align_records(books, trades)
        self.assertEqual(result["aligned_trades"], 1)
        self.assertEqual(result["sample_age_ms"]["max"], 25)
        self.assertEqual(result["sample_age_threshold_counts"][">20"], 1)
        self.assertEqual(result["sample_age_threshold_counts"][">50"], 0)
        self.assertEqual(result["side_consistency_pct"], 100.0)


    def test_side_consistency_is_split_by_timestamp_ties_and_book_age(self):
        books = [snapshot(100), update(200, ask="100")]
        trades = [(150, 101.0, "buy"), (200, 100.5, "buy")]
        result = align_records(books, trades)

        by_timestamp = result["side_consistency_by_timestamp"]
        self.assertEqual(by_timestamp["strict_preceding"]["consistent"], 1)
        self.assertEqual(by_timestamp["strict_preceding"]["mismatch"], 0)
        self.assertEqual(by_timestamp["same_timestamp"]["consistent"], 0)
        self.assertEqual(by_timestamp["same_timestamp"]["mismatch"], 1)

        by_age = result["side_consistency_by_age"]
        self.assertEqual(by_age["20-50ms"]["consistent"], 1)
        self.assertEqual(by_age[">50ms"]["mismatch"], 1)

    def test_non_monotonic_book_timestamps_fail_closed(self):
        books = [snapshot(100), update(90, ask="100")]
        with self.assertRaises(ValueError):
            align_records(books, [])

    def test_non_monotonic_trade_timestamps_fail_closed(self):
        books = [snapshot(100)]
        trades = [(120, 101.0, "buy"), (110, 101.0, "buy")]
        with self.assertRaises(ValueError):
            align_records(books, trades)


    def test_alignment_reports_book_and_trade_timestamp_coverage(self):
        books = [snapshot(100), update(200, ask="100")]
        trades = [(150, 101.0, "buy"), (200, 100.5, "buy")]
        result = align_records(books, trades)
        self.assertEqual(result["book_timestamp_ms"], {"first": 100, "last": 200})
        self.assertEqual(result["trade_timestamp_ms"], {"first": 150, "last": 200})
        self.assertIsNone(result["first_no_preceding_book_trade_ms"])

    def test_alignment_identifies_first_trade_before_initial_snapshot(self):
        books = [snapshot(100), update(200)]
        trades = [(99, 101.0, "buy"), (150, 101.0, "buy")]
        result = align_records(books, trades)
        self.assertEqual(result["no_preceding_book"], 1)
        self.assertEqual(result["first_no_preceding_book_trade_ms"], 99)
        self.assertEqual(result["book_timestamp_ms"], {"first": 100, "last": 200})
        self.assertEqual(result["trade_timestamp_ms"], {"first": 99, "last": 150})


if __name__ == "__main__":
    unittest.main()
