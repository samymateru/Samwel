from AuditNew.Internal.dashboards.schemas import *
from utils import get_current_user, get_async_db_connection
from schema import CurrentUser
from fastapi import APIRouter, Depends
from AuditNew.Internal.dashboards.databases import *

router = APIRouter(prefix="/dashboards")

@router.get("/eauditNext/{module_id}")
async def fetch_main_dashboard(
        module_id: str,
        connection=Depends(get_async_db_connection),
        #_: CurrentUser = Depends(get_current_user)
):
    try:
        issues = await fetch_all_issue_data(connection=connection, module_id=module_id)

        process_summary = await summarize_field(field="process", issues=issues)

        impact_summary = await summarize_field(field="impact_category", issues=issues)

        risk_ratings = await summarize_field(field="risk_rating", issues=issues)

        root_cause_summary = await summarize_field(field="root_cause", issues=issues)

        status = await summarize_status(issues=issues)

        over_due = await get_overdue_issues(issues)

        data = await summarize_engagement_status(
            connection=connection,
            module_id=module_id
        )

        recurring = await summarize_recurring_status(issues=issues)

        return {
            "risk_rating": risk_ratings,
            "process": process_summary,
            "impact_category": impact_summary,
            "root_cause": root_cause_summary,
            "issue_status": status,
            "over_due": over_due,
            "audit_summary": data,
            "recurring": recurring
        }


    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/eauditNext/home/{module_id}", response_model=ModuleHomeDashboard)
async def fetch_module_dashboard(
        module_id: str,
        db = Depends(get_async_db_connection),
        #user: CurrentUser  = Depends(get_current_user)
    ):
    try:
        data = await get_modules_dashboard(connection=db, module_id=module_id)
        if data is None:
            raise HTTPException(status_code=400, detail="Error querying module dashboard")
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/eauditNext/plan_details/{plan_id}", response_model=PlanDetails)
async def fetch_plan_details(
        plan_id: str,
        db=Depends(get_async_db_connection),
        #user: CurrentUser = Depends(get_current_user)
):
    try:
        data = await query_planning_details(connection=db, plan_id=plan_id)
        if data is None:
            raise HTTPException(status_code=400, detail="No plan details available")
        return PlanDetails(
            total=data.get("planning_summary", {}).get("total", 0),
            completed=data.get("planning_summary", {}).get("completed", 0),
            ongoing=data.get("planning_summary", {}).get("ongoing", 0),
            pending=data.get("planning_summary", {}).get("pending", 0)
        )
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/eauditNext/engagement_details/{engagement_id}")
async def fetch_engagement_details(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        #user: CurrentUser = Depends(get_current_user)
):
    try:
        data = await query_engagement_details(connection=db, engagement_id=engagement_id)
        return data

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
