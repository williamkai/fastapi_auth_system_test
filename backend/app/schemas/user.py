# backend/app/schemas/user.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 輸入用戶資料
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    birthday: Optional[datetime]

class UserLogin(BaseModel):
    username: str
    password: str

# 回傳用戶資料（隱藏密碼,允許狀態）
class UserOut(BaseModel):
    id: int
    username: str
    full_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    birthday: Optional[datetime]
    role: str

    class Config:
        from_attributes = True

class UserDetailOut(BaseModel):
    id: int
    username: str
    full_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    birthday: Optional[datetime]
    role: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class UserUpdateStatus(BaseModel):
    is_active: bool
    
# 登入回傳 token
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str
