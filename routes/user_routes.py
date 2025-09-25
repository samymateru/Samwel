from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from models.user_models import register_new_user, create_new_organization_user, create_new_module_user, \
    get_module_users, get_organization_users, get_entity_users, get_module_user_details, delete_user_in_module, \
    edit_entity_user, edit_module_user
from schema import ResponseMessage, CurrentUser
from schemas.user_schemas import NewUser, UserTypes, BaseUser, ReadModuleUsers, UpdateEntityUser, UpdateModuleUser, \
ReadOrganizationUser
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.security.security import get_current_user
from utils import exception_response, return_checker

router = APIRouter(prefix="/users")


@router.post("/{organization_id}", status_code=201, response_model=ResponseMessage)
async def create_new_user(
        organization_id: str,
        user: NewUser,
        module_id: str = Query(None),
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


        organization_user_data = await create_new_organization_user(
            connection=connection,
            organization_id=organization_id,
            user_id=new_user_data.get("id"),
            administrator=False,
            owner=False,
            category="Management" if user.category == "Management" else "Module"
        )

        if organization_user_data is None:
            raise HTTPException(status_code=400, detail="Failed To Attach User To Organization")

        if user.type != UserTypes.MANAGEMENT:
            if module_id is None:
                raise HTTPException(status_code=400, detail="Module ID Needed")
            module_user_data = await create_new_module_user(
                connection=connection,
                user=user,
                module_id=module_id,
                user_id=new_user_data.get("id")
            )

            return await return_checker(
                data=module_user_data,
                passed="User Successfully Created",
                failed="Failed Creating  User"
            )

        else:
            return await return_checker(
                data=organization_user_data,
                passed="Management User Successfully Created",
                failed="Failed Creating  Management User"
            )


@router.get("/entity/{entity_id}", response_model=List[BaseUser])
async def fetch_entity_users(
        entity_id: Optional[str] = None,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
    ):
    with exception_response():
        data = await get_entity_users(
            connection=connection,
            entity_id=entity_id
        )

        return data


@router.get("/organization/{organization_id}", response_model=List[ReadOrganizationUser])
async def fetch_organization_users(
        organization_id: Optional[str] = None,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
    ):
    with exception_response():
        data = await get_organization_users(
            connection=connection,
            organization_id=organization_id
        )

        return data


@router.get("/module/{module_id}", response_model=List[ReadModuleUsers])
async def fetch_module_users(
        module_id: Optional[str] = None,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
    ):
    with exception_response():
        data = await get_module_users(
            connection=connection,
            module_id=module_id
        )

        return data


@router.get("/module/user/{module_id}", response_model=ReadModuleUsers)
async def fetch_module_user_details(
        module_id: Optional[str] = None,
        user_id: str = Query(...),
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
    ):
    with exception_response():
        data = await get_module_user_details(
            connection=connection,
            module_id=module_id,
            user_id=user_id
        )
        if data is None:
            raise HTTPException(status_code=404, detail="User Not Found")
        return data


@router.put("/entity_user/{user_id}")
async def updating_entity_user_details(
        user_id: str,
        user: UpdateEntityUser,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
    ):
    with exception_response():
        result = edit_entity_user(
            connection=connection,
            user=user,
            user_id=user_id
        )

        return await return_checker(
            data=result,
            passed="Entity User Successfully Updated",
            failed="Failed Updating  Entity User"
        )


@router.put("/module_user/{user_id}")
async def updating_module_user_details(
        user_id: str,
        user: UpdateModuleUser,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
    ):
    with exception_response():
        result = edit_module_user(
            connection=connection,
            user=user,
            user_id=user_id
        )

        return await return_checker(
            data=result,
            passed="Module User Successfully Updated",
            failed="Failed Updating  Module User"
        )


@router.delete("/module/{module_id}")
async def remove_user_in_module(
        module_id: str ,
        user_id: str = Query(...),
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
    ):
    with exception_response():
        results = await delete_user_in_module(
            connection=connection,
            module_id=module_id,
            user_id=user_id
        )

        return await return_checker(
            data=results,
            passed="User Successfully Deleted",
            failed="Failed Deleting  User"
        )





