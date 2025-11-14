# FastAPI 用戶管理系統

## ✨專案說明
本專案是一個完整的用戶身份驗證系統，使用 **FastAPI** 開發後端，提供安全且可擴展的用戶管理功能，並搭配 **React + Vite** 開發前端介面。  

系統支援兩種角色：
- **admin（管理員）**：擁有完整用戶管理權限，包括查看所有用戶資料、變更用戶登入權限（啟用/停用）、刪除使用者。
- **user（一般用戶）**：只能查詢自己的帳戶資料，以及進行登入、登出操作。

### 功能概要
1. **用戶註冊與登入**
   - 使用者可透過帳號與密碼註冊。
   - 登入後會取得 **JWT**，分為短時效 **access token** 與長時效 **refresh token**。
   - JWT 用於驗證 API 請求，確保使用者身份與權限。

2. **角色權限控制**
   - 系統自動辨識使用者角色 (`admin` 或 `user`)。
   - API 端點會依角色限制存取權限。
   - 例如：一般用戶無法存取管理員專用的 `/users` 端點。

3. **用戶管理（Admin 專用）**
   - 列出所有用戶資料。
   - 修改使用者登入狀態（啟用或停用）。
   - 刪除使用者（無法刪除其他管理員）。

4. **前端介面**
   - 使用 **React** 建置。
   - 提供註冊、登入、登出功能。
   - 管理員可透過介面操作用戶管理功能。
   - 前端呼叫後端 API，並透過 JWT 進行認證。

5. **API 安全性**
   - 使用 JWT 進行認證與授權。
   - 短時效 token 提高安全性，長時效 token 用於刷新。
   - 支援跨域請求（CORS）配置，可與本地或外部前端連接。

---
## 🛠️ 技術棧與架構設計

### 開發技術
- **後端**：
  - **框架**：FastAPI，用於建立高效能 API 與身份驗證系統
  - **資料庫操作**：SQLAlchemy ORM，搭配 PostgreSQL（SQLite）
  - **資料驗證與序列化**：Pydantic
  - **身份驗證**：JWT（access 與 refresh tokens），bcrypt 密碼加密
  - **權限控制**：角色分級管理 (`admin` 與 `user`)
- **前端**：
  - **框架**：React + Vite
  - **功能**：與後端 API 連接，處理登入/登出、資料顯示與管理介面
- **測試**：
  - **工具**：pytest，測試 API 與後端功能正確性

### 專案架構設計

- **後端模組架構說明**：
- core/：核心設定與環境變數，例如資料庫連線設定、APP 配置。
- models/：ORM 資料模型，用於 SQLAlchemy 定義資料表結構。
- schemas/：Pydantic 資料驗證與序列化，用於 API 輸入與輸出。
- crud/：資料庫 CRUD 封裝，將資料操作邏輯與路由分離。
- dependencies/：共用依賴，例如資料庫 Session、權限檢查函式。
- routers/：API 路由模組，依功能分類，例如 auth、users、me。
- utils/：工具函式。

- **前端設計**：
  - 清楚分離介面與資料邏輯
  - 可透過 fetch 與後端 API 溝通
  - 支援不同角色顯示不同功能

### 容器化與部署
- **容器化**：Docker + Docker Compose
  - 方便快速啟動資料庫、後端、前端整套環境
- **部署平台**：Render

### 未來優化方向
- 設計 `session` 表紀錄不同裝置登入狀態，提供更精細的登入控制
- 可加入封鎖登入、異常登入提醒等安全機制
- 後端 API 可加入更多角色或設定群組及權限細分
- 前端可支援更完整的使用者操作與管理功能,及各種應用

---

## 🚀 啟動步驟

確保你的電腦上已安裝 `Docker` 和 `Docker Compose`。

1.  **Clone 專案**
    ```bash
    git clone https://github.com/williamkai/fastapi_auth_system_test.git
    cd fastapi_auth_system_test
    ```

2.  **啟動所有服務**
    在專案根目錄下，執行以下命令：
    ```bash
    docker compose up --build -d
    ```
    - `--build`: 強制重新建構映像檔，確保程式碼更新生效。
    - `-d`: 在背景模式下執行。

    第一次啟動會需要一些時間來下載映像檔和安裝依賴。

