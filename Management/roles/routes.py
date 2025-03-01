from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection, get_current_user, CurrentUser
from schema import *
from Management.roles.databases import *
from Management.roles.schemas import *


router = APIRouter(prefix="/roles")

@router.get("/", response_model=List[Role])
def fetch_roles(
        db = Depends(get_db_connection),
        #user: CurrentUser = Depends(get_current_user)
):
    #if user.status_code != 200:
        #raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        roles = get_roles(db, column="company", value=1)
        return roles
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/", response_model=ResponseMessage)
def add_roles(
        role: NewRole,
        db = Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_role(db, company_id=user.company_id, data=role)
        return {"detail": "Role added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


