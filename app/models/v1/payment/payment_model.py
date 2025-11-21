from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum

class PaymentStatusEnum(str, Enum):
    menunggu = "menunggu"
    berhasil = "berhasil"
    gagal = "gagal"
    
class PaymentBase(BaseModel):
    reservation_id: int = Field(..., description="ID unik untuk reservasi yang dibayar")
    amount: float = Field(..., description="Jumlah pembayaran")
    payment_date: datetime = Field(..., description="Tanggal pembayaran dalam format YYYY-MM-DD")
    status: PaymentStatusEnum = Field(..., description="Status pembayaran")
  

class PaymentCreate(PaymentBase):
    """Model untuk membuat pembayaran baru"""
    pass

class PaymentUpdate(BaseModel):
    """Schema untuk update data payment"""
    reservation_id: int | None = None
    amount: float | None = None
    status: PaymentStatusEnum | None = None
    payment_date: datetime | None = None

class PaymentResponse(PaymentBase):
    """Model untuk memberikan response pembayaran"""
    payment_id: int = Field(..., description="UUID unik untuk pembayaran")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat(timespec="milliseconds") + "Z"
        }
    )

