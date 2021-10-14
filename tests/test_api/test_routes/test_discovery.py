import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_get_page():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:get"), json={"name": "test1"})
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_page_no_name():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:get"))
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_discovery():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:create"), json={"mask": "192.168.100.0/24",
                                                                             "name": "test2"})
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "insert data"}


@pytest.mark.anyio
async def test_start_discovery_not_host():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:start"))
    assert response.status_code == 422


@pytest.mark.anyio
async def test_start_discovery_host():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:start"), json={"name": "test1"})
    assert response.status_code == 200
