from typing import List
from app.core.schema import AssetPrediction, UserProfile, PortfolioAsset

class Allocator:
    def __init__(self):
        pass

    def allocate(self, user_profile: UserProfile, predictions: List[AssetPrediction]) -> List[PortfolioAsset]:
        """
        Generate final portfolio allocation respecting user constraints.
        """
        total_alloc = 0
        portfolio = []

        # Apply initial suggested allocations
        for asset in predictions:
            alloc = asset.suggested_allocation

            # Apply constraints
            if "max_equity" in user_profile.constraints and asset.ticker in ["SPY","QQQ","AAPL","TSLA","GOOGL"]:
                alloc = min(alloc, user_profile.constraints["max_equity"])
            if "min_bonds" in user_profile.constraints and asset.ticker == "BND":
                alloc = max(alloc, user_profile.constraints["min_bonds"])
            if "min_cash" in user_profile.constraints and asset.ticker == "CASH":
                alloc = max(alloc, user_profile.constraints["min_cash"])

            portfolio.append(PortfolioAsset(ticker=asset.ticker, allocation=alloc))
            total_alloc += alloc

        # Normalize to 100%
        if total_alloc > 0:
            for p in portfolio:
                p.allocation = round(p.allocation / total_alloc, 4)

        return portfolio
