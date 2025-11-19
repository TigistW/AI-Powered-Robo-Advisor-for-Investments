# orchestrator_agent/main.py
from fastapi import FastAPI
from app.routers.orchestrator_router import router as orch_router

app = FastAPI(
    title="Orchestrator Agent",
    version="1.0.0",
    description="Coordinates User Agent, Model Agent, and Planner Agent"
)

app.include_router(orch_router, prefix="/orchestrator", tags=["Orchestrator"])

@app.get("/")
async def root():
    return {"message": "Orchestrator Agent is running"}
