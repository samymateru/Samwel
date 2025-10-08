from AuditNew.Internal.engagements.reporting.schemas import ProgramSummary, EngagementPrograms
from schemas.issue_schemas import ReadIssues
from fastapi import APIRouter, Depends
from utils import  get_async_db_connection
from AuditNew.Internal.engagements.reporting.databases import *
from typing import List

router = APIRouter(prefix="/engagements")



@router.get("/summary_findings/{engagement_id}", response_model=List[ReadIssues])
async def fetch_summary_of_findings(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        #user: CurrentUser = Depends(get_current_user)
):
    try:
        data = await get_summary_findings(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/summary_audit_process/{engagement_id}", response_model=EngagementPrograms)
async def fetch_summary_of_audit_process(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        #user: CurrentUser = Depends(get_current_user)
):
    try:
        data = await get_summary_audit_process(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)