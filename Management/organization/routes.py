from fastapi import APIRouter, Depends
from schema import ResponseMessage, CurrentUser
from Management.organization.databases import *
from utils import get_async_db_connection, get_current_user
from typing import List

router = APIRouter(prefix="/organization")

@router.post("/{entity_id}", response_model=ResponseMessage)
async def create_new_organization(
        entity_id: str,
        organization: Organization,
        db=Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await new_organization(db, organization=organization, entity_id=entity_id, user_id=user.user_id)
        return ResponseMessage(detail="Organization successfully created")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/")
async def fetch_user_organizations(
        db=Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_user_organizations(db, user_id=user.user_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=401, detail="No organization found")
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{organization_id}", response_model=Organization)
async def fetch_organization_data(
        organization_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_organization_data(db, organization_id=organization_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="Organization not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{organization_id}", response_model=ResponseMessage)
async def edit_entity_organization(
        organization_id: str,
        organization: Organization,
        db=Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await update_organization(connection=db, organization=organization, organization_id=organization_id)
        return ResponseMessage(detail="Organization updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)