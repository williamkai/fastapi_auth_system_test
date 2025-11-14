# tests/test_main_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid

from app.core.config import settings
from app.crud.user import get_user_by_username
from app.schemas.user import UserCreate

# 為測試定義一個唯一的用戶名，避免與其他測試衝突
# 使用 uuid 確保每次測試運行時的用戶名都是唯一的
def generate_unique_username():
    return f"testuser_{uuid.uuid4().hex[:8]}"

def generate_unique_admin_username():
    return f"admin_{uuid.uuid4().hex[:8]}"

# --- 測試 1: 用戶註冊與登入 ---
def test_user_registration_and_login(client: TestClient):
    """
    測試：
    1. 成功註冊一個新用戶。
    2. 使用新用戶的憑證成功登入。
    3. 登入後應返回 access_token 和 refresh_token。
    """
    username = generate_unique_username()
    password = "testpassword"
    
    # 1. 註冊
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "password": password,
            "full_name": None,
            "email": None,
            "phone": None,
            "gender": None,
            "birthday": None
        }
    )
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == username
    assert "id" in user_data

    # 2. 登入
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password}
    )
    assert login_response.status_code == 200
    tokens = login_response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"

# --- 測試 2: 權限驗證 (Admin vs User) ---
def test_admin_required_permissions(client: TestClient, db_session: Session):
    """
    測試：
    1. 建立一個普通用戶和一個管理員用戶。
    2. 普通用戶嘗試訪問僅限管理員的端點 (GET /api/v1/users/)，應收到 403 Forbidden。
    3. 管理員用戶訪問該端點，應成功返回用戶列表。
    """
    # 1. 建立用戶
    user_username = generate_unique_username()
    user_password = "password123"
    admin_username = generate_unique_admin_username()
    admin_password = "adminpassword"

    # 註冊普通用戶
    client.post(
        "/api/v1/auth/register",
        json={
            "username": user_username,
            "password": user_password,
            "full_name": None,
            "email": None,
            "phone": None,
            "gender": None,
            "birthday": None
        }
    )
    
    # 註冊管理員用戶 (先註冊為普通用戶)
    client.post(
        "/api/v1/auth/register",
        json={
            "username": admin_username,
            "password": admin_password,
            "full_name": None,
            "email": None,
            "phone": None,
            "gender": None,
            "birthday": None
        }
    )

    # 從資料庫中取得管理員用戶並更新其角色
    from app.models.user import User
    admin_user_db = db_session.query(User).filter(User.username == admin_username).first()
    assert admin_user_db is not None
    admin_user_db.role = "admin"# type: ignore
    db_session.add(admin_user_db)
    db_session.commit()
    db_session.refresh(admin_user_db)

    # 2. 普通用戶登入並嘗試訪問
    user_login_res = client.post("/api/v1/auth/login", data={"username": user_username, "password": user_password})
    user_token = user_login_res.json()["access_token"]
    
    user_headers = {"Authorization": f"Bearer {user_token}"}
    response_user = client.get("/api/v1/users/users", headers=user_headers)
    assert response_user.status_code == 403  # 應該被拒絕
    # 3. 管理員用戶登入並嘗試訪問
    admin_login_res = client.post("/api/v1/auth/login", data={"username": admin_username, "password": admin_password})
    admin_token = admin_login_res.json()["access_token"]

    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    response_admin = client.get("/api/v1/users/users", headers=admin_headers)
    assert response_admin.status_code == 200  # 應該成功
    assert isinstance(response_admin.json(), list) # 應返回列表

# --- 測試 3: Token 刷新機制 ---
def test_token_refresh(client: TestClient):
    """
    測試：
    1. 註冊並登入用戶以獲取 refresh_token。
    2. 使用 refresh_token 成功換取新的 access_token。
    3. 驗證新的 access_token 可以成功訪問受保護的端點。
    """
    username = generate_unique_username()
    password = "refresh_test_password"

    # 1. 註冊並登入
    client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "password": password,
            "full_name": None,
            "email": None,
            "phone": None,
            "gender": None,
            "birthday": None
        }
    )
    login_response = client.post("/api/v1/auth/login", data={"username": username, "password": password})
    
    login_data = login_response.json()
    original_access_token = login_data["access_token"]
    refresh_token = login_data["refresh_token"]

    # 2. 刷新 Token
    refresh_response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_response.status_code == 200
    new_tokens = refresh_response.json()
    assert "access_token" in new_tokens

    # 3. 使用新 Token 訪問受保護的端點
    new_access_token = new_tokens["access_token"]
    me_response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {new_access_token}"}
    )
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["username"] == username