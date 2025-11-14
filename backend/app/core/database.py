# backend/app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

def get_engine(database_url: str):
    """
    根據 DATABASE_URL 自動選擇資料庫引擎參數
    - SQLite 需要 connect_args={"check_same_thread": False}
    - 其他資料庫使用預設設定
    """
    if database_url.startswith("sqlite"):
        return create_engine(database_url, connect_args={"check_same_thread": False})
    else:
        # 可擴充：這裡可以加更多參數，例如 pool_size、echo 等
        return create_engine(database_url)

engine = get_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()