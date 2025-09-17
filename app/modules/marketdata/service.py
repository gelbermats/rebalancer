from typing import List, Optional
from datetime import datetime

import httpx

from app.config import settings
from app.modules.marketdata.models import Security, Quote
from app.storage import DataManager
from app.modules.marketdata.schemas import SecurityCreate, QuoteCreate


class MOEXAdapter:
    
    def __init__(self):
        self.base_url = settings.moex_api_url
        self.client = httpx.AsyncClient()
    
    async def get_securities(self, engine: str = "stock", market: str = "shares") -> List[dict]:
        url = f"{self.base_url}/iss/engines/{engine}/markets/{market}/securities.json"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            
            if "securities" in data and "data" in data["securities"]:
                return data["securities"]["data"]
            return []
        except Exception as e:
            print(f"Error fetching securities: {e}")
            return []
    
    async def get_quotes(self, secid: str, from_date: Optional[datetime] = None) -> List[dict]:
        url = f"{self.base_url}/iss/engines/stock/markets/shares/securities/{secid}/candles.json"
        params = {"interval": "1", "iss.meta": "off"}
        
        if from_date:
            params["from"] = from_date.strftime("%Y-%m-%d")
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "candles" in data and "data" in data["candles"]:
                return data["candles"]["data"]
            return []
        except Exception as e:
            print(f"Error fetching quotes for {secid}: {e}")
            return []
    
    async def close(self):
        await self.client.aclose()


class MarketDataService:

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.moex_adapter = MOEXAdapter()
    
    async def get_securities(self, skip: int = 0, limit: int = 100) -> List[Security]:
        securities = self.data_manager.get_all_securities()
        return securities[skip:skip + limit]
    
    async def create_security(self, security_data: SecurityCreate) -> Security:
        security = Security(
            secid=security_data.secid,
            name=security_data.name,
            isin=security_data.isin,
            engine=security_data.engine,
            market=security_data.market,
            board=security_data.board
        )
        self.data_manager.add_security(security)
        return security
    
    async def sync_securities_from_moex(self) -> int:
        securities_data = await self.moex_adapter.get_securities()
        count = 0
        
        for sec_data in securities_data:
            if len(sec_data) >= 2:
                secid, name = sec_data[0], sec_data[1]
                
                if not self.data_manager.security_exists(secid):
                    security = Security(secid=secid, name=name)
                    self.data_manager.add_security(security)
                    count += 1
        
        return count
    
    async def get_latest_quote(self, secid: str) -> Optional[Quote]:
        return self.data_manager.get_latest_quote(secid)
    
    async def close(self):
        await self.moex_adapter.close()
