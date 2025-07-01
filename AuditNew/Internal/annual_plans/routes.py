import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Form, UploadFile, File, BackgroundTasks
from AuditNew.Internal.annual_plans.databases import *
from utils import get_async_db_connection, check_permission
from AuditNew.Internal.annual_plans.schemas import *
from typing import List
from utils import get_current_user
from schema import CurrentUser, ResponseMessage
import uuid
import tempfile
import shutil
from s3 import upload_file



load_dotenv()

router = APIRouter(prefix="/annual_plans")
@router.get("/{company_module_id}", response_model=List[AnnualPlan])
async def fetch_annual_plans(
        company_module_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user),
        dep: bool = Depends(check_permission("audit_plans", "view"))
):
    if user.status_code != 200 and dep:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_annual_plans(connection=db, company_module_id=company_module_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/plan/{plan_id}", response_model=AnnualPlan)
async def fetch_annual_plans(
        plan_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user),
        dep: bool = Depends(check_permission("audit_plans", "view"))
):
    if user.status_code != 200 and dep:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_annual_plan(connection=db, plan_id=plan_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=401, detail="Plan not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/{company_module_id}", response_model=ResponseMessage)
async def create_new_annual_plan(
        company_module_id: str,
        name: str = Form(...),
        year: str = Form(...),
        start: datetime = Form(...),
        end: datetime = Form(...),
        attachment: UploadFile = File(...),
        db = Depends(get_async_db_connection),
        background_tasks: BackgroundTasks = BackgroundTasks(),
        user: CurrentUser  = Depends(get_current_user),
        dep: bool = Depends(check_permission("audit_plans", "create"))
):
    if user.status_code != 200 and dep:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            shutil.copyfileobj(attachment.file, tmp)
            temp_path = tmp.name

        key: str = f"annual_plans/{user.module_name}/{uuid.uuid4()}-{attachment.filename}"
        public_url: str = f"https://{os.getenv('S3_BUCKET_NAME')}.s3.{os.getenv('AWS_DEFAULT_REGION')}.amazonaws.com/{key}"

        background_tasks.add_task(upload_file, temp_path, key)
        audit_plan = AnnualPlan(
            name=name,
            year=year,
            start=start,
            end=end,
            attachment=public_url
        )
        await add_new_annual_plan(db, audit_plan=audit_plan, company_module_id=company_module_id)
        return {"detail": "Annual plan successfully created"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{annual_plan_id}", response_model=ResponseMessage)
async def update_annual_plan(
        annual_plan_id: str,
        name: str = Form(...),
        year: str = Form(...),
        start: datetime = Form(...),
        end: datetime = Form(...),
        attachment: UploadFile = File(...),
        db = Depends(get_async_db_connection),
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
        await edit_annual_plan(db, annual_plan=annual_plan, annual_plan_id=annual_plan_id)
        return {"detail": "annual plan successfully updated"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{annual_plan_id}", response_model=ResponseMessage)
async def delete_annual_plan(
        annual_plan_id: str,
        db = Depends(get_async_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        raise HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        await remove_annual_plan(db, annual_plan_id=annual_plan_id)
        return ResponseMessage(detail="successfully delete the annual plan")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
