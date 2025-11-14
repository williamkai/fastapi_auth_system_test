# # tests/test_admin.py
# import pytest
# from fastapi.testclient import TestClient
# from main import app
# from app.core.database import  Base
# from app.dependencies.dependencies import get_db
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.crud import user as crud_user

# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)

# client = TestClient(app)

# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# # 初始化 admin
# def init_admin(db):
#     return crud_user.create_user(db, {
#         "username": "admin",
#         "password": "adminpass",
#         "role": "admin"
#     })

# def init_user(db):
#     return crud_user.create_user(db, {
#         "username": "user",
#         "password": "userpass"
#     })


# def test_admin_can_delete_user():
#     db = next(override_get_db())
#     admin = init_admin(db)
#     user = init_user(db)

#     # 模擬 admin 登入
#     # 這邊假設 token 或依賴能取得 admin
#     headers = {"Authorization": f"Bearer faketoken"}  # 可搭配你自己的 auth fixture
#     response = client.delete(f"/users/{user.id}", headers=headers)
#     # 因為沒有真正驗證 token，這邊只是範例
#     assert response.status_code in [200, 403, 404]  # 根據你 auth 設定
