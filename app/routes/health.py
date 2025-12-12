from fastapi import APIRouter
from datetime import datetime

from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    return {
        "message": settings.app_name,
        "version": settings.app_version
    }


@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancers"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": settings.app_name,
        "version": settings.app_version
    }
