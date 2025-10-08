from fastapi import APIRouter, Depends, Query
from utils import get_async_db_connection
from Management.users.databases import *
from Management.users.schemas import *
from utils import get_current_user
from schema import CurrentUser, ResponseMessage
from Management.roles.databases import *

router = APIRouter(prefix="/users")

@router.get("/entity/{entity_id}", response_model=List[EntityUser])
async def fetch_entity_users(
        entity_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_entity_users(db, entity_id=entity_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/organization/{organization_id}", response_model=List[OrganizationUser])
async def fetch_organization_users(
        organization_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_organizations_users(db, organization_id=organization_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/module/{module_id}", response_model=List[ModuleUser])
async def fetch_module_users(
        module_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_module_users(db, module_id=module_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/module/user/{user_id}", response_model=ModuleUser)
async def fetch_module_user(
        user_id: str,
        module_id: str = Query(...),
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_module_user(connection=db, module_id=module_id, user_id=user_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="User not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/{entity_id}", response_model=ResponseMessage)
async def invite_user_to_module(
        entity_id: str,
        new_user: NewUser,
        organization_id: str = Query(...),
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await invite_user(connection=db, entity_id=entity_id, organization_id=organization_id, new_user=new_user)
        return ResponseMessage(detail="User successfully invited")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.put("/{user_id}")
async def update_user(
        user_id: str,
        user: UpdateModuleUser,
        db = Depends(get_async_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        await update_module_user(connection=db, user=user, user_id=user_id, module_id=current_user.module_id)
        return ResponseMessage(detail="user successfully updated")
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db = Depends(get_async_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="your not admin")
    try:
        pass
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
