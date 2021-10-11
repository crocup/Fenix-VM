import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_get_page():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get(app.url_path_for("discovery:get"))
    assert response.status_code == 200


@pytest.mark.anyio
async def test_start_discovery_not_host():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:start"))
    assert response.status_code == 422


@pytest.mark.anyio
async def test_start_discovery_host():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:start"), json={"host": "192.168.1.1", "options": "123"})
    assert response.status_code == 200
