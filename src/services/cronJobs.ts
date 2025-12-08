import cron from "node-cron";
import { sendNotificationToAll } from "./notificationService";
// import { sendNotificationToUser } from "./notificationService"; // Uncomment when needed

export const cronTimeOptions = {
  hourly: "0 * * * *",
  everyMinute: "* * * * *",
  everyFiveMinutes: "*/5 * * * *",
  everyTenMinutes: "*/10 * * * *",
  everyThirtyMinutes: "*/30 * * * *",
  daily: "0 9 * * *",
  weekly: "0 9 * * 1",
};

cron.schedule("0 9 * * *", async () => {
  console.log("Running daily reminder cron job...");
  const result = await sendNotificationToAll({
    title: "Daily Reminder",
    body: "Don't forget to check your tasks for today!",
    priority: "normal",
  });
  console.log("Daily reminder result:", result);
});

export function startCronJobs(): void {
  console.log("✅ Cron jobs started");
}

export function stopCronJobs(): void {
  console.log("🛑 Cron jobs stopped");
}
