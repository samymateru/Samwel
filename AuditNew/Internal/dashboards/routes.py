from utils import get_current_user, get_async_db_connection
from schema import CurrentUser
from fastapi import APIRouter, Depends
from AuditNew.Internal.dashboards.databases import *

router = APIRouter(prefix="/dashboards")

@router.get("/eauditNext/{company_module_id}")
async def fetch_main_dashboard(
        company_module_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        issues_data = await query_all_issues(connection=db, company_module_id=company_module_id)
        audit_summary = await query_audit_summary(connection=db, company_module_id=company_module_id)
        if issues_data is  None and audit_summary is None:
            raise HTTPException(status_code=400, detail="No data to show")
        data = {
            "issues_data": issues_data,
            "audits_summary": audit_summary.get("annual_plans")
        }
        return data

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

