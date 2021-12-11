import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_get_page():
    """Получение информации по всем хостам"""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get(app.url_path_for("discovery:tasks"))
    assert response.status_code == 200


@pytest.mark.anyio
async def test_start_discovery_host():
    """запуск задачи"""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:start"))
    assert response.status_code == 200
    assert response.json() == {"success": True}
