from utils import get_current_user
from schema import CurrentUser
from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.engagements.planning.schemas import StandardTemplate
from AuditNew.Internal.engagements.finalizations.databases import *
from typing import List

router = APIRouter(prefix="/engagements")

@router.post("/finalization_procedures/{engagement_id}")
def create_new_finalization_procedure(
        engagement_id: int,
        finalization: StandardTemplate,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        add_finalization_procedure(db, finalization=finalization, engagement_id=engagement_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/finalization_procedures/{engagement_id}", response_model=List[StandardTemplate])
def fetch_finalization_procedures(
        engagement_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_finalization_procedures(db, column="engagement", value=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/finalization_procedures/{procedure_id}")
def update_finalization_procedure(
        procedure_id: int,
        finalization: StandardTemplate,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        edit_finalization_procedure(db, finalization=finalization, procedure_id=procedure_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)