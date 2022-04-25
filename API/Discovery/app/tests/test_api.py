import pytest
from httpx import AsyncClient
from app.models.model import Result
from app.main import app


@pytest.mark.anyio
async def test_start_task_discovery_mask():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:start"), json={"host": "127.0.0.1"})
    assert response.status_code == 200
    assert response.json() == Result(success=True)


@pytest.mark.anyio
async def test_start_task_discovery_ip():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:start"), json={"host": "127.0.0.1"})
    assert response.status_code == 200
    assert response.json() == Result(success=True)
