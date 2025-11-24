from fastapi import APIRouter, HTTPException, Depends, Response, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.v1.reservation.reservation_model import ReservationCreate, ReservationResponse, ReservationUpdate
from app.api.v1.reservation import reservation_service
from app.core.auth import require_role, get_current_user
from pydantic import BaseModel
from orm_models import User, UserRole

class PaginationResponse(BaseModel):
    data: list[ReservationResponse]
    total: int
    skip: int
    limit: int


router = APIRouter(
    prefix="/reservation",
    tags=["Reservation"]
)

""""Get /reservation = semua data reservasi dengan pagination"""
@router.get("/", response_model=PaginationResponse)
def get_all_reservation(
    db: Session = Depends(get_db),
    current_waiter = Depends(require_role(UserRole.waiter, UserRole.reservationStaff, UserRole.manager, UserRole.admin)),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    reservations = reservation_service.get_all_reservation(db, skip=skip, limit=limit)
    total = reservation_service.get_total_reservation_count(db)
    
    return {
        "data": reservations,
        "total": total,
        "skip": skip,
        "limit": limit
    }
    

""""Get by ID"""
@router.get("/id/{reservation_id}", response_model=ReservationResponse)
def get_reservation(reservation_id: int, db: Session = Depends(get_db),
                    current_waiter = Depends(require_role(UserRole.waiter, UserRole.reservationStaff, UserRole.manager, UserRole.admin))):
    return reservation_service.get_reservation_by_id(db, reservation_id)


""""Buat bikin data reservasi"""
@router.post("/", response_model=ReservationResponse)
def create_reservation(request:ReservationCreate ,db: Session = Depends(get_db),
                       current_user = Depends(get_current_user)):
    return reservation_service.create_reservation(request, db)
    
""""Update data reservasi"""
@router.patch("/id/{reservation_id}", response_model=ReservationResponse)
def update_reservation(reservation_id: int, request: ReservationUpdate, db: Session = Depends(get_db),
                       current_user = Depends(get_current_user)):
    return reservation_service.update_reservation(db, reservation_id, request)

@router.get("/me")
def get_my_reservations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reservations = reservation_service.get_reservations_by_user(db, current_user)
    return {"status": "success", "data": reservations}

""""Delete data reservasi"""
@router.delete("/id/{reservation_id}", status_code=204)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db),
                       current_admin = Depends(require_role(UserRole.admin))):
    deleted = reservation_service.delete_reservation(db, reservation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return Response(status_code=204)
                     