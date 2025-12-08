import { Expo } from "expo-server-sdk";
import { getExpoTokensCollection } from "../models/expoToken";

const expo = new Expo();

interface NotificationPayload {
  title: string;
  body: string;
  data?: Record<string, unknown>;
  sound?: "default" | null;
  badge?: number;
  priority?: "default" | "normal" | "high";
  user_id?: string;
  expo_token?: string;
}

export async function sendNotificationToAll(payload: NotificationPayload): Promise<{
  success: boolean;
  sentCount: number;
  message: string;
  error?: string;
}> {
  try {
    const collection = getExpoTokensCollection();
    const allTokens = await collection.find({}).toArray();
    const validTokens = allTokens
      .map((t) => t.expo_token)
      .filter((token): token is string => Expo.isExpoPushToken(token));

    if (validTokens.length === 0) {
      return {
        success: false,
        sentCount: 0,
        message: "No valid Expo push tokens found",
        error: "No valid tokens",
      };
    }

    const messages = validTokens.map((token) => ({
      to: token,
      sound: payload.sound ?? "default",
      title: payload.title,
      body: payload.body,
      data: payload.data ?? {},
      badge: payload.badge,
      priority: payload.priority ?? "default",
    }));

    const chunks = expo.chunkPushNotifications(messages);
    const tickets = [];

    for (const chunk of chunks) {
      try {
        const ticketChunk = await expo.sendPushNotificationsAsync(chunk);
        tickets.push(...ticketChunk);
      } catch (error) {
        console.error("Error sending push notification:", error);
        return {
          success: false,
          sentCount: 0,
          message: "Failed to send push notifications",
          error: error instanceof Error ? error.message : "Unknown error",
        };
      }
    }

    return {
      success: true,
      sentCount: tickets.length,
      message: `Sent ${tickets.length} notification(s)`,
    };
  } catch (error) {
    console.error("Error in sendNotificationToAll:", error);
    return {
      success: false,
      sentCount: 0,
      message: "Failed to send notifications",
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}

export async function sendNotificationToUser(
  user_id: string,
  payload: NotificationPayload
): Promise<{
  success: boolean;
  sentCount: number;
  message: string;
  error?: string;
}> {
  try {
    const collection = getExpoTokensCollection();
    const tokenDoc = await collection.findOne({ user_id });

    if (!tokenDoc) {
      return {
        success: false,
        sentCount: 0,
        message: `No expo token found for user_id: ${user_id}`,
        error: "Token not found",
      };
    }

    if (!Expo.isExpoPushToken(tokenDoc.expo_token)) {
      return {
        success: false,
        sentCount: 0,
        message: "Invalid Expo push token format",
        error: "Invalid token",
      };
    }

    const messages = [
      {
        to: tokenDoc.expo_token,
        sound: payload.sound ?? "default",
        title: payload.title,
        body: payload.body,
        data: payload.data ?? {},
        badge: payload.badge,
        priority: payload.priority ?? "default",
      },
    ];

    const chunks = expo.chunkPushNotifications(messages);
    const tickets = [];

    for (const chunk of chunks) {
      try {
        const ticketChunk = await expo.sendPushNotificationsAsync(chunk);
        tickets.push(...ticketChunk);
      } catch (error) {
        console.error("Error sending push notification:", error);
        return {
          success: false,
          sentCount: 0,
          message: "Failed to send push notification",
          error: error instanceof Error ? error.message : "Unknown error",
        };
      }
    }

    return {
      success: true,
      sentCount: tickets.length,
      message: `Sent ${tickets.length} notification(s)`,
    };
  } catch (error) {
    console.error("Error in sendNotificationToUser:", error);
    return {
      success: false,
      sentCount: 0,
      message: "Failed to send notification",
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}
