from datetime import datetime
from typing import Optional

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
