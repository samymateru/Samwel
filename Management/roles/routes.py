from fastapi import APIRouter, Depends
from utils import get_current_user, get_async_db_connection
from schema import *
from Management.roles.databases import *
from Management.roles.schemas import *


router = APIRouter(prefix="/roles")

@router.get("/", response_model=Role)
async def fetch_roles(
        db = Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        roles = await get_roles(connection=db, company_id=user.company_id)
        if roles.__len__() == 0:
            raise HTTPException(status_code=400, detail="No roles")
        return roles[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/", response_model=ResponseMessage)
async def add_roles(
        role: Category,
        db = Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await add_role(connection=db, company_id=user.company_id, role=role)
        return ResponseMessage(detail="Role added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/", response_model=ResponseMessage)
async def add_roles(
        name: str,
        role: Category,
        db = Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_role(db, company_id=user.company_id, role=role, name=name)
        return ResponseMessage(detail="Role added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

