import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.monitoring import trigger_continuous_scan

logger = logging.getLogger("cloudguard.scheduler")

# Instantiate the Async scheduler
scheduler = AsyncIOScheduler()

def start_scheduler():
    # Keep your logging statement
    logger.info("Initializing CloudGuard continuous monitoring scheduler...")
    # Add a direct print statement so you can see it instantly in the terminal
    print("\n🚀 [CLOUTFUARD SCHEDULER] Background worker successfully initialized! 🚀\n")
    
    scheduler.add_job(
        trigger_continuous_scan,
        trigger=IntervalTrigger(hours=1),
        id="hourly_aws_security_scan",
        replace_existing=True
    )
    
    scheduler.start()
    print("✅ [CLOUDGUARD SCHEDULER] Hourly job active.")
    
    # --- ADD THIS LINE FOR TESTING ---
    # This schedules the scan to run exactly 1 second from now
    scheduler.add_job(trigger_continuous_scan, id="immediate_test_scan")
    
def shutdown_scheduler():
    logger.info("Shutting down security monitor scheduler...")
    scheduler.shutdown()
    