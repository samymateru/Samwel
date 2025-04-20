from fastapi import APIRouter, Depends
from utils import get_async_db_connection
from Management.company_modules.databases import *
from Management.company_modules.schemas import *
from Management.users.schemas import Module
from Management.users.databases import add_user_module
from typing import List
from utils import get_current_user
from schema import CurrentUser, ResponseMessage

router = APIRouter(prefix="/company_modules")

@router.get("/", response_model=List[CompanyModule])
async def fetch_company_modules(
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_company_modules(db, company_id=user.company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/", response_model=ResponseMessage)
async def create_new_company_module(
        company_module: CompanyModule,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        module = CompanyModule(
            name=company_module.name,
            purchase_date=None,
            status="active"
        )
        id = await add_new_company_module(connection=db, company_module=module, company_id=user.company_id)
        user_module = Module(
            id = id,
            name = module.name
        )
        await add_user_module(connection=db, module=user_module, user_id=user.user_id)
        return ResponseMessage(detail="Company module create successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)



