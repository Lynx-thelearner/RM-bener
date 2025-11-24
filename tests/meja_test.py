import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_create_meja(auth_header):
    transport = ASGITransport(app=app)
    #buat data meja yang mau dibikin
    payload = {
        "kode_meja": "L12",
        "kapasitas": 4,
        "lokasi": "Balkon outdoor",
        "status": "tersedia"
    } 
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        #Endpointn buat meja
        respon = await ac.post("/meja/", json=payload, headers=auth_header)
        assert respon.status_code == 201
        data = respon.json()
        
        assert data["kode_meja"] == payload["kode_meja"]
        assert data["kapasitas"] == payload["kapasitas"]
        assert data["lokasi"] == payload["lokasi"]
        assert data["status"] == payload["status"]
        assert "meja_id" in data
        
@pytest.mark.asyncio
async def test_get_all_meja(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        #endpoint ambil semua meja
        respon = await ac.get("/meja/")
        
        assert respon.status_code == 200 
        data = respon.json()
        
        #buat data dalam bentuk list
        assert isinstance(data, list)
        #minmal 1 data
        assert len(data) >= 1
        #ngecek apa yang di return
        assert "meja_id" in data[0]
        assert "kode_meja" in data[0]
        assert "kapasitas" in data[0]
        assert "status" in data[0]
        
@pytest.mark.asyncio
async def test_get_meja_by_kode_meja(auth_header):
    transport = ASGITransport(app=app)
    #payload dulu data yang mau dicari
    payload = {
        "kode_meja": "D2",
        "kapasitas": 4,
        "lokasi": "Dekat pintu balkon",
        "status": "tidakTersedia"
    } 
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_response = await ac.post("/meja/", json=payload, headers=auth_header)
        assert create_response.status_code == 201
        created_meja = create_response.json()
        kode_meja = created_meja["kode_meja"]
        
        #get bukunya berdasarkan id
        get_response = await ac.get(f"/meja/{kode_meja}")
        
        assert get_response.status_code == 200
        data = get_response.json()
        
        assert data["kode_meja"] == kode_meja
        
@pytest.mark.asyncio
async def test_get_meja_by_status_tersedia(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        #endpoint buat ambil meja tersedia
        response = await ac.get("/meja/available", headers=auth_header)
        assert response.status_code == 200
        data = response.json()
        
        #buat data dalam bentuk list
        assert isinstance(data, list)
        #minmal 1 data
        assert len(data) >= 1
        #ngecek apa yang di return
        assert "meja_id" in data[0]
        assert "kode_meja" in data[0]
        assert "kapasitas" in data[0]
        assert "status" in data[0]
        assert data[0]["status"] == "tersedia"
        
@pytest.mark.asyncio
async def test_patch_meja_by_kode_meja(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as ac:
    #buat data yang mau diubah
        payload = {
            "kode_meja": "D4",
            "kapasitas": 4,
            "lokasi": "lantai 2",
            "status": "tersedia"
          }   
        old_data = await ac.post("/meja/", json=payload, headers=auth_header)
        assert old_data.status_code == 201
        created_data = old_data.json()
        kode_meja = created_data["kode_meja"]
        
        #update data meja euy
        update_payload = {
            "kode_meja":"D35"
        }
        
        data = await ac.patch(f"/meja/{kode_meja}", json=update_payload, headers=auth_header)
        assert data.status_code == 200
        updated_meja = data.json()
        assert updated_meja["kode_meja"] == update_payload["kode_meja"] #memastikan kode meja berubah
        assert updated_meja["status"] == created_data["status"] #memastikan status tidak berubah
        
@pytest.mark.asyncio
async def test_delete_meja(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", headers=auth_header) as ac:
        #buat data yang mau dihapus
        payload = {
            "kode_meja": "D4",
            "kapasitas": 4,
            "lokasi": "lantai 2",
            "status": "tersedia"
        }
        response = await ac.post("/meja/", json=payload)
        assert response.status_code == 201
        created_meja = response.json()
        kode_meja = created_meja["kode_meja"]
        
        #Tinggal delete meja
        detele_response = await ac.delete(f"/meja/{kode_meja}")
        assert detele_response.status_code == 200
        #ambil data yang dihapus buat memastikan udah gada
        get_respon = await ac.get(f"/meja/{kode_meja}")
        assert get_respon.status_code == 404
        