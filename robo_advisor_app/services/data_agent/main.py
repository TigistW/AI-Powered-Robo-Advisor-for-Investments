from fastapi import FastAPI, HTTPException, Query
from app.routers.data import router as data_router

app = FastAPI(
    title="Data Agent Service",
    version="1.0.0",
    description="Fetches historical market data via yfinance."
)

app.include_router(data_router, prefix="/data", tags=["DataAgent"])

@app.get("/")
async def root():
    return {"message": "Data Agent is running"}
