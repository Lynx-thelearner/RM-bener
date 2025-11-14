import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest, pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_create_reservation(auth_header):
    transport = ASGITransport(app=app)
    #data reservasi yang mau dikirim
    payload = {
        "user_id":""
    }