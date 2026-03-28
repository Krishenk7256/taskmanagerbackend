from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate
from .base import CRUDBase

class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    async def get_multi_by_project(self, db: AsyncSession, *, project_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        result = await db.execute(
            select(Task)
            .where(Task.project_id == project_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_multi_by_assignee(self, db: AsyncSession, *, assignee_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        result = await db.execute(
            select(Task)
            .where(Task.assignee_id == assignee_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

task = CRUDTask(Task)