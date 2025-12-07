from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.database import get_expo_tokens_collection

router = APIRouter(prefix="/notifications", tags=["Notifications"])

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"


class NotificationRequest(BaseModel):
    """Request model for sending notifications."""

    title: str = Field(default="Test Notification", description="Notification title")
    body: str = Field(default="This is a test notification!", description="Notification body")
    data: Optional[dict] = Field(default=None, description="Additional data payload")


class NotificationResult(BaseModel):
    """Result of a single notification send."""

    user_id: str
    expo_token: str
    status: str
    message: Optional[str] = None


class NotificationResponse(BaseModel):
    """Response model for notification sending."""

    success: bool
    total_tokens: int
    sent: int
    failed: int
    results: list[NotificationResult]


async def send_expo_notification(
    expo_token: str, title: str, body: str, data: Optional[dict] = None
) -> dict:
    """Send a single notification via Expo Push API."""
    message = {
        "to": expo_token,
        "sound": "default",
        "title": title,
        "body": body,
    }

    if data:
        message["data"] = data

    async with httpx.AsyncClient() as client:
        response = await client.post(
            EXPO_PUSH_URL,
            json=message,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        return response.json()


@router.post("/send-all", response_model=NotificationResponse)
async def send_notification_to_all(notification: Optional[NotificationRequest] = None):
    """
    Send a push notification to ALL registered expo tokens.

    Default message is a test notification if no body is provided.
    """
    if notification is None:
        notification = NotificationRequest()
    collection = get_expo_tokens_collection()

    tokens = []
    async for token_doc in collection.find():
        tokens.append(token_doc)

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No expo tokens found in database"
        )

    results = []
    sent_count = 0
    failed_count = 0

    for token_doc in tokens:
        try:
            response = await send_expo_notification(
                expo_token=token_doc["expo_token"],
                title=notification.title,
                body=notification.body,
                data=notification.data,
            )

            # Check Expo response
            if "data" in response and response["data"].get("status") == "ok":
                results.append(
                    NotificationResult(
                        user_id=token_doc["user_id"],
                        expo_token=token_doc["expo_token"],
                        status="sent",
                        message="Notification sent successfully",
                    )
                )
                sent_count += 1
            else:
                error_msg = response.get("data", {}).get("message", "Unknown error")
                results.append(
                    NotificationResult(
                        user_id=token_doc["user_id"],
                        expo_token=token_doc["expo_token"],
                        status="failed",
                        message=error_msg,
                    )
                )
                failed_count += 1

        except Exception as e:
            results.append(
                NotificationResult(
                    user_id=token_doc["user_id"],
                    expo_token=token_doc["expo_token"],
                    status="error",
                    message=str(e),
                )
            )
            failed_count += 1

    return NotificationResponse(
        success=failed_count == 0,
        total_tokens=len(tokens),
        sent=sent_count,
        failed=failed_count,
        results=results,
    )


@router.post("/send-test", response_model=dict)
async def send_test_notification():
    """
    Quick endpoint to send a test notification to all users.
    Uses default "Testing Notification" message.
    """
    collection = get_expo_tokens_collection()

    tokens = []
    async for token_doc in collection.find():
        tokens.append(token_doc)

    if not tokens:
        return {"success": False, "message": "No expo tokens found in database", "total_tokens": 0}

    sent = 0
    failed = 0

    for token_doc in tokens:
        try:
            print(f"📤 Sending to user: {token_doc['user_id']}, token: {token_doc['expo_token']}")
            response = await send_expo_notification(
                expo_token=token_doc["expo_token"],
                title="🔔 Testing Notification",
                body="This is a test notification from your backend!",
                data={"type": "test", "timestamp": "now"},
            )
            print(f"📥 Expo response: {response}")

            if "data" in response and response["data"].get("status") == "ok":
                print(f"✅ Success for user: {token_doc['user_id']}")
                sent += 1
            else:
                error_msg = response.get("data", {}).get("message", response)
                print(f"❌ Failed for user: {token_doc['user_id']}, error: {error_msg}")
                failed += 1
        except Exception as e:
            print(f"💥 Exception for user: {token_doc['user_id']}, error: {e!s}")
            failed += 1

    return {
        "success": True,
        "message": f"Test notifications sent! {sent} succeeded, {failed} failed",
        "total_tokens": len(tokens),
        "sent": sent,
        "failed": failed,
    }


@router.post("/send-to-user/{user_id}", response_model=dict)
async def send_notification_to_user(
    user_id: str, notification: Optional[NotificationRequest] = None
):
    """Send a notification to a specific user by their user_id."""
    if notification is None:
        notification = NotificationRequest()
    collection = get_expo_tokens_collection()

    token_doc = await collection.find_one({"user_id": user_id})

    if not token_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No expo token found for user: {user_id}"
        )

    try:
        response = await send_expo_notification(
            expo_token=token_doc["expo_token"],
            title=notification.title,
            body=notification.body,
            data=notification.data,
        )

        if "data" in response and response["data"].get("status") == "ok":
            return {
                "success": True,
                "message": f"Notification sent to user {user_id}",
                "expo_response": response,
            }
        return {
            "success": False,
            "message": "Failed to send notification",
            "expo_response": response,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending notification: {e!s}",
        ) from e
