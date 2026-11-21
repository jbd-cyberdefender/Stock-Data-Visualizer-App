"""Stock Data Visualizer - entry point."""
from dotenv import load_dotenv

import input_handler
import api_client
import data_processor
import chart_generator


def run_once():
    symbol = input_handler.get_symbol()
    chart_type = input_handler.get_chart_type()
    function = input_handler.get_time_series()
    start, end = input_handler.get_date_range()

    try:
        data = api_client.fetch_stock_data(symbol, function)
    except api_client.StockAPIError as e:
        print(f"\nError: {e}")
        return

    series = data_processor.extract_series(data)
    filtered = data_processor.filter_by_date(series, start, end)
    if not filtered:
        print("\nNo data found for that date range. Try a different range or time series.")
        return

    dates, chart_series = data_processor.to_chart_data(filtered)
    path = chart_generator.generate_chart(symbol, chart_type, dates, chart_series, start, end)
    print(f"\nChart opened in your browser (saved to {path}).")


def main():
    load_dotenv()
    print("Stock Data Visualizer")
    print("---------------------")
    while True:
        run_once()
        again = input("\nWould you like to view more stock data? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
