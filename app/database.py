from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import get_settings


class Database:
    """MongoDB database connection manager."""

    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None


db = Database()


async def connect_to_database():
    """Connect to MongoDB database."""
    settings = get_settings()

    print(f"🔌 Connecting to MongoDB ({settings.db_mode} mode)...")

    db.client = AsyncIOMotorClient(settings.mongodb_uri)
    db.db = db.client[settings.database_name]

    # Test the connection
    try:
        await db.client.admin.command("ping")
        print(f"✅ Successfully connected to MongoDB ({settings.db_mode})")
        print(f"📁 Database: {settings.database_name}")
        
        # Create indexes for new collections
        await create_indexes()
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise e


async def create_indexes():
    """Create database indexes for performance."""
    try:
        # Conversations collection indexes
        conversations_collection = get_conversations_collection()
        await conversations_collection.create_index("user_id")
        await conversations_collection.create_index("session_id", unique=True)
        await conversations_collection.create_index("expires_at")
        await conversations_collection.create_index([("user_id", 1), ("created_at", -1)])
        
        # Rate limits collection indexes
        rate_limits_collection = get_rate_limits_collection()
        await rate_limits_collection.create_index([("user_id", 1), ("date", 1)], unique=True)
        await rate_limits_collection.create_index("date")
        
        print("✅ Database indexes created successfully")
    except Exception as e:
        print(f"⚠️  Warning: Failed to create indexes: {e}")
        # Don't fail startup if indexes fail


async def close_database_connection():
    """Close MongoDB database connection."""
    if db.client:
        db.client.close()
        print("🔌 MongoDB connection closed")


def get_database() -> AsyncIOMotorDatabase:
    """Get the database instance."""
    if db.db is None:
        raise RuntimeError("Database not initialized. Call connect_to_database first.")
    return db.db


def get_expo_tokens_collection():
    """Get the expo_tokens collection."""
    return get_database()["expo_tokens"]


def get_conversations_collection():
    """Get the conversations collection."""
    return get_database()["conversations"]


def get_rate_limits_collection():
    """Get the rate_limits collection."""
    return get_database()["rate_limits"]
