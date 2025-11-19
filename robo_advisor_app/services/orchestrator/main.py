from fastapi import FastAPI
from app.routers.orchestrator import router as orchestrator_router

app = FastAPI(
    title="Orchestrator Agent",
    version="1.0.0",
    description="Coordinates User, Model, and Planner Agents"
)

app.include_router(orchestrator_router, prefix="/orchestrator", tags=["Orchestrator"])

@app.get("/")
async def root():
    return {"message": "Orchestrator running"}
