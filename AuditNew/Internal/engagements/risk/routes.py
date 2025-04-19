from fastapi import APIRouter, Depends
from utils import  get_async_db_connection
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage
from AuditNew.Internal.engagements.risk.databases import *
from typing import List

router = APIRouter(prefix="/risk")

@router.post("/{sub_program_id}", response_model=ResponseMessage)
async def create_new_risk(
        sub_program_id: str,
        risk: Risk,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await add_new_risk(db, risk=risk, sub_program_id=sub_program_id)
        return ResponseMessage(detail="Risk added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{risk_id}", response_model=ResponseMessage)
async def update_risk(
        risk_id: str,
        risk: Risk,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_risk(db, risk=risk, risk_id=risk_id)
        return ResponseMessage(detail="Risk successfully updated")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{risk_id}", response_model=ResponseMessage)
async def delete_risk(
        risk_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await remove_risk(connection=db, risk_id=risk_id)
        return ResponseMessage(detail="Risk deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{sub_program_id}", response_model=List[Risk])
async def fetch_risk(
        sub_program_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_risk(connection=db, sub_program_id=sub_program_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
