from typing import List

from fastapi import APIRouter, Depends

from models.notification_models import fetch_all_user_notification_model, remove_single_user_notification_model, \
    remove_all_user_notifications_model, update_user_notification_after_read_model
from schema import ResponseMessage
from schemas.notification_schemas import ReadUserNotification, UpdateNotificationRead
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker

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
        notification: UpdateNotificationRead,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_user_notification_after_read_model(
            connection=connection,
            notification=notification,
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