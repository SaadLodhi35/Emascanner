# Cross-EMA Symbol Filter

Cross-EMA Symbol Filter is a Python-based tool that identifies cryptocurrency trading pairs on Binance that meet specific technical analysis criteria, such as proximity to the 200 EMA and recent crossovers of the 50 EMA and 100 EMA.

## Features

- **Fetch Trading Pairs**: Automatically retrieves all trading pairs with USDT as the quote asset from Binance, excluding stablecoins as base assets.
- **Technical Analysis**: 
  - Identifies pairs where the price is within a defined threshold of the 200 EMA.
  - Detects recent EMA crossovers between the 50 EMA and 100 EMA within a configurable lookback period.
- **Customizable Parameters**: 
  - Adjust the threshold for proximity to the 200 EMA.
  - Modify the lookback period for detecting EMA crossovers.
- **Error Handling**: Gracefully handles API rate limits and errors during data retrieval.

## Requirements

To run this project, you'll need the following:
- Python 3.8 or higher
- The following Python packages:
  - `requests`
  - `pandas`
  - `ta` (Technical Analysis library)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/cross-ema-symbol-filter.git
   cd cross-ema-symbol-filter
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script using the following command:
```bash
python crossema.py
```

### Example Output

The script will print a list of trading pairs that meet the criteria for both conditions:
- Price is close to the 200 EMA.
- There was a recent 50/100 EMA crossover within the defined lookback period.

Example output:
```
BTCUSDT meets the criteria (close to 200 EMA and recent 50/100 EMA cross).
ETHUSDT meets the criteria (close to 200 EMA and recent 50/100 EMA cross).

Symbols meeting the enhanced criteria:
['BTCUSDT', 'ETHUSDT']
```

## How It Works

1. **Fetch Symbols**: The script retrieves all trading pairs with USDT as the quote asset from Binance's API.
2. **Retrieve Historical Data**: It fetches the last 250 hourly candlesticks for each symbol.
3. **EMA Calculations**:
   - Computes the 200 EMA to check price proximity.
   - Computes the 50 and 100 EMA to identify crossovers.
4. **Filtering**:
   - Determines if the latest price is within a 1% threshold of the 200 EMA.
   - Scans the past 72 hours for a crossover of the 50 and 100 EMA.

## Configurable Parameters

You can modify the following parameters in the script:
- **EMA Proximity Threshold**: Default is 1% (`threshold=0.01`).
- **Lookback Period for EMA Crossover**: Default is 72 candlesticks (`lookback=72`).

To adjust these, update the respective function calls in the code:
```python
is_close_to_ema(df, threshold=0.01)
had_recent_ema_cross(df, lookback=72)
```

## API Rate Limiting

To adhere to Binance's API rate limits, the script introduces a 100ms delay between API calls:
```python
time.sleep(0.1)
```

## Contributing

Contributions are welcome! If you have ideas for improvements, bug fixes, or additional features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- **Binance API**: For providing access to market data.
- **TA Library**: For its robust technical analysis tools.

---

Start identifying promising cryptocurrency trading opportunities today with Cross-EMA Symbol Filter!
