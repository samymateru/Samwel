import asyncio
from fastapi import APIRouter, Depends, HTTPException
from background import set_company_profile
from models.entity_models import register_new_entity, get_entity_details, get_organization_entity_details, \
    delete_entity_completely, edit_entity_data
from models.organization_models import register_new_organization
from models.user_models import register_new_user, create_new_organization_user
from schema import ResponseMessage
from schemas.entity_schemas import NewEntity, ReadEntity, UpdateEntity
from schemas.organization_schemas import NewOrganization
from schemas.user_schemas import NewUser, UserTypes
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker

router = APIRouter(prefix="/entity")


@router.post("/", status_code=201, response_model=ResponseMessage)
async def create_new_entity(
        entity: NewEntity,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        entity_data = await register_new_entity(connection=connection, entity=entity)
        if entity_data is None:
            raise HTTPException(status_code=400, detail="Failed Creating  Entity")

        user = NewUser(
            name=entity.owner,
            email=entity.email,
            type=UserTypes.AUDIT.value
        )


        user_data = await register_new_user(
            connection=connection,
            user=user,
            entity_id=entity_data.get("id"),
            password=entity.password,
            administrator=True,
            owner=True
        )

        if user_data is None:
            raise HTTPException(status_code=400, detail="Failed Creating  User During Entity Creation")

        organization = NewOrganization(
            name=entity.name,
            email=entity.email,
            type=entity.type
        )

        organization_data = await register_new_organization(
            connection=connection,
            organization=organization,
            entity_id=entity_data.get("id"),
            creator=user_data.get("id"),
            default=True
        )

        if organization_data is None:
            raise HTTPException(status_code=400, detail="Failed Creating  Organization During Entity Creation")

        organization_user_data = await create_new_organization_user(
            connection=connection,
            organization_id=organization_data.get("id"),
            user_id=user_data.get("id"),
            administrator=True,
            owner=True,
            management_title="Organization Owner"
        )

        asyncio.create_task(set_company_profile(company_id=entity_data.get("id")))

        return await return_checker(
            data=organization_user_data,
            passed="Entity Successfully Created",
            failed="Failed Creating  Entity"
        )


@router.get("/{entity_id}", response_model=ReadEntity)
async def fetch_entity_data(
        entity_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_entity_details(
            connection=connection,
            entity_id=entity_id
        )
        if data is None:
            raise HTTPException(status_code=404, detail="Entity Not Found")
        return data


@router.get("/organization/{organization_id}", response_model=ReadEntity)
async def fetch_organization_entity_data(
        organization_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await get_organization_entity_details(
            connection=connection,
            organization_id=organization_id
        )
        if data is None:
            raise HTTPException(status_code=404, detail="Organization Entity Not Found")
        return data


@router.delete("/{entity_id}", )
async def remove_entity(
        entity_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        data = await delete_entity_completely(
            connection=connection,
            entity_id=entity_id
        )

        return await return_checker(
            data=data,
            passed="Entity Successfully Deleted",
            failed="Failed Deleting  Entity"
        )


@router.put("/{entity_id}", )
async def update_entity_data(
        entity_id: str,
        entity: UpdateEntity,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        results = await edit_entity_data(
            connection=connection,
            entity=entity,
            entity_id=entity_id
        )

        return await return_checker(
            data=results,
            passed="Entity Successfully Updated",
            failed="Failed Updating  Entity"
        )
