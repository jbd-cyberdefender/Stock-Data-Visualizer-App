<<<<<<< HEAD
import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

import api_client
import data_processor

app = Flask(__name__)

# Load stock symbols from CSV file for the drop-down menu
def load_stock_symbols():
    symbols = []
    csv_path = os.path.join(os.path.dirname(__file__), 'stocks.csv')
    if os.path.exists(csv_path):
        try:
            with open(csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Adjust column keys depending on your CSV headers (e.g., 'Symbol', 'Ticker', 'Name')
                    symbol = row.get('Symbol') or row.get('Ticker') or list(row.values)[0]
                    name = row.get('Name') or row.get('Company Name') or ''
                    if symbol:
                        symbols.append({'symbol': symbol.strip().upper(), 'name': name.strip()})
        except Exception as e:
            print(f"Error loading stocks.csv: {e}")
    
    # Fallback default list if CSV isn't found
    if not symbols:
        symbols = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corporation'},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.'},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.'}
        ]
    return symbols

@app.route('/', methods=['GET', 'POST'])
def index():
    stocks = load_stock_symbols()
    error = None
    svg_data = None
    chart_title = None

    if request.method == 'POST':
        symbol = request.form.get('symbol', '').strip().upper()
        chart_type = request.form.get('chart_type', 'Line')
        time_series = request.form.get('time_series', 'TIME_SERIES_DAILY')
        start_str = request.form.get('start_date')
        end_str = request.form.get('end_date')

        try:
            start = datetime.strptime(start_str, "%Y-%m-%d").date()
            end = datetime.strptime(end_str, "%Y-%m-%d").date()
            if end < start:
                raise ValueError("End date cannot be before start date.")

            # Fetch data using your api_client
            raw_data = api_client.fetch_stock_data(symbol, time_series)
            series = data_processor.extract_series(raw_data)
            filtered = data_processor.filter_by_date(series, start, end)
            
            if not filtered:
                raise ValueError("No data found for that date range. Try a different range.")

            dates, chart_series = data_processor.to_chart_data(filtered)

            # Generate pygal chart object instead of saving to disk directly
            import pygal
            chart_class = pygal.Bar if chart_type == "Bar" else pygal.Line
            chart = chart_class(
                x_label_rotation=45,
                show_minor_x_labels=False,
                x_labels_major_count=min(len(dates), 15),
                width=1000,
                height=500,
            )
            chart.title = f"Stock Data for {symbol}: {start} to {end}"
            chart.x_labels = dates
            for name, values in chart_series.items():
                chart.add(name, values)
            
            # Render chart to SVG string so it can be embedded cleanly in HTML
            svg_data = chart.render(is_unicode=True)
            chart_title = chart.title

        except (api_client.StockAPIError, ValueError) as e:
            error = str(e)
        except Exception as e:
            error = f"An unexpected error occurred: {e}"

    return render_template('index.html', stocks=stocks, error=error, svg_data=svg_data, chart_title=chart_title)

if __name__ == '__main__':
=======
import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

import api_client
import data_processor

app = Flask(__name__)

# Load stock symbols from CSV file for the drop-down menu
def load_stock_symbols():
    symbols = []
    csv_path = os.path.join(os.path.dirname(__file__), 'stocks.csv')
    if os.path.exists(csv_path):
        try:
            with open(csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Adjust column keys depending on your CSV headers (e.g., 'Symbol', 'Ticker', 'Name')
                    symbol = row.get('Symbol') or row.get('Ticker') or list(row.values)[0]
                    name = row.get('Name') or row.get('Company Name') or ''
                    if symbol:
                        symbols.append({'symbol': symbol.strip().upper(), 'name': name.strip()})
        except Exception as e:
            print(f"Error loading stocks.csv: {e}")
    
    # Fallback default list if CSV isn't found
    if not symbols:
        symbols = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corporation'},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.'},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.'}
        ]
    return symbols

@app.route('/', methods=['GET', 'POST'])
def index():
    stocks = load_stock_symbols()
    error = None
    svg_data = None
    chart_title = None

    if request.method == 'POST':
        symbol = request.form.get('symbol', '').strip().upper()
        chart_type = request.form.get('chart_type', 'Line')
        time_series = request.form.get('time_series', 'TIME_SERIES_DAILY')
        start_str = request.form.get('start_date')
        end_str = request.form.get('end_date')

        try:
            start = datetime.strptime(start_str, "%Y-%m-%d").date()
            end = datetime.strptime(end_str, "%Y-%m-%d").date()
            if end < start:
                raise ValueError("End date cannot be before start date.")

            # Fetch data using your api_client
            raw_data = api_client.fetch_stock_data(symbol, time_series)
            series = data_processor.extract_series(raw_data)
            filtered = data_processor.filter_by_date(series, start, end)
            
            if not filtered:
                raise ValueError("No data found for that date range. Try a different range.")

            dates, chart_series = data_processor.to_chart_data(filtered)

            # Generate pygal chart object instead of saving to disk directly
            import pygal
            chart_class = pygal.Bar if chart_type == "Bar" else pygal.Line
            chart = chart_class(
                x_label_rotation=45,
                show_minor_x_labels=False,
                x_labels_major_count=min(len(dates), 15),
                width=1000,
                height=500,
            )
            chart.title = f"Stock Data for {symbol}: {start} to {end}"
            chart.x_labels = dates
            for name, values in chart_series.items():
                chart.add(name, values)
            
            # Render chart to SVG string so it can be embedded cleanly in HTML
            svg_data = chart.render(is_unicode=True)
            chart_title = chart.title

        except (api_client.StockAPIError, ValueError) as e:
            error = str(e)
        except Exception as e:
            error = f"An unexpected error occurred: {e}"

    return render_template('index.html', stocks=stocks, error=error, svg_data=svg_data, chart_title=chart_title)

if __name__ == '__main__':
>>>>>>> ae94ff0b619a36c8f8baa0a2ffd4cbc9110bba5b
    app.run(host='0.0.0.0', port=5000, debug=True)