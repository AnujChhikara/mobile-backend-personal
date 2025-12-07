from functools import lru_cache
from typing import Literal, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with support for Docker and Atlas MongoDB connections."""

    # Database mode: "docker" for local MongoDB, "atlas" for MongoDB Atlas
    db_mode: Literal["docker", "atlas"] = "docker"

    # Docker MongoDB Settings
    mongo_docker_host: str = "localhost"
    mongo_docker_port: int = 27017
    mongo_docker_user: str = "admin"
    mongo_docker_password: str = "password123"

    # MongoDB Atlas Settings
    mongo_atlas_uri: str = "mongodb+srv://username:password@cluster.mongodb.net/"

    # Database Name
    database_name: str = "expo_tokens_db"

    # Scheduler/Cron Settings
    run_cron: bool = True  # Set to False to disable scheduled tasks

    # AI Provider Settings (Gemini only)
    google_api_key: Optional[str] = None  # For Gemini
    ai_model: str = "gemini-1.5-flash"  # Default Gemini model

    # Backend API Settings
    backend_url: str = "https://staging-api.realdevsquad.com"

    # Rate Limiting
    rate_limit: int = 20  # API calls per day per user

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def mongodb_uri(self) -> str:
        """Get the appropriate MongoDB URI based on db_mode."""
        if self.db_mode == "atlas":
            return self.mongo_atlas_uri
        # Docker/local MongoDB connection string
        return (
            f"mongodb://{self.mongo_docker_user}:{self.mongo_docker_password}"
            f"@{self.mongo_docker_host}:{self.mongo_docker_port}"
        )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
