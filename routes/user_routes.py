from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query

from core.tables import Tables
from models.user_models import register_new_user, create_new_organization_user, create_new_module_user, \
    get_module_users, get_organization_users, get_entity_users, get_module_user_details, delete_user_in_module, \
    edit_entity_user, edit_module_user
from schema import ResponseMessage, CurrentUser
from schemas.notification_schemas import SendUserInvitationNotification, NewUserInvitation
from schemas.user_schemas import NewUser, BaseUser, ReadModuleUsers, UpdateEntityUser, UpdateModuleUser, \
    ReadOrganizationUser, OrganizationUserColumns, UpdateOrganizationUserRole, OrganizationUserRolesTypes
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.connections.postgres.update import UpdateQueryBuilder
from services.logging.logger import global_logger
from services.security.security import get_current_user
from utils import exception_response, return_checker

router = APIRouter(prefix="/users")


@router.post("/{organization_id}", status_code=201, response_model=ResponseMessage)
async def create_new_user(
        organization_id: str,
        user: NewUser,
        module_id: str = Query(...),
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        password = "123456"


        new_user_data = await register_new_user(
            connection=connection,
            entity_id=auth.entity_id,
            password=password,
            user=user,
            check_if_exist=False
        )


        if new_user_data is None:
            global_logger.exception("Failed To Create New User")
            raise HTTPException(status_code=400, detail="Failed To Create New User")


        organization_user_data = await create_new_organization_user(
            connection=connection,
            organization_id=organization_id,
            user_id=new_user_data.get("id"),
            administrator=False,
            owner=False,
            management_title=user.title
        )


        if organization_user_data is None:
            raise HTTPException(status_code=400, detail="Failed To Attach User To Organization")


        module_user_data = await create_new_module_user(
            connection=connection,
            user=user,
            module_id=module_id,
            user_id=new_user_data.get("id"),
            organization_id=organization_id
        )


        data = SendUserInvitationNotification(
            to=user.email,
            template_id=41703594,
            template_model=NewUserInvitation(
                name=user.name,
                email=user.email,
                password=password
            )
        )


        _ = { "mode": "single", "data": data.model_dump() }


        return await return_checker(
            data=module_user_data,
            passed="User Successfully Created",
            failed="Failed Creating  User"
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



@router.get("/organization/{organization_id}")
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
        module_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
    ):
    with exception_response():
        data = await get_module_users(
            connection=connection,
            module_id=module_id,
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



@router.put("/organization_roles/{organization_id}")
async def change_organization_user_role(
        organization_id: str,
        action: OrganizationUserRolesTypes,
        user_id: str = Query(...),
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():

        __user__ = UpdateOrganizationUserRole(
            administrator=True if action.value == OrganizationUserRolesTypes.UPGRADE else False
        )


        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ORGANIZATIONS_USERS.value)
            .values(__user__)
            .where({OrganizationUserColumns.ORGANIZATION_ID.value: organization_id})
            .where({OrganizationUserColumns.USER_ID.value: user_id})
            .check_exists({OrganizationUserColumns.USER_ID.value: user_id})
            .returning(OrganizationUserColumns.ORGANIZATION_USER_ID.value)
            .execute()
        )


        return await return_checker(
            data=builder,
            passed="User Role Successfully Updated",
            failed="Failed Updating  User Role"
        )





