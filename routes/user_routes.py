from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from models.user_models import register_new_user, create_new_organization_user, create_new_module_user
from schema import ResponseMessage, CurrentUser
from schemas.user_schemas import NewUser
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.security.security import get_current_user
from utils import exception_response, return_checker

router = APIRouter(prefix="/users")


@router.post("/", status_code=201, response_model=ResponseMessage)
async def create_new_user(
        user: NewUser,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        new_user_data = await register_new_user(
            connection=connection,
            entity_id=auth.entity_id,
            user=user,
            check_if_exist=False
        )

        if new_user_data is None:
            raise HTTPException(status_code=400, detail="Failed To Create New User")


        module_user_data = await create_new_module_user(
            connection=connection,
            user=user,
            module_id=auth.module_id,
            user_id=new_user_data.get("id")
        )

        if module_user_data is None:
            raise HTTPException(status_code=400, detail="Failed To Attach User To Module")


        organization_user_data = await create_new_organization_user(
            connection=connection,
            organization_id=auth.organization_id,
            user_id=new_user_data.get("id"),
            administrator=True,
            owner=True
        )

        return await return_checker(
            data=organization_user_data,
            passed="User Successfully Created",
            failed="Failed Creating  User"
        )


@router.get("/entity/{entity_id}")
async def fetch_entity_users_(
        entity_id: Optional[str] = None,
        _ = Depends(AsyncDBPoolSingleton.get_db_connection),
    ):
    with exception_response():
        pass


@router.get("/organization/{organization_id}")
async def fetch_organization_users_(
        organization_id: Optional[str] = None,
        _ = Depends(AsyncDBPoolSingleton.get_db_connection),
    ):
    with exception_response():
        pass


@router.get("/module/{module_id}")
async def fetch_module_users_(
        module_id: Optional[str] = None,
        _ = Depends(AsyncDBPoolSingleton.get_db_connection),
    ):
    with exception_response():
        pass


@router.get("/module/user/{module_id}")
async def fetch_module_user_details(
        module_id: Optional[str] = None,
        _ = Depends(AsyncDBPoolSingleton.get_db_connection),
    ):
    with exception_response():
        pass


@router.delete("/module/{module_id}")
async def remove_user_in_module(
        module_id: Optional[str] = None,
        _ = Depends(AsyncDBPoolSingleton.get_db_connection),
    ):
    with exception_response():
        pass


