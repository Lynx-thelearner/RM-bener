from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.v1.payment.payment_model import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse,
)
from app.api.v1.payment import payment_service
from orm_models import User
from app.core.auth import get_current_admin, get_current_user, get_current_manager, get_current_petugas

router = APIRouter( tags=["Payment"], prefix="/payment")


""" GET /payment = semua pembayaran """
@router.get("/", response_model=list[PaymentResponse])
def list_payments(db: Session = Depends(get_db),
                  current_manager: User = Depends(get_current_manager)
                  ):
    return payment_service.get_all_payments(db)


""" GET /payment/{id} = detail pembayaran berdasarkan id"""
@router.get("/{id}", response_model=PaymentResponse)
def get_payment(id: int, db: Session = Depends(get_db),
                current_manager: User = Depends(get_current_manager)
                ):
    payment = payment_service.get_payment_by_id(db, id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment tidak ditemukan")
    return payment


""" POST /payment = buat pembayaran baru """
@router.post("/", response_model=PaymentResponse, status_code=201)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db),
                   current_petugas = Depends(get_current_petugas)
                   ):
    return payment_service.create_payment(db, payment)


""" PUT /payment/{id} = update pembayaran """
@router.patch("/{id}", response_model=PaymentResponse)
def update_payment(id: int, payment: PaymentUpdate, db: Session = Depends(get_db),
                   current_petugas = Depends(get_current_petugas)
                   ):
    updated_payment = payment_service.update_payment(db, id, payment)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment tidak ditemukan")
    return updated_payment


""" DELETE /payment/{id} = hapus pembayaran """
@router.delete("/{id}", response_model=PaymentResponse)
def delete_payment(id: int, db: Session = Depends(get_db),
                   current_admin: User = Depends(get_current_admin)
                   ):
    deleted_payment = payment_service.delete_payment(db, id)
    if not deleted_payment:
        raise HTTPException(status_code=404, detail="Payment tidak ditemukan")
    return deleted_payment