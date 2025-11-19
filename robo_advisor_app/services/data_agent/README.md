# Data Agent Service

This microservice provides market data using Yahoo Finance via the `yfinance` Python library.

## Endpoints

- `GET /data/assets`  
  Returns a list of supported tickers.

- `GET /data/history?ticker={ticker}&period={period}&interval={interval}`  
  Returns historical OHLCV data for a given ticker.

## Example Request

