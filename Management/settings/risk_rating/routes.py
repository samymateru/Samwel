from fastapi import APIRouter, Depends, HTTPException
from schema import CurrentUser
from utils import get_current_user, get_db_connection
from typing import List
from Management.settings.risk_rating.databases import *
from Management.settings.risk_rating.schemas import *

router = APIRouter(prefix="/settings")

@router.get("/risk_rating", response_model=List[RiskRating])
def fetch_risk_rating(
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_risk_rating(db, column="company", value="4")
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)