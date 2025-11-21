from datetime import datetime
from sqlalchemy.orm import Session
from app.models.v1.feedback.feedback_models import (
    FeedbackCreate,
    FeedbackUpdate,
    
)
from orm_models  import Feedback


def get_all_feedback(db: Session):
    """Service function untuk mendapatkan semua feedback"""
    return db.query(Feedback).all()


def get_feedback_by_id(db: Session, feedback_id: int):
    """Helper function untuk mendapatkan feedback berdasarkan ID"""
    return db.query(Feedback).filter(Feedback.feedback_id == feedback_id).first()


def create_feedback(db: Session, feedback: FeedbackCreate):
    """Function untuk menambah feedback baru"""
    new_feedback = Feedback(
        feedback_date=datetime.now(),
        **feedback.model_dump(),
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback


def update_feedback(db: Session, feedback_id: int, feedback_update: FeedbackUpdate, current_user=None, **kwargs):
    """Function untuk mengupdate data feedback"""
    feedback = get_feedback_by_id(db, feedback_id)
    if not feedback:
        return None

    update_data = feedback_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(feedback, key, value)

    db.commit()
    db.refresh(feedback)
    return feedback


def delete_feedback(db: Session, feedback_id: int):
    """Function untuk menghapus feedback berdasarkan ID"""
    feedback = get_feedback_by_id(db, feedback_id)
    if not feedback:
        return None

    db.delete(feedback)
    db.commit()
    return feedback