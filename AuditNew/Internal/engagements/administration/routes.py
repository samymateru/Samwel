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
        business_contacts: BusinessContact,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_business_contact(db, business_contact=business_contacts, engagement_id=engagement_id)
        return ResponseMessage(detail="Business contact updated successfully")
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











