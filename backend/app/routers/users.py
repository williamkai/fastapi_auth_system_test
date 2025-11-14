# backend/app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.dependencies import get_db, admin_required
from app.crud import user as crud_user
from app.schemas import user as schemas_user

router = APIRouter(tags=["Users"])

@router.get("/users", response_model=list[schemas_user.UserDetailOut])
def list_users(db: Session = Depends(get_db), _: schemas_user.UserOut = Depends(admin_required)):
    return crud_user.get_all_users(db)

@router.patch("/users/{user_id}/status")
def update_user_status_route(
    user_id: int,
    update: schemas_user.UserUpdateStatus,
    db: Session = Depends(get_db),
    _: schemas_user.UserOut = Depends(admin_required)
):
    db_user = crud_user.get_user_by_id(db, user_id) 
    if not db_user: 
        raise HTTPException(status_code=404, detail="User not found") 
    
    # 用 ORM 屬性存取
    if db_user.role == "admin":# type: ignore 
        raise HTTPException(status_code=403, detail="You cannot delete another admin")
    
    updated_user = crud_user.update_user_status(db, user_id, update.is_active)
    
    return {
        "id": updated_user.id,# type: ignore
        "username": updated_user.username,# type: ignore
        "is_active": updated_user.is_active# type: ignore
    }



@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: schemas_user.UserOut = Depends(admin_required)
):
    db_user = crud_user.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.role == "admin":# type: ignore
        raise HTTPException(status_code=403, detail="You cannot delete another admin")

    crud_user.delete_user(db, user_id)
    return {"detail": "User deleted"}
