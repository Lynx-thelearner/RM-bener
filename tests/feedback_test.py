""" Endpoint tests for feedback  Routes """
from httpx import AsyncClient, ASGITransport
import pytest
from main import app


@pytest.mark.asyncio
async def test_create_feedback(auth_header):
    transport = ASGITransport(app=app)
    # data feedback yang mau dikirim
    payload = {
        "user_id": "87be1754-1213-42b4-9caa-632d1879050a",
        "reservation_id":1,
        "rating": 5,
        "comments": "Pelayanan sangat baik dan makanan lezat!"
    
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Endpoint untuk feedback
        respon = await ac.post("/feedback/", json=payload, headers=auth_header)
        assert respon.status_code == 201
        data = respon.json()

        assert data["user_id"] == payload["user_id"]
        assert data["reservation_id"] == payload["reservation_id"]
        assert data["rating"] == payload["rating"]
        assert data["comments"] == payload["comments"]
        assert "feedback_id" in data

@pytest.mark.asyncio
async def test_get_all_feedback(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # endpoint ambil semua feedback
        respon = await ac.get("/feedback/", headers=auth_header)
        assert respon.status_code == 200
        data = respon.json()

        # buat data dalam bentuk list
        assert isinstance(data, list)
        # minimal satu data
        assert len(data) >= 1
        # ngecek apa yang di return
        assert "feedback_id" in data[0]
        assert "user_id" in data[0]
        assert "reservation_id" in data[0]
        assert "rating" in data[0]
        assert "comments" in data[0]

@pytest.mark.asyncio
async def test_get_feedback_by_id(auth_header):
    transport = ASGITransport(app=app)
    # payloadnya terlebih dahulu dibuat baru dicari
    payload = {
        "user_id": "87be1754-1213-42b4-9caa-632d1879050a",
        "reservation_id":2,
        "rating": 4,
        "comments": "Makanan enak tapi pelayanannya bisa ditingkatkan."
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Membuat feedback baru
        create_respon = await ac.post("/feedback/", json=payload, headers=auth_header)
        assert create_respon.status_code == 201
        created_data = create_respon.json()
        feedback_id = created_data["feedback_id"]

        # Mengambil feedback berdasarkan ID
        get_respon = await ac.get(f"/feedback/{feedback_id}", headers=auth_header)
        assert get_respon.status_code == 200
        data = get_respon.json()

        assert data["feedback_id"] == feedback_id
        assert data["user_id"] == payload["user_id"]
        assert data["reservation_id"] == payload["reservation_id"]
        assert data["rating"] == payload["rating"]
        assert data["comments"] == payload["comments"]

@pytest.mark.asyncio
async def test_update_feedback(auth_header):
    transport = ASGITransport(app=app)
    # payloadnya terlebih dahulu dibuat baru diupdate
    payload = {
        "user_id": "87be1754-1213-42b4-9caa-632d1879050a",
        "reservation_id":6,
        "rating": 3,
        "komentar": "Rata-rata saja."
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Membuat feedback baru
        create_respon = await ac.post("/feedback/", json=payload, headers=auth_header)
        assert create_respon.status_code == 201
        created_data = create_respon.json()
        feedback_id = created_data["feedback_id"]

        # Data update feedback
        update_payload = {
            "rating": 4,
            "comments": "Setelah dipikir-pikir, cukup baik."
        }

        # Mengupdate feedback berdasarkan ID
        update_respon = await ac.put(f"/feedback/{feedback_id}", json=update_payload, headers=auth_header)
        assert update_respon.status_code == 200
        data = update_respon.json()

        assert data["feedback_id"] == feedback_id
        assert data["rating"] == update_payload["rating"]
        assert data["comments"] == update_payload["comments"]

@pytest.mark.asyncio
async def test_delete_feedback(auth_header):
    transport = ASGITransport(app=app)
    # payloadnya terlebih dahulu dibuat baru dihapus
    payload = {
        "user_id": "87be1754-1213-42b4-9caa-632d1879050a",
        "reservation_id":9,
        "rating": 2,
        "comments": "Perlu banyak perbaikan."

    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Membuat feedback baru
        create_respon = await ac.post("/feedback/", json=payload, headers=auth_header)
        assert create_respon.status_code == 201
        created_data = create_respon.json()
        feedback_id = created_data["feedback_id"]

        # Menghapus feedback berdasarkan ID
        delete_respon = await ac.delete(f"/feedback/{feedback_id}", headers=auth_header)
        assert delete_respon.status_code == 200
        data = delete_respon.json()

        assert data["feedback_id"] == feedback_id

        # Verifikasi bahwa feedback telah dihapus
        get_respon = await ac.get(f"/feedback/{feedback_id}", headers=auth_header)
        assert get_respon.status_code == 404

