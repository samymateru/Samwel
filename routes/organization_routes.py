from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from models.organization_models import register_new_organization, get_user_organizations, get_entity_organizations, \
    get_organization_details, get_module_organization, edit_organization_details, delete_organization
from schema import ResponseMessage, CurrentUser
from schemas.organization_schemas import NewOrganization, ReadOrganization, UpdateOrganization
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.security.security import get_current_user
from utils import exception_response, return_checker

router = APIRouter(prefix="/organizations")

@router.post("/", status_code=201, response_model=ResponseMessage)
async def create_new_organization(
        organization: NewOrganization,
        user_id: Optional[str] = None,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        auth: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await register_new_organization(
            connection=connection,
            organization=organization,
            entity_id=auth.entity_id,
            creator=user_id
        )

        return await return_checker(
            data=results,
            passed="Organization Created Successfully",
            failed="Failed Creating  Organization"
        )


@router.get("/user/{user_id}", response_model=List[ReadOrganization])
async def fetch_user_organizations(
        user_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        data = await get_user_organizations(
            connection=connection,
            user_id=user_id
        )
        return data


@router.get("/entity/{entity_id}", response_model=List[ReadOrganization])
async def fetch_entity_organizations(
        entity_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        data = await get_entity_organizations(
            connection=connection,
            entity_id=entity_id
        )
        return data


@router.get("/module/{module_id}", response_model=ReadOrganization)
async def fetch_module_organization(
        module_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        data = await get_module_organization(
            connection=connection,
            module_id=module_id
        )
        if data is None:
            raise HTTPException(status_code=404, detail="Organization Not Found")
        return data


@router.get("/{organization_id}", response_model=ReadOrganization)
async def fetch_single_organization_details(
        organization_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        data = await get_organization_details(
            connection=connection,
            organization_id=organization_id
        )
        return data


@router.delete("/{organization_id}")
async def remove_organization(
        organization_id: str,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await delete_organization(
            connection=connection,
            organization_id=organization_id
        )

        return await return_checker(
            data=results,
            passed="Organization Remove Successfully",
            failed="Failed Removing  Organization"
        )


@router.put("/{organization_id}")
async def update_organization_details(
        organization_id: str,
        organization: UpdateOrganization,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
        _: CurrentUser = Depends(get_current_user)
):
    with exception_response():
        results = await edit_organization_details(
            connection=connection,
            organization=organization,
            organization_id=organization_id,
        )

        return await return_checker(
            data=results,
            passed="Organization Updated Successfully",
            failed="Failed Updating  Organization"
        )

