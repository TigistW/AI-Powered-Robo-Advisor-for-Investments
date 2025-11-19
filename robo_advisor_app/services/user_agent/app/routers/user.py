from fastapi import APIRouter
from .core.schema import QuestionnaireInput, UserProfile
from .services.questionnaire import QuestionnaireService
from .services.profile_builder import ProfileBuilder

router = APIRouter()

questionnaire_service = QuestionnaireService()
profile_builder = ProfileBuilder()

@router.get("/questions")
async def get_questions():
    """Return the questionnaire definition for frontend."""
    return questionnaire_service.get_questionnaire()

@router.post("/profile", response_model=UserProfile)
async def generate_profile(payload: QuestionnaireInput):
    """Accept questionnaire answers and generate a user risk profile."""
    validated = questionnaire_service.validate_answers(payload.answers)
    profile = profile_builder.build_profile(validated)
    return profile
