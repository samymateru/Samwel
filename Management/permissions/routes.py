from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from schema import CurrentUser
from utils import get_current_user

router = APIRouter(prefix="/permissions")
@router.get("/")
def get_modules(
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    pass