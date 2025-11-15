# tests/conftest.py
import sys
from pathlib import Path

# 將 backend 目錄加入 Python 搜尋路徑
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.core.database import Base
from app.dependencies.dependencies import get_db

# 使用記憶體中的 SQLite 資料庫進行測試
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # 使用靜態池，確保每次測試都使用同一個連線
)

# 建立測試用的 Session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 在測試開始前建立資料表
Base.metadata.create_all(bind=engine)

# 覆寫 get_db 依賴，改用測試資料庫
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 將 app 中的 get_db 依賴替換為 override_get_db
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    """
    提供一個 TestClient，並在每次測試後清理資料庫。
    """
    # 每次測試前，重新建立所有資料表 (確保乾淨的環境)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def db_session():
    """
    提供一個資料庫 session fixture，方便在測試中直接操作資料庫。
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
