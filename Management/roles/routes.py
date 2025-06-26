from fastapi import APIRouter, Depends
from typing import List
from constants import head_of_audit, audit_reviewer, audit_lead, audit_member, business_manager, risk_manager, \
    compliance_manager
from utils import get_current_user, get_async_db_connection
from schema import *
from Management.roles.databases import *
from Management.roles.schemas import *


router = APIRouter(prefix="/roles")

@router.get("/{module_id}", response_model=List[Roles])
async def fetch_roles(
        module_id: str,
        db = Depends(get_async_db_connection),
        #user: CurrentUser = Depends(get_current_user)
):
    #if user.status_code != 200:
        #raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        roles : List[Roles] = [
            head_of_audit,
            audit_lead,
            audit_reviewer,
            audit_member,
            business_manager,
            risk_manager,
            compliance_manager
        ]
        data = await get_roles(connection=db, module_id=module_id)
        return roles + data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/{module_id}", response_model=ResponseMessage)
async def add_roles(
        module_id: str,
        role: Roles,
        db = Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await add_role(connection=db, module_id=module_id, role=role)
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

