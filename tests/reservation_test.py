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
        "user_id":"c4b3075b-f0b4-4ad8-8f50-39bee8a3df65",
        "meja_id":8,
        "tanggal_reservasi": "2025-11-15",
        "jam_reservasi": "08:00:00",
        "jumlah_orang": 2,
        "status": "menunggu"
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        #Endpoint untuk reservation
        respon = await ac.post("/reservation/", json=payload, headers=auth_header)
        assert respon.status_code == 200
        data = respon.json()

        assert data ["user_id"] == payload ["user_id"]
        assert data ["meja_id"] == payload ["meja_id"]
        assert data ["tanggal_reservasi"] == payload ["tanggal_reservasi"]
        assert data ["jam_reservasi"] == payload ["jam_reservasi"]
        assert data ["jumlah_orang"] == payload ["jumlah_orang"]
        assert data ["status"] == payload ["status"]
        assert "reservation_id" in data


@pytest.mark.asyncio
async def test_get_all_reservation(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        #endpoint ambil semua reservasi
        respon = await ac.get("/reservation/")
        assert respon.status_code == 200
        data = respon.json()

        #buat data dalam bentuk list
        assert isinstance(data, list)
        #minimal satu data
        assert len(data) >= 1
        #ngecek apa yang di return
        assert "reservation_id" in data [0]
        assert "user_id" in data [0]
        assert "meja_id" in data [0]
        assert "tanggal_reservasi" in data [0]
        assert "jumlah_orang" in data [0]
        assert "status" in data [0]

@pytest.mark.asyncio
async def test_get_reservation_by_id(auth_header):
    transport =ASGITransport(app=app)
    #payloadnya terlebih dahulu dibuat baru dicari
    payload = {
        "user_id":"c4b3075b-f0b4-4ad8-8f50-39bee8a3df65",
        "meja_id":17,
        "tanggal_reservasi": "2025-11-16",
        "jam_reservasi": "08:00:00",
        "jumlah_orang": 4,
        "status": "menunggu"
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # buat reservation terlebih dahulu
        post_res = await ac.post("/reservation/", json=payload, headers=auth_header)
        assert post_res.status_code == 200
        created = post_res.json()
        assert "reservation_id" in created
        reservation_id = created["reservation_id"]

        # ambil reservation berdasarkan id
        get_res = await ac.get(f"/reservation/{reservation_id}", headers=auth_header)
        assert get_res.status_code == 200
        data = get_res.json()

        # cek isi data sesuai payload
        assert data["reservation_id"] == reservation_id
        assert data["user_id"] == payload["user_id"]
        assert data["meja_id"] == payload["meja_id"]
        assert data["tanggal_reservasi"] == payload["tanggal_reservasi"]
        assert data["jam_reservasi"] == payload["jam_reservasi"]
        assert data["jumlah_orang"] == payload["jumlah_orang"]
        assert data["status"] == payload["status"]

@pytest.mark.asyncio
async def test_patch_reservation_by_id(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        #buat data baru sebelum update
        payload = {
        "user_id":"c4b3075b-f0b4-4ad8-8f50-39bee8a3df65",
        "meja_id":19,
        "tanggal_reservasi": "2025-11-17",
        "jam_reservasi": "12:00:00",
        "jumlah_orang": 4,
        "status": "menunggu"
        }
        old_data = await ac.post("/reservation/", json=payload, headers=auth_header)
        assert old_data.status_code == 200
        created_data = old_data.json()
        assert "reservation_id" in created_data
        reservation_id = created_data["reservation_id"]

        # payload untuk update (contoh: status)
        update_payload = {
            "status": "berhasil"
        }

        patch_res = await ac.patch(f"/reservation/{reservation_id}", json=update_payload, headers=auth_header)
        # tergantung implementasi API, bisa 200 atau 204; biasanya 200 dengan body yang berisi resource
        assert patch_res.status_code in (200, 204)

        if patch_res.status_code == 200:
            data = patch_res.json()
        else:
            # jika 204 No Content, ambil ulang resource untuk verifikasi
            get_res = await ac.get(f"/reservation/{reservation_id}", headers=auth_header)
            assert get_res.status_code == 200
            data = get_res.json()

        # cek perubahan sesuai update_payload
        assert data["reservation_id"] == reservation_id
        assert data["status"] == update_payload["status"]

@pytest.mark.asyncio
async def test_delete_reservation(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        
        payload = {
            "user_id": "c4b3075b-f0b4-4ad8-8f50-39bee8a3df65",
            "meja_id": 20,
            "tanggal_reservasi": "2025-11-17",
            "jam_reservasi": "12:00:00",
            "jumlah_orang": 4,
            "status": "menunggu"
        }

        # Create reservation
        response = await ac.post("/reservation/", json=payload, headers=auth_header)
        assert response.status_code == 200
        created = response.json()
        reservation_id = created["reservation_id"]

        # Delete reservation (FIX: add headers and trailing slash consistency)
        delete_response = await ac.delete(
            f"/reservation/{reservation_id}",
            headers=auth_header
        )
        print(delete_response.text)
        assert delete_response.status_code == 204