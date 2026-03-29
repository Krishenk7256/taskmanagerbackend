import pytest
from httpx import AsyncClient

from app.models.project import Project
from app.models.user import User


class TestProjects:
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
    async def test_create_project(self, client: AsyncClient, test_user: User):
        token = await self._login_and_get_token(client, test_user)

        response = await client.post(
            "/api/v1/projects",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "New Project",
                "description": "Test project description",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "New Project"
        assert data["description"] == "Test project description"
        assert data["owner_id"] == test_user.id

    @pytest.mark.asyncio
    async def test_list_projects(
        self, client: AsyncClient, test_user: User, test_project: Project
    ):
        token = await self._login_and_get_token(client, test_user)

        response = await client.get(
            "/api/v1/projects",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(p["id"] == test_project.id for p in data)

    @pytest.mark.asyncio
    async def test_list_projects_other_user_projects_hidden(
        self, client: AsyncClient, test_user: User, test_user_2: User, test_project: Project
    ):
        token = await self._login_and_get_token(client, test_user_2)

        response = await client.get(
            "/api/v1/projects",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert not any(p["id"] == test_project.id for p in data)

    @pytest.mark.asyncio
    async def test_get_project(self, client: AsyncClient, test_user: User, test_project: Project):
        token = await self._login_and_get_token(client, test_user)

        response = await client.get(
            f"/api/v1/projects/{test_project.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_project.id
        assert data["title"] == test_project.title

    @pytest.mark.asyncio
    async def test_get_project_not_found(self, client: AsyncClient, test_user: User):
        token = await self._login_and_get_token(client, test_user)

        response = await client.get(
            "/api/v1/projects/999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_other_user_project(
        self, client: AsyncClient, test_user_2: User, test_project: Project
    ):
        token = await self._login_and_get_token(client, test_user_2)

        response = await client.get(
            f"/api/v1/projects/{test_project.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_project(self, client: AsyncClient, test_user: User, test_project: Project):
        token = await self._login_and_get_token(client, test_user)

        response = await client.patch(
            f"/api/v1/projects/{test_project.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Updated Project",
                "description": "Updated description",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Project"
        assert data["description"] == "Updated description"

    @pytest.mark.asyncio
    async def test_delete_project(self, client: AsyncClient, test_user: User, test_project: Project):
        token = await self._login_and_get_token(client, test_user)

        response = await client.delete(
            f"/api/v1/projects/{test_project.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 204

        # Verify deletion
        response = await client.get(
            f"/api/v1/projects/{test_project.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404
