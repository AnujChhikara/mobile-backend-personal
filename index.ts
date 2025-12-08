import { connectToDatabase, closeDatabaseConnection } from "./src/db/connection";
import { expoTokensRoutes } from "./src/routes/expoTokens";
import { notificationRoutes } from "./src/routes/notifications";
import { statsRoutes } from "./src/routes/stats";
import { startCronJobs, stopCronJobs } from "./src/services/cronJobs";
import { readFileSync } from "fs";
import { join } from "path";

await connectToDatabase();
startCronJobs();

const port = parseInt(process.env.PORT || "8000", 10);

const server = Bun.serve({
  port,
  async fetch(req) {
    const url = new URL(req.url);
    const pathname = url.pathname;
    const method = req.method;

    if (method === "GET" && pathname === "/health") {
      return new Response(JSON.stringify({ status: "ok", timestamp: new Date().toISOString() }), {
        headers: { "Content-Type": "application/json" },
      });
    }

    // Dashboard route
    if (method === "GET" && pathname === "/dashboard") {
      try {
        const dashboardPath = join(import.meta.dirname, "dashboard.html");
        const dashboardHtml = readFileSync(dashboardPath, "utf-8");
        return new Response(dashboardHtml, {
          headers: { "Content-Type": "text/html" },
        });
      } catch (error) {
        console.error("Error reading dashboard file:", error);
        return new Response("Dashboard not found", { status: 404 });
      }
    }

    // Stats routes
    for (const [route, handler] of Object.entries(statsRoutes)) {
      const parts = route.split(" ");
      if (parts.length !== 2) continue;

      const [routeMethod, path] = parts;

      if (method !== routeMethod || !path) continue;

      if (path === pathname) {
        try {
          return await handler(req, {});
        } catch (error) {
          console.error("Error handling request:", error);
          return new Response(JSON.stringify({ error: "Internal server error" }), {
            status: 500,
            headers: { "Content-Type": "application/json" },
          });
        }
      }
    }

    // Notification routes
    for (const [route, handler] of Object.entries(notificationRoutes)) {
      const parts = route.split(" ");
      if (parts.length !== 2) continue;

      const [routeMethod, path] = parts;

      if (method !== routeMethod || !path) continue;

      if (path === pathname) {
        try {
          return await handler(req, {});
        } catch (error) {
          console.error("Error handling request:", error);
          return new Response(JSON.stringify({ error: "Internal server error" }), {
            status: 500,
            headers: { "Content-Type": "application/json" },
          });
        }
      }

      const routePattern = path.replace(/:[^/]+/g, "([^/]+)");
      const regex = new RegExp(`^${routePattern}$`);
      const match = pathname.match(regex);

      if (match) {
        const paramNames = path.match(/:[^/]+/g) || [];
        const params: Record<string, string> = {};

        paramNames.forEach((param, index) => {
          const paramName = param.slice(1);
          const paramValue = match[index + 1];
          if (paramValue) {
            params[paramName] = paramValue;
          }
        });

        try {
          return await handler(req, params);
        } catch (error) {
          console.error("Error handling request:", error);
          return new Response(JSON.stringify({ error: "Internal server error" }), {
            status: 500,
            headers: { "Content-Type": "application/json" },
          });
        }
      }
    }

    for (const [route, handler] of Object.entries(expoTokensRoutes)) {
      const parts = route.split(" ");
      if (parts.length !== 2) continue;

      const [routeMethod, path] = parts;

      if (method !== routeMethod || !path) continue;

      if (path === pathname) {
        try {
          return await handler(req, {});
        } catch (error) {
          console.error("Error handling request:", error);
          return new Response(JSON.stringify({ error: "Internal server error" }), {
            status: 500,
            headers: { "Content-Type": "application/json" },
          });
        }
      }

      const routePattern = path.replace(/:[^/]+/g, "([^/]+)");
      const regex = new RegExp(`^${routePattern}$`);
      const match = pathname.match(regex);

      if (match) {
        const paramNames = path.match(/:[^/]+/g) || [];
        const params: Record<string, string> = {};

        paramNames.forEach((param, index) => {
          const paramName = param.slice(1);
          const paramValue = match[index + 1];
          if (paramValue) {
            params[paramName] = paramValue;
          }
        });

        try {
          return await handler(req, params);
        } catch (error) {
          console.error("Error handling request:", error);
          return new Response(JSON.stringify({ error: "Internal server error" }), {
            status: 500,
            headers: { "Content-Type": "application/json" },
          });
        }
      }
    }

    return new Response(JSON.stringify({ error: "Not found" }), {
      status: 404,
      headers: { "Content-Type": "application/json" },
    });
  },
});

const serverUrl = server.url.toString();
console.log(`Server listening on ${serverUrl}`);

process.on("SIGINT", () => {
  console.log("\nShutting down server...");
  stopCronJobs();
  void closeDatabaseConnection().then(() => {
    process.exit(0);
  });
});

process.on("SIGTERM", () => {
  console.log("\nShutting down server...");
  stopCronJobs();
  void closeDatabaseConnection().then(() => {
    process.exit(0);
  });
});
