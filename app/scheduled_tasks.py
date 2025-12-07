"""
Standalone scheduled tasks script.
This can be run independently via system cron if you prefer that approach.

Usage with system cron:
    # Edit crontab: crontab -e
    # Add this line to run daily at 2:00 AM:
    0 2 * * * /usr/bin/python3 /path/to/app/scheduled_tasks.py
"""
import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import connect_to_database, close_database_connection
from app.scheduler import daily_cleanup_task, daily_notification_task, weekly_report_task
from app.config import get_settings


async def run_daily_cleanup():
    """Run the daily cleanup task."""
    settings = get_settings()
    print(f"🔌 Connecting to database ({settings.db_mode} mode)...")
    await connect_to_database()
    
    try:
        await daily_cleanup_task()
    finally:
        await close_database_connection()


async def run_daily_notification():
    """Run the daily notification task."""
    settings = get_settings()
    print(f"🔌 Connecting to database ({settings.db_mode} mode)...")
    await connect_to_database()
    
    try:
        await daily_notification_task()
    finally:
        await close_database_connection()


async def run_weekly_report():
    """Run the weekly report task."""
    settings = get_settings()
    print(f"🔌 Connecting to database ({settings.db_mode} mode)...")
    await connect_to_database()
    
    try:
        await weekly_report_task()
    finally:
        await close_database_connection()


if __name__ == "__main__":
    # Determine which task to run based on command line argument
    task_name = sys.argv[1] if len(sys.argv) > 1 else "cleanup"
    
    if task_name == "cleanup":
        asyncio.run(run_daily_cleanup())
    elif task_name == "notification":
        asyncio.run(run_daily_notification())
    elif task_name == "report":
        asyncio.run(run_weekly_report())
    else:
        print(f"❌ Unknown task: {task_name}")
        print("Available tasks: cleanup, notification, report")
        sys.exit(1)

