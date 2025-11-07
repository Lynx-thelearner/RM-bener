import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest, pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
import uuid

@pytest.mark.asyncio
@pytest.mark.parametrize("payload", [
    {
        "nama": "Test User",
        "username": "testuser",
        "no_telp": "081234567890",
        "email": "usertest@test.com",
        "role": "customer",
        "password": "testpassword"
    },
    {
        "nama": "Jane Doe",
        "username": "janedoe",
        "no_telp": "089876543210",
        "email": "janedoe@test.com",
        "role": "admin",
        "password": "janepassword"
    },
    {
        "nama": "John Smith",
        "username": "johnsmith",
        "no_telp": "087654321098",
        "email": "johnsmith@user.com",
        "role": "manager",
        "password": "johnpassword"
    }
])
async def test_create_user(payload: dict, auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as ac:
        respon = await ac.post("/user/", json=payload)
        assert respon.status_code == 201, respon.text
        data = respon.json()
        assert data["username"] == payload["username"]
        assert data["email"] == payload["email"]
        assert data["role"] == payload["role"]
        assert "user_id" in data
        assert "password" not in data
    
@pytest.mark.asyncio
async def test_get_all_user(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as ac:
        #end point get all user
        respon = await ac.get("/user/")
        assert respon.status_code == 200, respon.text
        data = respon.json()
        
        #Pake list
        assert isinstance(data, list)
        #Pastikan ada user di list
        assert len(data) >=1
        #Cek struktur data user
        for user in data:
            assert "user_id" in user
            assert "username" in user
            assert "email" in user
            assert "role" in user
            
@pytest.mark.asyncio
async def test_get_user_by_id(auth_header):
    transport = ASGITransport(app=app)
    #Buat data user baru dulu
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "nama": "Test User",
            "username": "useruser",
            "no_telp": "+6281122334455",
            "email": "testing@gmail.com",
            "role": "customer",
            "password": "testpassword"
        }
        create_respon = await ac.post("/user/", json=payload, headers=auth_header)
        assert create_respon.status_code == 201, create_respon.text
        created_user = create_respon.json()
        user_id = created_user["user_id"]
        
        #Sekarang coba ambil user berdasarkan ID
        get_respon = await ac.get(f"/user/{user_id}", headers=auth_header)
        assert get_respon.status_code == 200, get_respon.text
        data = get_respon.json()
        
        assert data["user_id"] == user_id
        assert data["username"] == payload["username"]
        assert data["email"] == payload["email"]
        
@pytest.mark.asyncio
async def test_get_profile(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as ac:
        respon = await ac.get("/user/profile")
        assert respon.status_code == 200, respon.text
        data = respon.json()
        
        assert "user_id" in data
        assert "username" in data
        assert "email" in data
        
@pytest.mark.asyncio
async def test_profile_update(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as ac:
        #Ambil profile dulu
        respon = await ac.get("/user/profile")
        assert respon.status_code == 200, respon.text
        data = respon.json()
               
        #Update profile
        update_payload = {
            "nama": "Updated Diaz",
            "no_telp": "081298765432"
        }
        update_respon = await ac.patch(f"/user/profile", json=update_payload, headers=auth_header)
        assert update_respon.status_code == 200, update_respon.text
        
        #ambil lagi untuk verifikasi
        new = await ac.get("/user/profile", headers=auth_header)
        assert new.status_code == 200, new.text
        new_data = new.json()
        
        assert new_data["nama"] == update_payload["nama"]
        assert new_data["no_telp"] == update_payload["no_telp"]
        assert new_data["username"] == data["username"]  # pastikan username tidak berubah
        
@pytest.mark.asyncio
async def test_update_user(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as ac:
    #data user baru sebelum update
        payload = {
            "nama": "belum update user",
            "username": "belumupdate",
            "no_telp": "+6281122334455",
            "email": "Belum@gmail.com",
            "role": "customer",
            "password": "testpassword"
        }
        old_data = await ac.post("/user/", json=payload, headers=auth_header)
        assert old_data.status_code == 201, old_data.text
        created_user = old_data.json()
        user_id = created_user["user_id"]
    
        #data user setelah update
        update_payload = {
            "nama": "sudah update user"
        }
        data = await ac.patch(f"/user/{user_id}", json=update_payload, headers=auth_header)
        assert data.status_code == 200, data.text
        updated_user = data.json()
        assert updated_user["nama"] == update_payload["nama"]
        assert updated_user["username"] == payload["username"] # memastikan username tidak berubah
    
@pytest.mark.asyncio
async def test_delete_user(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as ac:
        #buat data yang mau dihapus
        payload = {
        "nama": "dataterhapus",
        "username": "hapushapus",
        "no_telp": "+6281122334455",
        "email": "hapus@gmail.com",
        "role": "customer",
        "password": "testpassword"
        }
        data = await ac.post("/user/", json=payload, headers=auth_header)
        assert data.status_code == 201, data.text
        created_user = data.json()
        user_id = created_user["user_id"]
        
        #hapus user
        delete_respon = await ac.delete(f"/user/{user_id}", headers=auth_header)
        assert delete_respon.status_code == 204, delete_respon.text
        #coba ambil user yang sudah dihapus
        get_respon = await ac.get(f"/user/{user_id}", headers=auth_header)
        assert get_respon.status_code == 404, get_respon.text
        
        
       