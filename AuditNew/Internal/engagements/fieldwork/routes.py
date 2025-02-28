from utils import get_current_user
from schema import CurrentUser
from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.engagements.fieldwork.schemas import *
from AuditNew.Internal.engagements.fieldwork.databases import *

router = APIRouter(prefix="/engagements")

@router.get("/fieldwork/summary_procedures/{engagement_id}", response_model=SummaryProcedures)
def fetch_summary_procedures(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    pass

@router.get("/fieldwork/summary_review_notes/{engagement_id}", response_model=SummaryReviewNotes)
def fetch_summary_review_notes(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    pass

@router.post("/fieldwork/task/{engagement_id}")
def create_new_task(
        engagement_id: int,
        task: Task,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        pass
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/fieldwork/review_notes/{engagement_id}")
def create_new_review_notes(
        engagement_id: int,
        note: Note,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        pass
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
