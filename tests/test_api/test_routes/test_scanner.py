import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_get_page_scanner():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("scanner:get"), json={"name": "test"})
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_page_scanner_no_data():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("scanner:get"), json={"name": "test5"})
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_page_scanner_no_name():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("scanner:get"))
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_task_scanner():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("scanner:create"), json={"mask": "192.168.1.1",
                                                                           "name": "test2"})
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "insert data"}


@pytest.mark.anyio
async def test_start_scanner_not_host():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("scanner:start"))
    assert response.status_code == 422


@pytest.mark.anyio
async def test_start_scanner():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("scanner:start"), json={"uuid": "4e403d1b-e97a-4091-9bfa-6d7a79c924e0"})
    assert response.status_code == 422
