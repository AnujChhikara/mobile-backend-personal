from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from app.database import connect_to_database, close_database_connection
from app.routers import health, expo_tokens, notifications
from app.config import get_settings

# Get the directory where static files are located
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - startup and shutdown events."""
    # Startup
    settings = get_settings()
    print(f"🚀 Starting Expo Token Backend...")
    print(f"📊 Database mode: {settings.db_mode}")
    
    await connect_to_database()
    
    yield
    
    # Shutdown
    await close_database_connection()
    print("👋 Expo Token Backend shutdown complete")


app = FastAPI(
    title="Expo Token Backend",
    description="FastAPI backend for managing Expo push notification tokens",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(expo_tokens.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/dashboard")
async def dashboard():
    """Serve the admin dashboard."""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

