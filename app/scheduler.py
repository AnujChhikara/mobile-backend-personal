"""
Scheduler module for running periodic tasks.
Uses APScheduler to manage cron jobs and scheduled tasks.
"""

import logging
from datetime import datetime

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from app.database import get_expo_tokens_collection

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = AsyncIOScheduler()


async def daily_cleanup_task():
    """
    Example daily task: Clean up old or invalid tokens.
    Runs every day at 2:00 AM.
    """
    try:
        logger.info("🧹 Starting daily cleanup task...")
        collection = get_expo_tokens_collection()

        # Example: Count total tokens
        total_count = await collection.count_documents({})
        logger.info(f"📊 Total registered tokens: {total_count}")

        # Example: Find tokens older than 90 days (optional cleanup)
        # from datetime import timedelta
        # cutoff_date = datetime.utcnow() - timedelta(days=90)
        # old_tokens = await collection.count_documents({
        #     "created_at": {"$lt": cutoff_date}
        # })
        # logger.info(f"🗑️ Found {old_tokens} tokens older than 90 days")

        logger.info("✅ Daily cleanup task completed")
    except Exception as e:
        logger.error(f"❌ Error in daily cleanup task: {e}")


async def daily_notification_task():
    """
    Example daily task: Send daily notifications to all users.
    Runs every day at 9:00 AM.
    """
    try:
        logger.info("📬 Starting daily notification task...")
        collection = get_expo_tokens_collection()

        # Get all active tokens
        tokens = await collection.find({}).to_list(length=None)
        token_count = len(tokens)

        if token_count > 0:
            logger.info(f"📱 Found {token_count} registered tokens")
            # Here you could send a daily notification
            # from app.routers.notifications import send_notification_to_all
            # await send_notification_to_all(
            #     title="Daily Update",
            #     body="Good morning! Here's your daily update."
            # )
            logger.info("✅ Daily notification task completed")
        else:
            logger.info("ℹ️ No tokens to send notifications to")
    except Exception as e:
        logger.error(f"❌ Error in daily notification task: {e}")


async def weekly_report_task():
    """
    Example weekly task: Generate weekly statistics report.
    Runs every Monday at 8:00 AM.
    """
    try:
        logger.info("📊 Starting weekly report task...")
        collection = get_expo_tokens_collection()

        # Get statistics
        total_users = await collection.count_documents({})

        # Get unique device types
        pipeline = [
            {"$group": {"_id": "$device_type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ]
        device_stats = await collection.aggregate(pipeline).to_list(length=None)

        logger.info("📈 Weekly Report:")
        logger.info(f"   Total Users: {total_users}")
        logger.info(f"   Device Types: {device_stats}")

        logger.info("✅ Weekly report task completed")
    except Exception as e:
        logger.error(f"❌ Error in weekly report task: {e}")


async def test_notification_task():
    """
    TEST TASK: Send notification every 20 seconds for testing purposes.
    This will send a test notification to all registered users.
    """
    try:
        logger.info("🧪 [TEST] Starting test notification task (every 20 seconds)...")
        collection = get_expo_tokens_collection()

        # Get all tokens
        tokens = []
        async for token_doc in collection.find():
            tokens.append(token_doc)

        if not tokens:
            logger.info("ℹ️ [TEST] No tokens found - skipping notification")
            return

        logger.info(f"📱 [TEST] Sending test notification to {len(tokens)} user(s)...")

        # Send notification to each token
        EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"
        sent = 0
        failed = 0

        for token_doc in tokens:
            try:
                message = {
                    "to": token_doc["expo_token"],
                    "sound": "default",
                    "title": "🧪 Test Notification",
                    "body": f"Test notification sent at {datetime.now().strftime('%H:%M:%S')}",
                    "data": {"type": "test", "timestamp": datetime.now().isoformat()},
                }

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        EXPO_PUSH_URL,
                        json=message,
                        headers={
                            "Accept": "application/json",
                            "Content-Type": "application/json",
                        },
                    )
                    result = response.json()

                    if "data" in result and result["data"].get("status") == "ok":
                        logger.info(f"✅ [TEST] Sent to user: {token_doc['user_id']}")
                        sent += 1
                    else:
                        error_msg = result.get("data", {}).get("message", "Unknown error")
                        logger.warning(
                            f"⚠️ [TEST] Failed for user {token_doc['user_id']}: {error_msg}"
                        )
                        failed += 1

            except Exception as e:
                logger.error(f"❌ [TEST] Error sending to user {token_doc['user_id']}: {e}")
                failed += 1

        logger.info(f"✅ [TEST] Test notification task completed - Sent: {sent}, Failed: {failed}")

    except Exception as e:
        logger.error(f"❌ [TEST] Error in test notification task: {e}")


def setup_scheduler():
    """
    Configure and start the scheduler with all scheduled tasks.
    """
    # TEST: Send notification every 20 seconds (for testing)
    scheduler.add_job(
        test_notification_task,
        trigger=IntervalTrigger(seconds=20),
        id="test_notification",
        name="Test Notification (Every 20 seconds)",
        replace_existing=True,
    )

    # Daily cleanup at 2:00 AM
    scheduler.add_job(
        daily_cleanup_task,
        trigger=CronTrigger(hour=2, minute=0),
        id="daily_cleanup",
        name="Daily Cleanup Task",
        replace_existing=True,
    )

    # Daily notification at 9:00 AM
    scheduler.add_job(
        daily_notification_task,
        trigger=CronTrigger(hour=9, minute=0),
        id="daily_notification",
        name="Daily Notification Task",
        replace_existing=True,
    )

    # Weekly report every Monday at 8:00 AM
    scheduler.add_job(
        weekly_report_task,
        trigger=CronTrigger(day_of_week="mon", hour=8, minute=0),
        id="weekly_report",
        name="Weekly Report Task",
        replace_existing=True,
    )

    logger.info("⏰ Scheduler configured with scheduled tasks:")
    logger.info("   - TEST Notification: Every 20 seconds ⚠️ (FOR TESTING)")
    logger.info("   - Daily Cleanup: Every day at 2:00 AM")
    logger.info("   - Daily Notification: Every day at 9:00 AM")
    logger.info("   - Weekly Report: Every Monday at 8:00 AM")


def start_scheduler():
    """Start the scheduler."""
    if not scheduler.running:
        scheduler.start()
        logger.info("🚀 Scheduler started")


def shutdown_scheduler():
    """Shutdown the scheduler gracefully."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("🛑 Scheduler stopped")
