from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services.data_service import DataService

router = APIRouter()
svc = DataService()

@router.get("/assets")
async def get_assets():
    assets = svc.get_supported_assets()
    return {"assets": assets}

@router.get("/history")
async def get_history(
    ticker: str,
    period: str = Query("1mo", description="Period for historical data (e.g., 1d, 5d, 1mo, 1y)"),
    interval: str = Query("1d", description="Interval between data points (1d, 1wk, 1mo)")
):
    try:
        df = svc.fetch_history(ticker, period=period, interval=interval)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Convert to JSON serializable format: list of dicts
    data = []
    for idx, row in df.iterrows():
        data.append({
            "date": idx.isoformat(),
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"],
            "volume": row["Volume"]
        })
    return {"ticker": ticker, "history": data}
