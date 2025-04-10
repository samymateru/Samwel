from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File

from AuditNew.Internal.annual_plans.databases import *
from utils import get_db_connection
from AuditNew.Internal.annual_plans.schemas import *
from typing import List
from utils import get_current_user
from schema import CurrentUser, ResponseMessage

router = APIRouter(prefix="/annual_plans")

@router.get("/{company_module_id}", response_model=List[AnnualPlan])
def fetch_annual_plans(
        company_module_id: int,
        db = Depends(get_db_connection),
        user: CurrentUser  = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_annual_plans(db, company_module_id=company_module_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/{company_module_id}", response_model=ResponseMessage)
async def create_new_annual_plan(
        company_module_id: int,
        name: str = Form(...),
        year: str = Form(...),
        start: datetime = Form(...),
        end: datetime = Form(...),
        attachment: UploadFile = File(...),
        db = Depends(get_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        audit_plan = AnnualPlan(
            name=name,
            year=year,
            start=start,
            end=end,
            attachment=""
        )
        add_new_annual_plan(db, audit_plan=audit_plan, company_module_id=company_module_id)
        return {"detail": "Annual plan successfully created"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{annual_plan_id}", response_model=ResponseMessage)
def update_annual_plan(
        annual_plan_id: int,
        name: str = Form(...),
        year: str = Form(...),
        start: datetime = Form(...),
        end: datetime = Form(...),
        attachment: UploadFile = File(...),
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    annual_plan = AnnualPlan(
        name=name,
        year=year,
        start=start,
        end=end,
        attachment=attachment.filename
    )
    if current_user.status_code != 200:
        raise HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        edit_annual_plan(db, annual_plan=annual_plan, annual_plan_id=annual_plan_id)
        return {"detail": "annual plan successfully updated"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{annual_plan_id}", response_model=ResponseMessage)
def delete_annual_plan(
        annual_plan_id: int,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        raise HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        remove_annual_plan(db, annual_plan_id=annual_plan_id)
        return {"detail": "successfully delete the annual plan"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
