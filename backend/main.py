# backend/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.crud import user as crud_user
from app.routers import auth, users, me

# ------------------------------
# 建立資料表（啟動程式時自動建立）
# ------------------------------
Base.metadata.create_all(bind=engine)

# ------------------------------
# 初始化 admin
# ------------------------------
def init_admin(db):
    admin_user = crud_user.get_user_by_username(db, settings.ADMIN_USERNAME)
    if not admin_user:
        # 假設 crud_user.create_user() 自帶 bcrypt 或 hash 參數
        crud_user.create_user(
            db, 
            username=settings.ADMIN_USERNAME, 
            password=settings.ADMIN_PASSWORD, 
            role="admin"
        )
        print(f"Admin user '{settings.ADMIN_USERNAME}' created.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動時執行
    db = SessionLocal()
    try:
        init_admin(db)
    finally:
        db.close()

    yield  # 程式運行期間

    # 可選：關閉時清理資源
    # print("App shutdown")

# ------------------------------
# 建立 FastAPI app
# ------------------------------
app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# ------------------------------
# 導入 routers
# ------------------------------
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(me.router)

# ------------------------------
# 測試啟動訊息
# ------------------------------
@app.get("/health")
async def health_check():
    return {"status": "ok", "app_name": settings.APP_NAME}
