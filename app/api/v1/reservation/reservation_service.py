from sqlalchemy.orm import Session
from app.models.v1.reservation.reservation_model import (
    ReservationCreate,
    ReservationUpdate,
    ReservationResponse
)
from sqlalchemy.dialects.postgresql import UUID
from orm_models import Reservation, Meja
from fastapi import HTTPException

""" Function untuk ambil data reservation """
def get_all_reservation(db: Session):
    return db.query(Reservation).all()

""" Function untuk ambil data reservation berdasarkan ID """
def get_reservation_by_id(db: Session, reservation_id: int):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

""""Fucntion buat ngampilkan data reservation berdasarkan yang login"""
def get_reservations_by_user(db: Session, current_user_id):
    return db.query(Reservation).filter(Reservation.user_id == current_user_id.user_id).order_by(Reservation.reservation_id.desc()).all()

""" Function untuk tambah data reservation """
def create_reservation(db: Session, reservation: ReservationCreate):
    #buat ngecek apakah mejanya tersedia atau tidak
    meja = db.query(Meja).filter(Meja.kode_meja == reservation.kode_meja).first()
    if not meja:
        raise HTTPException(status_code=404, detail="meja tidak ditemukan")
    
    #buat ngecek statusnya
    if meja.status != "tersedia":
        raise HTTPException(status_code=400, detail="Meja tidak tersedia")
    
    #buat data reservasi
    new_reservation = Reservation(**reservation.model_dump())
    db.add(new_reservation)
    
    #ubah status mejanya
    meja.status = "tidak tersedia"
    
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

""" Function untuk update data reservation """
def update_reservation(db: Session, reservation_id: int, reservation_update: ReservationUpdate):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if reservation:
        for key, value in reservation_update.model_dump(exclude_unset=True).items():
            setattr(reservation, key, value)
        db.commit()
        db.refresh(reservation)
    return reservation

"""Function hapus data reservasi"""
def delete_reservation(db: Session, reservation_id: int):
    reservation = db.query(Reservation).filter(reservation.id == reservation_id).first()
    if not reservation:
        return None
    #Simpan datanya
    deleted_reservation = reservation
    db.delete(reservation)
    db.commit()
    return deleted_reservation