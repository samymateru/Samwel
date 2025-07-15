from fastapi import APIRouter, Depends

from Management.users.databases import attach_user_to_module
from Management.users.schemas import ModulesUsers
from utils import get_async_db_connection
from Management.company_modules.databases import *
from typing import List
from utils import get_current_user
from schema import CurrentUser, ResponseMessage

router = APIRouter(prefix="/modules")

@router.get("/organization/{organization_id}", response_model=List[Module])
async def fetch_organization_modules(
        organization_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_organization_modules(connection=db, organization_id=organization_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{organization_id}", response_model=List[Module])
async def fetch_users_modules(
        organization_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_users_modules(connection=db, user_id="23777b70230b", organization_id=organization_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/{organization_id}", response_model=ResponseMessage)
async def create_new_organization_module(
        organization_id: str,
        new_module: NewModule,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        module = Module(
            id=get_unique_key(),
            name=new_module.name
        )

        module_id = await add_new_organization_module(
            connection=db,
            module=module,
            organization_id=organization_id
        )

        attach_data = ModulesUsers(
            module_id=module_id,
            user_id=user.user_id,
            title="Owner",
            role="Administrator"
        )

        await attach_user_to_module(connection=db, attach_data=attach_data)

        return ResponseMessage(detail="Organization module create successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)



