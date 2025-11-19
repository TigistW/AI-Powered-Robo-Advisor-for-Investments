from pydantic import BaseModel
from typing import List, Dict, Any

class HistoryPoint(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float

class HistoryResponse(BaseModel):
    ticker: str
    history: List[HistoryPoint]

class AssetsResponse(BaseModel):
    assets: List[str]
