from typing import List
from fastapi import APIRouter, Depends
from models.notification_models import fetch_all_user_notification_model, remove_single_user_notification_model, \
    remove_all_user_notifications_model, update_user_notification_after_read_model, add_notification_to_user_model
from models.recent_activity_models import fetch_recent_activities
from schema import ResponseMessage
from schemas.notification_schemas import ReadUserNotification, CreateNotifications, NotificationsStatus
from schemas.recent_activities_schemas import RecentActivities
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker, get_unique_key
from datetime import datetime


router = APIRouter(prefix="/notifications")


@router.get("/{user_id}", response_model=List[ReadUserNotification])
async def fetch_all_user_notification(
        user_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():

        data = await fetch_all_user_notification_model(
            connection=connection,
            user_id=user_id
        )

        return data



@router.put("/{notification_id}", response_model=ResponseMessage)
async def update_user_notification_after_read(
        notification_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_user_notification_after_read_model(
            connection=connection,
            notification_id=notification_id
        )

        return await return_checker(
            data=results,
            passed="Notification Successfully Read",
            failed="Failed Reading  Notification"
        )



@router.delete("/single/{notification_id}", response_model=ResponseMessage)
async def remove_single_user_notification(
        notification_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await remove_single_user_notification_model(
            connection=connection,
            notification_id=notification_id
        )

        return await return_checker(
            data=results,
            passed="Notification Successfully Deleted",
            failed="Failed Deleting  Notification"
        )



@router.delete("/all/{user_id}", response_model=ResponseMessage)
async def remove_all_user_notifications(
        user_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await remove_all_user_notifications_model(
            connection=connection,
            user_id=user_id
        )

        return await return_checker(
            data=results,
            passed="Notifications Successfully Deleted",
            failed="Failed Deleting  Notifications"
        )



@router.get("/recent_activities/{module_id}", response_model=List[RecentActivities])
async def fetch_module_recent_activities(
        module_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await fetch_recent_activities(
            connection=connection,
            module_id=module_id
        )
        return data