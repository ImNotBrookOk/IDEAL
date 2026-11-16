import unittest

from compare_bbo_series import compare_rows


class CompareBboTests(unittest.TestCase):
    def test_equal_timestamp_is_reported_as_ambiguous_and_not_used_for_strict_match(self):
        official = [
            (1_000_000, "100", "101"),
            (2_000_000, "101", "102"),
        ]
        tardis = [(2_000_000, "101", "102")]
        result = compare_rows(tardis, official)

        self.assertEqual(result["same_timestamp_samples"], 1)
        self.assertEqual(result["no_preceding_official"], 0)
        self.assertEqual(result["strict_preceding"]["exact_bbo_match_pct"], 0.0)
        self.assertEqual(result["inclusive_same_timestamp"]["exact_bbo_match_pct"], 100.0)

    def test_missing_preceding_official_state_is_not_fabricated(self):
        official = [(1_000_000, "100", "101")]
        tardis = [(500_000, "100", "101")]
        result = compare_rows(tardis, official)

        self.assertEqual(result["no_preceding_official"], 1)
        self.assertEqual(result["strict_preceding"]["compared"], 0)
        self.assertEqual(result["inclusive_same_timestamp"]["compared"], 0)

    def test_strict_preceding_exact_match_and_age(self):
        official = [(1_000_000, "100", "101")]
        tardis = [(1_500_000, "100", "101")]
        result = compare_rows(tardis, official)

        self.assertEqual(result["strict_preceding"]["exact_bbo_match_pct"], 100.0)
        self.assertEqual(result["strict_preceding"]["age_ms"]["median"], 500.0)

    def test_unsorted_input_is_rejected(self):
        official = [
            (2_000_000, "101", "102"),
            (1_000_000, "100", "101"),
        ]
        with self.assertRaises(ValueError):
            compare_rows([(3_000_000, "101", "102")], official)

    def test_invalid_or_crossed_bbo_is_rejected(self):
        with self.assertRaises(ValueError):
            compare_rows([(2_000_000, "102", "101")], [(1_000_000, "100", "101")])


if __name__ == "__main__":
    unittest.main()
