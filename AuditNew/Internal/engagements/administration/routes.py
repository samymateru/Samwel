from utils import get_current_user
from schema import CurrentUser
from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.engagements.administration.schemas import *

router = APIRouter(prefix="/engagements")

@router.get("/profile/{engagement_id}", response_model=EngagementProfile)
def fetch_engagement_profile(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        pass
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)