import { Expo } from "expo-server-sdk";
import { getExpoTokensCollection } from "../models/expoToken";

const expo = new Expo();

interface NotificationRequest {
  title: string;
  body: string;
  data?: Record<string, unknown>;
  sound?: "default" | null;
  badge?: number;
  priority?: "default" | "normal" | "high";
  user_id?: string;
  expo_token?: string;
}

interface BatchNotificationRequest {
  notifications: Array<{
    title: string;
    body: string;
    data?: Record<string, unknown>;
    sound?: "default" | null;
    badge?: number;
    priority?: "default" | "normal" | "high";
  }>;
}

async function parseJsonBody(request: Request): Promise<NotificationRequest | null> {
  try {
    return (await request.json()) as NotificationRequest;
  } catch {
    return null;
  }
}

async function parseBatchJsonBody(request: Request): Promise<BatchNotificationRequest | null> {
  try {
    return (await request.json()) as BatchNotificationRequest;
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

type RouteParams = Record<string, string>;
type RouteHandler = (req: Request, params: RouteParams) => Promise<Response>;

export const notificationRoutes: Record<string, RouteHandler> = {
  "POST /api/notifications/send": async (req: Request, _params: RouteParams) => {
    const body = await parseJsonBody(req);
    if (!body || !body.title || !body.body) {
      return errorResponse("title and body are required", 400);
    }

    const collection = getExpoTokensCollection();
    let tokens: string[] = [];

    if (body.expo_token) {
      if (!Expo.isExpoPushToken(body.expo_token)) {
        return errorResponse("Invalid Expo push token format", 400);
      }
      tokens = [body.expo_token];
    } else if (body.user_id) {
      const tokenDoc = await collection.findOne({ user_id: body.user_id });
      if (!tokenDoc) {
        return errorResponse(`No expo token found for user_id: ${body.user_id}`, 404);
      }
      if (!Expo.isExpoPushToken(tokenDoc.expo_token)) {
        return errorResponse("Invalid Expo push token format", 400);
      }
      tokens = [tokenDoc.expo_token];
    } else {
      const allTokens = await collection.find({}).toArray();
      tokens = allTokens
        .map((t) => t.expo_token)
        .filter((token): token is string => Expo.isExpoPushToken(token));
    }

    if (tokens.length === 0) {
      return errorResponse("No valid Expo push tokens found", 404);
    }

    const messages = tokens.map((token) => ({
      to: token,
      sound: body.sound ?? "default",
      title: body.title,
      body: body.body,
      data: body.data ?? {},
      badge: body.badge,
      priority: body.priority ?? "default",
    }));

    const chunks = expo.chunkPushNotifications(messages);
    const tickets = [];

    for (const chunk of chunks) {
      try {
        const ticketChunk = await expo.sendPushNotificationsAsync(chunk);
        tickets.push(...ticketChunk);
      } catch (error) {
        console.error("Error sending push notification:", error);
        return errorResponse("Failed to send push notifications", 500);
      }
    }

    const results = {
      success: true,
      tickets,
      sentCount: tickets.length,
      message: `Sent ${tickets.length} notification(s)`,
    };

    return jsonResponse(results, 200);
  },

  "POST /api/notifications/send-batch": async (req: Request, _params: RouteParams) => {
    const body = await parseBatchJsonBody(req);
    if (!body || !Array.isArray(body.notifications)) {
      return errorResponse("notifications array is required", 400);
    }

    const collection = getExpoTokensCollection();
    const allTokens = await collection.find({}).toArray();
    const validTokens = allTokens
      .map((t) => t.expo_token)
      .filter((token): token is string => Expo.isExpoPushToken(token));

    if (validTokens.length === 0) {
      return errorResponse("No valid Expo push tokens found", 404);
    }

    const messages: Array<{
      to: string;
      sound: "default" | null;
      title: string;
      body: string;
      data?: Record<string, unknown>;
      badge?: number;
      priority?: "default" | "normal" | "high";
    }> = [];

    for (const notification of body.notifications) {
      if (!notification.title || !notification.body) {
        continue;
      }

      for (const token of validTokens) {
        messages.push({
          to: token,
          sound: notification.sound ?? "default",
          title: notification.title,
          body: notification.body,
          data: notification.data ?? {},
          badge: notification.badge,
          priority: notification.priority ?? "default",
        });
      }
    }

    if (messages.length === 0) {
      return errorResponse("No valid notifications to send", 400);
    }

    const chunks = expo.chunkPushNotifications(messages);
    const tickets = [];

    for (const chunk of chunks) {
      try {
        const ticketChunk = await expo.sendPushNotificationsAsync(chunk);
        tickets.push(...ticketChunk);
      } catch (error) {
        console.error("Error sending push notification:", error);
        return errorResponse("Failed to send push notifications", 500);
      }
    }

    const results = {
      success: true,
      tickets,
      sentCount: tickets.length,
      message: `Sent ${tickets.length} notification(s)`,
    };

    return jsonResponse(results, 200);
  },
};
