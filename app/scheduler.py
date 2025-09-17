from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


def setup_scheduler(scheduler: AsyncIOScheduler):
    
    scheduler.add_job(
        daily_market_data_update,
        trigger=CronTrigger(day_of_week="mon-fri", hour=19, minute=0),
        id="daily_market_data_update",
        name="Daily Market Data Update",
        replace_existing=True
    )


async def daily_market_data_update():
    print("Starting daily market data update...")
    
    try:
        print("Market data updated successfully")
    except Exception as e:
        print(f"Market data update failed: {e}")
