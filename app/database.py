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
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise e


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
