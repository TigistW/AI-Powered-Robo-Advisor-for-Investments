from pydantic import BaseModel
from typing import List, Dict

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

class PortfolioRequest(BaseModel):
    user_profile: UserProfile
    asset_predictions: List[AssetPrediction]

class PortfolioAsset(BaseModel):
    ticker: str
    allocation: float

class PortfolioResponse(BaseModel):
    total_allocation: float
    portfolio: List[PortfolioAsset]
