from sqlalchemy.orm import Session
from app.models.v1.meja.meja_models import (         
    MejaCreate,   
    MejaUpdate,   
)
from orm_models import Meja


def get_all_meja(db: Session):
    """Service functions untuk meja"""
    return db.query(Meja).all()

def get_available_meja(db: Session):
    """Service function untuk mendapatkan semua meja yang tersedia"""
    available_meja = db.query(Meja).filter(Meja.status == "tersedia").all()
    return available_meja

def check_available_meja(db: Session):
    """Function untuk ngecek apakah ada meja yang tersedia"""
    available_meja = db.query(Meja).filter(Meja.status == "tersedia").all()
    if not available_meja:
        return {
            "available": False,
            "message": "Tidak ada meja yang tersedia saat ini",
            "data": []
        }
    return available_meja



def get_meja_by_kode_meja(db: Session, kode_meja: str):
    """Helper function untuk mendapatkan meja berdasarkan kode_meja"""
    return db.query(Meja).filter(Meja.kode_meja == kode_meja).first()


def create_meja(db: Session, meja: MejaCreate):
    """Function untuk menambah meja baru"""
    new_meja = Meja(**meja.model_dump())
    db.add(new_meja)

    """ check apakah kode meja yang diinput sudah ada atau belum, jika sudah ada maka return pesan "table number sudah ada" """
    existing_meja = db.query(Meja).filter(Meja.kode_meja == meja.kode_meja).first()
    if existing_meja:
        raise ValueError("Kode Meja sudah ada")

    db.commit()
    db.refresh(new_meja)
    return new_meja


def update_meja(db: Session, kode_meja: str, meja_update: MejaUpdate):
    """Function untuk mengupdate data meja"""
    meja = get_meja_by_kode_meja(db, kode_meja)
    if not meja:
        return None

    update_data = meja_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(meja, key, value)

    db.commit()
    db.refresh(meja)
    return meja


def delete_and_return_meja(db: Session, kode_meja: str):
    """Function untuk menghapus meja"""
    meja = get_meja_by_kode_meja(db, kode_meja)
    if not meja:
        return None

    db.delete(meja)
    db.commit()
    return meja