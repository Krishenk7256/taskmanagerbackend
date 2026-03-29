import asyncio
import os
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.core.security import get_password_hash
from app.main import app
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from fastapi.testclient import TestClient
from httpx import AsyncClient


TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop_policy():
    policy = asyncio.get_event_loop_policy()
    yield policy


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(
        TEST_SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_local = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_local() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield test_db

    from app.core.deps import get_db
    app.dependency_overrides[get_db] = override_get_db

    from httpx import ASGITransport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_db: AsyncSession) -> User:
    from app.crud.user import user as user_crud
    from app.schemas.user import UserCreate

    user_create = UserCreate(
        email="testuser@example.com",
        username="testuser",
        password="testpassword123",
    )
    user = await user_crud.create(test_db, obj_in=user_create)
    return user


@pytest.fixture
async def test_user_2(test_db: AsyncSession) -> User:
    from app.crud.user import user as user_crud
    from app.schemas.user import UserCreate

    user_create = UserCreate(
        email="testuser2@example.com",
        username="testuser2",
        password="testpassword123",
    )
    user = await user_crud.create(test_db, obj_in=user_create)
    return user


@pytest.fixture
async def test_project(test_db: AsyncSession, test_user: User) -> Project:
    from app.models.project import Project

    project = Project(
        title="Test Project",
        description="This is a test project",
        owner_id=test_user.id,
    )
    test_db.add(project)
    await test_db.commit()
    await test_db.refresh(project)
    return project


@pytest.fixture
async def test_task(test_db: AsyncSession, test_project: Project) -> Task:
    from app.models.task import Task

    task = Task(
        title="Test Task",
        description="This is a test task",
        completed=False,
        project_id=test_project.id,
        assignee_id=None,
    )
    test_db.add(task)
    await test_db.commit()
    await test_db.refresh(task)
    return task
