from fastapi import APIRouter, Depends
from schema import ResponseMessage, CurrentUser
from Management.organization.databases import *
from utils import get_async_db_connection, get_current_user
from typing import List

router = APIRouter(prefix="/organization")

@router.post("/", response_model=ResponseMessage)
async def create_new_organization(
        organization: Organization,
        db=Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await new_organization(db, organization=organization, entity_id=user.company_id)
        return ResponseMessage(detail="Organization created successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/", response_model=List[Organization])
async def get_entity_organization(
        db=Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await fetch_organization(db, company_id=user.company_id)
        return data
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
        await update_organization(db, organization=organization, organization_id=organization_id)
        return ResponseMessage(detail="Organization updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)