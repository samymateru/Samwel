from fastapi import Depends, HTTPException, APIRouter
from utils import get_db_connection, get_current_user
from Management.companies.profile.risk_category.databases import *

router = APIRouter(prefix="/profile")

@router.get("/risk_category")
def fetch_combined_root_cause_category(
        db=Depends(get_db_connection),
        #user: CurrentUser = Depends(get_current_user)
):
    #if user.status_code != 200:
        #raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_combined_risk_category(db, column="company", value=18)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)