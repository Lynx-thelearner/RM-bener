from orm_models import User
from app.core.auth import get_current_admin, get_current_user, get_current_petugas
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.v1.feedback import (
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackResponse,
)
from app.api.v1.feedback import feedback_service

router = APIRouter(tags=["Feedback"])


""" GET /feedback = semua feedback """
@router.get("/", response_model=list[FeedbackResponse])
def list_feedback(db: Session = Depends(get_db)):
    return feedback_service.get_all_feedback(db)


""" GET /feedback/{id} = detail feedback """
@router.get("/{id}", response_model=FeedbackResponse)
def get_feedback(id: int, db: Session = Depends(get_db),
                 current_petugas = Depends(get_current_petugas)
                 ):
    feedback = feedback_service.get_feedback_by_id(db, id)
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
@router.put("/{id}", response_model=FeedbackResponse)
def update_feedback(id: int, feedback_update: FeedbackUpdate, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)
                    ):
    updated_feedback = feedback_service.update_feedback(db, id, feedback_update, current_user.id)
    if not updated_feedback:
        raise HTTPException(status_code=404, detail="Feedback tidak ditemukan atau Anda tidak memiliki izin untuk memperbarui feedback ini")
    return updated_feedback


""" DELETE /feedback/{id} = hapus feedback """
@router.delete("/{id}", response_model=FeedbackResponse)
def delete_feedback(id: int, db: Session = Depends(get_db), 
                    current_admin: User= Depends (get_current_admin)
                    ):
    deleted_feedback = feedback_service.delete_feedback(db, id)
    if not deleted_feedback:
        raise HTTPException(status_code=404, detail="Feedback tidak ditemukan")
    return deleted_feedback