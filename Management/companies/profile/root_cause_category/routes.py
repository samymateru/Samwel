from fastapi import APIRouter, Depends, HTTPException
from schema import CurrentUser
from Management.companies.profile.root_cause_category.databases import *
from utils import get_db_connection, get_current_user

router = APIRouter(prefix="/profile")


@router.get("/root_cause_category")
def fetch_root_cause_category(
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_combined_root_cause_category(db, column="company", value=user.company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
