import requests
import pandas as pd
import time
from ta.trend import EMAIndicator

def get_all_symbols():
    url = 'https://api.binance.com/api/v3/exchangeInfo'
    response = requests.get(url)
    data = response.json()

    # Known stablecoins to exclude as base assets
    stablecoins = {"USDC", "FDUSD","EUR","AEUR","EURI","BUSD", "TUSD", "PAX", "USDP", "DAI", "UST"} 

    symbols = []
    for s in data['symbols']:
        if (s['status'] == 'TRADING' and
            s['isSpotTradingAllowed'] and
            s['quoteAsset'] == 'USDT' and
            s['baseAsset'] not in stablecoins):
            symbols.append(s['symbol'])
    return symbols

def get_historical_klines(symbol, interval='1h', limit=250):
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()
    if isinstance(data, dict) and 'code' in data:
        raise Exception(f"Error fetching data for {symbol}: {data['msg']}")
    df = pd.DataFrame(data, columns=[
        'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close time', 'Quote asset volume', 'Number of trades',
        'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
    ])
    df['Close'] = df['Close'].astype(float)
    return df

def is_close_to_ema(df, threshold=0.01):
    # Calculate 200 EMA
    ema_indicator = EMAIndicator(close=df['Close'], window=200)
    df['EMA200'] = ema_indicator.ema_indicator()
    latest_price = df['Close'].iloc[-1]
    latest_ema = df['EMA200'].iloc[-1]
    difference = abs(latest_price - latest_ema) / latest_ema
    return difference <= threshold

def had_recent_ema_cross(df, lookback=72):
    """
    Check if there was a cross of the 50 and 100 EMA in the last `lookback` bars.
    A cross occurs when the sign of (EMA50 - EMA100) changes from one candle to the next.
    """
    # Calculate 50 and 100 EMA
    ema50 = EMAIndicator(close=df['Close'], window=50).ema_indicator()
    ema100 = EMAIndicator(close=df['Close'], window=100).ema_indicator()

    df['EMA50'] = ema50
    df['EMA100'] = ema100

    # Consider the recent period
    recent_df = df.iloc[-lookback:].copy()

    recent_df['EMA_DIFF'] = recent_df['EMA50'] - recent_df['EMA100']

    # Check if sign changed in recent lookback candles
    ema_diff = recent_df['EMA_DIFF'].values
    for i in range(1, len(ema_diff)):
        # Sign change indicates a cross between EMA50 and EMA100
        if ema_diff[i] * ema_diff[i-1] < 0:
            return True
    return False

def main():
    symbols = get_all_symbols()
    close_to_ema_symbols = []
    for symbol in symbols:
        try:
            df = get_historical_klines(symbol)
            if len(df) < 200:
                # Not enough data to calculate 200 EMA reliably
                continue
            
            # Check both conditions: close to 200 EMA and recent 50/100 EMA cross
            if is_close_to_ema(df) and had_recent_ema_cross(df, lookback=72):
                close_to_ema_symbols.append(symbol)
                print(f"{symbol} meets the criteria (close to 200 EMA and recent 50/100 EMA cross).")
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
        
        # Rate limiting: sleep for 100 milliseconds after each API call
        time.sleep(0.1)
        
    print("\nSymbols meeting the enhanced criteria:")
    print(close_to_ema_symbols)

if __name__ == "__main__":
    main()
