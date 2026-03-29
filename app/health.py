import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.database import ping_db

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health/live")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness() -> JSONResponse:
    try:
        await ping_db()
    except Exception:
        logger.exception("Database readiness check failed")
        return JSONResponse(
            status_code=503,
            content={"status": "unavailable", "database": "disconnected"},
        )
    return JSONResponse(status_code=200, content={"status": "ok", "database": "connected"})
