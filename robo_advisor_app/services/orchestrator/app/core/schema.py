from pydantic import BaseModel
from typing import List, Dict

# Redefine the user profile schema
class UserProfile(BaseModel):
    risk_score: int
    risk_category: str
    investment_horizon_years: int
    goals: str
    liquidity_need: str
    experience_level: str
    loss_aversion_score: int
    constraints: Dict[str, float]

# Redefine model agent output schema
class AssetPrediction(BaseModel):
    ticker: str
    expected_return: float
    volatility: float
    suggested_allocation: float

# Redefine planner agent portfolio schema
class PortfolioAsset(BaseModel):
    ticker: str
    allocation: float

# Orchestrator request/response
class OrchestratorRequest(BaseModel):
    user_profile: UserProfile

class OrchestratorResponse(BaseModel):
    asset_predictions: List[AssetPrediction]
    final_portfolio: List[PortfolioAsset]
    total_allocation: float
