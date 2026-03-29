import pytest
from httpx import AsyncClient

from app.models.project import Project
from app.models.task import Task
from app.models.user import User


class TestTasks:
    async def _login_and_get_token(self, client: AsyncClient, user: User) -> str:
        response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": user.username,
                "password": "testpassword123",
            },
        )
        return response.json()["access_token"]

    @pytest.mark.asyncio
    async def test_create_task(self, client: AsyncClient, test_user: User, test_project: Project):
        token = await self._login_and_get_token(client, test_user)

        response = await client.post(
            f"/api/v1/projects/{test_project.id}/tasks",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "New Task",
                "description": "Task description",
                "completed": False,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Task"
        assert data["completed"] is False
        assert data["project_id"] == test_project.id

    @pytest.mark.asyncio
    async def test_create_task_with_assignee(
        self, client: AsyncClient, test_user: User, test_user_2: User, test_project: Project
    ):
        token = await self._login_and_get_token(client, test_user)

        response = await client.post(
            f"/api/v1/projects/{test_project.id}/tasks",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Task with assignee",
                "description": "Assigned task",
                "completed": False,
                "assignee_id": test_user_2.id,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["assignee_id"] == test_user_2.id

    @pytest.mark.asyncio
    async def test_create_task_invalid_assignee(
        self, client: AsyncClient, test_user: User, test_project: Project
    ):
        token = await self._login_and_get_token(client, test_user)

        response = await client.post(
            f"/api/v1/projects/{test_project.id}/tasks",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Task",
                "description": "Description",
                "completed": False,
                "assignee_id": 999,
            },
        )
        assert response.status_code == 400
        assert "Assignee not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_list_tasks(
        self, client: AsyncClient, test_user: User, test_project: Project, test_task: Task
    ):
        token = await self._login_and_get_token(client, test_user)

        response = await client.get(
            f"/api/v1/projects/{test_project.id}/tasks",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(t["id"] == test_task.id for t in data)

    @pytest.mark.asyncio
    async def test_list_tasks_other_user_project(
        self, client: AsyncClient, test_user_2: User, test_project: Project
    ):
        token = await self._login_and_get_token(client, test_user_2)

        response = await client.get(
            f"/api/v1/projects/{test_project.id}/tasks",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_task(
        self, client: AsyncClient, test_user: User, test_project: Project, test_task: Task
    ):
        token = await self._login_and_get_token(client, test_user)

        response = await client.get(
            f"/api/v1/projects/{test_project.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_task.id
        assert data["title"] == test_task.title

    @pytest.mark.asyncio
    async def test_get_task_not_found(self, client: AsyncClient, test_user: User, test_project: Project):
        token = await self._login_and_get_token(client, test_user)

        response = await client.get(
            f"/api/v1/projects/{test_project.id}/tasks/999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_task(
        self, client: AsyncClient, test_user: User, test_project: Project, test_task: Task
    ):
        token = await self._login_and_get_token(client, test_user)

        response = await client.patch(
            f"/api/v1/projects/{test_project.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Updated Task",
                "completed": True,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Task"
        assert data["completed"] is True

    @pytest.mark.asyncio
    async def test_update_task_invalid_assignee(
        self, client: AsyncClient, test_user: User, test_project: Project, test_task: Task
    ):
        token = await self._login_and_get_token(client, test_user)

        response = await client.patch(
            f"/api/v1/projects/{test_project.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "assignee_id": 999,
            },
        )
        assert response.status_code == 400
        assert "Assignee not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_delete_task(
        self, client: AsyncClient, test_user: User, test_project: Project, test_task: Task
    ):
        token = await self._login_and_get_token(client, test_user)

        response = await client.delete(
            f"/api/v1/projects/{test_project.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 204

        # Verify deletion
        response = await client.get(
            f"/api/v1/projects/{test_project.id}/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
