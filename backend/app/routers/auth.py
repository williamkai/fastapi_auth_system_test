# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies.dependencies import get_db
from app.crud import user as crud_user
from app.schemas import user as schemas_user
from app.auth.auth import create_access_token, create_refresh_token, verify_password
from typing import Optional
from jose import jwt, JWTError
from app.core.config import settings
import os

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM

router = APIRouter(tags=["Auth"])

@router.post("/register", response_model=schemas_user.UserOut)
def register(user: schemas_user.UserCreate, db: Session = Depends(get_db)):
    if crud_user.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = crud_user.create_user(db, **user.model_dump())
    return new_user


@router.post("/login", response_model=schemas_user.Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = crud_user.get_user_by_username(db, form_data.username)
    # 帳號不存在
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    # 密碼錯誤
    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    # 帳號被停用
    if not bool(db_user.is_active):
        raise HTTPException(status_code=403, detail="User account is disabled")
    
    access_token = create_access_token({"sub": db_user.username, "role": db_user.role})
    refresh_token = create_refresh_token({"sub": db_user.username, "role": db_user.role})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=schemas_user.Token)
def refresh_token(token_data: schemas_user.RefreshTokenRequest, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid refresh token")
    try:
        payload = jwt.decode(token_data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        role: Optional[str] = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 查資料庫
    db_user = crud_user.get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not bool(db_user.is_active):
        raise HTTPException(status_code=403, detail="User account is disabled")

    access_token = create_access_token({"sub": username, "role": role})
    refresh_token_new = create_refresh_token({"sub": username, "role": role})
    return {"access_token": access_token, "refresh_token": refresh_token_new, "token_type": "bearer"}

