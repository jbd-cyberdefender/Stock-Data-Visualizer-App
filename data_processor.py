"""Extracts and filters the time series data."""
from datetime import datetime


def extract_series(data):
    for key, value in data.items():
        if key != "Meta Data" and isinstance(value, dict):
            return value
    return {}


def filter_by_date(series, start, end):
    """Returns a chronologically sorted list of (timestamp, values) within the range."""
    filtered = []
    for timestamp, values in series.items():
        day = datetime.strptime(timestamp[:10], "%Y-%m-%d").date()
        if start <= day <= end:
            filtered.append((timestamp, values))
    filtered.sort(key=lambda item: item[0])
    return filtered


def to_chart_data(filtered):
    dates = [ts for ts, _ in filtered]
    fields = {"Open": "1. open", "High": "2. high", "Low": "3. low", "Close": "4. close"}
    series = {name: [float(v[key]) for _, v in filtered] for name, key in fields.items()}
    return dates, series
