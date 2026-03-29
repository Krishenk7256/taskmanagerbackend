from fastapi import APIRouter

from .auth import router as auth_router
from .projects import router as projects_router
from .tasks import router as tasks_router
from .users import router as users_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(projects_router, prefix="/projects", tags=["projects"])
api_router.include_router(tasks_router, prefix="/projects/{project_id}/tasks", tags=["tasks"])
