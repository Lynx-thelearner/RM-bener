from sqlalchemy.orm import Session
from app.models.v1.payment.payment_model import (
    PaymentCreate
    , PaymentResponse,
    PaymentUpdate
)
from orm_models import Payment

""" Fungsi untuk operasi pengambilan data pembayaran """
def get_all_payments(db: Session):
    return db.query(Payment).all()


""" Fungsi untuk mendapatkan pembayaran berdasarkan ID """
def get_payment_by_id(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()


""" Fungsi untuk membuat pembayaran baru """
def create_payment(db: Session, payment: PaymentCreate):
    new_payment = Payment(**payment.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


""" Fungsi untuk memperbarui pembayaran """
def update_payment(db: Session, payment_id: int, payment_update: PaymentUpdate):
    payment = get_payment_by_id(db, payment_id)
    if not payment:
        return None

    update_data = payment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)
    return payment


""" Fungsi untuk menghapus pembayaran """
def delete_payment(db: Session, payment_id: int):
    payment = get_payment_by_id(db, payment_id)
    if not payment:
        return None

    db.delete(payment)
    db.commit()
    return payment