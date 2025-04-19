from utils import get_current_user
from schema import CurrentUser
from fastapi import APIRouter, Depends
from utils import get_db_connection_async
from AuditNew.Internal.engagements.fieldwork.schemas import *
from AuditNew.Internal.engagements.fieldwork.databases import *

router = APIRouter(prefix="/engagements")

@router.get("/fieldwork/summary_procedures/{engagement_id}", response_model=List[SummaryAuditProcedure])
async def fetch_summary_procedures(
        engagement_id: str,
        db=Depends(get_db_connection_async),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_summary_procedures(db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/fieldwork/summary_review_notes/{engagement_id}", response_model=List[SummaryReviewNotes])
async def fetch_summary_review_notes(
        engagement_id: str,
        db=Depends(get_db_connection_async),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_summary_review_notes(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/fieldwork/summary_task/{engagement_id}", response_model=List[SummaryTask])
async def fetch_summary_task(
        engagement_id: str,
        db=Depends(get_db_connection_async),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_summary_task(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
