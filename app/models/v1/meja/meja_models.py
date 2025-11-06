from pydantic import BaseModel, Field, EmailStr, StringConstraints, ConfigDict
from typing import Optional, Annotated
from enum import Enum

class MejaBase(BaseModel):
    """Model Awal Meja"""
    kode_meja: str = Field(..., description="Kode unik untuk meja")
    kapasitas: int = Field(..., description="Kapasitas maksimum meja")
    lokasi: str = Field(..., description="Lokasi meja di restoran")

class MejaCreate(MejaBase):
    """Model untuk membuat meja baru"""
    pass

class MejaResponse(BaseModel):
    """Model untuk memberikan response meja"""
    meja_id: int = Field(..., description="ID unik untuk meja")
    
    model_config = ConfigDict(from_attributes=True)
    
class MejaUpdate(BaseModel):
    kode_meja: Optional[str] = None
    kapasitas: Optional[int] = None
    lokasi: Optional[str] = None

class MejaDeleteResponse(BaseModel):
    detail: str
    data: MejaResponse

    class ConfigDict:
        from_attributes = True