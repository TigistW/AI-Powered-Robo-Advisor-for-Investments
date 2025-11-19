from fastapi import APIRouter
from app.core.schema import PortfolioRequest, PortfolioResponse
from app.planner.allocator import Allocator

router = APIRouter()
allocator = Allocator()

@router.post("/allocate", response_model=PortfolioResponse)
async def allocate_portfolio(request: PortfolioRequest):
    portfolio = allocator.allocate(request.user_profile, request.asset_predictions)
    total = round(sum([p.allocation for p in portfolio]), 4)
    return PortfolioResponse(total_allocation=total, portfolio=portfolio)
