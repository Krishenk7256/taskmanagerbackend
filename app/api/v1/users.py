from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.deps import get_current_active_user, get_db
from ...models.user import User
from ...schemas.user import UserOut

router = APIRouter()


@router.get("/me", response_model=UserOut)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user
