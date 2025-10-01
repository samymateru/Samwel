from fastapi import APIRouter, Depends
from schema import CurrentUser, ResponseMessage
from utils import get_current_user, get_async_db_connection
from Management.entity.profile.engagement_type.databases import *
from typing import List

router = APIRouter(prefix="/profile/engagement_type")


@router.get("/{entity_id}", response_model=EngagementType)
async def fetch_company_engagement_type(
        entity_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_company_engagement_type(db, company_id=entity_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="Engagement type not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
