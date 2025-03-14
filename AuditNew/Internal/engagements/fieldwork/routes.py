from utils import get_current_user
from schema import CurrentUser
from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.engagements.fieldwork.schemas import *
from AuditNew.Internal.engagements.fieldwork.databases import *

router = APIRouter(prefix="/engagements")

@router.get("/fieldwork/summary_procedures/{engagement_id}", response_model=List[SummaryAuditProcedure])
def fetch_summary_procedures(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_summary_procedures(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/fieldwork/summary_review_notes/{engagement_id}")
def fetch_summary_review_notes(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_summary_review_notes(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
