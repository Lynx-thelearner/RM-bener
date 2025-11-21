"""Endpoint Test On Payment router"""

import pytest
from fastapi import status
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_create_payment(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        #data pembayaran yang mau dikirim
        payload = {
  "reservation_id": 1,
  "amount": 100,
  "payment_date": "2025-11-17T06:35:50.228Z",
  "status": "menunggu"
}
        respon = await ac.post("/payment/", json=payload, headers=auth_header)
        assert respon.status_code == 201
        data = respon.json()

        assert data ["reservation_id"] == payload ["reservation_id"]
        assert data ["amount"] == payload ["amount"]
        assert data ["payment_date"] == payload ["payment_date"]
        assert data ["status"] == payload ["status"]
        assert "payment_id" in data
   
@pytest.mark.asyncio
async def test_get_payment_by_id(auth_header):
    transport = ASGITransport(app=app)
    #payloadnya terlebih dahulu dibuat baru dicari
    payload = {
        "reservation_id": 2,
        "amount": 150.0,
        "payment_date": "2025-11-18T05:59:54.408Z",
        "status": "berhasil"
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        #membuat payment baru
        create_respon = await ac.post("/payment/", json=payload, headers=auth_header)
        assert create_respon.status_code == 201
        created_data = create_respon.json()
        payment_id = created_data["payment_id"]

        #mengambil payment berdasarkan id
        get_respon = await ac.get(f"/payment/{payment_id}", headers=auth_header)
        assert get_respon.status_code == 200
        get_data = get_respon.json()

        assert get_data ["payment_id"] == payment_id
        assert get_data ["reservation_id"] == payload ["reservation_id"]
        assert get_data ["amount"] == payload ["amount"]
        assert get_data ["payment_date"] == payload ["payment_date"]
        assert get_data ["status"] == payload ["status"]



@pytest.mark.asyncio
async def test_update_payment(auth_header):
    transport = ASGITransport(app=app)
    #payloadnya terlebih dahulu dibuat baru diupdate
    payload = {
        "reservation_id": 6,
        "amount": 200.0,
        "payment_date": "2025-11-19T05:59:54.408Z", 
        "status": "menunggu"
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # buat payment terlebih dahulu
        post_res = await ac.post("/payment/", json=payload, headers=auth_header)
        assert post_res.status_code == 201
        created = post_res.json()
        assert "payment_id" in created
        payment_id = created["payment_id"]

        # update payment berdasarkan id
        update_payload = {
            "amount": 250.0,
            "status": "berhasil"
        }
        patch_res = await ac.patch(f"/payment/{payment_id}", json=update_payload, headers=auth_header)
        assert patch_res.status_code == 200
        updated_data = patch_res.json()

        # cek isi data sesuai payload update
        assert updated_data["payment_id"] == payment_id
        assert updated_data["amount"] == update_payload["amount"]
        assert updated_data["status"] == update_payload["status"]
        # memastikan field yang tidak diupdate tetap sama
        assert updated_data["payment_date"] == payload["payment_date"]
        assert updated_data["reservation_id"] == payload["reservation_id"]

@pytest.mark.asyncio
async def test_delete_payment(auth_header):
    transport = ASGITransport(app=app)
    #payloadnya terlebih dahulu dibuat baru dihapus
    payload = {
        "reservation_id": 9,
        "amount": 300.0,
        "payment_date": "2025-11-20T05:59:54.408Z",
        "status": "gagal"
    }
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # buat payment terlebih dahulu
        post_res = await ac.post("/payment/", json=payload, headers=auth_header)
        assert post_res.status_code == 201
        created = post_res.json()
        assert "payment_id" in created
        payment_id = created["payment_id"]

        # hapus payment berdasarkan id
        delete_res = await ac.delete(f"/payment/{payment_id}",  headers=auth_header)
        assert delete_res.status_code == 200
        deleted_data = delete_res.json()

        # cek data yang dihapus sesuai dengan yang dibuat
        assert deleted_data["payment_id"] == payment_id
        assert deleted_data["reservation_id"] == payload["reservation_id"]
        assert deleted_data["amount"] == payload["amount"]
        assert deleted_data["payment_date"] == payload["payment_date"]
        assert deleted_data["status"] == payload["status"]

        # pastikan data sudah tidak ada lagi
        get_res = await ac.get(f"/payment/{payment_id}", headers=auth_header)
        assert get_res.status_code == 404

@pytest.mark.asyncio
async def test_list_payments(auth_header):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        respon = await ac.get("/payment/", headers=auth_header)
        assert respon.status_code == 200
        data = respon.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "amount" in data [0]
            assert "payment_date" in data [0]
            assert "status" in data [0]
            assert "reservation_id" in data [0]
            assert "payment_id" in data [0]