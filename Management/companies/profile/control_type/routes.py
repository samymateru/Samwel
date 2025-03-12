from fastapi import APIRouter, Depends
from schema import CurrentUser, ResponseMessage
from utils import get_db_connection, get_current_user
from Management.companies.profile.control_type.databases import *
from typing import List

router = APIRouter(prefix="/profile/control_type")

@router.post("/{company_id}", response_model=ResponseMessage)
def create_control_type(
        company_id: int,
        control_type: ControlType,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        new_control_type(db, control_type=control_type, company_id=company_id)
        return {"detail": "Control effectiveness rating added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/company/{company_id}", response_model=List[ControlType])
def fetch_company_control_type(
        company_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_company_control_type(db, company_id=company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{control_type_id}", response_model=ControlType)
def fetch_control_weakness_rating(
        control_type_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_control_type(db, control_type_id=control_type_id)
        return data
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