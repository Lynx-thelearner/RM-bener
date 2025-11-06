from sqlalchemy.orm import Session
from app.models.v1.reservation.reservation_model import (
    ReservationCreate,
    ReservationUpdate,
    ReservationResponse
)
from sqlalchemy.dialects.postgresql import UUID
from orm_models import Reservation

""" Function untuk ambil data reservation """
def get_all_reservation(db: Session):
    return db.query(Reservation).all()

""" Function untuk ambil data reservation berdasarkan ID """
def get_reservation_by_id(db: Session, reservation_id: int):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

""" Function untuk tambah data reservation """
def create_reservation(db: Session, reservation: ReservationCreate):
    new_reservation = Reservation(**reservation.model_dump())
    db.add(new_reservation)
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
    return delete_reservation