# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   # ← 新增
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
        crud_user.create_user(
            db,
            username=settings.ADMIN_USERNAME,
            password=settings.ADMIN_PASSWORD,
            role="admin"
        )
        print(f"Admin user '{settings.ADMIN_USERNAME}' created.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        init_admin(db)
    finally:
        db.close()

    yield


# ------------------------------
# 建立 FastAPI app
# ------------------------------
app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# ------------------------------
# ⭐ 加入 CORS (放這裡)
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# 導入 routers
# ------------------------------
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(users.router, prefix="/api/v1/users")
app.include_router(me.router, prefix="/api/v1/me")

# ------------------------------
# 測試啟動訊息
# ------------------------------
@app.get("/health")
async def health_check():
    return {"status": "ok", "app_name": settings.APP_NAME}
