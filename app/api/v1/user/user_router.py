from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.v1.user.user_model import  UserCreate,  UserUpdate,  UserResponse
from app.api.v1.user import user_service
from orm_models import User, UserRole
from app.core.auth import get_current_user, require_role
from uuid import UUID

router = APIRouter( tags=["User"], prefix="/user")

"""=============================PROFILE TERITORI====================================="""
@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user



@router.patch("/profile", response_model=UserResponse)
def update_profile(user_update: UserUpdate, db: Session= Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_user = user_service.update_user(db, current_user.user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return updated_user

"""=============================PROFILE TERITORI====================================="""


""" GET /user = daftar user """
@router.get("/", response_model=list[UserResponse])
def list_user(db: Session = Depends(get_db),
               user: User = Depends(require_role(UserRole.admin))
               ):
    return user_service.get_all_user(db)

""" GET /user/{id} = detail user """
@router.get("/{id}", response_model=UserResponse)
def get_user(id:UUID, db: Session = Depends(get_db),
              current_manager: User= Depends(require_role(UserRole.manager, UserRole.admin))
              ):
    user = user_service.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return user


""" POST /user = tambah user"""
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db),
                current_admin: User = Depends(require_role(UserRole.admin))
                 
                 ):
    return user_service.create_user(db, user)



""" PUT /user/{id} = update user"""
@router.patch("/{id}", response_model=UserResponse)
def update_user(id: UUID, user: UserUpdate, db: Session = Depends(get_db),
                 current_admin: User = Depends(require_role(UserRole.admin))
                 ):
    updated_user = user_service.update_user(db, id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return updated_user



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: UUID, db: Session = Depends(get_db),
                 current_admin: User = Depends(require_role(UserRole.admin))):
    deleted_user = user_service.delete_and_return_user(db, id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return Response(status_code=status.HTTP_204_NO_CONTENT)