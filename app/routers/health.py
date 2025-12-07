from fastapi import APIRouter, HTTPException
from app.models import HealthResponse
from app.database import db
from app.config import get_settings

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the service and database connection.
    """
    settings = get_settings()
    
    # Check database connection
    db_status = "disconnected"
    if db.client:
        try:
            await db.client.admin.command('ping')
            db_status = "connected"
        except Exception:
            db_status = "error"
    
    if db_status != "connected":
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "message": "Database connection failed",
                "database": db_status,
                "db_mode": settings.db_mode
            }
        )
    
    return HealthResponse(
        status="healthy",
        message="Service is running",
        database=db_status,
        db_mode=settings.db_mode
    )


@router.get("/", response_model=dict)
async def root():
    """Root endpoint - basic service info."""
    return {
        "service": "Expo Token Backend",
        "version": "1.0.0",
        "docs": "/docs"
    }

