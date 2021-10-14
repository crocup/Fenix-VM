import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.anyio
async def test_404_page():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/")
    assert response.status_code == 404
    assert response.json() == {'errors': 'Not Found'}


@pytest.mark.anyio
async def test_404_all_page():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/sdfhstysg")
    assert response.status_code == 404
    assert response.json() == {'errors': 'Not Found'}
