from fastapi import APIRouter, Depends
from utils import get_async_db_connection
from Management.company_modules.databases import *
from typing import List
from utils import get_current_user
from schema import CurrentUser, ResponseMessage

router = APIRouter(prefix="/modules")

@router.get("/{organization_id}", response_model=List[Module])
async def fetch_organization_modules(
        organization_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_organization_modules(connection=db, organization_id=organization_id)
        for module in data:
            for user_ in module.get("users"):
                if user.user_id == user_.get("id", ""):
                    module["assigned"] = True

        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/")
async def fetch_users_modules(
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_users_modules(connection=db, user_id=user.user_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/{organization_id}", response_model=ResponseMessage)
async def create_new_organization_module(
        organization_id: str,
        module: Module,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await add_new_organization_module(
            connection=db,
            organization_module=module,
            organization_id=organization_id,
            user_id=user.user_id
        )
        return ResponseMessage(detail="Organization module create successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)



