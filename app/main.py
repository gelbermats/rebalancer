from contextlib import asynccontextmanager

from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import settings
from app.scheduler import setup_scheduler
from app.modules.marketdata.api import router as marketdata_router
from app.modules.portfolio.api import router as portfolio_router


scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.scheduler_enabled:
        setup_scheduler(scheduler)
        scheduler.start()
    
    yield
    
    if scheduler.running:
        scheduler.shutdown()


app = FastAPI(
    title=settings.app_name,
    description="Low-activity investment service for MOEX",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(marketdata_router, prefix="/api/v1/marketdata", tags=["MarketData"])
app.include_router(portfolio_router, prefix="/api/v1/portfolio", tags=["Portfolio"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Rebalancer service is running", "version": "0.1.0"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
