""" Auth.py Berisikan Functions yang menhandle autentikasi, jwt"""
from uuid import UUID
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from orm_models import User
from sqlalchemy.orm import Session
from app.core.deps import get_db
from dotenv import load_dotenv
import os
from orm_models import UserRole
#==========================Config==============================

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

class TokenData(BaseModel):
    user_id: UUID
    role: Optional[UserRole] = None

#===============================JWT FUNCTION ==================================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    # konversi semua UUID dalam data ke string
    for key, value in to_encode.items():
        if isinstance(value, UUID):
            to_encode[key] = str(value)

    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        role = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception

        # konversi kembali ke UUID
        try:
            user_id = UUID(user_id)
        except ValueError:
            raise credentials_exception

        return TokenData(user_id=user_id, role=UserRole(role))
    except JWTError:
        raise credentials_exception


""" ================= ROLE CHECK DEPENDENCY ================= """
def require_role(*allowed_roles: str):
    """
    Dependency reusable untuk membatasi akses endpoint berdasarkan role.
    """
    def dependency(token_data: TokenData = Depends(verify_token)):
        if token_data.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return token_data
    return dependency


""" ================= OPTIONAL HELPER ================= """
""" Mengambil user yang sedang login universal"""
def get_current_user(
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(verify_token)
):
    user = db.query(User).filter(User.user_id == token_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

def get_current_admin(current_user: User = Depends(get_current_user)):
    print(current_user.role)
    if current_user.role != UserRole.admin :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya user dengan role admin yang boleh mengakses"
        )
    return current_user


""" Mengambil user yang sedang login dan harus manager atau admin"""
def get_current_manager(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya user dengan role manager atau admin yang boleh mengakses"
        )
    return current_user

def get_current_reservationStaff(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.admin, UserRole.manager, UserRole.reservationStaff]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya user dengan role reservationStaff, manager atau admin yang boleh mengakses"
        )
    return current_user


"""" Mengambil user yang sedang login dan harus petugas (admin, manager, reservationStaff, waiter)"""
def get_current_petugas(current_user: User = Depends(get_current_user)):
    if current_user.role == [UserRole.admin, UserRole.manager, UserRole.reservationStaff, UserRole.waiter]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Hanya user dengan role dari petugas yang boleh mengakses"
        )
    return current_user