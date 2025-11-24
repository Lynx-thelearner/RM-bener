from sqlalchemy.orm import Session
from app.models.v1.reservation.reservation_model import (
    ReservationCreate,
    ReservationUpdate,
)
from sqlalchemy.dialects.postgresql import UUID
from orm_models import Reservation, Meja, StatusMeja
from fastapi import HTTPException

""" Function untuk ambil data reservation """
def get_all_reservation(db: Session, skip: int = 0, limit: int = 10):
    return (
        db.query(Reservation).order_by(Reservation.reservation_id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

""" Function untuk ambil total count reservation """
def get_total_reservation_count(db: Session):
    return db.query(Reservation).count()

""""Buat ambil data reservasi berdasarkan user"""
def get_reservations_by_user(db: Session, current_user):
    return (
        db.query(Reservation).filter(Reservation.user_id == current_user.user_id).order_by(Reservation.reservation_id.desc()).all()
    )

""" Function untuk ambil data reservation berdasarkan ID """
def get_reservation_by_id(db: Session, reservation_id: int):
    return db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()

def create_reservation(request: ReservationCreate, db: Session):
    # cek apakah meja tersedia
    meja = db.query(Meja).filter(Meja.meja_id == request.meja_id).first()
    if not meja:
        raise HTTPException(status_code=404, detail="Meja tidak ditemukan")

    # cek status meja
    if meja.status is not StatusMeja.tersedia:
        print("REQUEST:", request.meja_id)
        print("MEJA QUERY RESULT:", meja)
        print("STATUS RAW:", repr(meja.status) if meja else None)

        raise HTTPException(status_code=400, detail="Meja tidak tersedia")

    # buat data reservasi
    new_reservation = Reservation(**request.model_dump())
    db.add(new_reservation)

    # ubah status meja
    meja.status = StatusMeja.tidaktersedia

    db.commit()
    db.refresh(new_reservation)
    return new_reservation



""" Function untuk update data reservation """
def update_reservation(db: Session, reservation_id: int, reservation_update: ReservationUpdate):
    reservation = db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()
    if reservation:
        for key, value in reservation_update.model_dump(exclude_unset=True).items():
            setattr(reservation, key, value)
        db.commit()
        db.refresh(reservation)
    return reservation

"""Function hapus data reservasi"""
def delete_reservation(db: Session, reservation_id: int):
    reservation = db.query(Reservation).filter(Reservation.reservation_id == reservation_id).first()
    if not reservation:
        return None
    db.delete(reservation)
    db.commit()
    return True

