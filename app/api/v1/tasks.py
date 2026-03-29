from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.deps import get_current_active_user, get_db
from ...crud import project as project_crud
from ...crud import task as task_crud
from ...crud import user as user_crud
from ...models.project import Project
from ...models.task import Task
from ...models.user import User
from ...schemas.task import TaskCreate, TaskCreateInProject, TaskOut, TaskUpdate

router = APIRouter()


async def _require_owned_project(
    db: AsyncSession,
    project_id: int,
    current_user: User,
) -> Project:
    p = await project_crud.get(db, id=project_id)
    if p is None or p.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return p


@router.get("", response_model=List[TaskOut])
async def list_tasks(
    project_id: int = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> List[Task]:
    await _require_owned_project(db, project_id, current_user)
    return await task_crud.get_multi_by_project(
        db, project_id=project_id, skip=skip, limit=limit
    )


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    body: TaskCreateInProject,
    project_id: int = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Task:
    await _require_owned_project(db, project_id, current_user)
    if body.assignee_id is not None:
        assignee = await user_crud.get(db, id=body.assignee_id)
        if assignee is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assignee not found",
            )

    task_in = TaskCreate(
        title=body.title,
        description=body.description,
        completed=body.completed,
        project_id=project_id,
        assignee_id=body.assignee_id,
    )
    return await task_crud.create(db, obj_in=task_in)


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(
    task_id: int,
    project_id: int = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Task:
    await _require_owned_project(db, project_id, current_user)
    t = await task_crud.get(db, id=task_id)
    if t is None or t.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return t


@router.patch("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int,
    body: TaskUpdate,
    project_id: int = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Task:
    await _require_owned_project(db, project_id, current_user)
    t = await task_crud.get(db, id=task_id)
    if t is None or t.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if body.assignee_id is not None:
        assignee = await user_crud.get(db, id=body.assignee_id)
        if assignee is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assignee not found",
            )
    return await task_crud.update(db, db_obj=t, obj_in=body)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    project_id: int = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    await _require_owned_project(db, project_id, current_user)
    t = await task_crud.get(db, id=task_id)
    if t is None or t.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    await task_crud.remove(db, id=task_id)
