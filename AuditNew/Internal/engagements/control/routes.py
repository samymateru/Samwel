from typing import List

from fastapi import APIRouter, Depends
from utils import  get_db_connection
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage
from AuditNew.Internal.engagements.control.databases import *

router = APIRouter(prefix="/control")

@router.post("/{sub_program_id}", response_model=ResponseMessage)
def create_new_control(
        sub_program_id: int,
        control: Control,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_new_control(db, control=control, sub_program_id=sub_program_id)
        return ResponseMessage(detail="Control added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{control_id}", response_model=ResponseMessage)
def update_control(
        control_id: int,
        control: Control,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_control(db, control=control, control_id=control_id)
        return ResponseMessage(detail="Control successfully updated")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{control_id}", response_model=ResponseMessage)
def delete_control(
        control_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        remove_control(connection=db, control_id=control_id)
        return ResponseMessage(detail="Control deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{sub_program_id}", response_model=List[Control])
def fetch_control(
        sub_program_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        get_control(connection=db, sub_program_id=sub_program_id)
        return ResponseMessage(detail="Control fetched successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

