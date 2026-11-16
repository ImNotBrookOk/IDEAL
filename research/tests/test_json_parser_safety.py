import unittest

import orjson


class JsonParserSafetyTests(unittest.TestCase):
    def test_deeply_nested_serialization_fails_with_bounded_error(self):
        value = []
        for _ in range(10_000):
            value = [value]

        with self.assertRaises(orjson.JSONEncodeError):
            orjson.dumps(value)

    def test_deeply_nested_input_is_rejected_with_decode_error(self):
        payload = b"[" * 2_000 + b"0" + b"]" * 2_000

        with self.assertRaises(orjson.JSONDecodeError):
            orjson.loads(payload)


if __name__ == "__main__":
    unittest.main()
