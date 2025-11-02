from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from datetime import datetime, timedelta

from app.config import settings
from app.database import SessionLocal
from app.services.activity_service import ActivityService

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

async def sync_activities_job():
    """Scheduled job to sync activities from Intervals.icu"""
    try:
        logger.info("Starting scheduled activity sync...")
        
        db = SessionLocal()
        try:
            activity_service = ActivityService(db)
            
            # Sync activities from the last week
            oldest_date = datetime.now().date() - timedelta(days=7)
            
            result = await activity_service.sync_from_intervals_icu(
                oldest=oldest_date,
                limit=200
            )
            
            logger.info(f"Scheduled sync completed: {result}")
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error in scheduled activity sync: {e}")

def start_scheduler():
    """Start the background scheduler"""
    if not settings.INTERVALS_ICU_API_KEY:
        logger.warning(f"No Intervals.icu API key configured (key: '{settings.INTERVALS_ICU_API_KEY}'), skipping scheduler start")
        return
    
    # Add the sync job
    scheduler.add_job(
        sync_activities_job,
        trigger=IntervalTrigger(minutes=settings.FETCH_INTERVAL_MINUTES),
        id="sync_activities",
        name="Sync activities from Intervals.icu",
        replace_existing=True
    )
    
    logger.info(f"Scheduler started with {settings.FETCH_INTERVAL_MINUTES} minute intervals")
    scheduler.start()

def stop_scheduler():
    """Stop the background scheduler"""
    scheduler.shutdown()
    logger.info("Scheduler stopped")