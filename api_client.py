"""Requests stock data from the Alpha Vantage API."""
import os
import requests
import time

BASE_URL = "https://www.alphavantage.co/query"


class StockAPIError(Exception):
    pass


def get_api_key():
    key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not key:
        raise StockAPIError(
            "No API key found. Create a .env file with ALPHA_VANTAGE_API_KEY=your_key"
        )
    return key


def _request(params):
    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        raise StockAPIError(f"Network error: {e}")
    return response.json()


def fetch_stock_data(symbol, function):
    params = {"function": function, "symbol": symbol, "apikey": get_api_key()}
    if function == "TIME_SERIES_INTRADAY":
        params["interval"] = "60min"
    if function in ("TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY"):
        params["outputsize"] = "full"

    data = _request(params)

    # Free keys can't use outputsize=full on some endpoints; wait, then retry with compact.
    info = data.get("Information", "")
    if "outputsize" in params and "outputsize" in info.lower() and not _has_series(data):
        time.sleep(1.5)
        params["outputsize"] = "compact"
        data = _request(params)

    if "Error Message" in data:
        raise StockAPIError(f"Invalid symbol or request: {symbol}")
    if "Note" in data or ("Information" in data and not _has_series(data)):
        raise StockAPIError("API limit reached or request not allowed: "
                            + data.get("Note", data.get("Information", "")))
    if not _has_series(data):
        raise StockAPIError("Unexpected response from API.")
    return data


def _has_series(data):
    return any(k != "Meta Data" and isinstance(v, dict) for k, v in data.items())
