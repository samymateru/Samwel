from fastapi import APIRouter, Depends
from schema import CurrentUser, ResponseMessage
from utils import get_db_connection, get_current_user, get_async_db_connection
from Management.entity.profile.control_type.databases import *
from typing import List

router = APIRouter(prefix="/profile/control_type")

@router.post("/", response_model=ResponseMessage)
def create_control_type(
        control_type: ControlType,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        new_control_type(db, control_type=control_type, company_id=user.entity_id)
        return {"detail": "Control effectiveness rating added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/", response_model=ControlType)
async def fetch_company_control_type(
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_company_control_type(db, company_id=user.entity_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="Control type not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{control_type_id}", response_model=ResponseMessage)
def update_control_type(
        control_type_id: int,
        control_type: ControlType,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_control_type(
            db,
            control_type=control_type,
            control_type_id=control_type_id)
        return {"detail": "Control weakness rating updated successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{control_type_id}", response_model=ResponseMessage)
def remove_control_type(
        control_type_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        remove_control_type(db, control_type_id=control_type_id)
        return {"detail": "Control weakness rating deleted successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)