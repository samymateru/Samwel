import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from AuditNew.Internal.dashboards.databases import query_engagement_details
from background import set_engagement_templates
from core.utils import get_hits, determine_priority_stage
from models.annual_plan_models import get_annual_plan_dashboard_metrics
from models.engagement_models import register_new_engagement, \
    get_single_engagement_details, get_all_annual_plan_engagement, archive_annual_plan_engagement, \
    complete_annual_plan_engagement, remove_engagement_partially, \
    update_engagement_data, update_risk_maturity_rating_table_model, update_risk_maturity_rating_lower_section_model, \
    adding_engagement_staff_model, get_engagement_stage, get_all_annual_plan_engagement_v2
from models.recent_activity_models import add_new_recent_activity
from models.roll_forwar_model import engagement_roll_forward_model
from models.user_models import get_module_users
from schema import ResponseMessage, CurrentUser
from schemas.engagement_schemas import NewEngagement, ReadEngagement,  UpdateEngagement_, EngagementRiskMaturityRating, UpdateRiskMaturityRatingLowerPart
from schemas.recent_activities_schemas import RecentActivities, RecentActivityCategory
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.security.security import get_current_user
from utils import exception_response, return_checker, get_unique_key, get_async_db_connection
from datetime import datetime

router = APIRouter(prefix="/engagements")


