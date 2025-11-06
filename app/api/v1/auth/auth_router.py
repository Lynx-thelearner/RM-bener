from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.auth import create_access_token
from app.core.deps import get_db
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.v1.user import user_service
from app.api.v1.auth import auth_service
from app.models.v1.user.user_model import UserCreate, UserRegis, UserResponse


router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

""" ================= UNIVERSAL LOGIN ================= """
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Universal login untuk Swagger (Customer & Staff)."""
    # coba login sebagai customer
    user = auth_service.authenticate_customer(db, form_data.username, form_data.password)
    if user:
        token = create_access_token({"id": user.user_id, "role": "customer"})
        return {"access_token": token, "token_type": "bearer"}

    # coba login sebagai staff
    user = auth_service.authenticate_staff(db, form_data.username, form_data.password)
    if user:
        token = create_access_token({"user_id": user.id, "role": user.role})
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid username or password")


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserRegis, db: Session = Depends(get_db)):
    return user_service.create_register(db, user)