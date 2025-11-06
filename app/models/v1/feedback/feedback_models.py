from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date
from decimal import Decimal
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class Feedback(BaseModel):
    user_id: UUID = Field(..., description="UUID unik untuk user yang memberikan feedback")
    reservation_id: str = Field(..., description="ID unik untuk reservasi yang diberikan feedback")
    rating: int = Field(..., ge=1, le=5, description="Rating feedback dari 1 hingga 5")
    comments: Optional[str] = Field(None, description="Komentar tambahan untuk feedback")
    feedback_date: date = Field(..., description="Tanggal feedback dalam format YYYY-MM-DD")
    
class FeedbackCreate(Feedback):
    """Model untuk membuat feedback baru"""
    pass

class FeedbackResponse(Feedback):
    """Model untuk memberikan response feedback"""
    id: str = Field(..., description="UUID unik untuk feedback")
    
    model_config = ConfigDict(from_attributes=True)
    
class FeedbackUpdate(BaseModel):
    user_id: Optional[UUID] = Field(None, description="UUID unik untuk user yang memberikan feedback")
    reservation_id: Optional[str] = Field(None, description="ID unik untuk reservasi yang diberikan feedback")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating feedback dari 1 hingga 5")
    comments: Optional[str] = Field(None, description="Komentar tambahan untuk feedback")
    feedback_date: Optional[date] = Field(None, description="Tanggal feedback dalam format YYYY-MM-DD")