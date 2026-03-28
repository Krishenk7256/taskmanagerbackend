from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    complete: bool = False

class TaskCreate(TaskBase):
    project_id: int
    assignee_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    complete: Optional[bool] = False
    assignee_id: Optional[int] = None

class TaskOut(TaskBase):
    id: int
    project_id: int
    assignee_id: int

    class Config:
        from_attributes = True