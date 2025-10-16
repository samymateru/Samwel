from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from models.engagement_models import get_single_engagement_details
from models.engagement_staff_models import create_new_engagement_staff_model, fetch_engagement_staff_model, \
    update_staff_model, delete_staff_model
from models.notification_models import add_notification_to_user_model
from models.user_models import get_user_by_email
from schema import ResponseMessage
from schemas.engagement_staff_schemas import NewEngagementStaff, UpdateStaff, ReadEngagementStaff
from schemas.notification_schemas import CreateNotifications, NotificationsStatus
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.logging.logger import global_logger
from utils import exception_response, return_checker, get_unique_key

router = APIRouter(prefix="/engagements")

@router.post("/staff/{engagement_id}", status_code=201, response_model=ResponseMessage)
async def create_new_engagement_staff(
        engagement_id: str,
        staff: NewEngagementStaff,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():

        results = await create_new_engagement_staff_model(
            connection=connection,
            staff=staff,
            engagement_id=engagement_id
        )

        if results is None:
            raise HTTPException(status_code=400, detail="Failed To Create Engagement Staff")


        user_data = await get_user_by_email(
            connection=connection,
            email=staff.email
        )

        if user_data is None:
            raise HTTPException(status_code=404, detail=f"User With Email {staff.email} Not Found")

        engagement_data = await get_single_engagement_details(
            connection=connection,
            engagement_id=engagement_id
        )

        if engagement_data is None:
            global_logger.exception("Engagement Not Found")


        await add_notification_to_user_model(
            connection=connection,
            notification=CreateNotifications(
                id=get_unique_key(),
                title="Engagement invitation",
                user_id=user_data.get("id"),
                message=f"Your have been invited to Engagement: {engagement_data.get('name')} as {staff.role}",
                status=NotificationsStatus.NEW,
                created_at=datetime.now()
            )
        )


        return await return_checker(
            data=True,
            passed="Engagement Staff Successfully Created",
            failed="Failed Creating  Engagement Staff"
        )



@router.get("/staff/{engagement_id}", response_model=List[ReadEngagementStaff])
async def fetch_engagement_staff(
        engagement_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection)
):
    with exception_response():
        data = await fetch_engagement_staff_model(
            connection=connection,
            engagement_id=engagement_id,
        )

        return data



@router.put("/staff/{staff_id}", response_model=ResponseMessage)
async def update_staff(
        staff_id: str,
        staff: UpdateStaff,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_staff_model(
            connection=connection,
            staff=staff,
            staff_id=staff_id
        )

        return await return_checker(
            data=results,
            passed="Engagement Staff Successfully Updated",
            failed="Failed Updating  Engagement Staff"
        )



@router.delete("/staff/{staff_id}", response_model=ResponseMessage)
async def delete_staff(
        staff_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_staff_model(
            connection=connection,
            staff_id=staff_id
        )

        return await return_checker(
            data=results,
            passed="Engagement Staff Successfully Deleted",
            failed="Failed Deleting  Engagement Staff"
        )