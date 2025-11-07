import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest, pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app

#Fixture untuk client async
@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
        
#Fixture buat token JWT
@pytest_asyncio.fixture
async def auth_header():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        #login dan dapetin token
        login_data = {
            "username": "Naga",
            "password": "naganaga"
        }
        respon = await ac.post("/api/v1/auth/login", data=login_data)
        assert respon.status_code == 200, respon.text
        token = respon.json().get("access_token")
        return {"Authorization": f"Bearer {token}"}