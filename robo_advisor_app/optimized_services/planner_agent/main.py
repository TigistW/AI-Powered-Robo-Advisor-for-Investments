# planner_agent/main.py
from fastapi import FastAPI
from app.routers.planner import router as planner_router

app = FastAPI(
    title="Planner Agent Service",
    version="1.0.0",
    description="Plans portfolio allocations using GA based on LSTM predictions."
)

app.include_router(planner_router, prefix="/planner", tags=["PlannerAgent"])

@app.get("/")
async def root():
    return {"message": "Planner Agent is running"}
