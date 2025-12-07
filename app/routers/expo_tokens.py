from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from datetime import datetime

from app.models import (
    ExpoTokenCreate,
    ExpoTokenUpdate,
    ExpoTokenResponse,
    ExpoTokenInDB,
    MessageResponse
)
from app.database import get_expo_tokens_collection

router = APIRouter(prefix="/expo-tokens", tags=["Expo Tokens"])


def token_helper(token: dict) -> ExpoTokenResponse:
    """Convert MongoDB document to ExpoTokenResponse."""
    return ExpoTokenResponse(
        id=str(token["_id"]),
        user_id=token["user_id"],
        expo_token=token["expo_token"],
        created_at=token.get("created_at", datetime.utcnow()),
        updated_at=token.get("updated_at", datetime.utcnow())
    )


@router.post("/", response_model=ExpoTokenResponse, status_code=status.HTTP_201_CREATED)
async def create_expo_token(token_data: ExpoTokenCreate):
    """
    Create a new Expo token entry.
    
    If a token already exists for the user_id, it will be updated instead.
    """
    collection = get_expo_tokens_collection()
    
    # Check if user already has a token
    existing = await collection.find_one({"user_id": token_data.user_id})
    
    if existing:
        # Update existing token
        now = datetime.utcnow()
        await collection.update_one(
            {"user_id": token_data.user_id},
            {
                "$set": {
                    "expo_token": token_data.expo_token,
                    "updated_at": now
                }
            }
        )
        updated = await collection.find_one({"user_id": token_data.user_id})
        return token_helper(updated)
    
    # Create new token entry
    now = datetime.utcnow()
    token_doc = {
        "user_id": token_data.user_id,
        "expo_token": token_data.expo_token,
        "created_at": now,
        "updated_at": now
    }
    
    result = await collection.insert_one(token_doc)
    created = await collection.find_one({"_id": result.inserted_id})
    
    return token_helper(created)


@router.get("/", response_model=List[ExpoTokenResponse])
async def get_all_expo_tokens():
    """Get all Expo tokens."""
    collection = get_expo_tokens_collection()
    tokens = []
    
    async for token in collection.find():
        tokens.append(token_helper(token))
    
    return tokens


@router.get("/{token_id}", response_model=ExpoTokenResponse)
async def get_expo_token(token_id: str):
    """Get a specific Expo token by ID."""
    collection = get_expo_tokens_collection()
    
    if not ObjectId.is_valid(token_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token ID format"
        )
    
    token = await collection.find_one({"_id": ObjectId(token_id)})
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expo token not found"
        )
    
    return token_helper(token)


@router.get("/user/{user_id}", response_model=ExpoTokenResponse)
async def get_expo_token_by_user(user_id: str):
    """Get Expo token by user ID."""
    collection = get_expo_tokens_collection()
    
    token = await collection.find_one({"user_id": user_id})
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Expo token found for user: {user_id}"
        )
    
    return token_helper(token)


@router.put("/{token_id}", response_model=ExpoTokenResponse)
async def update_expo_token(token_id: str, token_data: ExpoTokenUpdate):
    """Update an Expo token by ID."""
    collection = get_expo_tokens_collection()
    
    if not ObjectId.is_valid(token_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token ID format"
        )
    
    # Check if token exists
    existing = await collection.find_one({"_id": ObjectId(token_id)})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expo token not found"
        )
    
    # Build update data
    update_data = {k: v for k, v in token_data.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    update_data["updated_at"] = datetime.utcnow()
    
    await collection.update_one(
        {"_id": ObjectId(token_id)},
        {"$set": update_data}
    )
    
    updated = await collection.find_one({"_id": ObjectId(token_id)})
    return token_helper(updated)


@router.delete("/{token_id}", response_model=MessageResponse)
async def delete_expo_token(token_id: str):
    """Delete an Expo token by ID."""
    collection = get_expo_tokens_collection()
    
    if not ObjectId.is_valid(token_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token ID format"
        )
    
    result = await collection.delete_one({"_id": ObjectId(token_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expo token not found"
        )
    
    return MessageResponse(message="Expo token deleted successfully")


@router.delete("/user/{user_id}", response_model=MessageResponse)
async def delete_expo_token_by_user(user_id: str):
    """Delete Expo token by user ID."""
    collection = get_expo_tokens_collection()
    
    result = await collection.delete_one({"user_id": user_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Expo token found for user: {user_id}"
        )
    
    return MessageResponse(message=f"Expo token for user {user_id} deleted successfully")

