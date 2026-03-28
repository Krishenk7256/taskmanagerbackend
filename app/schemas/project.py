from pydantic import BaseModel, Field
from typing import Optional

class ProjectBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None

class ProjectOut(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True