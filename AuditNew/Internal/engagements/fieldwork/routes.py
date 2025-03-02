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
