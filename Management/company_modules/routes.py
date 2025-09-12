from fastapi import APIRouter, Depends
from Management.subscriptions.databases import attach_licence_to_module
from Management.users.databases import attach_user_to_module, remove_module, attach_risk_user_to_module
from Management.users.schemas import ModulesUsers
from core.constants import plans
from utils import get_async_db_connection
from Management.company_modules.databases import *
from typing import List
from utils import get_current_user
from schema import CurrentUser, ResponseMessage

router = APIRouter(prefix="/modules")

@router.get("/organization/{organization_id}", response_model=List[OrganizationModule])
async def fetch_organization_modules(
        organization_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_organization_modules(connection=db, organization_id=organization_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/{organization_id}", response_model=List[ReadModule])
async def fetch_users_modules(
        organization_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        risk = await get_risk_module_users(connection=db, user_id=user.user_id, organization_id=organization_id)
        eaudit = await get_users_modules(connection=db, user_id=user.user_id, organization_id=organization_id)
        return risk + eaudit
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{module_id}", response_model=ResponseMessage)
async def delete_module(
        module_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await remove_module(connection=db, module_id=module_id)
        return ResponseMessage(detail="Module deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/{organization_id}", response_model=ResponseMessage)
async def create_new_organization_module(
        organization_id: str,
        new_module: NewModule,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        if new_module.name == "eAuditNext" or new_module.name == "eRisk":
            module = Module(
                id=get_unique_key(),
                name=new_module.name
            )

            licence = plans.get(new_module.licence_id)
            if licence is None:
                raise HTTPException(status_code=400, detail="Unknown Licence")

            module_id = await add_new_organization_module(
                connection=db,
                module=module,
                organization_id=organization_id
            )

            if new_module.name == "eAuditNext":
                attach_data = ModulesUsers(
                    module_id=module_id,
                    user_id=user.user_id,
                    title="Administrator",
                    role="Administrator",
                    type="audit",
                )

                await attach_user_to_module(connection=db, attach_data=attach_data)
                await attach_licence_to_module(connection=db, licence=plans.get(new_module.licence_id), module_id=module_id)

            if new_module.name == "eRisk":
                attach_data = ModulesUsers(
                    module_id=module_id,
                    user_id=user.user_id,
                    role="Administrator",
                    type="Risk",
                    status="Active"
                )
                await attach_risk_user_to_module(connection=db, attach_data=attach_data)

            return ResponseMessage(detail="Organization module create successfully")
        else:
            raise HTTPException(status_code=400, detail="Module Not Ready Yet")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
