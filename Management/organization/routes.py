from fastapi import APIRouter, Depends

from Management.users.databases import attach_user_to_organization
from Management.users.schemas import OrganizationsUsers
from schema import ResponseMessage, CurrentUser
from Management.organization.databases import *
from utils import get_async_db_connection, get_current_user, get_unique_key
from typing import List

router = APIRouter(prefix="/organization")

@router.post("/{entity_id}", response_model=ResponseMessage)
async def create_new_organization(
        entity_id: str,
        new_organization: NewOrganization,
        db=Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        organization = Organization(
            id=get_unique_key(),
            name=new_organization.name,
            email=new_organization.email,
            telephone=new_organization.telephone,
            type=new_organization.type,
            website=new_organization.website,
        )

        organization_id = await create_organization(db, organization=organization, entity_id=entity_id, user_id=user.user_id)

        attach_data = OrganizationsUsers(
            organization_id=organization_id,
            user_id=user.user_id,
            administrator=True,
            owner=True
        )

        await attach_user_to_organization(connection=db, attach_data=attach_data)
        return ResponseMessage(detail="Organization successfully created")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/", response_model=List[Organization])
async def fetch_user_organizations(
        db=Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_user_organizations(db, user_id=user.user_id)
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

@router.delete("/{organization_id}", response_model=ResponseMessage)
async def remove_entity_organization(
        organization_id: str,
        db=Depends(get_async_db_connection),
        #user: CurrentUser  = Depends(get_current_user)
    ):
    #if user.status_code != 200:
        #raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await trash_organizations(connection=db, organization_id=organization_id)
        return ResponseMessage(detail="Organization deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)