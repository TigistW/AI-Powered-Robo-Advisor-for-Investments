# planner_agent/app/planner/ga_portfolio.py
import numpy as np
from deap import base, creator, tools, algorithms
from app.model.schema import AssetPrediction

def fitness(weights, asset_predictions, horizon='1m'):
    """
    GA fitness function: maximize risk-adjusted return.
    
    Args:
        weights: array of allocations
        asset_predictions: list of AssetPrediction objects
        horizon: '1d', '1w', '1m', '3m'
    
    Returns:
        tuple: fitness score
    """
    weights = np.array(weights)
    weights = weights / np.sum(weights)  # normalize sum to 1

    returns = np.array([getattr(asset, f"{horizon}_return") for asset in asset_predictions])
    vols = np.array([asset.volatility for asset in asset_predictions])

    port_return = np.dot(weights, returns)
    port_vol = np.sqrt(np.dot(weights**2, vols**2))  # simplified risk
    sharpe_like = port_return / (port_vol + 1e-8)
    return (sharpe_like,)

def optimize_portfolio(asset_predictions, horizon='1m', n_generations=50, population_size=100):
    """
    Run GA to optimize portfolio allocation.
    
    Returns:
        array of weights (sum=1)
    """
    n_assets = len(asset_predictions)

    # Setup DEAP
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", np.random.rand)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=n_assets)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", fitness, asset_predictions=asset_predictions, horizon=horizon)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=population_size)
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=n_generations, verbose=False)

    best = tools.selBest(pop, k=1)[0]
    weights = np.array(best)
    weights = weights / np.sum(weights)
    return weights
