from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date
from decimal import Decimal
from enum import Enum

class PaymentStatusEnum(str, Enum):
    menunggu = "menunggu"
    berhasil = "berhasil"
    gagal = "gagal"
    
class PaymentBase(BaseModel):
    reservation_id: str = Field(..., description="ID unik untuk reservasi yang dibayar")
    amount: float = Field(..., description="Jumlah pembayaran")
    payment_date: date = Field(..., description="Tanggal pembayaran dalam format YYYY-MM-DD")
    status: PaymentStatusEnum = Field(..., description="Status pembayaran")
    
class PaymentCreate(PaymentBase):
    """Model untuk membuat pembayaran baru"""
    pass

class PaymentResponse(PaymentBase):
    """Model untuk memberikan response pembayaran"""
    id: str = Field(..., description="UUID unik untuk pembayaran")
    
    model_config = ConfigDict(from_attributes=True)
    