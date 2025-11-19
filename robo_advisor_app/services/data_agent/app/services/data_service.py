import yfinance as yf
from functools import lru_cache
import pandas as pd

class DataService:
    def __init__(self):
        # You could expand this list to more tickers / ETFs
        self.supported = ["SPY", "QQQ", "BND", "TSLA", "AAPL", "GOOGL"]

    def get_supported_assets(self):
        return self.supported

    @lru_cache(maxsize=32)
    def fetch_history(self, ticker: str, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
        if ticker not in self.supported:
            raise ValueError(f"Ticker '{ticker}' not supported")

        # Using yfinance to fetch historical data
        try:
            data = yf.download(ticker, period=period, interval=interval, progress=False)
        except Exception as e:
            raise ValueError(f"Error fetching data for {ticker}: {e}")

        if data.empty:
            raise ValueError(f"No data returned for ticker '{ticker}' with period={period}, interval={interval}")

        return data

