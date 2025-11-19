# app/core/schema.py
from pydantic import BaseModel
from typing import Dict, List

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
    expected_return: float          # 1-day prediction
    weekly_return: float            # 1-week prediction
    monthly_return: float           # 1-month prediction
    quarterly_return: float         # 3-month prediction
    volatility: float
    suggested_allocation: float

class PredictionResponse(BaseModel):
    predictions: List[AssetPrediction]
