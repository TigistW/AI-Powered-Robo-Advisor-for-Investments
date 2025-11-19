import httpx
import pandas as pd
import numpy as np
from app.core.schema import UserProfile, PredictionResponse, AssetPrediction

class Predictor:
    def __init__(self):
        # Supported tickers
        self.supported = ["SPY", "QQQ", "BND", "TSLA", "AAPL", "GOOGL"]
        # Base URL of Data Agent
        self.data_agent_url = "http://localhost:7004/data"

    def fetch_data(self, ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        url = f"{self.data_agent_url}/history?ticker={ticker}&period={period}&interval={interval}"
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url)
            resp.raise_for_status()
            data = resp.json().get("history", [])
            if not data:
                raise ValueError(f"No data returned for {ticker}")

            flattened = []
            for row in data:
                try:
                    flattened.append({
                        "Open": float(row["open"][ticker]),
                        "High": float(row["high"][ticker]),
                        "Low": float(row["low"][ticker]),
                        "Close": float(row["close"][ticker]),
                        "Volume": float(row["volume"][ticker]),
                        "Date": row["date"]
                    })
                except Exception as e:
                    raise ValueError(f"Invalid row for {ticker}: {row}. Error: {e}")

            df = pd.DataFrame(flattened)
            df["Date"] = pd.to_datetime(df["Date"])
            df.set_index("Date", inplace=True)
            return df


    def compute_metrics(self, df: pd.DataFrame):
        """
        Compute expected return and volatility from historical data
        """
        df["returns"] = df["Close"].pct_change()
        expected_return = df["returns"].mean() * 252  # annualized
        volatility = df["returns"].std() * np.sqrt(252)  # annualized
        return expected_return, volatility

    def suggest_allocation(self, risk_category: str, expected_return: float, volatility: float):
        """
        Suggest allocation based on risk category and asset risk metrics
        """
        if risk_category.lower() == "conservative":
            return max(0.05, 0.4 - volatility)
        elif risk_category.lower() == "moderate":
            return max(0.1, 0.6 - volatility / 2)
        # aggressive
        return max(0.15, 0.8 - volatility / 3)

    def predict(self, user_profile: UserProfile):
        """
        Generate predictions for all supported assets
        """
        predictions = []
        for ticker in self.supported:
            df = self.fetch_data(ticker)
            exp_return, vol = self.compute_metrics(df)
            allocation = self.suggest_allocation(user_profile.risk_category, exp_return, vol)

            predictions.append(
                AssetPrediction(
                    ticker=ticker,
                    expected_return=round(float(exp_return), 4),
                    volatility=round(float(vol), 4),
                    suggested_allocation=round(float(allocation), 4)
                )
            )

        return PredictionResponse(predictions=predictions)
