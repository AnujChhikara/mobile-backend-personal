import { getExpoTokensCollection } from "../models/expoToken";
import type { ExpoToken } from "../models/expoToken";
import { ObjectId } from "mongodb";

type RouteParams = Record<string, string>;

interface RequestBody {
  user_id?: string;
  expo_token?: string;
}

async function parseJsonBody(request: Request): Promise<RequestBody | null> {
  try {
    return (await request.json()) as RequestBody;
  } catch {
    return null;
  }
}

function jsonResponse(data: unknown, status: number = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function errorResponse(message: string, status: number = 400): Response {
  return jsonResponse({ error: message }, status);
}

type RouteHandler = (req: Request, params: RouteParams) => Promise<Response>;

export const expoTokensRoutes: Record<string, RouteHandler> = {
  "POST /api/expo-tokens": async (req: Request, _params: RouteParams) => {
    const body = await parseJsonBody(req);
    if (!body || !body.user_id || !body.expo_token) {
      return errorResponse("user_id and expo_token are required", 400);
    }

    const collection = getExpoTokensCollection();
    const now = new Date();

    const result = await collection.findOneAndUpdate(
      { user_id: body.user_id },
      {
        $set: {
          expo_token: body.expo_token,
          updated_at: now,
        },
        $setOnInsert: {
          created_at: now,
        },
      },
      { upsert: true, returnDocument: "after" }
    );

    return jsonResponse(result, 201);
  },

  "GET /api/expo-tokens": async (_req: Request, _params: RouteParams) => {
    const collection = getExpoTokensCollection();
    const tokens = await collection.find({}).toArray();
    return jsonResponse(tokens);
  },

  "GET /api/expo-tokens/:id": async (req: Request, params: RouteParams) => {
    const id = params.id;
    if (!id) {
      return errorResponse("ID parameter is required", 400);
    }
    if (!ObjectId.isValid(id)) {
      return errorResponse("Invalid ID format", 400);
    }

    const collection = getExpoTokensCollection();
    const token = await collection.findOne({ _id: new ObjectId(id) });

    if (!token) {
      return errorResponse("Expo token not found", 404);
    }

    return jsonResponse(token);
  },

  "GET /api/expo-tokens/user/:user_id": async (req: Request, params: RouteParams) => {
    const user_id = params.user_id;
    if (!user_id) {
      return errorResponse("user_id parameter is required", 400);
    }
    const collection = getExpoTokensCollection();
    const token = await collection.findOne({ user_id });

    if (!token) {
      return errorResponse("Expo token not found for user", 404);
    }

    return jsonResponse(token);
  },

  "PUT /api/expo-tokens/:id": async (req: Request, params: RouteParams) => {
    const id = params.id;
    if (!id) {
      return errorResponse("ID parameter is required", 400);
    }
    if (!ObjectId.isValid(id)) {
      return errorResponse("Invalid ID format", 400);
    }

    const body = await parseJsonBody(req);
    if (!body || (!body.expo_token && !body.user_id)) {
      return errorResponse("At least one field (expo_token or user_id) is required", 400);
    }

    const collection = getExpoTokensCollection();
    const updateData: Partial<ExpoToken> = {
      updated_at: new Date(),
    };

    if (body.expo_token) {
      updateData.expo_token = body.expo_token;
    }
    if (body.user_id) {
      updateData.user_id = body.user_id;
    }

    const result = await collection.findOneAndUpdate(
      { _id: new ObjectId(id) },
      { $set: updateData },
      { returnDocument: "after" }
    );

    if (!result) {
      return errorResponse("Expo token not found", 404);
    }

    return jsonResponse(result);
  },

  // DELETE /api/expo-tokens/:id - Delete expo token by ID
  "DELETE /api/expo-tokens/:id": async (req: Request, params: RouteParams) => {
    const id = params.id;
    if (!id) {
      return errorResponse("ID parameter is required", 400);
    }
    if (!ObjectId.isValid(id)) {
      return errorResponse("Invalid ID format", 400);
    }

    const collection = getExpoTokensCollection();
    const result = await collection.findOneAndDelete({
      _id: new ObjectId(id),
    });

    if (!result) {
      return errorResponse("Expo token not found", 404);
    }

    return jsonResponse({ message: "Expo token deleted successfully" });
  },

  // DELETE /api/expo-tokens/user/:user_id - Delete expo token by user
  "DELETE /api/expo-tokens/user/:user_id": async (req: Request, params: RouteParams) => {
    const user_id = params.user_id;
    if (!user_id) {
      return errorResponse("user_id parameter is required", 400);
    }
    const collection = getExpoTokensCollection();
    const result = await collection.findOneAndDelete({
      user_id,
    });

    if (!result) {
      return errorResponse("Expo token not found for user", 404);
    }

    return jsonResponse({ message: "Expo token deleted successfully" });
  },
};