3.  **確認服務狀態**
    服務啟動後，你可以透過以下網址確認各服務是否正常運作：
    - **前端應用程式**: [http://localhost:3000](http://localhost:3000)
    - **後端 API 文件 (Swagger UI)**: [http://localhost:8010/docs](http://localhost:8010/docs)
    - **後端健康檢查**: [http://localhost:8010/health](http://localhost:8010/health)
        回傳範例：
        ```json
        {
          "status": "ok",
          "app_name": "FastAPI Auth System"
        }
        ```

4.  **停止服務**
    若要停止所有服務，請在專案根目錄下執行：
    ```bash
    docker compose down
    ```

---

## 🌐 前端存取網址

- **開發環境**：http://localhost:3000
- **部署後環境**：[部屬於Render](https://fastapi-user-test-frontend.onrender.com/)

---


## 🧑‍🤝‍🧑 測試帳號說明

| 角色  | 帳號        | 密碼           | 權限說明 |
|-------|------------|----------------|---------|
| admin | laiwelltest | qwe123qwe123  | 可查看所有使用者帳號列表及個別資訊，變更使用者登入狀態，刪除使用者 |
| user  | 由註冊建立  | 任意密碼       | 僅能登入查看自己的帳號資訊及登出 |


---

## 🤖 API 使用範例


### 驗證 (Authentication)

#### 1. 註冊新使用者
- **Endpoint**: `POST /api/v1/auth/register`
- **說明**: 建立一個新使用者。`username` 和 `password` 為必填。
```bash
curl -X POST "http://localhost:8010/api/v1/auth/register" \
-H "Content-Type: application/json" \
-d 
{
  "username": "newuser",
  "password": "newpassword123",
  "email": "newuser@example.com",
  "full_name": "New User"
}
```

#### 2. 登入以取得 Token
- **Endpoint**: `POST /api/v1/auth/token`
- **說明**: 使用者名稱和密碼登入，以獲取 API 操作所需的 `access_token` 和 `refresh_token`。
```bash
curl -X POST "http://localhost:8010/api/v1/auth/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=newuser&password=newpassword123"
```
- **成功回傳**:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

#### 3. 刷新 Access Token
- **Endpoint**: `POST /api/v1/auth/refresh`
- **說明**: 當 `access_token` 過期時，使用 `refresh_token` 來獲取一組新的 token。
```bash
curl -X POST "http://localhost:8010/api/v1/auth/refresh" \
-H "Content-Type: application/json" \
-d 
{
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
```

---

### 一般使用者 (Authenticated User)

*以下請求皆需在 Header 中加入 `Authorization: Bearer YOUR_ACCESS_TOKEN`*

#### 獲取個人資訊
- **Endpoint**: `GET /api/v1/me`
- **說明**: 獲取當前登入使用者的個人公開資訊。
```bash
curl -X GET "http://localhost:8010/api/v1/me" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 管理員 (Admin Only)

*以下請求皆需使用**管理員帳號**的 Access Token*

#### 1. 獲取所有使用者列表
- **Endpoint**: `GET /api/v1/users`
- **說明**: 列出系統中所有使用者的詳細資訊。
```bash
curl -X GET "http://localhost:8010/api/v1/users" \
-H "Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN"
```

#### 2. 更新使用者狀態 (啟用/停用)
- **Endpoint**: `PATCH /api/v1/users/{user_id}/status`
- **說明**: 啟用或停用指定 ID 的使用者。
```bash
# 停用 ID 為 2 的使用者
curl -X PATCH "http://localhost:8010/api/v1/users/2/status" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN" \
-d '{"is_active": false}'
```

#### 3. 刪除使用者
- **Endpoint**: `DELETE /api/v1/users/{user_id}`
- **說明**: 刪除指定 ID 的使用者。
```bash
curl -X DELETE "http://localhost:8010/api/v1/users/2" \
-H "Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN"
```

---

## 🧪 測試執行方式

1. 確認已安裝 pytest
```bash
pip install pytest
```
2. 執行後端測試
```bash
pytest tests/
```
3. 預期測試：
- 用戶註冊 / 登入
- 權限驗證 (admin vs user)
- Token 刷新機制

---
