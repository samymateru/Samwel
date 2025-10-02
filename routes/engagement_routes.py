import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from background import set_engagement_templates
from models.engagement_models import register_new_engagement, \
    get_single_engagement_details, get_all_annual_plan_engagement, archive_annual_plan_engagement, \
    complete_annual_plan_engagement, remove_engagement_partially, update_engagement_opinion_rating, \
    update_engagement_data
from models.engagement_staff_models import create_new_engagement_staff_model
from models.notification_models import add_notification_to_user_model
from models.recent_activity_models import add_new_recent_activity
from models.roll_forwar_model import engagement_roll_forward_model
from schema import ResponseMessage, CurrentUser
from schemas.engagement_schemas import NewEngagement, ReadEngagement, \
    AddOpinionRating, UpdateEngagement_
from schemas.engagement_staff_schemas import NewEngagementStaff
from schemas.notification_schemas import CreateNotifications, NotificationsStatus
from schemas.recent_activities_schemas import RecentActivities, RecentActivityCategory
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.security.security import get_current_user
from utils import exception_response, return_checker, get_unique_key
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

        for lead in engagement.leads:
            staff = NewEngagementStaff(
                name=lead.name,
                role="Audit Lead",
                email=lead.email,
                start_date=datetime.now(),
                end_date=datetime.now(),
                tasks=""
            )

            await create_new_engagement_staff_model(
                connection=connection,
                staff=staff,
                engagement_id=results.get("id")
            )

            await add_notification_to_user_model(
                connection=connection,
                notification=CreateNotifications(
                    id=get_unique_key(),
                    title="Engagement invitation",
                    user_id=lead.id,
                    message=f"Your have been invited to engagement {engagement.name} as Engagement lead",
                    status=NotificationsStatus.NEW,
                    created_at=datetime.now()
                )
            )

        await add_new_recent_activity(
            connection=connection,
            recent_activity=RecentActivities(
                activity_id=get_unique_key(),
                module_id=module_id,
                name=engagement.name,
                description="New Engagement Created",
                category=RecentActivityCategory.ENGAGEMENT_CREATED,
                created_by="",
                created_at=datetime.now()
            )
        )

        asyncio.create_task(set_engagement_templates(engagement_id=results.get("id")))


        return await return_checker(
            data=results,
            passed="Engagement Successfully Created",
            failed="Failed Creating  Engagement"
        )



@router.get("/{annual_plan_id}", response_model=List[ReadEngagement])
async def fetch_all_annual_plan_engagements(
        annual_plan_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_all_annual_plan_engagement(
            connection=connection,
            annual_plan_id=annual_plan_id
        )

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
                created_by="",
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
                created_by="",
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
                description="Engagement Archived",
                category=RecentActivityCategory.ENGAGEMENT_ARCHIVED,
                created_by="",
                created_at=datetime.now()
            )
        )

        return await return_checker(
            data=results,
            passed="Engagement Successfully Completed",
            failed="Failed Completing  Engagement"
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



@router.put("/opinion_rating/{engagement_id}")
async def edit_engagement_opinion_rating(
        engagement_id: str,
        opinion_rating: AddOpinionRating,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_engagement_opinion_rating(
            connection=connection,
            opinion_rating=opinion_rating,
            engagement_id=engagement_id
        )

        return await return_checker(
            data=results,
            passed="Opinion Rating Updated",
            failed="Failed Updating Opinion Rating"
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
