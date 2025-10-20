from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File, BackgroundTasks
from core.utils import upload_attachment
from models.annual_plan_models import register_new_annual_plan, get_module_annual_plans, get_annual_plan_details, \
    remove_annual_plan_partially, edit_annual_plan_details
from models.attachment_model import add_new_attachment
from models.recent_activity_models import add_new_recent_activity
from schema import ResponseMessage, CurrentUser
from schemas.annual_plan_schemas import NewAnnualPlan, ReadAnnualPlan, UpdateAnnualPlan
from schemas.attachement_schemas import AttachmentCategory
from schemas.recent_activities_schemas import RecentActivities, RecentActivityCategory
from schemas.role_schemas import RolesSections, Permissions
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.logging.logger import global_logger
from services.security.security import check_permission
from utils import exception_response, return_checker, get_unique_key
from datetime import datetime



router = APIRouter(prefix="/annual_plans")


@router.post("/{module_id}", status_code=201, response_model=ResponseMessage)
async def create_new_annual_plan(
        module_id: str,
        name: str = Form(...),
        year: str = Form(...),
        start: datetime = Form(...),
        end: datetime = Form(...),
        attachment: UploadFile = File(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        background_tasks: BackgroundTasks = BackgroundTasks(),
        _: CurrentUser = Depends(check_permission(RolesSections.AUDIT_PLAN, Permissions.CREATE))
):
    with exception_response():

        annual_plan = NewAnnualPlan(
            name=name,
            year=year,
            start=start,
            end=end,
        )

        annual_plan_results = await register_new_annual_plan(
            connection=connection,
            annual_plan=annual_plan,
            module_id=module_id,
            user_id=""
        )

        if annual_plan_results is None:
            global_logger.error(f"Failed to Create Annual Plan Module: {module_id}")


        await add_new_attachment(
            connection=connection,
            attachment=attachment,
            item_id=annual_plan_results.get("id"),
            module_id=module_id,
            url=upload_attachment(
            category=AttachmentCategory.ANNUAL_PLAN,
            background_tasks=background_tasks,
            file=attachment
            ),
            category=AttachmentCategory.ANNUAL_PLAN
        )

        await add_new_recent_activity(
            connection=connection,
            recent_activity=RecentActivities(
                activity_id=get_unique_key(),
                module_id=module_id,
                name=name,
                description="New Annual Plan Created",
                category=RecentActivityCategory.ANNUAL_PLAN_CREATED,
                created_by="",
                created_at=datetime.now()
            )
        )


        return await return_checker(
            data=annual_plan_results,
            passed="Annual Plan Successfully Created",
            failed="Failed Creating  Annual Plan"
        )



@router.get("/{module_id}")
async def fetch_all_module_annual_plans(
        module_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(check_permission(RolesSections.AUDIT_PLAN, Permissions.VIEW))
):
    with exception_response():
        data = await get_module_annual_plans(
            connection=connection,
            module_id=module_id
        )
        return data




@router.get("/single_plan/{annual_plan_id}", response_model=ReadAnnualPlan)
async def fetch_single_plan_data(
        annual_plan_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(check_permission(RolesSections.AUDIT_PLAN, Permissions.VIEW))
):
    with exception_response():
        data = await get_annual_plan_details(
            connection=connection,
            annual_plan_id=annual_plan_id
        )


        if data is None:
            raise HTTPException(status_code=404, detail="Annual Plan Not Found")
        return data



@router.put("/{annual_plan_id}", response_model=ResponseMessage)
async def update_annual_plan_data(
        annual_plan_id: str,
        annual_plan: UpdateAnnualPlan,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(check_permission(RolesSections.AUDIT_PLAN, Permissions.EDIT))

):
    with exception_response():
        results = await edit_annual_plan_details(
            connection=connection,
            annual_plan=annual_plan,
            annual_plan_id=annual_plan_id
        )

        return await return_checker(
            data=results,
            passed="Annual Plan Successfully Updated",
            failed="Failed Updating  Annual Plan"
        )



@router.delete("/{annual_plan_id}", response_model=ResponseMessage)
async def remove_annual_plan_data(
        annual_plan_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(check_permission(RolesSections.AUDIT_PLAN, Permissions.DELETE))
):
    with exception_response():

        results = await remove_annual_plan_partially(
            connection=connection,
            annual_plan_id=annual_plan_id
        )

        return await return_checker(
            data=results,
            passed="Annual Plan Successfully Deleted",
            failed="Failed Deleting  Annual Plan"
        )

