from typing import List
from fastapi import APIRouter, Depends, HTTPException
from models.role_models import create_role_model, get_module_roles_model, get_role_data_model, update_role_model, \
    delete_role_model
from schemas.role_schemas import CreateRole, NewRole, Default, ReadRole, UpdateRole
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, get_unique_key, return_checker
from datetime import datetime

router = APIRouter(prefix="/roles")


@router.post("/{module_id}")
async def create_module_role(
        module_id: str,
        new_role: NewRole,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with (exception_response()):
        """
        Create a new role for a given module.
        - Ensures role name uniqueness per module.
        - Returns the created role with full details.
        """
        role = CreateRole(
            **new_role.model_dump(),
            id=get_unique_key(),
            reference="",
            default=Default.NO,
            module=module_id,
            created_at=datetime.now()
        )

        results = await create_role_model(
            connection=connection,
            role=role
        )

        return await return_checker(
            data=results,
            passed="Role Successfully Created",
            failed="Failed Creating  Role"
        )



@router.get("/{module_id}", response_model=List[ReadRole])
async def fetch_module_roles(
        module_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_module_roles_model(
            connection=connection,
            module_id=module_id
        )

        return data



@router.get("/single/{role_id}", response_model=ReadRole)
async def fetch_single_role_data(
        role_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_role_data_model(
            connection=connection,
            role_id=role_id
        )

        if data is None:
            raise HTTPException(status_code=404, detail="Role Not Found")

        return data






@router.put("/{role_id}")
async def update_role_data(
        role_id: str,
        role: UpdateRole,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await update_role_model(
            connection=connection,
            role=role,
            role_id=role_id
        )

        return await return_checker(
            data=results,
            passed="Role Successfully Updated",
            failed="Failed Updating  Role"
        )




@router.delete("/{role_id}")
async def delete_role_data(
        role_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await delete_role_model(
            connection=connection,
            role_id=role_id
        )

        return await return_checker(
            data=results,
            passed="Role Successfully Deleted",
            failed="Failed Deleting  Role"
        )
