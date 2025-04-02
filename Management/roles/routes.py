from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection, get_current_user, CurrentUser
from schema import *
from Management.roles.databases import *
from Management.roles.schemas import *


router = APIRouter(prefix="/roles")

@router.get("/", response_model=Role)
def fetch_roles(
        db = Depends(get_db_connection),
        #user: CurrentUser = Depends(get_current_user)
):
    #if user.status_code != 200:
       # raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        roles = get_roles(db, column="company", value=2)
        if roles.__len__() != 0:
            return roles[0]
        raise HTTPException(status_code=203, detail="No roles")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/", response_model=ResponseMessage)
def add_roles(
        role: Category,
        db = Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_role(db, company_id=user.company_id, role=role)
        return ResponseMessage(detail="Role added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/", response_model=ResponseMessage)
def add_roles(
        name: str,
        role: Category,
        db = Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_role(db, company_id=20, role=role, name=name)
        return ResponseMessage(detail="Role added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

