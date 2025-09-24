from fastapi import APIRouter, Depends, Query
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response

router = APIRouter(prefix="/notifications")

@router.get("/{user_id}")
async def fetch_all_user_notification(
        user_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass

@router.delete("/{notification_id}")
async def remove_single_user_notification(
        notification_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass

@router.delete("/{user_id}")
async def remove_all_user_notifications(
        user_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass