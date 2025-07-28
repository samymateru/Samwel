from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, Query, HTTPException
from datetime import datetime
from AuditNew.Internal.engagements.attachments.databases import add_procedure_attachment, get_procedure_attachment
from AuditNew.Internal.engagements.attachments.schemas import Attachment, AttachmentSections
from schema import CurrentUser, ResponseMessage
from utils import get_async_db_connection, get_current_user, get_unique_key

router = APIRouter(prefix="/attachments")


@router.post("/planning/{engagement_id}", response_model=ResponseMessage)
async def add_planning_attachment(
        engagement_id: str,
        procedure_id: str = Query(...),
        attachment: UploadFile = File(...),
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):

    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        attachment = Attachment(
            id=get_unique_key(),
            engagement=engagement_id,
            procedure=procedure_id,
            name=attachment.filename,
            type=attachment.content_type.split("/")[1],
            size=attachment.size,
            section=AttachmentSections.PLANNING,
            creator_name=user.user_name,
            creator_email=user.user_email,
            created_at=datetime.now(),
            url=""
        )
        await add_procedure_attachment(connection=db, attachment=attachment)
        return ResponseMessage(detail="Planning attachment added")
    except HTTPException:
        raise

@router.post("/reporting/{engagement_id}", response_model=ResponseMessage)
async def add_reporting_attachment(
        engagement_id: str,
        procedure_id: str = Query(...),
        attachment: UploadFile = File(...),
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):

    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        attachment = Attachment(
            id=get_unique_key(),
            engagement=engagement_id,
            procedure=procedure_id,
            name=attachment.filename,
            type=attachment.content_type.split("/")[1],
            size=attachment.size,
            section=AttachmentSections.REPORTING,
            creator_name=user.user_name,
            creator_email=user.user_email,
            created_at=datetime.now(),
            url=""
        )
        await add_procedure_attachment(connection=db, attachment=attachment)
        return ResponseMessage(detail="Planning attachment added")
    except HTTPException:
        raise

@router.post("/finalization/{engagement_id}", response_model=ResponseMessage)
async def add_finalization_attachment(
        engagement_id: str,
        procedure_id: str = Query(...),
        attachment: UploadFile = File(...),
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):

    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        attachment = Attachment(
            id=get_unique_key(),
            engagement=engagement_id,
            procedure=procedure_id,
            name=attachment.filename,
            type=attachment.content_type.split("/")[1],
            size=attachment.size,
            section=AttachmentSections.FINALIZATION,
            creator_name=user.user_name,
            creator_email=user.user_email,
            created_at=datetime.now(),
            url=""
        )
        await add_procedure_attachment(connection=db, attachment=attachment)
        return ResponseMessage(detail="Planning attachment added")
    except HTTPException:
        raise

@router.post("/program/{engagement_id}", response_model=ResponseMessage)
async def add_program_attachment(
        engagement_id: str,
        procedure_id: str = Query(...),
        attachment: UploadFile = File(...),
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        attachment = Attachment(
            id=get_unique_key(),
            engagement=engagement_id,
            procedure=procedure_id,
            name=attachment.filename,
            type=attachment.content_type.split("/")[1],
            size=attachment.size,
            section=AttachmentSections.PROGRAM,
            creator_name=user.user_name,
            creator_email=user.user_email,
            created_at=datetime.now(),
            url=""
        )
        await add_procedure_attachment(connection=db, attachment=attachment)
        return ResponseMessage(detail="Planning attachment added")
    except HTTPException:
        raise

@router.get("/{engagement_id}", response_model=List[Attachment])
async def fetch_procedure_attachment(
        engagement_id: str,
        procedure_id: str = Query(...),
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_procedure_attachment(connection=db, engagement_id=engagement_id, procedure_id=procedure_id)
        return data
    except HTTPException:
        raise


@router.get("/{engagement_id}", response_model=List[Attachment])
async def fetch_procedure_attachment(
        engagement_id: str,
        procedure_id: str = Query(...),
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_procedure_attachment(connection=db, engagement_id=engagement_id, procedure_id=procedure_id)
        return data
    except HTTPException:
        raise


