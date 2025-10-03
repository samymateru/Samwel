from typing import List

from AuditNew.Internal.reports.schemas import ReportIssues
from core.utils import extract_text
from utils import get_current_user, get_async_db_connection, exception_response
from schema import CurrentUser
from fastapi import APIRouter, Depends
from AuditNew.Internal.reports.databases import *


router = APIRouter(prefix="/reports")

@router.get("/issue_detailed/{module_id}", response_model=List[ReportIssues])
async def fetch_detailed_issue_reports(
        module_id: str,
        db=Depends(get_async_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        data = await get_all_issue_reports(connection=db, module_id=module_id)
        issues = []
        for x in data:
            refined = {
                **x,
                "criteria": extract_text(x.get("criteria")),
                "recommendation": extract_text(x.get("recommendation")),
                "finding": extract_text(x.get("finding")),
                "root_cause_description": extract_text(x.get("root_cause_description")),
                "impact_description": extract_text(x.get("impact_description")),
                "management_action_plan": extract_text(x.get("management_action_plan"))
            }
            issues.append(refined)

        return issues


@router.get("/review_comments/{company_module_id}")
async def fetch_review_comments(
        company_module_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_review_comments_report(connection=db, company_module_id=company_module_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)



@router.get("/tasks/{company_module_id}")
async def fetch_tasks(
        company_module_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_tasks_report(connection=db, company_module_id=company_module_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)