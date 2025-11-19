# orchestrator_agent/app/services/orchestrator.py
import httpx
from app.model.schema import UserProfile, PredictionResponse
from typing import Literal

class OrchestratorService:
    def __init__(self):
        self.user_agent_url = "http://localhost:7001/user"
        self.model_agent_url = "http://localhost:7002/model"
        self.planner_agent_url = "http://localhost:7003/planner"

    def get_user_profile(self, user_id: str) -> UserProfile:
        """Fetch user profile from User Agent"""
        url = f"{self.user_agent_url}/profile?user_id={user_id}"
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url)
            resp.raise_for_status()
            data = resp.json()
        return UserProfile(**data)

    def get_user_answers(self, user_id: str) -> dict:
        """Fetch user questionnaire answers"""
        url = f"{self.user_agent_url}/questions?user_id={user_id}"
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url)
            resp.raise_for_status()
            return resp.json()

    def get_predictions(self, user_profile: UserProfile) -> PredictionResponse:
        """Get multi-horizon predictions from Model Agent"""
        url = f"{self.model_agent_url}/model/predict"
        with httpx.Client(timeout=15.0) as client:
            resp = client.post(url, json=user_profile.dict())
            resp.raise_for_status()
            data = resp.json()
        return PredictionResponse(**data)

    def plan_portfolio(self, user_profile: UserProfile, method: Literal['GA','Markowitz']='GA') -> PredictionResponse:
        """Call Planner Agent to optimize portfolio"""
        # Step 1: Get predictions
        predictions = self.get_predictions(user_profile)

        # Step 2: Send predictions + user horizon + method to planner
        payload = {
            "user_profile": user_profile.dict(),
            "method": method
        }
        url = f"{self.planner_agent_url}/planner/plan"
        with httpx.Client(timeout=20.0) as client:
            resp = client.post(url, params={"method": method}, json=user_profile.dict())
            resp.raise_for_status()
            data = resp.json()
        return PredictionResponse(**data)
