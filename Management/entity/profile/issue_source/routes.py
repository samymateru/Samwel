from fastapi import APIRouter, Depends, HTTPException
from schema import ResponseMessage, CurrentUser
from utils import get_current_user, get_async_db_connection
from Management.entity.profile.issue_source.databases import *
from Management.entity.profile.issue_source.schemas import *


router = APIRouter(prefix="/profile/issue_source")


@router.get("/{entity_id}", response_model=IssueSource)
async def fetch_company_issue_source(
        entity_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_company_issue_source(connection=db, company_id=entity_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="Issue source not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

