# app/model/predictor.py
import httpx
import pandas as pd
import numpy as np
import torch
import pickle
from app.core.schema import UserProfile, PredictionResponse, AssetPrediction

class Seq2SeqLSTMPredictor:
    def __init__(self):
        self.supported = ["SPY", "QQQ", "BND", "TSLA", "AAPL", "GOOGL"]
        self.data_agent_url = "http://localhost:7004/data"

        # Load pre-trained seq2seq LSTM model
        self.model = torch.load("app/model/ml_model/trained_lstm_model.pt")
        self.model.eval()

        # Load scaler
        with open("app/model/ml_model/scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)

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
                        "Close": float(row["close"][ticker]),
                        "Date": row["date"]
                    })
                except Exception as e:
                    raise ValueError(f"Invalid row for {ticker}: {row}. Error: {e}")

            df = pd.DataFrame(flattened)
            df["Date"] = pd.to_datetime(df["Date"])
            df.set_index("Date", inplace=True)
            return df

    def predict_returns_seq(self, df: pd.DataFrame):
        prices = df["Close"].values.reshape(-1, 1)
        scaled = self.scaler.transform(prices)
        tensor_data = torch.tensor([scaled], dtype=torch.float32)

        with torch.no_grad():
            seq_pred = self.model(tensor_data)
            seq_pred = seq_pred.numpy().flatten()

        return {
            "1d": seq_pred[0],
            "1w": seq_pred[4],
            "1m": seq_pred[19],
            "3m": seq_pred[59]
        }

    def predict(self, user_profile: UserProfile):
        predictions = []
        for ticker in self.supported:
            df = self.fetch_data(ticker)
            future_returns = self.predict_returns_seq(df)
            volatility = df["Close"].pct_change().std() * np.sqrt(252)

            predictions.append(
                AssetPrediction(
                    ticker=ticker,
                    expected_return=round(float(future_returns["1d"]), 4),
                    weekly_return=round(float(future_returns["1w"]), 4),
                    monthly_return=round(float(future_returns["1m"]), 4),
                    quarterly_return=round(float(future_returns["3m"]), 4),
                    volatility=round(float(volatility), 4),
                    suggested_allocation=0.0
                )
            )
        return PredictionResponse(predictions=predictions)
