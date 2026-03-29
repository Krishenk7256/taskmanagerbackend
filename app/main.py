import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.core.config import Environment, settings
from app.core.database import Base, engine
from app.health import router as health_router

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.AUTO_CREATE_TABLES and settings.ENV != Environment.production:
        logger.warning(
            "AUTO_CREATE_TABLES is enabled: creating tables from models "
            "(use Alembic migrations in staging/production)"
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    elif settings.ENV == Environment.production:
        logger.info("Production mode: ensure database schema is migrated (Alembic)")
    yield
    await engine.dispose()


app = FastAPI(title="Task manager API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(api_router, prefix="/api/v1")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Task manager API", "health": "/health/live"}
