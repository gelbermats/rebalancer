from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

from app.modules.marketdata.service import MarketDataService
from app.storage import DataManager


def setup_scheduler(scheduler: AsyncIOScheduler):
    
    scheduler.add_job(
        daily_market_data_update,
        trigger=CronTrigger(day_of_week='mon-fri', hour=19, minute=0),
        id='daily_market_data_update',
        name='Daily Market Data Update',
        replace_existing=True
    )


async def daily_market_data_update():
    """Ежедневное обновление рыночных данных с MOEX."""
    from datetime import datetime, timedelta
    
    print(f'Starting daily market data update at {datetime.now()}')
    
    try:
        data_manager = DataManager()
        market_service = MarketDataService(data_manager)
        
        securities = await market_service.get_securities()
        
        if not securities:
            print('No securities found in local storage, loading from MOEX...')
            loaded_count = await market_service.sync_securities_from_moex()
            print(f'Loaded {loaded_count} securities from MOEX')
            securities = await market_service.get_securities()
        
        if not securities:
            print('Failed to load securities data')
            return
        
        security_codes = [sec.secid for sec in securities]
        print(f'Processing {len(security_codes)} securities...')
        
        historical_updated = 0
        
        for secid in security_codes:
            try:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30)
                
                history_count = await market_service.sync_quotes_for_security(
                    secid=secid,
                    from_date=start_date,
                    to_date=end_date
                )
                historical_updated += history_count
                print(f'Updated {history_count} historical quotes for {secid}')
                
            except Exception as e:
                print(f'Failed to update historical data for {secid}: {e}')
                continue
        
        print(f'Market data update completed successfully:')
        print(f'  - Historical quotes updated: {historical_updated}')
        print(f'  - Securities processed: {len(security_codes)}')
        
    except Exception as e:
        print(f'Market data update failed: {e}')
        import traceback
        traceback.print_exc()
    
    finally:
        try:
            await market_service.close()
        except:
            pass
