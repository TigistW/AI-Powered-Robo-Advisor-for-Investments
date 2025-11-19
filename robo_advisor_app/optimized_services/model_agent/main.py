# main.py
from fastapi import FastAPI
from app.routers.model import router as model_router

app = FastAPI(
    title="Model Agent Optimized Service",
    version="1.0.0",
    description="Predicts expected returns, risk, and portfolio allocation."
)

app.include_router(model_router, prefix="/model", tags=["OptimizedModelAgent"])

@app.get("/")
async def root():
    return {"message": "Model Agent Optimized is running"}
