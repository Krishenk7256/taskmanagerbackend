from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    project_id: int
    assignee_id: Optional[int] = None


class TaskCreateInProject(TaskBase):
    """Создание задачи внутри проекта: project_id задаётся в URL."""

    assignee_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = False
    assignee_id: Optional[int] = None


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    assignee_id: Optional[int] = None