@router.post("/{annual_plan_id}", status_code=201, response_model=ResponseMessage)
async def create_new_engagement(
        annual_plan_id: str,
        engagement: NewEngagement,
        module_id: str = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await register_new_engagement(
            connection=connection,
            engagement=engagement,
            annual_plan_id=annual_plan_id,
            module_id=module_id
        )


        if results is None:
            raise HTTPException(status_code=400, detail="Failed To Create Engagement")


        module_users = await get_module_users(
            connection=connection,
            module_id=module_id
        )

        head_users = [user for user in module_users if user["role"] == "Head of Audit"]


        if head_users.__len__() == 0:
            raise HTTPException(status_code=400, detail="No Head Of Audit Found, Cant Create Engagement")


        asyncio.create_task(set_engagement_templates(engagement_id=results.get("id")))


        asyncio.create_task(adding_engagement_staff_model(
            engagement=engagement,
            engagement_id=results.get("id"),
            module_id=module_id,
            head_of_audit=head_users[0]
        ))


        return await return_checker(
            data=results,
            passed="Engagement Successfully Created",
            failed="Failed Creating  Engagement"
        )



@router.get("/{annual_plan_id}", response_model=List[ReadEngagement])
async def fetch_all_annual_plan_engagements(
        annual_plan_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser =Depends(get_current_user)
):
    with exception_response():
        data = await get_all_annual_plan_engagement(
            connection=connection,
            annual_plan_id=annual_plan_id,
            user_id=auth.user_id
        )


        for engagement in data:
            stage_data = await get_engagement_stage(
                connection=connection,
                engagement_id=engagement.get("id")
            )

            stage = get_hits(stage_data)

            engagement["stage"] = determine_priority_stage(stage)

        return data


@router.get("/v2/{annual_plan_id}", response_model=List[ReadEngagement])
async def fetch_all_annual_plan_engagements_v2(
        annual_plan_id: str,
        connection=Depends(get_async_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        data = await get_all_annual_plan_engagement_v2(
            connection=connection,
            annual_plan_id=annual_plan_id,
            user_id=auth.user_id
        )

        annual_plan_dashboard = await get_annual_plan_dashboard_metrics(
            connection=connection,
            annual_plan_id=annual_plan_id
        )


        for engagement in data:
            stage_data = await get_engagement_stage(
                connection=connection,
                engagement_id=engagement.get("id")
            )

            stage = get_hits(stage_data)

            engagement["stage"] = determine_priority_stage(stage)

        return data


@router.get("/engagement_data/{engagement_id}", response_model=ReadEngagement)
async def fetch_single_engagement_details(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_single_engagement_details(
            connection=connection,
            engagement_id=engagement_id
        )

        if data is None:
            raise HTTPException(status_code=404, detail="Engagement Not Found")
        return data



@router.put("/{engagement_id}")
async def update_engagement_details(
        engagement_id: str,
        engagement: UpdateEngagement_,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await update_engagement_data(
            connection=connection,
            engagement=engagement,
            engagement_id=engagement_id
        )

        await add_new_recent_activity(
            connection=connection,
            recent_activity=RecentActivities(
                activity_id=get_unique_key(),
                module_id=auth.module_id,
                name=engagement.name,
                description="Engagement Updated",
                category=RecentActivityCategory.ENGAGEMENT_UPDATED,
                created_by=auth.user_id,
                created_at=datetime.now()
            )
        )

        return await return_checker(
            data=results,
            passed="Engagement Successfully Updated",
            failed="Failed Updating  Engagement"
        )



@router.put("/archive/{engagement_id}")
async def archive_engagement(
        engagement_id: str,
        name: Optional[str] = Query(None),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await archive_annual_plan_engagement(
            connection=connection,
            engagement_id=engagement_id
        )

        await add_new_recent_activity(
            connection=connection,
            recent_activity=RecentActivities(
                activity_id=get_unique_key(),
                module_id=auth.module_id,
                name=name,
                description="Engagement Archived",
                category=RecentActivityCategory.ENGAGEMENT_ARCHIVED,
                created_by=auth.user_id,
                created_at=datetime.now()
            )
        )

        return await return_checker(
            data=results,
            passed="Engagement Successfully Archived",
            failed="Failed Archiving  Engagement"
        )




@router.put("/complete/{engagement_id}")
async def complete_engagement(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await complete_annual_plan_engagement(
            connection=connection,
            engagement_id=engagement_id
        )

        engagement_data = await query_engagement_details(
            connection=connection,
            engagement_id=engagement_id
        )


        await add_new_recent_activity(
            connection=connection,
            recent_activity=RecentActivities(
                activity_id=get_unique_key(),
                module_id=auth.module_id,
                name=engagement_data.get("name") or "",
                description="Engagement Completed",
                category=RecentActivityCategory.ENGAGEMENT_COMPLETED,
                created_by=auth.user_id,
                created_at=datetime.now()
            )
        )

        return await return_checker(
            data=results,
            passed="Engagement Successfully Completed",
            failed="Failed Completing  Engagement"
        )



@router.put("/reopen/{engagement_id}")
async def reopen_engagement(
        engagement_id: str,
        name: Optional[str] = Query(None),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await complete_annual_plan_engagement(
            connection=connection,
            engagement_id=engagement_id
        )

        await add_new_recent_activity(
            connection=connection,
            recent_activity=RecentActivities(
                activity_id=get_unique_key(),
                module_id=auth.module_id,
                name=name,
                description="Engagement Reopened",
                category=RecentActivityCategory.ENGAGEMENT_REOPEN,
                created_by=auth.user_id,
                created_at=datetime.now()
            )
        )

        return await return_checker(
            data=results,
            passed="Engagement Successfully Reopened",
            failed="Failed Reopening  Engagement"
        )




@router.delete("/{engagement_id}")
async def delete_engagement_data_partially(
        engagement_id: str,
        name: Optional[str] = Query(None),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await remove_engagement_partially(
            connection=connection,
            engagement_id=engagement_id
        )

        await add_new_recent_activity(
            connection=connection,
            recent_activity=RecentActivities(
                activity_id=get_unique_key(),
                module_id=auth.module_id,
                name=name,
                description="Engagement Deleted",
                category=RecentActivityCategory.ENGAGEMENT_DELETED,
                created_by="",
                created_at=datetime.now()
            )
        )

        return await return_checker(
            data=results,
            passed="Engagement Successfully Deleted",
            failed="Failed Deleting  Engagement"
        )




@router.put("/roll_forward/{engagement_id}")
async def engagement_roll_forward(
        engagement_id: str,
        annual_plan: str = Query(...),
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await engagement_roll_forward_model(
            connection=connection,
            engagement_id=engagement_id,
            annual_plan=annual_plan,
            module_id=auth.module_id
        )

        return await return_checker(
            data=results,
            passed="Engagement Successfully Roll Forwarded",
            failed="Failed Roll Forward Engagement"
        )



@router.put("/risk_maturity_rating_table/{engagement_id}")
async def update_engagement_risk_maturity_rating_table(
        engagement_id: str,
        engagement: EngagementRiskMaturityRating,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await update_risk_maturity_rating_table_model(
            connection=connection,
            engagement=engagement,
            engagement_id=engagement_id
        )

        return await return_checker(
            data=results,
            passed="Maturity Rating Successfully Updated",
            failed="Failed Updating Maturity Rating"
        )




@router.put("/risk_maturity_rating_lower_section/{engagement_id}")
async def update_engagement_risk_maturity_rating_lower_section_table(
        engagement_id: str,
        engagement: UpdateRiskMaturityRatingLowerPart,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await update_risk_maturity_rating_lower_section_model(
            connection=connection,
            engagement=engagement,
            engagement_id=engagement_id
        )

        return await return_checker(
            data=results,
            passed="Maturity Rating Successfully Updated",
            failed="Failed Updating Maturity Rating"
        )
