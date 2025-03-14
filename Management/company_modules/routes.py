from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from Management.company_modules.databases import *
from Management.company_modules.schemas import *
from Management.users.schemas import Module
from Management.users.databases import add_user_module
from typing import List
from utils import get_current_user
from schema import CurrentUser, ResponseMessage

router = APIRouter(prefix="/company_modules")

@router.get("/", response_model=List[CompanyModule])
def fetch_company_modules(
        db = Depends(get_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_company_modules(db, column="company", value=user.company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/{company_id}", response_model=ResponseMessage)
def create_new_company_module(
        company_id: int,
        company_module: CompanyModule,
        db = Depends(get_db_connection),
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
        id = add_new_company_module(connection=db, company_module=module, company_id=company_id)
        user_module = Module(
            id = id,
            name = module.name
        )
        add_user_module(connection=db, module=user_module, user_id=user.user_id)
        return {"detail": "Company module create successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)



