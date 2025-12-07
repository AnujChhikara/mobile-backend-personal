"""Rate limiting per user per day using MongoDB."""

import logging
from datetime import date, datetime

from fastapi import HTTPException, status

from app.config import get_settings
from app.database import get_rate_limits_collection

logger = logging.getLogger(__name__)


async def check_rate_limit(user_id: str, limit: int) -> tuple[bool, int, int]:
    """Check if user has exceeded rate limit.

    Args:
        user_id: User ID to check
        limit: Daily limit (from config)

    Returns:
        Tuple of (is_allowed, current_count, limit)
    """
    collection = get_rate_limits_collection()
    today = date.today().isoformat()

    # Get or create rate limit record
    rate_limit = await collection.find_one({"user_id": user_id, "date": today})

    if not rate_limit:
        # First call today - create record
        now = datetime.utcnow()
        next_reset = datetime(now.year, now.month, now.day, 0, 0, 0)
        next_reset = next_reset.replace(day=next_reset.day + 1)  # Tomorrow midnight UTC

        await collection.insert_one(
            {
                "user_id": user_id,
                "date": today,
                "count": 1,
                "limit": limit,
                "last_reset": now,
                "next_reset": next_reset,
                "created_at": now,
                "updated_at": now,
            }
        )
        return True, 1, limit

    # Check if limit exceeded
    current_count = rate_limit.get("count", 0)
    if current_count >= limit:
        return False, current_count, limit

    # Increment count
    await collection.update_one(
        {"user_id": user_id, "date": today},
        {"$inc": {"count": 1}, "$set": {"updated_at": datetime.utcnow()}},
    )

    return True, current_count + 1, limit


async def enforce_rate_limit(user_id: str, limit: int):
    """Enforce rate limit - raise exception if exceeded.

    Args:
        user_id: User ID to check
        limit: Daily limit

    Raises:
        HTTPException: If rate limit exceeded
    """
    is_allowed, current, max_limit = await check_rate_limit(user_id, limit)

    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "message": f"You have reached the daily limit of {max_limit} API calls. Please try again tomorrow.",
                "limit": max_limit,
                "current": current,
                "reset_at": "00:00:00 UTC tomorrow",
            },
        )


async def get_rate_limit_status(user_id: str, limit: int) -> dict:
    """Get current rate limit status for user.

    Args:
        user_id: User ID
        limit: Daily limit

    Returns:
        Dictionary with rate limit status
    """
    is_allowed, current, max_limit = await check_rate_limit(user_id, limit)
    return {
        "allowed": is_allowed,
        "current": current,
        "limit": max_limit,
        "remaining": max(0, max_limit - current),
    }
