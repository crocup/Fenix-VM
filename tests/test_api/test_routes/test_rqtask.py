import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_job():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get(app.url_path_for("task:status", **{"job_key": "cc29a2b3-218e-4b58-8899-86d199842216"}))
    assert response.status_code == 200
    assert response.json() == {"success": False}


@pytest.mark.anyio
async def test_no_job():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get(app.url_path_for("task:status", **{"job_key": "78"}))
    assert response.status_code == 200
    assert response.json() == {"success": False}


@pytest.mark.anyio
async def test_no_job_default():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get(app.url_path_for("task:default"))
    assert response.status_code == 204
    assert response.json() == {"success": False}
