from fastapi import APIRouter, HTTPException
from app.core.schema import UserProfile, PredictionResponse
from app.model.predictor import Predictor

router = APIRouter()
predictor = Predictor()

@router.post("/predict", response_model=PredictionResponse)
async def predict(user_profile: UserProfile):
    try:
        result = predictor.predict(user_profile)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result
