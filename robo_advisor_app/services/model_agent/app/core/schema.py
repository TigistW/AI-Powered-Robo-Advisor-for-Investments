from pydantic import BaseModel, Field
from typing import Dict, List, Any

class UserProfile(BaseModel):
    risk_score: int
    risk_category: str
    investment_horizon_years: int
    goals: str
    liquidity_need: str
    experience_level: str
    loss_aversion_score: int
    constraints: Dict[str, float]

class AssetPrediction(BaseModel):
    ticker: str
    expected_return: float
    volatility: float
    suggested_allocation: float

class PredictionResponse(BaseModel):
    predictions: List[AssetPrediction]
