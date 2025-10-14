from typing import List
from fastapi import APIRouter, Depends
from models.management_models import create_new_management_model, fetch_organization_management_model, \
    update_organization_management_model, delete_organization_management_model
from schema import ResponseMessage
from schemas.management_schemas import NewManagement, UpdateManagement, ReadManagement
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker


router = APIRouter(prefix="/management")



@router.post("/{organization_id}", status_code=201, response_model=ResponseMessage)
async def create_new_management(
        organization_id: str,
        management: NewManagement,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await create_new_management_model(
            connection=connection,
            management=management,
            organization_id=organization_id
        )

        return await return_checker(
            data=results,
            passed="Management Successfully Created",
            failed="Failed Creating Management"
        )



@router.get("/{organization_id}", response_model=List[ReadManagement])
async def fetch_organization_management(
        organization_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():

        data = await fetch_organization_management_model(
            connection=connection,
            organization_id=organization_id
        )

        return data



@router.put("/{management_id}", response_model=ResponseMessage)
async def update_organization_management(
        management_id: str,
        management: UpdateManagement,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():

        results = await update_organization_management_model(
            connection=connection,
            management=management,
            management_id=management_id
        )

        return await return_checker(
            data=results,
            passed="Management Successfully Updated",
            failed="Failed Updating Management"
        )


@router.delete("/{management_id}", response_model=ResponseMessage)
async def delete_organization_management(
        management_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_organization_management_model(
            connection=connection,
            management_id=management_id
        )

        return await return_checker(
            data=results,
            passed="Management Successfully Deleted",
            failed="Failed Deleting Management"
        )