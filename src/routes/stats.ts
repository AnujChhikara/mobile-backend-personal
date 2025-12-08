import { getExpoTokensCollection } from "../models/expoToken";

function jsonResponse(data: unknown, status: number = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

type RouteParams = Record<string, string>;
type RouteHandler = (req: Request, params: RouteParams) => Promise<Response>;

export const statsRoutes: Record<string, RouteHandler> = {
  "GET /api/stats": async (_req: Request, _params: RouteParams) => {
    try {
      const collection = getExpoTokensCollection();
      const totalUsers = await collection.countDocuments({});
      const allTokens = await collection.find({}).toArray();

      return jsonResponse({
        totalUsers,
        totalTokens: allTokens.length,
        timestamp: new Date().toISOString(),
      });
    } catch (error) {
      console.error("Error fetching stats:", error);
      return jsonResponse({ error: "Failed to fetch stats" }, 500);
    }
  },
};
