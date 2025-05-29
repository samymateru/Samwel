from fastapi import APIRouter, Depends, HTTPException
from Management.organization.databases import get_user_organizations
from Management.users.schemas import __User__
from utils import get_db_connection, get_async_db_connection
from Management.users.databases import *
from Management.users.schemas import *
from utils import get_current_user
from schema import CurrentUser, ResponseMessage
from Management.roles.databases import *

router = APIRouter(prefix="/users")

@router.get("/organization/{organization_id}", response_model=List[__User__])
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

@router.get("/module/{module_id}", response_model=List[__User__])
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

@router.get("/", response_model=__User__)
async def fetch_user(
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_user(connection=db, user_id=user.user_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="User not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/{organization_id}", response_model=ResponseMessage)
async def create_new_user(
        organization_id: str,
        user_: User,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await new_user(connection=db, user=user_,  organization_id=organization_id)
        return ResponseMessage(detail="User successfully created")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.put("/")
async def update_user(
        user_update: User,
        db = Depends(get_async_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        pass
        return ResponseMessage(detail="user successfully updated")
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db = Depends(get_db_connection),
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



