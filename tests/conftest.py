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
            "username": "",
            "password": ""
        }