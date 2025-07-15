from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from Management.modules import databases
from Management.modules.schemas import *
from typing import Tuple, Dict
from utils import get_current_user
from schema import CurrentUser
from datetime import datetime

router = APIRouter(prefix="/modules")

@router.get("/{organization_id}")
def get_modules(
        organization_id: str,
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type == "admin":
        try:
            module_data: List[Dict] = databases.get_modules(db, column="company_id", value=current_user.company_id)
            if module_data.__len__() == 0:
                return {"detail": "no modules available", "status_code": 201}
            return {"payload":module_data, "status_code": 200}
        except HTTPException as e:
            return HTTPException(status_code=e.status_code, detail=e.detail)
    else:
        try:
            module_data: List[Dict] = databases.get_active_modules(db, company_id=current_user.company_id)
            if module_data.__len__() == 0:
                return {"detail": "no modules available", "status_code": 201}
            return {"payload":module_data, "status_code": 200}
        except HTTPException as e:
            return HTTPException(status_code=e.status_code, detail=e.detail)




@router.post("/new_module")
def create_new_module(
        module: NewModule,
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="Your not admin")
    try:
        databases.create_new_module(db, module, current_user.company_id)
        return {"detail": "module successfully created", "status_code": 501}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/update_module")
def update_module(
        module: UpdateModule,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="Your not admin")
    try:
        databases.update_module(db, module)
        return {"detail": "module successfully updated", "status_code": 502}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/delete_module")
def delete_module(
        module_id: DeleteModule,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    print(module_id)
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="Your not admin")
    try:
        databases.delete_module(connection=db, module_id=module_id.id)
        return {"detail": "successfully delete the modules", "status_code": 503}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
