from fastapi import APIRouter, Depends

from Management.organization.databases import create_organization
from Management.organization.schemas import Organization, OrganizationStatus
from Management.users.databases import create_new_user, attach_user_to_organization
from Management.users.schemas import OrganizationsUsers, User
from utils import get_async_db_connection, generate_hash_password
from schema import CurrentUser, ResponseMessage
from utils import get_current_user
from background import set_company_profile
from Management.entity.databases import *
import asyncio

router = APIRouter(prefix="/entity")

@router.post("/", response_model=ResponseMessage)
async def create_entity(
        entity: NewEntity,
        db_async = Depends(get_async_db_connection),
    ):
    try:
        organization = Organization(
            id=get_unique_key(),
            name=entity.name,
            email=entity.email,
            telephone=entity.telephone,
            type=entity.type,
            website=entity.website,
            status=OrganizationStatus.OPENED.value,
            default=True,
            created_at=datetime.now()
        )

        entity_id = await create_new_entity(connection=db_async, entity=entity)

        new_user = User(
            id=get_unique_key(),
            name=entity.owner,
            email=entity.email,
            telephone=entity.telephone,
            password=generate_hash_password(entity.password),
            administrator=True,
            owner=True,
            entity_id=entity_id
        )

        organization_id = await create_organization(connection=db_async, organization=organization, entity_id=entity_id)
        user_id = await create_new_user(connection=db_async, new_user=new_user)

        attach_data = OrganizationsUsers(
            organization_id=organization_id,
            user_id=user_id,
            administrator=True,
            owner=True
        )
        await attach_user_to_organization(connection=db_async, attach_data=attach_data)
        asyncio.create_task(set_company_profile(company_id=entity_id))
        return ResponseMessage(detail="Entity successfully created")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/", response_model=Entity)
async def fetch_entity_by_email(
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_entities_by_email(db, email=user.user_email)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="No data found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{organization_id}", response_model=Entity)
async def fetch_entity_by_email(
        organization_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_entity(db, organization_id=organization_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="Entity not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)







