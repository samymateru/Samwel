from schemas.issue_schemas import ReadIssues
from utils import get_current_user
from schema import CurrentUser, ResponseMessage
from fastapi import APIRouter, Depends
from utils import  get_async_db_connection
from AuditNew.Internal.engagements.reporting.databases import *
from typing import List

router = APIRouter(prefix="/engagements")

@router.post("/reporting_procedures/{engagement_id}", response_model=ResponseMessage)
async def create_new_reporting_procedure(
        engagement_id: str,
        report: NewReportingProcedure,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await add_reporting_procedure(db, report=report, engagement_id=engagement_id)
        return ResponseMessage(detail="Reporting procedure added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/reporting_procedures/{engagement_id}", response_model=List[StandardTemplate])
async def fetch_reporting_procedures(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_reporting_procedures(db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/reporting_procedures/{procedure_id}", response_model=ResponseMessage)
async def update_reporting_procedure(
        procedure_id: str,
        report: StandardTemplate,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_reporting_procedure(db, report=report, procedure_id=procedure_id)
        return ResponseMessage(detail="Reporting procedure updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

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

@router.get("/summary_audit_process/{engagement_id}", response_model=List[ProgramSummary])
async def fetch_summary_of_audit_process(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        #user: CurrentUser = Depends(get_current_user)
):
    #if user.status_code != 200:
        #raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_summary_audit_process(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)