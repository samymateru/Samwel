from fastapi import APIRouter, Depends

from mx import email_queue
from utils import get_async_db_connection
from schema import CurrentUser, ResponseMessage, EmailSchema
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
        entity_id = await create_new_entity(connection=db_async, entity=entity)
        asyncio.create_task(set_company_profile(company_id=entity_id))
        email = EmailSchema(to=entity.email, subject="Entity created", body="Congrats new entity has been created success fully please visit our login page with your credentials")
        await email_queue.put(email.model_dump())
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







