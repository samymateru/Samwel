from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from utils import  get_db_connection
from AuditNew.Internal.annual_plans import databases
from AuditNew.Internal.annual_plans.schemas import *
from typing import Tuple, Dict, List
from utils import get_current_user
from schema import CurrentUser
from Management.users import databases as user_database
from Management.roles import databases as role_database

router = APIRouter(prefix="/annual_plans")

@router.get("/")
def get_annual_plans(
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        # role_ids: List[int] = user_database.get_user(db, column="id", value=1)[0].get("role_id")
        # user_roles: List[Dict] = role_database.get_user_roles(db, role_ids)
        # matching_dicts = [d for d in user_roles if d.get("category") == "AnnualPlan"]
        # print(matching_dicts)
        # for i in matching_dicts:
        #     if i.get("read"):
        annual_plans_data: List[Dict] = databases.get_annual_plans(db, column="company_id", value=current_user.company_id)
        if annual_plans_data.__len__() == 0:
            return {"payload": [], "status_code": 200}
        return {"payload": annual_plans_data, "status_code": 200}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/new_annual_plan")
def create_new_annual_plan(
        name: str = Form(...),
        year: str = Form(...),
        start: datetime = Form(...),
        end: datetime = Form(...),
        file: UploadFile = File(...),
        db = Depends(get_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        return HTTPException(status_code=user.status_code, detail=user.description)
    try:
        annual_audit_plan = NewAnnualPlan(
            name=name,
            year=year,
            start=start,
            end=end,
            file=file.filename
        )
        databases.create_new_annual_plan(db, annual_audit_plan=annual_audit_plan, company_id=user.company_id)
        return {"detail": "Annual plan successfully created", "status_code": 501}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/update_annual_plan")
def update_annual_plan(
        annual_plan: UpdateAnnualPlan,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.update_annual_plan(db, annual_plan)
        return {"detail": "annual plan successfully updated", "status_code": 502}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/delete_annual_plan")
def delete_annual_plan(
        plan_id: DeleteAnnualPlan,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.delete_annual_plan(db, plan_id.plan_id)
        return {"detail": "successfully delete the annual plan", "status_code": 503}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
