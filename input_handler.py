"""Collects and validates user input."""
from datetime import datetime

CHART_TYPES = {"1": "Bar", "2": "Line"}

TIME_SERIES = {
    "1": "TIME_SERIES_INTRADAY",
    "2": "TIME_SERIES_DAILY",
    "3": "TIME_SERIES_WEEKLY",
    "4": "TIME_SERIES_MONTHLY",
}


def get_symbol():
    while True:
        symbol = input("\nEnter the stock symbol you are looking for: ").strip().upper()
        if symbol.isalpha() and 1 <= len(symbol) <= 7:
            return symbol
        print("Invalid symbol. Use letters only (e.g., AAPL, GOOGL).")


def _choose(prompt, options):
    while True:
        print(prompt)
        for key, value in options.items():
            print(f"  {key}. {value}")
        choice = input("Enter choice: ").strip()
        if choice in options:
            return options[choice]
        print(f"Please enter a number from 1 to {len(options)}.")


def get_chart_type():
    return _choose("\nChart Types\n-----------", CHART_TYPES)


def get_time_series():
    return _choose("\nSelect the Time Series of the chart you want to generate\n"
                   "--------------------------------------------------------", TIME_SERIES)


def _get_date(prompt):
    while True:
        text = input(prompt).strip()
        try:
            return datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD format (e.g., 2024-01-15).")


def get_date_range():
    start = _get_date("\nEnter the start date (YYYY-MM-DD): ")
    while True:
        end = _get_date("Enter the end date (YYYY-MM-DD): ")
        if end >= start:
            return start, end
        print("End date cannot be before the start date. Try again.")
