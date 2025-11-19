# planner_agent/app/planner/portfolio_engine.py
from app.model.schema import AssetPrediction
from app.planner.ga_portfolio import optimize_portfolio
from app.planner.markowitz_portfolio import optimize_markowitz

def plan_portfolio(asset_predictions: list[AssetPrediction], user_horizon: str, method='GA'):
    """
    Plan portfolio allocation using GA or Markowitz.
    
    Args:
        asset_predictions: list of AssetPrediction
        user_horizon: '1d', '1w', '1m', '3m'
        method: 'GA' or 'Markowitz'
    """
    if method.lower() == 'ga':
        allocation = optimize_portfolio(asset_predictions, horizon=user_horizon)
    elif method.lower() == 'markowitz':
        allocation = optimize_markowitz(asset_predictions, horizon=user_horizon)
    else:
        raise ValueError("Invalid method. Choose 'GA' or 'Markowitz'")

    # Apply allocation to assets
    for asset, weight in zip(asset_predictions, allocation):
        asset.suggested_allocation = round(float(weight), 4)
    
    return asset_predictions
