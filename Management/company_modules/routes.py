from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from Management.company_modules import databases
from Management.company_modules.schemas import *
from typing import Tuple, List, Dict
from utils import get_current_user
from schema import CurrentUser
from datetime import datetime

router = APIRouter(prefix="/company_modules")

@router.get("/")
def get_get_company_modules(
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="your not admin")
    try:
        company_module_data: List[Dict] = databases.get_company_modules(db)
        if company_module_data.__len__() == 0:
            return {"message": "no company modules available", "code": 404}
        return company_module_data
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/new_company_module")
def create_new_company_module(
        company_module: NewCompanyModule,
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="your not admin")
    new_company_module: Tuple = (
        current_user.company_id,
        company_module.module_id,
        company_module.is_active,
        datetime.now(),
        datetime.now()
    )
    try:
        databases.create_new_company_module(db, new_company_module)
        return {"message": "company module successfully created", "code": 501}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/update_company_module")
def update_company_module(
        audit_log: UpdateCompanyModule,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="your not admin")
    try:
        databases.update_company_module(db, audit_log)
        return {"message": "company module successfully updated", "code": 502}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/delete_company_module")
def delete_company_module(
        log_id: DeleteCompanyModule,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="your not admin")
    try:
        databases.delete_company_module(db, log_id.log_id)
        return {"message": "successfully delete the company module", "code": 503}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

