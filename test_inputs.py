import datetime
import unittest
from validators import (
    parse_date,
    validate_chart_type,
    validate_date_range,
    validate_symbol,
    validate_time_series,
)


class TestStockVisualizerInputs(unittest.TestCase):
    # --- 1. Symbol: capitalized, 1-7 alpha characters ---
    def test_valid_symbols(self):
        self.assertTrue(validate_symbol("A"))
        self.assertTrue(validate_symbol("AAPL"))
        self.assertTrue(validate_symbol("GOOGL"))
        self.assertTrue(validate_symbol("ABCDEFG"))  # 7 chars boundary

    def test_invalid_symbols(self):
        self.assertFalse(validate_symbol(""))            # empty
        self.assertFalse(validate_symbol("ABCDEFGH"))    # 8 chars (too long)
        self.assertFalse(validate_symbol("aapl"))        # lowercase
        self.assertFalse(validate_symbol("Aapl"))        # mixed case
        self.assertFalse(validate_symbol("APPL1"))       # contains digit
        self.assertFalse(validate_symbol("BRK.B"))       # contains punctuation
        self.assertFalse(validate_symbol("AAPL "))       # trailing space

    # --- 2. Chart Type: 1 numeric character, 1 or 2 ---
    def test_valid_chart_types(self):
        self.assertTrue(validate_chart_type("1"))
        self.assertTrue(validate_chart_type("2"))

    def test_invalid_chart_types(self):
        self.assertFalse(validate_chart_type("0"))
        self.assertFalse(validate_chart_type("3"))
        self.assertFalse(validate_chart_type("12"))
        self.assertFalse(validate_chart_type("a"))
        self.assertFalse(validate_chart_type(""))
        self.assertFalse(validate_chart_type(" 1"))

    # --- 3. Time Series: 1 numeric character, 1 - 4 ---
    def test_valid_time_series(self):
        for ts in ["1", "2", "3", "4"]:
            with self.subTest(time_series=ts):
                self.assertTrue(validate_time_series(ts))

    def test_invalid_time_series(self):
        for ts in ["0", "5", "12", "x", "", "2 "]:
            with self.subTest(time_series=ts):
                self.assertFalse(validate_time_series(ts))

    # --- 4 & 5. Start Date & End Date: YYYY-MM-DD ---
    def test_valid_dates(self):
        self.assertEqual(parse_date("2025-01-15"), datetime.date(2025, 1, 15))
        self.assertEqual(parse_date("2024-02-29"), datetime.date(2024, 2, 29))  # leap year

    def test_invalid_dates(self):
        self.assertIsNone(parse_date("2025-02-29"))    # non-leap year Feb 29
        self.assertIsNone(parse_date("2025-13-01"))    # invalid month
        self.assertIsNone(parse_date("2025-01-32"))    # invalid day
        self.assertIsNone(parse_date("01-15-2025"))    # wrong format (MM-DD-YYYY)
        self.assertIsNone(parse_date("2025/01/15"))    # wrong separator
        self.assertIsNone(parse_date("25-01-15"))      # 2-digit year
        self.assertIsNone(parse_date("not-a-date"))
        self.assertIsNone(parse_date(""))

    def test_date_range_validation(self):
        self.assertTrue(validate_date_range("2025-01-01", "2025-01-31"))
        self.assertTrue(validate_date_range("2025-05-10", "2025-05-10"))  # same day allowed
        self.assertFalse(validate_date_range("2025-02-01", "2025-01-01")) # start after end
        self.assertFalse(validate_date_range("invalid", "2025-01-31"))
        self.assertFalse(validate_date_range("2025-01-01", "2025-99-99"))


if __name__ == "__main__":
    unittest.main()