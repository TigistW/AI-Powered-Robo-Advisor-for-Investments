# Model Agent Service

Predicts expected returns, risk (volatility), and suggests portfolio allocation per asset.

## Endpoint

### POST /model/predict
- Input: UserProfile JSON
- Output: Predicted returns, volatility, suggested allocation for each supported asset

## Run Service

```bash
uvicorn main:app --reload --port 7003
