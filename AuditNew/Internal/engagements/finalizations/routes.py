from utils import get_current_user
from schema import CurrentUser
from fastapi import APIRouter, Depends
from utils import  get_async_db_connection
from AuditNew.Internal.engagements.finalizations.databases import *
from typing import List
from schema import ResponseMessage

router = APIRouter(prefix="/engagements")

@router.post("/finalization_procedures/{engagement_id}", response_model=ResponseMessage)
async def create_new_finalization_procedure(
        engagement_id: str,
        finalization: NewFinalizationProcedure,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await add_finalization_procedure(db, finalization=finalization, engagement_id=engagement_id)
        return ResponseMessage(detail="Finalization procedure added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/finalization_procedures/{engagement_id}", response_model=List[StandardTemplate])
async def fetch_finalization_procedures(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_finalization_procedures(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/finalization_procedures/{procedure_id}",response_model=ResponseMessage)
async def update_finalization_procedure(
        procedure_id: str,
        finalization: StandardTemplate,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_finalization_procedure(db, finalization=finalization, procedure_id=procedure_id)
        return ResponseMessage(detail="Finalization procedure updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)