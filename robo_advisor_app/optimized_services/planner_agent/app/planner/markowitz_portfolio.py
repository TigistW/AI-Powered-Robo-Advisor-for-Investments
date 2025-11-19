# planner_agent/app/planner/markowitz_portfolio.py
import numpy as np
import cvxpy as cp
from app.model.schema import AssetPrediction

def optimize_markowitz(asset_predictions, horizon='1m', risk_aversion=1.0):
    """
    Optimize portfolio using Mean-Variance (Markowitz) optimization.
    
    Args:
        asset_predictions: List[AssetPrediction]
        horizon: '1d', '1w', '1m', '3m'
        risk_aversion: higher = more risk-averse
    
    Returns:
        np.array of weights (sum=1)
    """
    n_assets = len(asset_predictions)
    returns = np.array([getattr(asset, f"{horizon}_return") for asset in asset_predictions])
    
    # Simplified: use diagonal covariance (no correlation) if covariance unknown
    vols = np.array([asset.volatility for asset in asset_predictions])
    cov_matrix = np.diag(vols**2)

    w = cp.Variable(n_assets)
    expected_port_return = returns @ w
    port_risk = cp.quad_form(w, cov_matrix)

    objective = cp.Maximize(expected_port_return - risk_aversion * port_risk)
    constraints = [cp.sum(w) == 1, w >= 0]  # fully invested, no shorting
    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.SCS)

    if w.value is not None:
        weights = np.array(w.value)
        weights = weights / np.sum(weights)  # normalize
        return weights
    else:
        # fallback: equal weights
        return np.ones(n_assets) / n_assets
