from fastapi import APIRouter, Depends, HTTPException
from schema import CurrentUser
from utils import get_current_user, get_db_connection
from typing import List
from Management.settings.engagement_types.databases import *
from Management.settings.engagement_types.schemas import *

router = APIRouter(prefix="/settings")

@router.get("/engagement_types", response_model=List[EngagementTypes])
def fetch_engagement_type(
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_engagement_types(db, column="company", value=user.company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)