import httpx
from app.core.schema import UserProfile, AssetPrediction, PortfolioAsset

class OrchestratorService:
    def __init__(self):
        self.model_agent_url = "http://localhost:7003/model/predict"
        self.planner_agent_url = "http://localhost:7005/planner/allocate"

    def run_workflow(self, user_profile: UserProfile):
        # 1️⃣ Call Model Agent
        with httpx.Client(timeout=30.0) as client:
            model_resp = client.post(
                self.model_agent_url,
                json=user_profile.dict()
            )
            model_resp.raise_for_status()
            predictions_json = model_resp.json()["predictions"]

        # Convert JSON to AssetPrediction objects
        asset_predictions = [AssetPrediction(**p) for p in predictions_json]

        # 2️⃣ Call Planner Agent
        planner_payload = {
            "user_profile": user_profile.dict(),
            "asset_predictions": [p.dict() for p in asset_predictions]
        }

        with httpx.Client(timeout=30.0) as client:
            planner_resp = client.post(self.planner_agent_url, json=planner_payload)
            planner_resp.raise_for_status()
            planner_json = planner_resp.json()

        final_portfolio = [PortfolioAsset(**p) for p in planner_json["portfolio"]]
        total_alloc = planner_json["total_allocation"]

        return asset_predictions, final_portfolio, total_alloc
