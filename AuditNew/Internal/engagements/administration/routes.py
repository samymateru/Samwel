from utils import get_current_user
from schema import CurrentUser
from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks
from utils import get_async_db_connection
from AuditNew.Internal.engagements.administration.databases import *
from schema import ResponseMessage
from typing import List
import uuid
import tempfile
import shutil
from s3 import upload_file
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/engagements")

@router.get("/business_contact/{engagement_id}", response_model=List[BusinessContact])
async def fetch_business_contacts(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_business_contacts(db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/business_contact/{engagement_id}", response_model=ResponseMessage)
async def update_business_contact(
        engagement_id: str,
        business_contacts: List[BusinessContact],
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_business_contact(db, business_contacts=business_contacts, engagement_id=engagement_id)
        return ResponseMessage(detail="Business contact updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/profile/{engagement_id}", response_model=List[EngagementProfile])
async def fetch_engagement_profile(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_engagement_profile(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/profile/{engagement_id}", response_model=ResponseMessage)
async def update_profile(
        engagement_id: str,
        profile: EngagementProfile,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_engagement_profile(db, profile=profile, engagement_id=engagement_id)
        return ResponseMessage(detail="Profile updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/context/engagement_process/{engagement_process_id}", response_model=ResponseMessage)
async def update_engagement_process(
        engagement_process_id: str,
        engagement_process: EngagementProcess,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_engagement_process(db, engagement_process=engagement_process, engagement_process_id=engagement_process_id)
        return ResponseMessage(detail="Engagement process updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/context/policies/{policy_id}", response_model=ResponseMessage)
async def update_policies(
        policy_id: str,
        policy: Policy,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_policies(db, policy=policy, policy_id=policy_id)
        return ResponseMessage(detail="Policy updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.put("/context/regulations/{regulation_id}", response_model=ResponseMessage)
async def update_regulations(
        regulation_id: str,
        regulation: Regulations,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_regulations(db, regulation=regulation, regulation_id=regulation_id)
        return ResponseMessage(detail="Regulation updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/context/staff/{staff_id}", response_model=ResponseMessage)
async def update_staff(
        staff_id: str,
        staff: Staff,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_staff(db, staff=staff, staff_id=staff_id)
        return ResponseMessage(detail="Staff updated successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/context/policies/{engagement_id}", response_model=List[Policy])
async def fetch_engagement_policies(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_engagement_policies(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/context/policies/{engagement_id}", response_model=ResponseMessage)
async def create_engagement_policy(
        engagement_id: str,
        name: str = Form(...),
        version: str = Form(...),
        key_areas: str = Form(...),
        attachment: UploadFile = File(...),
        background_upload: BackgroundTasks = BackgroundTasks(),
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            shutil.copyfileobj(attachment.file, tmp)
            temp_path = tmp.name

        key: str = f"administration/policies/{user.company_name}/{uuid.uuid4()}-{attachment.filename}"
        public_url: str = f"https://{os.getenv("S3_BUCKET_NAME")}.s3.{os.getenv("AWS_DEFAULT_REGION")}.amazonaws.com/{key}"
        background_upload.add_task(upload_file, temp_path, key)
        policy = Policy(
            name=name,
            version=version,
            key_areas=key_areas,
            attachment=public_url
        )
        await add_engagement_policies(db, policy=policy, engagement_id=engagement_id)
        return ResponseMessage(detail="Policy added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/context/policies/{policy_id}", response_model=ResponseMessage)
async def delete_policy(
        policy_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await remove_policy(connection=db, policy_id=policy_id)
        return ResponseMessage(detail="Policy deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/context/engagement_process/{engagement_process_id}", response_model=ResponseMessage)
async def delete_engagement_process(
        engagement_process_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await remove_engagement_process(connection=db, engagement_process_id=engagement_process_id)
        return ResponseMessage(detail="Engagement process deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/context/engagement_process/{engagement_id}", response_model=List[EngagementProcess])
async def fetch_engagement_process(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_engagement_process(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/context/engagement_process/{engagement_id}", response_model=ResponseMessage)
async def create_new_engagement_process(
        engagement_id: str,
        process: EngagementProcess,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await add_engagement_process(db, process=process, engagement_id=engagement_id)
        return ResponseMessage(detail="Engagement process added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/context/regulations/{engagement_id}", response_model=List[Regulations])
async def fetch_regulations(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_engagement_regulations(db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/context/regulations/{engagement_id}", response_model=ResponseMessage)
async def create_engagement_regulations(
        engagement_id: str,
        name: str = Form(...),
        issue_date: datetime = Form(...),
        key_areas = Form(...),
        attachment: UploadFile = File(...),
        background_upload: BackgroundTasks = BackgroundTasks(),
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            shutil.copyfileobj(attachment.file, tmp)
            temp_path = tmp.name

        key: str = f"administration/regulations/{user.company_name}/{uuid.uuid4()}-{attachment.filename}"
        public_url: str = f"https://{os.getenv("S3_BUCKET_NAME")}.s3.{os.getenv("AWS_DEFAULT_REGION")}.amazonaws.com/{key}"
        background_upload.add_task(upload_file, temp_path, key)
        regulation = Regulations(
            name=name,
            issue_date=issue_date,
            key_areas=key_areas,
            attachment=public_url
        )
        await add_engagement_regulations(db, regulation=regulation, engagement_id=engagement_id)
        return ResponseMessage(detail="Regulation added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/context/regulations/{regulation_id}", response_model=ResponseMessage)
async def delete_regulation(
        regulation_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await remove_regulation(connection=db, regulation_id=regulation_id)
        return ResponseMessage(detail="Regulation deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/staff/{engagement_id}", response_model=List[Staff])
async def fetch_staff(
        engagement_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_engagement_staff(connection=db, engagement_id=engagement_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/staff/{engagement_id}", response_model=ResponseMessage)
async def create_engagement_staff(
        engagement_id: str,
        staff: Staff,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await add_engagement_staff(db, staff=staff, engagement_id=engagement_id)
        return ResponseMessage(detail="Staff added successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/context/staff/{staff_id}", response_model=ResponseMessage)
async def delete_staff(
        staff_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await remove_staff(connection=db, staff_id=staff_id)
        return ResponseMessage(detail= "Staff deleted successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)





