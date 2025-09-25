from typing import List

from fastapi import APIRouter, Depends
from models.engagement_staff_models import create_new_engagement_staff_model, fetch_engagement_staff_model, \
    update_staff_model, delete_staff_model
from schema import ResponseMessage
from schemas.engagement_staff_schemas import NewEngagementStaff, UpdateStaff, ReadEngagementStaff
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker

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

        return await return_checker(
            data=results,
            passed="Engagement Staff Successfully Created",
            failed="Failed Creating  Engagement Staff"
        )


@router.get("/staff/{engagement_id}", response_model=List[ReadEngagementStaff])
async def fetch_engagement_staff(
        engagement_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await fetch_engagement_staff_model(
            connection=connection,
            engagement_id=engagement_id
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