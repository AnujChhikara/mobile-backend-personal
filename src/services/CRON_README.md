# Cron Jobs Configuration

This directory contains scheduled notification jobs that run at specific intervals.

## Current Active Cron Jobs

### 1. Daily Reminder
- **Schedule:** Every day at 9:00 AM
- **Cron Expression:** `0 9 * * *`
- **Action:** Sends a daily reminder notification to all users

### 2. Weekly Summary
- **Schedule:** Every Monday at 8:00 AM
- **Cron Expression:** `0 8 * * 1`
- **Action:** Sends a weekly summary notification to all users

## Cron Expression Format

```
* * * * *
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, where 0 and 7 are Sunday)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

### Common Examples

- `0 9 * * *` - Every day at 9:00 AM
- `0 8 * * 1` - Every Monday at 8:00 AM
- `*/5 * * * *` - Every 5 minutes
- `0 * * * *` - Every hour
- `0 0 * * *` - Every day at midnight
- `0 0 1 * *` - First day of every month at midnight
- `0 0 * * 0` - Every Sunday at midnight

## Adding New Cron Jobs

Edit `src/services/cronJobs.ts` and add a new cron schedule:

```typescript
import { sendNotificationToAll, sendNotificationToUser } from "./notificationService";

// Example: Send notification every hour
cron.schedule("0 * * * *", async () => {
  console.log("Running hourly notification...");
  const result = await sendNotificationToAll({
    title: "Hourly Update",
    body: "This is your hourly update!",
    priority: "normal",
  });
  console.log("Result:", result);
});

// Example: Send to specific user
cron.schedule("0 10 * * *", async () => {
  const result = await sendNotificationToUser("user123", {
    title: "Personal Reminder",
    body: "This is a personal reminder for you!",
    priority: "high",
  });
  console.log("Result:", result);
});
```

## Available Functions

### `sendNotificationToAll(payload)`
Sends a notification to all registered users.

**Parameters:**
- `payload.title` (string, required): Notification title
- `payload.body` (string, required): Notification message
- `payload.data` (object, optional): Additional data
- `payload.sound` ("default" | null, optional): Sound setting
- `payload.badge` (number, optional): Badge count
- `payload.priority` ("default" | "normal" | "high", optional): Priority level

**Returns:**
```typescript
{
  success: boolean;
  sentCount: number;
  message: string;
  error?: string;
}
```

### `sendNotificationToUser(user_id, payload)`
Sends a notification to a specific user.

**Parameters:**
- `user_id` (string, required): User ID
- `payload` (same as above)

**Returns:** Same as `sendNotificationToAll`

## Testing Cron Jobs

For testing, you can use shorter intervals (commented out in the file):

```typescript
// Every 5 minutes (for testing)
cron.schedule("*/5 * * * *", async () => {
  // Your notification code
});
```

**⚠️ Remember to comment out or remove test cron jobs before production!**

## Timezone

Cron jobs run in the server's local timezone. Make sure your server timezone is set correctly.

To check server timezone:
```bash
date
```

## Logging

All cron job executions are logged to the console. Check your server logs to monitor cron job execution and results.
