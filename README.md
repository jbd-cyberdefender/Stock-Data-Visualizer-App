### Stock-Data-Visualizer-App
# Stock Data Visualizer

A Python command-line app that pulls historical stock data from the [Alpha Vantage](https://www.alphavantage.co/) API and displays it as a chart in your web browser.

## Features
- Look up any stock by its symbol (e.g., AAPL, MSFT)
- Choose a bar or line chart
- Choose a time series: intraday, daily, weekly, or monthly
- Pick a start and end date (YYYY-MM-DD)
- The chart opens automatically in your default browser

## Requirements
- Python 3.9 or newer
- A free Alpha Vantage API key: https://www.alphavantage.co/support/#api-key

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/OWNER/Stock-Data-Visualizer-App.git
   cd Stock-Data-Visualizer-App
   ```

2. **Create and activate a virtual environment**

   Mac/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key**

   Create a file named `.env` in the project folder containing:
   ```
   ALPHA_VANTAGE_API_KEY=your_key_here
   ```
   This file is listed in `.gitignore` and is never committed.

## Usage
```bash
python3 main.py
```
Follow the prompts to enter a stock symbol, chart type, time series, and date range. The chart opens in your browser and is saved as an `.svg` file in the project folder.

## Project Structure
| File | Purpose |
|------|---------|
| `main.py` | Entry point; runs the program loop |
| `input_handler.py` | Prompts for and validates user input |
| `api_client.py` | Requests data from Alpha Vantage and handles errors |
| `data_processor.py` | Filters data to the selected date range |
| `chart_generator.py` | Builds the chart with pygal and opens it in the browser |

## Notes
- The free API key allows 25 requests per day and 1 request per second.
- Intraday data only covers recent dates.
- On the free tier, daily data may only include roughly the last 100 trading days; use weekly or monthly for longer ranges.
- Weekends and market holidays have no data.

