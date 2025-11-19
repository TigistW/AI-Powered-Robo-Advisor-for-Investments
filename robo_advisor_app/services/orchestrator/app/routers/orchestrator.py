from fastapi import APIRouter
from app.core.schema import OrchestratorRequest, OrchestratorResponse
from app.services.orchestrator_service import OrchestratorService

router = APIRouter()
service = OrchestratorService()

@router.post("/run", response_model=OrchestratorResponse)
async def run_orchestrator(request: OrchestratorRequest):
    asset_preds, final_portfolio, total_alloc = service.run_workflow(request.user_profile)
    return OrchestratorResponse(
        asset_predictions=asset_preds,
        final_portfolio=final_portfolio,
        total_allocation=total_alloc
    )
