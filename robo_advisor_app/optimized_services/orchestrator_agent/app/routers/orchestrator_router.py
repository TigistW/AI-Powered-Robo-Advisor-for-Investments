# orchestrator_agent/app/routers/orchestrator_router.py
from fastapi import APIRouter, Query
from app.services.orchestrator import OrchestratorService
from app.model.schema import PredictionResponse

router = APIRouter()
service = OrchestratorService()

@router.get("/portfolio/{user_id}", response_model=PredictionResponse)
async def get_portfolio(user_id: str, method: str = Query('GA', enum=['GA','Markowitz'])):
    """
    Orchestrator endpoint:
    1. Fetch user profile and answers
    2. Get LSTM predictions from Model Agent
    3. Optimize portfolio with GA or Markowitz
    """
    user_profile = service.get_user_profile(user_id)
    optimized_portfolio = service.plan_portfolio(user_profile, method=method)
    return optimized_portfolio
