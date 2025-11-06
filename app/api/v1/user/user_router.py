from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.v1.user.user_model import  UserCreate,  UserUpdate,  UserResponse, DeleteUserResponse
from app.api.v1.user import user_service
from orm_models import User
from app.core.auth import get_current_user, get_current_admin, get_current_manager, get_current_petugas, get_current_reservationStaff
from uuid import UUID

router = APIRouter( tags=["User"])



""" GET /user = daftar user """
@router.get("/", response_model=list[UserResponse])
def list_user(db: Session = Depends(get_db),
               user: User = Depends(get_current_manager)
               ):
    return user_service.get_all_user(db)
"""=============================PROFILE TERITORI====================================="""
@router.get("/profile/", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user



@router.patch("/profile/", response_model=UserResponse)
def update_profile(user_update: UserUpdate, db: Session= Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_user = user_service.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return updated_user

"""=============================PROFILE TERITORI====================================="""



""" GET /user/{uuid} = detail user """
@router.get("/{uuid}", response_model=UserResponse)
def get_user(id:UUID, db: Session = Depends(get_db),
              current_manager: User= Depends(get_current_manager)
              ):
    user = user_service.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return user


""" POST /user = tambah user"""
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db),
                 current_admin: User = Depends(get_current_admin)
                 ):
    return user_service.create_user(db, user)



""" PUT /user/{uuid} = update user"""
@router.patch("/{uuid}", response_model=UserResponse)
def update_user(id: UUID, user: UserUpdate, db: Session = Depends(get_db),
                 current_admin: User = Depends(get_current_admin)
                 ):
    updated_user = user_service.update_user(db, id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return updated_user



@router.delete("/{uuid}", response_model=DeleteUserResponse)
def delete_user(id: UUID, db: Session = Depends(get_db),
                 current_admin: User = Depends(get_current_admin)):
    deleted_user = user_service.delete_and_return_user(db, id)
    if deleted_user:
        return {
            "detail": "User deleted successfully",
            "data": deleted_user
        }
    raise HTTPException(status_code=404, detail="User tidak ditemukan")