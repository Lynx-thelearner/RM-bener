from pydantic import BaseModel, Field, EmailStr, StringConstraints, ConfigDict, datetime_parse
from typing import Optional, Annotated
from enum import Enum
from sqlalchemy import Time
from sqlalchemy.dialects.postgresql import UUID
from datetime import date,time
import uuid

class ReservationStatusEnum(str, Enum):
    menunggu = "menunggu"
    berhasil = "berhasil"
    dibatalkan = "dibatalkan"
    
class ReservationBase(BaseModel):
    """Model Awal Reservasi"""
    user_id: uuid.UUID = Field(..., description="UUID unik untuk user yang melakukan reservasi")
    meja_id: int = Field(..., description="ID unik untuk meja yang dipesan")
    tanggal_reservasi: str  = Field(..., description="Tanggal reservasi dalam format YYYY-MM-DD")
    jam_reservasi: str = Field(..., description="Jam reservasi dalam format HH:MM:SS")
    jumlah_orang: int = Field(..., description="Jumlah orang untuk reservasi")
    status: ReservationStatusEnum = Field(..., description="Status reservasi")

class ReservationCreate(ReservationBase):
    """Model untuk membuat reservasi baru"""
    pass

class ReservationResponse(BaseModel):
    reservation_id: int
    tanggal_reservasi: date
    jam_reservasi: time
    user_id: uuid.UUID
    meja_id: int
    jumlah_orang: int
    status: ReservationStatusEnum

    class Config:
        from_attributes = True 
    
class ReservationUpdate(BaseModel):
    user_id: Optional[str] = None
    meja_id: Optional[int] = None
    tanggal_reservasi: Optional[str] = None
    jam_reservasi: Optional[str] = None
    jumlah_orang: Optional[int] = None
    status: Optional[ReservationStatusEnum] = None