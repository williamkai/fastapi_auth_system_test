from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)

    # 登入帳號名稱
    username = Column(String, unique=True, index=True, nullable=False)

    # 帳戶安全密碼
    hashed_password = Column(String, nullable=False)

    # 使用者角色（admin / user）
    role = Column(String, default="user", nullable=False)

    # -------------------------
    # 基本資訊（一般註冊會填）
    # -------------------------
    full_name = Column(String, nullable=True)  # 例如：王小明
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    gender = Column(String, nullable=True)     # 'male' / 'female' / 'other'
    birthday = Column(DateTime, nullable=True) # 生日，非必填

    # -------------------------
    # 帳號狀態
    # -------------------------
    is_active = Column(Boolean, default=True, nullable=False)

    # -------------------------
    # 時間記錄
    # -------------------------
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
