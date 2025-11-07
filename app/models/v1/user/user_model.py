from pydantic import BaseModel, Field, EmailStr, StringConstraints, ConfigDict, field_validator
from typing import Optional, Annotated
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Tipe data untuk nomor telepon
Phone = Annotated[
    str,
    StringConstraints(
        pattern=r"^(?:\+62|0)8[1-9][0-9]{6,11}$",
        min_length=10,
        max_length=15,
    )
]

class RoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    reservationStaff = "reservationStaff"
    waiter = "waiter"
    customer = "customer"
    
class UserBase(BaseModel):
    """Model Awal"""
    nama: str = Field(..., description="Nama lengkap user")
    username: str = Field(..., description="Username unik untuk login", min_length=3, max_length=50)    
    no_telp: Phone = Field(..., description="Nomor telepon user")
    email: EmailStr = Field(..., examples=["user@example.com"], description="Alamat email user")
    role: RoleEnum = Field(..., description="Role user")
    
class UserCreate(UserBase):
    """Model untuk membuat user baru"""
    password: str = Field(..., min_length=8, max_length=72, description="Password untuk login user (Minimal 8 karakter)")
    
    @field_validator("password", mode="before")
    def validate_password_bytes(cls, v):
        v = v.strip()
        if len(v.encode('utf-8')) > 72:
            raise ValueError("Password terlalu panjang setelah di-encode, maksimal 72 bytes")
        return v
    
    
class UserResponse(UserBase):
    """Model untuk memberikan response"""
    id_user: uuid.UUID = Field(default_factory=uuid.uuid4, description="UUID unik untuk user")
    
    model_config = ConfigDict(from_attributes=True)
    
class UserUpdate(BaseModel):
    nama: Optional[str] = None
    username: Optional[str] = None
    no_telp: Optional[Phone] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[RoleEnum] = None
    
class UserRegis(BaseModel):
    nama: str = Field(..., description="Nama lengkap")
    username: str = Field(..., description="Username unik untuk login", max_length=50)
    no_telp: Phone = Field(..., description="Nomor Telpon")
    email: EmailStr = Field(..., examples=["user@example.com"], description="Alamat Email anda")
    password: str = Field(..., min_length=8, max_length=72, description="Password User (Minimal 8 Karakter)")
    
    @field_validator("password", mode="before")
    def validate_password_bytes(cls, v):
        v = v.strip()
        if len(v.encode('utf-8')) > 72:
            raise ValueError("Password terlalu panjang setelah di-encode, maksimal 72 bytes")
        return v

class DeleteUserResponse(BaseModel):
    message: str = Field(..., description="Pesan konfirmasi penghapusan user")
    
