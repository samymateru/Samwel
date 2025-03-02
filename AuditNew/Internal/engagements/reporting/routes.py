from utils import get_current_user
from schema import CurrentUser
from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.engagements.reporting.schemas import *
from  AuditNew.Internal.engagements.planning.schemas import StandardTemplate
from AuditNew.Internal.engagements.reporting.databases import *
from typing import List

router = APIRouter(prefix="/engagements")

@router.post("/reporting_procedures/{engagement_id}")
def create_new_planning_procedure(
        engagement_id: int,
        report: StandardTemplate,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_reporting_procedure(db, report=report, engagement_id=engagement_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/reporting_procedures/{engagement_id}", response_model=List[StandardTemplate])
def fetch_planning_procedures(
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

@router.put("/planning_procedures/{procedure_id}")
def create_new_planning_procedure(
        procedure_id: int,
        report: StandardTemplate,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_reporting_procedure(db, report=report, procedure_id=procedure_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/summary_findings/{engagement_id}")
def fetch_summary_of_findings():
    pass

@router.get("/summary_audit_process/{engagement_id}")
def fetch_summary_of_audit_process():
    pass