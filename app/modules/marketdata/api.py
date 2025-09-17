from typing import List

from fastapi import APIRouter, HTTPException, Depends

from app.modules.marketdata.service import MarketDataService
from app.modules.marketdata.schemas import Security, Quote
from app.storage import get_data_manager, DataManager

router = APIRouter()


def get_marketdata_service(data_manager: DataManager = Depends(get_data_manager)) -> MarketDataService:
    return MarketDataService(data_manager)


@router.get("/securities", response_model=List[Security])
async def get_securities(
    skip: int = 0,
    limit: int = 100,
    service: MarketDataService = Depends(get_marketdata_service)
):
    try:
        securities = await service.get_securities(skip=skip, limit=limit)
        return securities
    finally:
        await service.close()


@router.post("/securities/sync")
async def sync_securities(service: MarketDataService = Depends(get_marketdata_service)):
    try:
        count = await service.sync_securities_from_moex()
        return {"message": f"Synchronized {count} securities"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await service.close()


@router.get("/quotes/{secid}/latest", response_model=Quote)
async def get_latest_quote(
    secid: str,
    service: MarketDataService = Depends(get_marketdata_service)
):
    try:
        quote = await service.get_latest_quote(secid)
        if not quote:
            raise HTTPException(status_code=404, detail="Quote not found")
        return quote
    finally:
        await service.close()
