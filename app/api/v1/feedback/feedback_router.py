from orm_models import User
from app.core.auth import get_current_admin, get_current_user, get_current_waiter
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.v1.feedback.feedback_models import (
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackResponse,
)
from app.api.v1.feedback import feedback_service

router = APIRouter(tags=["Feedback"], prefix="/feedback")


""" GET /feedback = semua feedback """
@router.get("/", response_model=list[FeedbackResponse])
def list_feedback(db: Session = Depends(get_db)):
    return feedback_service.get_all_feedback(db)


""" GET /feedback/{id} = feedback berdasarkan id """
@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = feedback_service.get_feedback_by_id(db, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback tidak ditemukan")
    return feedback

""" POST /feedback = tambah feedback baru """
@router.post("/", response_model=FeedbackResponse, status_code=201)
def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)
                    ):
    return feedback_service.create_feedback(db, feedback)


""" PUT /feedback/{id} = update feedback berdasarkan feedback orang yg login """
@router.put("/{feedback_id}", response_model=FeedbackResponse)
def update_feedback(feedback_id: int, feedback_update: FeedbackUpdate, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)
                    ):
    updated_feedback = feedback_service.update_feedback(db, feedback_id, feedback_update, current_user.user_id)
    if not updated_feedback:
        raise HTTPException(status_code=404, detail="Feedback tidak ditemukan atau Anda tidak memiliki izin untuk memperbarui feedback ini")
    return updated_feedback


""" DELETE /feedback/{id} = hapus feedback """
@router.delete("/{feedback_id}", response_model=FeedbackResponse)
def delete_feedback(feedback_id: int, db: Session = Depends(get_db), 
                    current_admin: User= Depends (get_current_admin)
                    ):
    deleted_feedback = feedback_service.delete_feedback(db, feedback_id)
    if not deleted_feedback:
        raise HTTPException(status_code=404, detail="Feedback tidak ditemukan")
    return deleted_feedback
