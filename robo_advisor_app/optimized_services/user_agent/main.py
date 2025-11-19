from fastapi import FastAPI
from app.routers.user import router as user_router

app = FastAPI(
    title="User Agent Optimized Service",
    version="1.0.0",
    description="Handles user profiling, questionnaire, and risk scoring."
)

app.include_router(user_router, prefix="/user", tags=["UserAgentOptimized"])

@app.get("/")
async def root():
    return {"message": "User Agent Optimized is running"}
