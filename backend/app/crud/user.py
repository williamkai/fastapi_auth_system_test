# backend/app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.auth import hash_password


# -------------------------------------------------
# 取得使用者
# -------------------------------------------------
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# -------------------------------------------------
# 建立使用者（支援更多欄位）
# -------------------------------------------------
def create_user(db: Session, **user_data):
    """
    最佳建立使用者方法。
    user_data 可包含任意欄位，只要 User model 有定義，就能自動填入。

    必要欄位:
        - username
        - password (會被自動 hash)
    """

    # password 不能直接塞進 User，要拿出來 hash
    raw_password = user_data.pop("password")
    hashed_pw = hash_password(raw_password)

    new_user = User(
        hashed_password=hashed_pw,
        **user_data  # 其餘欄位自動套入，不需每次新增欄位就改這裡
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



# -------------------------------------------------
# 取得全部使用者
# -------------------------------------------------
def get_all_users(db: Session):
    return db.query(User).all()


# -------------------------------------------------
# 更新 is_active
# -------------------------------------------------
def update_user_status(db: Session, user_id: int, is_active: bool):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.is_active = is_active# type: ignore
    db.commit()
    db.refresh(user)
    return user


# -------------------------------------------------
# 通用更新使用者（更新 profile 等）
# -------------------------------------------------
def update_user(db: Session, user_id: int, update_data: dict):
    """
    update_data 可包含 email, phone, full_name, gender, birthday...
    """
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    for field, value in update_data.items():
        if hasattr(user, field) and value is not None:
            setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


# -------------------------------------------------
# 刪除使用者
# -------------------------------------------------
def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return False

    db.delete(user)
    db.commit()
    return True


