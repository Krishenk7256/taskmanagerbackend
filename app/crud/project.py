from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectUpdate
from .base import CRUDBase

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    async def get_multi_by_owner(self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(Project)
            .where(Project.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

project = CRUDProject(Project)