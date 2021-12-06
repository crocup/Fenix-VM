import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_get_page():
    """Получение информации по задаче"""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:get"),
                                 json={"uuid": "4e403d1b-e97a-4091-9bfa-6d7a79c924e0"})
    assert response.status_code == 200


@pytest.mark.anyio
async def test_get_page_no_data():
    """Получение информации по задаче. Неправильный uuid"""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:get"), json={"uuid": "test5"})
    assert response.status_code == 200
    assert response.json() == {"data": [], "status": True}


@pytest.mark.anyio
async def test_get_page_no_name():
    """Получение информации по задаче. Нет данных json"""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:get"))
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_discovery():
    """создать задачу"""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:create"), json={"mask": "192.168.100.0/24",
                                                                             "name": "test2"})
    assert response.status_code == 200
    assert response.json() == {"success": True}


@pytest.mark.anyio
async def test_start_discovery_not_data():
    """создать задачу. Нет данных"""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:start"))
    assert response.status_code == 422


@pytest.mark.anyio
async def test_start_discovery_not_json():
    """создать задачу. Неполный json"""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:start"), json={"mask": "192.168.100.0/24"})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_start_discovery_host():
    """запуск задачи"""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:start"),
                                 json={"uuid": "4e403d1b-e97a-4091-9bfa-6d7a79c924e0"})
    assert response.status_code == 200
    assert response.json() == {"success": True}


@pytest.mark.anyio
async def test_start_discovery_error_uuid():
    """запуск задачи. Неправильный uuid"""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:start"),
                                 json={"uuid": "test"})
    assert response.status_code == 200
    assert response.json() == {"success": False}


@pytest.mark.anyio
async def test_start_discovery_not_json():
    """запуск задачи. Нет JSON"""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post(app.url_path_for("discovery:start"))
    assert response.status_code == 422


# @pytest.mark.anyio
# async def test_delete_discovery_task():
#     """ удаление задачи"""
#     async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
#         response = await ac.delete(app.url_path_for("discovery:delete"), json={"uuid": "te"})
#     assert response.status_code == 200
#     assert response.json() == {"success": True}


@pytest.mark.anyio
async def test_delete_discovery_task_no_json():
    """ удаление задачи"""
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.delete(app.url_path_for("discovery:delete"))
    assert response.status_code == 422
