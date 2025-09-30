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












