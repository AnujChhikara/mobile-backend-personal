from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class ExpoTokenBase(BaseModel):
    """Base model for Expo push token."""

    user_id: str = Field(..., description="Unique user identifier")
    expo_token: str = Field(..., description="Expo push notification token")


class ExpoTokenCreate(ExpoTokenBase):
    """Model for creating a new Expo token entry."""


class ExpoTokenUpdate(BaseModel):
    """Model for updating an Expo token entry."""

    user_id: Optional[str] = Field(None, description="Unique user identifier")
    expo_token: Optional[str] = Field(None, description="Expo push notification token")


class ExpoTokenResponse(ExpoTokenBase):
    """Model for Expo token response."""

    id: str = Field(..., description="Unique document identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class ExpoTokenInDB(ExpoTokenBase):
    """Model for Expo token stored in database."""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Service health status")
    message: str = Field(..., description="Health check message")
    database: str = Field(..., description="Database connection status")
    db_mode: str = Field(..., description="Current database mode (docker/atlas)")


class MessageResponse(BaseModel):
    """Generic message response."""

    message: str
    success: bool = True


# AI Chat Models
class ChatRequest(BaseModel):
    """Request model for AI chat endpoint."""

    message: str = Field(..., description="User message/input")
    user_id: str = Field(..., description="User ID")
    session_id: Optional[str] = Field(None, description="Existing session ID (optional)")


class PendingAction(BaseModel):
    """Model for pending action awaiting confirmation."""

    action: str = Field(..., description="Action name (e.g., 'createTask')")
    data: dict[str, Any] = Field(..., description="Action data/parameters")
    validation_results: Optional[dict[str, Any]] = Field(None, description="Validation results")


class ChatResponse(BaseModel):
    """Response model for AI chat endpoint."""

    message: str = Field(..., description="Assistant response message")
    session_id: str = Field(..., description="Session ID for conversation")
    requires_confirmation: bool = Field(
        False, description="Whether user confirmation is required"
    )
    pending_action: Optional[PendingAction] = Field(
        None, description="Pending action details if confirmation required"
    )
    success: bool = Field(True, description="Whether the request succeeded")
