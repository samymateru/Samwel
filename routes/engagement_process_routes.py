from fastapi import APIRouter, Depends, HTTPException
from models.engagement_process_models import create_engagement_process_model, get_engagement_processes_model, \
    get_single_engagement_process_model, update_engagement_process_model, delete_single_engagement_process_model
from schema import ResponseMessage
from schemas.engagement_process_schemas import NewEngagementProcess, UpdateEngagementProcess
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker


router = APIRouter(prefix="/engagements")


@router.post("/context/engagement_process/{engagement_id}", status_code=201, response_model=ResponseMessage)
async def create_engagement_process(
        engagement_id: str,
        engagement_process: NewEngagementProcess,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await create_engagement_process_model(
            connection=connection,
            engagement_process=engagement_process,
            engagement_id=engagement_id
        )

        return await return_checker(
            data=results,
            passed="Engagement Process Successfully Created",
            failed="Failed Creating  Engagement Process"
        )



@router.get("/context/engagement_process/{engagement_id}")
async def get_engagement_processes(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_engagement_processes_model(
            connection=connection,
            engagement_id=engagement_id
        )

        return data



@router.get("/context/engagement_process/single/{engagement_process_id}")
async def get_single_engagement_process(
        engagement_process_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_single_engagement_process_model(
            connection=connection,
            engagement_process_id=engagement_process_id
        )

        if data is None:
            raise HTTPException(status_code=404, detail="Engagement Process Not Found")

        return data


@router.put("/context/engagement_process/{engagement_process_id}", response_model=ResponseMessage)
async def update_engagement_process(
        engagement_process_id: str,
        engagement_process: UpdateEngagementProcess,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():

        results = await update_engagement_process_model(
            connection=connection,
            engagement_process=engagement_process,
            engagement_process_id=engagement_process_id
        )

        return await return_checker(
            data=results,
            passed="Engagement Process Successfully Updated",
            failed="Failed Updating  Engagement Process"
        )



@router.delete("/context/engagement_process/{engagement_process_id}", response_model=ResponseMessage)
async def delete_single_engagement_process(
        engagement_process_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_single_engagement_process_model(
            connection=connection,
            engagement_process_id=engagement_process_id
        )

        return await return_checker(
            data=results,
            passed="Engagement Process Successfully Deleted",
            failed="Failed Deleting  Engagement Process"
        )
