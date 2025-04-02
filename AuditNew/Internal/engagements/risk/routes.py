from fastapi import APIRouter, Depends
from utils import  get_db_connection
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage
from AuditNew.Internal.engagements.risk.databases import *

router = APIRouter(prefix="/risk")

@router.post("/{engagement_id}")
def create_new_risk(
        engagement_id: int,
        risk: Risk,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:

        add_new_risk(db, risk=risk, engagement_id=engagement_id)
        return {"detail": "Risk added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{risk_id}", response_model=ResponseMessage)
def update_risk(
        risk_id: int,
        risk: Risk,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_risk(db, risk=risk, risk_id=risk_id)
        return {"detail": "Risk successfully updated"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{risk_id}", response_model=ResponseMessage)
def delete_risk(
        risk_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        remove_risk(connection=db, risk_id=risk_id)
        return ResponseMessage(detail="Risk deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)