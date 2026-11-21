import re
from datetime import datetime


def validate_symbol(symbol: str) -> bool:
    """Capitalized, 1-7 alphabetic characters."""
    if not isinstance(symbol, str):
        return False
    return bool(re.fullmatch(r"[A-Z]{1,7}", symbol))


def validate_chart_type(chart_type: str) -> bool:
    """Single numeric character: '1' or '2'."""
    return isinstance(chart_type, str) and chart_type in {"1", "2"}


def validate_time_series(time_series: str) -> bool:
    """Single numeric character: '1' through '4'."""
    return isinstance(time_series, str) and time_series in {"1", "2", "3", "4"}


def parse_date(date_str: str):
    """Validates YYYY-MM-DD format and returns a datetime.date object, or None if invalid."""
    if not isinstance(date_str, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def validate_date_range(start_date_str: str, end_date_str: str) -> bool:
    """Ensures both dates are valid YYYY-MM-DD and start_date <= end_date."""
    start = parse_date(start_date_str)
    end = parse_date(end_date_str)
    if start is None or end is None:
        return False
    return start <= end