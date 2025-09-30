from fastapi import APIRouter, Depends, Query, Form, UploadFile, File, BackgroundTasks
from pydantic_core import ValidationError
from s3 import upload_file
from utils import get_async_db_connection
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage
from AuditNew.Internal.engagements.issue.databases import *
from datetime import datetime
import tempfile
import shutil
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/issue")

@router.put("/send_owner/{issue_id}", response_model=ResponseMessage)
async def submit_issue_to_owner(
        issue_id: str,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await send_issues_to_owner(
            connection=db,
            issue_id=issue_id,
            user_email=user.user_email,
            user_name=user.user_name)
        return ResponseMessage(detail="Successfully send the issue to owner")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.put("/accept_response/{issue_id}", response_model=ResponseMessage)
async def issue_accept_response_(
        issue_id: str,
        accept_actor: ResponseActors = Form(...),
        accept_notes: Optional[str] = Form(None),
        accept_attachment: Optional[UploadFile] = File(None),
        lod2_feedback: Optional[LOD2Feedback] = Form(None),
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        if accept_attachment is None:
            issue = IssueAcceptResponse(
                actor=accept_actor,
                accept_notes=accept_notes,
                lod2_feedback=lod2_feedback
            )
        else:
            issue = IssueAcceptResponse(
                actor=accept_actor,
                accept_notes=accept_notes,
                accept_attachment=[accept_attachment.filename],
                lod2_feedback=lod2_feedback
            )
        is_success = await send_accept_response(
            connection=db,
            issue=issue,
            issue_id=issue_id,
            user_email=user.user_email,
            user_name=user.user_name)
        if is_success:
            if accept_attachment is not None:
                pass
        return ResponseMessage(detail=f"Successfully send accept response ")
    except ValidationError as v:
        raise HTTPException(status_code=422, detail=v.errors()[0].get("msg"))

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.put("/decline_response/{issue_id}", response_model=ResponseMessage)
async def issue_decline_response_(
        issue_id: str,
        issue: IssueDeclineResponse,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await send_decline_response(
            connection=db,
            issue=issue,
            issue_id=issue_id,
            user_email=user.user_email,
            user_name=user.user_name)
        return ResponseMessage(detail=f"Successfully decline issue")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)




@router.get("/", response_model=List[Issue])
async def fetch_issue_based_on_actor(
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_issue_from_actor(connection=db, user_email=user.user_email)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)



@router.put("/prepared/{issue_id}", response_model=ResponseMessage)
async def prepare_issue(
        issue_id: str,
        prepare: User,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await mark_issue_prepared(connection=db, prepare=prepare, issue_id=issue_id)
        return ResponseMessage(detail="Issue marked prepared successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)



@router.put("/reviewed/{issue_id}", response_model=ResponseMessage)
async def review_issue(
        issue_id: str,
        review: User,
        db=Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await mark_issue_reviewed(connection=db, review=review, issue_id=issue_id)
        return ResponseMessage(detail="Issue marked reviewed successfully")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

