from sqlalchemy.orm import Session
from app.models.v1.user.user_model import (
    UserCreate,
    UserUpdate,
    UserRegis
)
from sqlalchemy.dialects.postgresql import UUID
from orm_models import User
from app.core.security import hash_password
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(UserCreate.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

""" Function untuk ambil data user """
def get_all_user(db: Session):
    return db.query(User).all()


""" Function untuk ambil data user berdasarkan ID """
def get_user_by_id(db: Session, user_id: UUID):
    return db.query(User).filter(User.user_id == user_id).first()


""" Function untuk tambah data user """
def create_user(db: Session, user: UserCreate):
    new_user_data = user.model_dump()
    new_user_data["password"] = hash_password(new_user_data["password"])
    
    new_user = User(**new_user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_register(db: Session, user: UserRegis):
    new_user_data = user.model_dump()
    new_user_data["password"] = hash_password(new_user_data["password"])
    new_user_data["role"] = "customer" 
    new_user = User(**new_user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


    """===================================================================================="""
    
""" Function untuk update data user """
def update_user(db: Session, user_id: UUID, user_update: UserUpdate):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in  update_data is not None:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


""" Function untuk hapus data user """
def delete_and_return_user(db: Session, user_id: UUID):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return None
    # simpan dulu datanya
    deleted_user = user
    db.delete(user)
    db.commit()
    return deleted_user