import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    app_name: str = 'Rebalancer'
    debug: bool = False
    
    database_url: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/rebalancer'
    
    moex_api_url: str = 'https://iss.moex.com'
    
    broker_api_url: Optional[str] = None
    broker_api_key: Optional[str] = None
    
    scheduler_enabled: bool = True
    
    model_config = {'env_file': '.env'}


settings = Settings()
