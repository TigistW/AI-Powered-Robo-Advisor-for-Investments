# planner_agent/app/routers/planner.py
from fastapi import APIRouter, Query
from app.model.schema import PredictionResponse, UserProfile
from app.planner.portfolio_engine import plan_portfolio
from app.model.predictor import Seq2SeqLSTMPredictor

router = APIRouter()
predictor = Seq2SeqLSTMPredictor()

@router.post("/plan", response_model=PredictionResponse)
async def plan(user_profile: UserProfile, method: str = Query('GA', enum=['GA','Markowitz'])):
    # Get LSTM predictions
    predictions = predictor.predict(user_profile)

    # Map user investment horizon to horizon key
    if user_profile.investment_horizon_years <= 1/12:
        horizon = '1d'
    elif user_profile.investment_horizon_years <= 1/4:
        horizon = '1w'
    elif user_profile.investment_horizon_years <= 1:
        horizon = '1m'
    else:
        horizon = '3m'

    optimized_assets = plan_portfolio(predictions.predictions, user_horizon=horizon, method=method)
    return PredictionResponse(predictions=optimized_assets)
