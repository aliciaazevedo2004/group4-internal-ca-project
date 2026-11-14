import os
from fastapi import APIRouter

router = APIRouter(tags=["API"])


@router.get("/health")
def get_health():
    return {
        "status": "healthy",
        "service": "internal-api",
        "version": "1.0",
        "mode": os.getenv("SERVICE_MODE", "http").upper(),
    }
