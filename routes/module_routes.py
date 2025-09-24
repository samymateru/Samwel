from typing import List
from fastapi import APIRouter, Depends, HTTPException
from core.constants import plans
from models.module_models import register_new_module, get_user_modules, get_organization_modules, get_module_details, \
    generate_module_activation_data, get_activation_data, activate_module, add_licence_to_module
from schema import ResponseMessage, CurrentUser
from schemas.module_schemas import NewModule, ReadModule
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.security.security import get_current_user
from utils import exception_response, return_checker

router = APIRouter(prefix="/module")

@router.post("/", status_code=201, response_model=ResponseMessage)
async def create_new_module(
        module: NewModule,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
    ):
    with exception_response():
        results = await register_new_module(
            connection=connection,
            module=module,
            organization_id=auth.organization_id
        )

        if results is None:
            raise HTTPException(status_code=400, detail="Failed To Register Module")

        licence = plans.get(module.licence_id)

        if licence is None:
            raise HTTPException(status_code=404, detail="Licence Not Found")

        licence_data = await add_licence_to_module(
            connection=connection,
            module_id=results.get("id"),
            plan_id=module.licence_id,
            licence=licence
        )

        if licence_data is None:
            raise HTTPException(status_code=400, detail="Failed To Add Licence To Module")

        activation_data = await generate_module_activation_data(
            connection=connection,
            module_id=results.get("id")
        )

        return await return_checker(
            data=activation_data,
            passed="Module Successfully Created",
            failed="Failed Creating  Module"
        )


@router.get("/user/{user_id}", response_model=List[ReadModule])
async def fetch_user_modules(
        user_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        data = await get_user_modules(
            connection=connection,
            user_id=user_id
        )

        return data


@router.get("/organization/{organization_id}", response_model=List[ReadModule])
async def fetch_organization_modules(
        organization_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        data = await get_organization_modules(
            connection=connection,
            organization_id=organization_id
        )
        return data


@router.get("/{module_id}", response_model=ReadModule)
async def fetch_single_module_details(
        module_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        data = await get_module_details(
            connection=connection,
            module_id=module_id
        )

        if data is None:
            raise HTTPException(status_code=404, detail="Module Not Exists")
        return data


@router.put("/activation/{activation_token}", response_model=ResponseMessage)
async def activate_module_licence(
        activation_token: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        activation_data = await get_activation_data(
            connection=connection,
            activation_token=activation_token
        )

        if activation_data is None:
            raise HTTPException(status_code=404, detail="Activation Token Not Found")

        results = await activate_module(
            connection=connection,
            module_id=activation_data.get("module_id")
        )

        return await return_checker(
            data=results,
            passed="Module Activation Succeed",
            failed="Failed Activating  Module"
        )
