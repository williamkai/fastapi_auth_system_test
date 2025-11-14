# tests/test_token.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_and_token():
    # 假設有 /login 路由
    response = client.post("/login", data={"username": "admin", "password": "adminpass"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    token = data["access_token"]

    # 用 token 訪問受保護路由
    headers = {"Authorization": f"Bearer {token}"}
    response2 = client.get("/users", headers=headers)
    assert response2.status_code == 200

def test_refresh_token():
    # 假設有 /refresh 路由
    response = client.post("/refresh", headers={"Authorization": "Bearer faketoken"})
    # 這裡只是示意，依你實作修改
    assert response.status_code in [200, 401]
