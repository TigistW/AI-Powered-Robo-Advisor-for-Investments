from pydantic import BaseModel, Field
from typing import Dict, Any

class QuestionnaireInput(BaseModel):
    answers: Dict[str, Any]

class UserProfile(BaseModel):
    risk_score: int = Field(..., ge=0, le=100)
    risk_category: str
    investment_horizon_years: int
    goals: str
    liquidity_need: str
    experience_level: str
    loss_aversion_score: int
    constraints: Dict[str, float]
