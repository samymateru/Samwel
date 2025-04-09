from AuditNew.Internal.engagements.fieldwork.databases import get_summary_procedures
from AuditNew.Internal.engagements.issue.schemas import Issue
from utils import get_current_user
from schema import CurrentUser, ResponseMessage
from fastapi import APIRouter, Depends, Query, Path
from utils import  get_db_connection
from AuditNew.Internal.engagements.reporting.databases import *
from typing import List, Optional

router = APIRouter(prefix="/engagements")

@router.post("/reporting_procedures/{engagement_id}", response_model=ResponseMessage)
def create_new_reporting_procedure(
        engagement_id: int,
        report: NewReportingProcedure,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_reporting_procedure(db, report=report, engagement_id=engagement_id)
        return ResponseMessage(detail="Reporting procedure added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/reporting_procedures/{engagement_id}", response_model=List[StandardTemplate])
def fetch_reporting_procedures(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_reporting_procedures(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/reporting_procedures/{procedure_id}", response_model=ResponseMessage)
def update_reporting_procedure(
        procedure_id: int,
        report: StandardTemplate,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_reporting_procedure(db, report=report, procedure_id=procedure_id)
        return ResponseMessage(detail="Reporting procedure updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/summary_findings/{engagement_id}", response_model=List[Issue])
def fetch_summary_of_findings(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_summary_findings(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/summary_audit_process/{engagement_id}", response_model=List[ProgramSummary])
def fetch_summary_of_audit_process(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_summary_audit_process(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)