from fastapi import APIRouter, Depends
from ..dependencies.dependencies import get_current_user
from ..schemas import user as schemas_user

router = APIRouter(tags=["Me"])

@router.get("/me", response_model=schemas_user.UserOut)
def read_me(current_user=Depends(get_current_user)):
    return current_user
