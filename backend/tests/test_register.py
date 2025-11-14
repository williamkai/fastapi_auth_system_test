# tests/test_register.py
import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.database import  Base
from app.dependencies.dependencies import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 使用 SQLite 記憶體資料庫
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立資料表
Base.metadata.create_all(bind=engine)

# 建立 TestClient
client = TestClient(app)

# 測試資料庫依賴
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


def test_register_user():
    response = client.post("/register", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["id"] is not None


def test_register_duplicate_user():
    # 先註冊一次
    client.post("/register", json={"username": "dupuser", "password": "pass"})
    # 再註冊同名
    response = client.post("/register", json={"username": "dupuser", "password": "pass"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"
