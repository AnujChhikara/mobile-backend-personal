import {
  connectToDatabase,
  closeDatabaseConnection,
} from "./src/db/connection";
import { expoTokensRoutes } from "./src/routes/expoTokens";

await connectToDatabase();

const port = parseInt(process.env.PORT || "8000", 10);

const server = Bun.serve({
  port,
  async fetch(req) {
    const url = new URL(req.url);
    const pathname = url.pathname;
    const method = req.method;

    if (method === "GET" && pathname === "/health") {
      return new Response(
        JSON.stringify({ status: "ok", timestamp: new Date().toISOString() }),
        {
          headers: { "Content-Type": "application/json" },
        }
      );
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
          return new Response(
            JSON.stringify({ error: "Internal server error" }),
            {
              status: 500,
              headers: { "Content-Type": "application/json" },
            }
          );
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
          return new Response(
            JSON.stringify({ error: "Internal server error" }),
            {
              status: 500,
              headers: { "Content-Type": "application/json" },
            }
          );
        }
      }
    }

    return new Response(JSON.stringify({ error: "Not found" }), {
      status: 404,
      headers: { "Content-Type": "application/json" },
    });
  },
});

console.log(`Server listening on ${server.url}`);

process.on("SIGINT", async () => {
  console.log("\nShutting down server...");
  await closeDatabaseConnection();
  process.exit(0);
});

process.on("SIGTERM", async () => {
  console.log("\nShutting down server...");
  await closeDatabaseConnection();
  process.exit(0);
});
