from fastapi import APIRouter, Depends

from services.connections.query_builder import ReadBuilder
from utils import get_current_user, get_async_db_connection
from schema import *
from Management.roles.databases import *
from Management.roles.schemas import *
from constants import administrator, head_of_audit, member, audit_lead, audit_reviewer, audit_member, business_manager, \
    risk_manager, compliance_manager

roles_map = {
    "Administrator": administrator,
    "Head of Audit": head_of_audit,
    "Member": member,
    "Audit Lead": audit_lead,
    "Audit Reviewer": audit_reviewer,
    "Audit Member": audit_member,
    "Business Manager": business_manager,
    "Risk Manager": risk_manager,
    "Compliance Manager": compliance_manager
}

router = APIRouter(prefix="/roles")

@router.get("/{module_id}", response_model=List[Roles])
async def fetch_roles(
        module_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        roles : List[Roles] = [
            head_of_audit,
            audit_lead,
            administrator,
            member,
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

@router.get("/role/{role_id}", response_model=Roles)
async def fetch_role(
        role_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        for role_value in roles_map.items():
            if role_value[1].id == role_id:
                return role_value[1]

        qb = await (ReadBuilder(connection=db)
                    .from_table("roles")
                    .where("id", role_id)).fetch_one()

        if qb is None:
            raise HTTPException(status_code=404, detail="Role not found")
        return qb
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

@router.put("/{role_id}", response_model=ResponseMessage)
async def edit_roles(
        role_id: str,
        role: EditRole,
        db = Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_role(db, role=role, role_id=role_id, module_id=user.module_id)
        return ResponseMessage(detail="Role edited successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

