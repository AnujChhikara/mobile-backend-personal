# Cron Job Setup Guide

This project supports scheduled tasks in two ways:

## Option 1: Built-in Scheduler (Recommended)

The FastAPI app includes APScheduler that runs tasks automatically when the server starts.

### Enable/Disable Scheduler:

You can control whether the scheduler runs using the `RUN_CRON` environment variable:

```env
# Enable scheduler (default)
RUN_CRON=true

# Disable scheduler
RUN_CRON=false
```

Add this to your `.env` file. When set to `false`, all scheduled tasks will be disabled and the scheduler won't start.

### Current Scheduled Tasks:

- **Daily Cleanup**: Every day at 2:00 AM
- **Daily Notification**: Every day at 9:00 AM
- **Weekly Report**: Every Monday at 8:00 AM

### Customizing Tasks:

Edit `app/scheduler.py` to modify existing tasks or add new ones.

### Changing Schedule:

In `app/scheduler.py`, modify the `CronTrigger` parameters:

```python
# Run every day at 3:00 PM
scheduler.add_job(
    your_task,
    trigger=CronTrigger(hour=15, minute=0),
    id="your_task_id",
    name="Your Task Name",
    replace_existing=True,
)
```

### Cron Expression Examples:

- `CronTrigger(hour=2, minute=0)` - Every day at 2:00 AM
- `CronTrigger(hour=9, minute=30)` - Every day at 9:30 AM
- `CronTrigger(day_of_week="mon", hour=8, minute=0)` - Every Monday at 8:00 AM
- `CronTrigger(day=1, hour=0, minute=0)` - First day of every month at midnight
- `CronTrigger(hour="*/6")` - Every 6 hours
- `CronTrigger(minute="*/30")` - Every 30 minutes

---

## Option 2: System Cron (Alternative)

If you prefer using system cron instead of the built-in scheduler:

### 1. Make the script executable:

```bash
chmod +x app/scheduled_tasks.py
```

### 2. Edit crontab:

```bash
crontab -e
```

### 3. Add cron jobs:

```bash
# Daily cleanup at 2:00 AM
0 2 * * * cd /path/to/mobile-backend-personal && /usr/bin/python3 app/scheduled_tasks.py cleanup >> logs/cron.log 2>&1

# Daily notification at 9:00 AM
0 9 * * * cd /path/to/mobile-backend-personal && /usr/bin/python3 app/scheduled_tasks.py notification >> logs/cron.log 2>&1

# Weekly report every Monday at 8:00 AM
0 8 * * 1 cd /path/to/mobile-backend-personal && /usr/bin/python3 app/scheduled_tasks.py report >> logs/cron.log 2>&1
```

### 4. Find Python path:

```bash
which python3
# or
which python
```

### Cron Format:

```
* * * * *
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, where 0 and 7 = Sunday)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

---

## Adding New Scheduled Tasks

### Method 1: Add to Built-in Scheduler

1. Create your task function in `app/scheduler.py`:

```python
async def my_custom_task():
    """My custom task description."""
    try:
        logger.info("🔄 Running my custom task...")
        # Your task logic here
        logger.info("✅ Task completed")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
```

2. Register it in `setup_scheduler()`:

```python
scheduler.add_job(
    my_custom_task,
    trigger=CronTrigger(hour=14, minute=0),  # 2:00 PM daily
    id="my_custom_task",
    name="My Custom Task",
    replace_existing=True,
)
```

### Method 2: Add to Standalone Script

1. Add your task function to `app/scheduled_tasks.py`
2. Add a new command-line option in the `if __name__ == "__main__"` block
3. Add a cron entry if using system cron

---

## Testing Scheduled Tasks

### Test Built-in Scheduler:

The tasks will run automatically when the FastAPI server starts. Check logs to see execution.

### Test Standalone Script:

```bash
# Test cleanup task
python3 app/scheduled_tasks.py cleanup

# Test notification task
python3 app/scheduled_tasks.py notification

# Test report task
python3 app/scheduled_tasks.py report
```

---

## Logging

Scheduled tasks log to the console. For production, consider:

- Setting up proper logging configuration
- Writing logs to files
- Using a logging service

Example logging setup in `app/scheduler.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scheduler.log'),
        logging.StreamHandler()
    ]
)
```

---

## Notes

- The built-in scheduler runs as long as the FastAPI server is running
- System cron is independent of the server and runs even if the server is down
- Choose the method that best fits your deployment strategy
- For Docker deployments, the built-in scheduler is usually easier to manage

